"""
DQN Agent with Prioritized Experience Replay
"""
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import sys
import os

# Add parent directory to path for common imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from drl.neural_network import DQN
from drl.replay_buffer import PrioritizedReplayBuffer
from drl.config import DRLConfig
from common.utils import get_device

class DQNAgent:
    """
    Deep Q-Network Agent for traffic signal control
    """
    def __init__(self, state_dim, action_dim, device=None):
        self.state_dim = state_dim
        self.action_dim = action_dim
        
        # Auto-detect best device using common utility
        self.device = get_device(device)
        print(f"Using device: {self.device}")
        
        # Networks
        self.policy_net = DQN(state_dim, action_dim).to(device)
        self.target_net = DQN(state_dim, action_dim).to(device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        
        # Optimizer and loss
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=DRLConfig.LEARNING_RATE)
        self.loss_fn = nn.MSELoss()
        
        # Replay buffer
        self.memory = PrioritizedReplayBuffer(DRLConfig.BUFFER_SIZE)
        
        # Exploration parameters
        self.epsilon = DRLConfig.EPSILON_START
        self.epsilon_decay = DRLConfig.EPSILON_DECAY
        self.epsilon_min = DRLConfig.EPSILON_END
        
        # Training counters
        self.steps = 0
        self.episode_count = 0
        
    def select_action(self, state, explore=True):
        """
        Select action using epsilon-greedy policy
        Args:
            state: np.array or torch.Tensor
            explore: bool, whether to use epsilon-greedy (True for training, False for testing)
        Returns:
            action: int
        """
        if explore and random.random() < self.epsilon:
            # Random action (exploration)
            return random.randrange(self.action_dim)
        
        # Convert state to tensor
        if isinstance(state, np.ndarray):
            state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        
        # Greedy action (exploitation)
        with torch.no_grad():
            q_values = self.policy_net(state)
            return q_values.argmax().item()
    
    def store_experience(self, state, action, reward, next_state, done, info):
        """
        Store experience in replay buffer
        """
        # Calculate TD error for prioritization
        td_error = self._calculate_td_error(state, action, reward, next_state, done)
        
        # Get event type from info
        event_type = info.get('event_type', 'normal')
        
        # Add to buffer
        self.memory.add(state, action, reward, next_state, done, td_error, event_type)
    
    def _calculate_td_error(self, state, action, reward, next_state, done):
        """
        Calculate TD error for prioritization
        """
        with torch.no_grad():
            state_t = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            next_state_t = torch.FloatTensor(next_state).unsqueeze(0).to(self.device)
            
            # Current Q-value
            q_current = self.policy_net(state_t)[0, action]
            
            # Target Q-value
            if done:
                q_target = reward
            else:
                q_next = self.target_net(next_state_t).max().item()
                q_target = reward + DRLConfig.GAMMA * q_next
            
            td_error = abs(q_target - q_current.item())
        
        return td_error
    
    def train(self):
        """
        Train the agent on a batch from replay buffer with FIXED loss calculation
        Returns:
            loss: float
        """
        # Check if enough experiences
        if len(self.memory) < DRLConfig.MIN_BUFFER_SIZE:
            return None
        
        # Sample batch
        batch, indices, weights = self.memory.sample(DRLConfig.BATCH_SIZE)
        
        # Unpack batch
        states, actions, rewards, next_states, dones = zip(*batch)
        
        # Convert to tensors
        states = torch.FloatTensor(np.array(states)).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)
        weights = torch.FloatTensor(weights).to(self.device)
        
        # CLIP REWARDS to prevent explosion
        rewards = torch.clamp(rewards, -10.0, 10.0)
        
        # Current Q-values
        current_q_values = self.policy_net(states).gather(1, actions.unsqueeze(1)).squeeze()
        
        # Target Q-values (Double DQN)
        with torch.no_grad():
            next_actions = self.policy_net(next_states).argmax(1)
            next_q_values = self.target_net(next_states).gather(1, next_actions.unsqueeze(1)).squeeze()
            
            # CLIP next Q-values
            next_q_values = torch.clamp(next_q_values, -10.0, 10.0)
            
            target_q_values = rewards + DRLConfig.GAMMA * next_q_values * (1 - dones)
            # CLIP targets
            target_q_values = torch.clamp(target_q_values, -10.0, 10.0)
        
        # Calculate TD errors
        td_errors = target_q_values - current_q_values
        
        # Huber loss instead of MSE (more stable)
        loss = torch.nn.functional.smooth_l1_loss(
            current_q_values, 
            target_q_values, 
            reduction='none'
        )
        loss = (weights * loss).mean()
        
        # CLIP loss
        loss = torch.clamp(loss, 0, 100.0)
        
        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        
        # STRONGER gradient clipping
        torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), 0.5)
        
        self.optimizer.step()
        
        # Update priorities (clip TD errors)
        td_errors_np = torch.clamp(td_errors, -10, 10).detach().cpu().numpy()
        self.memory.update_priorities(indices, np.abs(td_errors_np))
        
        # Update target network
        self.steps += 1
        if self.steps % DRLConfig.TARGET_UPDATE_FREQUENCY == 0:
            self.soft_update_target_network()
        
        return loss.item()
    
    def soft_update_target_network(self):
        """
        Soft update target network parameters
        θ_target = τ*θ_policy + (1-τ)*θ_target
        """
        for target_param, policy_param in zip(self.target_net.parameters(), self.policy_net.parameters()):
            target_param.data.copy_(
                DRLConfig.TAU * policy_param.data + (1 - DRLConfig.TAU) * target_param.data
            )
    
    def decay_epsilon(self):
        """
        Decay exploration rate
        """
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def save(self, filepath):
        """
        Save model checkpoint
        """
        checkpoint = {
            'policy_net_state_dict': self.policy_net.state_dict(),
            'target_net_state_dict': self.target_net.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'steps': self.steps,
            'episode_count': self.episode_count
        }
        torch.save(checkpoint, filepath)
        print(f"Model saved to {filepath}")
    
    def load(self, filepath):
        """
        Load model checkpoint
        """
        checkpoint = torch.load(filepath, map_location=self.device)
        self.policy_net.load_state_dict(checkpoint['policy_net_state_dict'])
        self.target_net.load_state_dict(checkpoint['target_net_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.epsilon = checkpoint['epsilon']
        self.steps = checkpoint['steps']
        self.episode_count = checkpoint['episode_count']
        print(f"Model loaded from {filepath}")
    
    def set_eval_mode(self):
        """
        Set networks to evaluation mode
        """
        self.policy_net.eval()
        self.target_net.eval()
    
    def set_train_mode(self):
        """
        Set networks to training mode
        """
        self.policy_net.train()
        self.target_net.eval()  # Target network always in eval mode
