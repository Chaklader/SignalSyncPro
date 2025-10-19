"""
DQN Agent with Prioritized Experience Replay for Traffic Signal Control

This module implements a Deep Q-Network (DQN) agent with several advanced features:
- Double DQN to reduce overestimation bias
- Prioritized Experience Replay (PER) for efficient learning
- Soft target network updates for training stability
- Multiple clipping strategies to prevent training instability

===================================================================================
MATHEMATICAL FOUNDATIONS
===================================================================================

1. Q-LEARNING BELLMAN EQUATION
-------------------------------
The optimal action-value function satisfies:

    Q*(s, a) = E[r + γ · max_a' Q*(s', a')]

Where:
    s     = current state (traffic conditions)
    a     = action taken (signal control decision)
    r     = immediate reward (negative waiting time, sync bonus, etc.)
    s'    = next state
    a'    = next action
    γ     = discount factor (0.95 in config)

2. TEMPORAL DIFFERENCE (TD) ERROR
-----------------------------------
Measures prediction error for prioritization:

    TD_error = |Q_target - Q_current|

    If episode done:
        Q_target = r
    Else:
        Q_target = r + γ · max_a' Q(s', a')

High TD error → High priority in replay buffer (learn from surprises)
Low TD error → Low priority (already know this well)

3. DOUBLE DQN
--------------
Separates action selection from action evaluation to reduce overestimation:

    Standard DQN:
        Q_target = r + γ · max_a' Q_target(s', a')  ← Same network for both

    Double DQN:
        a'_best = argmax_a' Q_policy(s', a')        ← Policy net selects
        Q_target = r + γ · Q_target(s', a'_best)    ← Target net evaluates

This prevents the maximization bias where the network overestimates Q-values.

4. SOFT TARGET NETWORK UPDATES
--------------------------------
Instead of hard copying weights periodically, gradually blend:

    θ_target ← τ · θ_policy + (1 - τ) · θ_target

Where τ = 0.005 (TAU in config)

This creates a slowly-moving target for stable learning.

5. LOSS FUNCTION
-----------------
Uses Smooth L1 Loss (Huber Loss) weighted by importance:

    L = mean(weights · smooth_l1_loss(Q_current, Q_target))

    smooth_l1_loss(x, y) = {
        0.5 · (x - y)²           if |x - y| < 1
        |x - y| - 0.5            otherwise
    }

This is less sensitive to outliers than MSE.

===================================================================================
CLIPPING STRATEGIES (Multi-layer protection against training instability)
===================================================================================

Layer 1: REWARD CLIPPING → [-10, 10]
    Prevents extreme rewards from rare events (safety violations, perfect sync)

Layer 2: Q-VALUE CLIPPING → [-10, 10]
    Prevents extreme Q-values from propagating through Bellman equation

Layer 3: LOSS CLIPPING → [0, 100]
    Final safety net against catastrophic loss values

Layer 4: GRADIENT CLIPPING → max_norm = 0.5
    Prevents exploding gradients during backpropagation

Example of protection cascade:
    Raw reward = -150 (safety violation)
    → Clipped to -10
    → Q-value calculated with -10
    → Q-value clipped to valid range
    → Loss computed and clipped
    → Gradients clipped before weight update

===================================================================================
TENSOR OPERATIONS
===================================================================================

Understanding gather() operation:
---------------------------------
Network output shape: [batch_size, action_dim] e.g., [32, 4]

    Q_values = [[Q(s₀,a₀), Q(s₀,a₁), Q(s₀,a₂), Q(s₀,a₃)],  ← Sample 0
                [Q(s₁,a₀), Q(s₁,a₁), Q(s₁,a₂), Q(s₁,a₃)],  ← Sample 1
                ...]

    actions = [1, 2, 0, ...]  ← Actions taken

    # We want Q-values for specific actions:
    Q_values.gather(1, actions.unsqueeze(1))
    → Selects along dimension 1 (columns/actions)
    → Returns [Q(s₀,a₁), Q(s₁,a₂), Q(s₂,a₀), ...]

Dimension meanings:
    dim=0 → Operate along rows (batch dimension)
    dim=1 → Operate along columns (action dimension)

Terminal state handling with (1 - done):
-----------------------------------------
    target = r + γ · Q_next · (1 - done)

    If done=0 (continuing): multiply by 1 → full future value
    If done=1 (terminal):   multiply by 0 → no future value

===================================================================================
EVENT TYPES FOR PRIORITIZED REPLAY
===================================================================================

Priority multipliers for different traffic events:
    'normal'            : 1x  (routine decisions)
    'sync_success'      : 3x  (successful coordination)
    'bus_conflict'      : 4x  (bus coordination issue)
    'ped_phase'         : 5x  (pedestrian phase activated)
    'sync_failure'      : 6x  (failed synchronization)
    'safety_violation'  : 10x (near-miss or safety issue)

High-priority events are sampled more frequently during training.

===================================================================================
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

from controls.drl.neural_network import DQN
from controls.drl.replay_buffer import PrioritizedReplayBuffer
from controls.drl.config import DRLConfig
from common.utils import get_device


class DQNAgent:
    """
    Deep Q-Network Agent for Multimodal Traffic Signal Control

    Implements DQN with advanced features for learning optimal traffic signal timing:
    - State: 45-dimensional traffic features (queues, phase info, detectors, sync timers)
    - Actions: 4 signal control decisions (Continue, Skip to Phase 1, Next, Pedestrian)
    - Reward: Multi-objective (waiting time, CO₂, synchronization, equity, safety)

    Architecture:
        - Policy Network: Makes decisions, continuously updated
        - Target Network: Provides stable targets, slowly updated (τ=0.005)
        - Replay Buffer: Stores 50,000 experiences with prioritization
        - Optimizer: Adam (lr=1e-5)

    Training Strategy:
        - Double DQN: Separates action selection from evaluation
            - Policy network selects the best action (argmax)
            - Target network evaluates that action's Q-value
        - Soft Updates: Gradual target network synchronization
        - ε-greedy: Decaying exploration from 1.0 → 0.01
        - PER: Prioritizes important experiences (safety, sync failures, ped phases)
        - Multi-layer Clipping: Rewards, Q-values, loss, and gradients

    Stability Mechanisms:
        - Reward clipping: [-10, 10]
        - Q-value clipping: [-10, 10]
        - Loss clipping: [0, 100]
        - Gradient clipping: max_norm=0.5
        - Smooth L1 loss (robust to outliers)

    Usage:
        # Training
        agent = DQNAgent(state_dim=45, action_dim=4)
        action = agent.select_action(state, explore=True)
        agent.store_experience(state, action, reward, next_state, done, info)
        loss = agent.train()
        agent.decay_epsilon()

        # Testing
        agent.set_eval_mode()
        action = agent.select_action(state, explore=False)
    """

    def __init__(self, state_dim, action_dim, device=None):
        """
        Initialize DQN Agent with dual networks and replay buffer.

        Creates two identical networks (policy and target) and initializes
        the prioritized replay buffer for experience storage.

        Args:
            state_dim (int): Dimension of state space (45 for traffic system)
            action_dim (int): Number of actions (4 for traffic control)
            device (str, optional): 'cuda', 'cpu', or None for auto-detect

        Networks:
            - Policy network: Actively trained, makes decisions
            - Target network: Slowly updated copy for stable targets
            - Both start with identical random weights
            - Target network set to eval mode (no dropout/batch norm updates)
        """
        self.state_dim = state_dim
        self.action_dim = action_dim

        # Auto-detect best device using common utility
        self.device = get_device(device)
        print(f"Using device: {self.device}")

        # Networks: Create policy and target with identical architecture
        self.policy_net = DQN(state_dim, action_dim).to(self.device)
        self.target_net = DQN(state_dim, action_dim).to(self.device)

        # Initialize target network with policy network's weights (clone the brain)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()  # Target network never trains directly

        # Optimizer and loss
        self.optimizer = optim.Adam(
            self.policy_net.parameters(), lr=DRLConfig.LEARNING_RATE
        )
        self.loss_fn = nn.MSELoss()

        # Replay buffer with prioritization
        self.memory = PrioritizedReplayBuffer(DRLConfig.BUFFER_SIZE)

        # Exploration parameters (ε-greedy)
        self.epsilon = DRLConfig.EPSILON_START  # Start: 1.0 (fully random)
        self.epsilon_decay = DRLConfig.EPSILON_DECAY  # Decay: 0.995 per episode
        self.epsilon_min = DRLConfig.EPSILON_END  # End: 0.01 (1% exploration)

        # Training counters
        self.steps = 0  # Total training steps across all episodes
        self.episode_count = 0  # Number of episodes completed

    def select_action(self, state, explore=True):
        """
        Select action using ε-greedy policy.

        During training (explore=True):
            - With probability ε: random action (exploration)
            - With probability (1-ε): best action from Q-values (exploitation)

        During testing (explore=False):
            - Always selects best action (pure exploitation)

        Args:
            state (np.ndarray or torch.Tensor): Traffic state [state_dim]
            explore (bool): Enable ε-greedy exploration (True for training, False for testing)

        Returns:
            int: Selected action index in [0, action_dim)

        Example:
            # Training: ε=0.3 means 30% random, 70% greedy
            action = agent.select_action(state, explore=True)

            # Testing: always greedy
            agent.epsilon = 0.0
            action = agent.select_action(state, explore=False)
        """
        # Exploration: random action
        if explore and random.random() < self.epsilon:
            return random.randrange(self.action_dim)

        # Convert numpy to tensor if needed
        if isinstance(state, np.ndarray):
            state = torch.FloatTensor(state).unsqueeze(0).to(self.device)

        # Exploitation: greedy action (highest Q-value)
        with torch.no_grad():  # No gradient computation for inference
            q_values = self.policy_net(state)  # [1, action_dim]
            return q_values.argmax().item()  # Index of max Q-value

    def store_experience(self, state, action, reward, next_state, done, info):
        """
        Store experience in prioritized replay buffer.

        Calculates TD error for prioritization and extracts event type
        for additional priority weighting (safety violations, pedestrian
        phases, sync failures get higher priority).

        Args:
            state (np.ndarray): Current traffic state [state_dim]
            action (int): Action taken
            reward (float): Reward received
            next_state (np.ndarray): Resulting traffic state [state_dim]
            done (bool): Whether episode terminated
            info (dict): Additional info with 'event_type' key

        Event Types (priority multipliers):
            'normal': 1x
            'sync_success': 3x
            'bus_conflict': 4x
            'ped_phase': 5x
            'sync_failure': 6x
            'safety_violation': 10x
        """
        # Calculate TD error for prioritization
        td_error = self._calculate_td_error(state, action, reward, next_state, done)

        # Extract event type (defaults to 'normal' if not provided)
        event_type = info.get("event_type", "normal")

        # Store in buffer with priority based on TD error and event type
        self.memory.add(state, action, reward, next_state, done, td_error, event_type)

    def _calculate_td_error(self, state, action, reward, next_state, done):
        """
        Calculate Temporal Difference error for prioritization.

        TD error measures how surprising/unexpected the outcome was:
        - Large TD error → bad prediction → high priority (learn from this!)
        - Small TD error → good prediction → low priority (already know this)

        Formula:
            If done: TD_error = |reward - Q_current|
            Else:    TD_error = |reward + γ·max(Q_next) - Q_current|

        Args:
            state (np.ndarray): Current state
            action (int): Action taken
            reward (float): Reward received
            next_state (np.ndarray): Next state
            done (bool): Episode termination flag

        Returns:
            float: Absolute TD error (always positive)

        Example:
            # Good prediction: Q_current=10, Q_target=9.5 → TD_error=0.5 (low priority)
            # Bad prediction:  Q_current=10, Q_target=50  → TD_error=40  (high priority)
        """
        with torch.no_grad():  # No gradients needed for prioritization
            # Convert states to tensors
            state_t = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            next_state_t = torch.FloatTensor(next_state).unsqueeze(0).to(self.device)

            # Current Q-value prediction
            q_current = self.policy_net(state_t)[0, action]

            # Target Q-value calculation
            if done:
                # Terminal state: no future rewards
                q_target = reward
            else:
                # Non-terminal: include discounted future value
                q_next = self.target_net(next_state_t).max().item()
                q_target = reward + DRLConfig.GAMMA * q_next

            # TD error = |target - prediction|
            td_error = abs(q_target - q_current.item())

        return td_error

    def train(self):
        """
        Train the agent on a mini-batch from replay buffer.

        Implements Double DQN with Prioritized Experience Replay:
        1. Sample prioritized batch from buffer
        2. Compute current Q-values from policy network
        3. Compute target Q-values using Double DQN:
           - Policy network selects best next actions
           - Target network evaluates those actions
        4. Calculate weighted Smooth L1 loss
        5. Backpropagate and update policy network
        6. Update experience priorities in buffer
        7. Soft update target network (every TARGET_UPDATE_FREQUENCY steps)

        Stability Features:
        - Multi-layer clipping (rewards, Q-values, loss)
        - Gradient clipping (max_norm=0.5)
        - Smooth L1 loss (robust to outliers)
        - Importance sampling weights from PER

        Returns:
            float or None: Training loss value, or None if buffer too small

        Algorithm:
            For each sample in batch:
                Q_current = policy_net(state)[action]
                next_action = argmax(policy_net(next_state))  # Policy selects
                Q_next = target_net(next_state)[next_action]   # Target evaluates
                Q_target = reward + γ · Q_next · (1 - done)
                loss = smooth_l1_loss(Q_current, Q_target)
        """
        # Wait until buffer has enough experiences
        if len(self.memory) < DRLConfig.MIN_BUFFER_SIZE:
            return None

        # Sample prioritized batch (high TD error samples more likely)
        batch, indices, weights = self.memory.sample(DRLConfig.BATCH_SIZE)

        # Unpack batch into separate lists
        states, actions, rewards, next_states, dones = zip(*batch)

        # Convert to PyTorch tensors
        states = torch.FloatTensor(np.array(states)).to(
            self.device
        )  # [batch, state_dim]
        actions = torch.LongTensor(actions).to(self.device)  # [batch]
        rewards = torch.FloatTensor(rewards).to(self.device)  # [batch]
        next_states = torch.FloatTensor(np.array(next_states)).to(
            self.device
        )  # [batch, state_dim]
        dones = torch.FloatTensor(dones).to(self.device)  # [batch]
        weights = torch.FloatTensor(weights).to(self.device)  # [batch]

        # Layer 1: Clip rewards to prevent extreme values
        rewards = torch.clamp(rewards, -10.0, 10.0)

        # Current Q-values: Q(s, a) for actions actually taken
        # gather(1, ...) selects Q-values along action dimension
        current_q_values = (
            self.policy_net(states).gather(1, actions.unsqueeze(1)).squeeze()
        )

        # Target Q-values using Double DQN
        with torch.no_grad():  # No gradients for target computation
            # Step 1: Policy network selects best actions for next states
            next_actions = self.policy_net(next_states).argmax(1)

            # Step 2: Target network evaluates those actions
            next_q_values = (
                self.target_net(next_states)
                .gather(1, next_actions.unsqueeze(1))
                .squeeze()
            )

            # Layer 2: Clip next Q-values
            next_q_values = torch.clamp(next_q_values, -10.0, 10.0)

            # Bellman equation with terminal state handling
            # (1 - dones): if done=1, multiply by 0 (no future); if done=0, multiply by 1 (include future)
            target_q_values = rewards + DRLConfig.GAMMA * next_q_values * (1 - dones)

            # Layer 3: Clip final targets
            target_q_values = torch.clamp(target_q_values, -10.0, 10.0)

        # Calculate TD errors for priority updates
        td_errors = target_q_values - current_q_values

        # Smooth L1 loss (Huber loss) - more robust than MSE
        # Less sensitive to outliers than squared error
        loss = torch.nn.functional.smooth_l1_loss(
            current_q_values,
            target_q_values,
            reduction="none",  # Compute per-sample losses
        )

        # Apply importance sampling weights from PER
        loss = (weights * loss).mean()

        # Layer 4: Clip loss as final safety net
        loss = torch.clamp(loss, 0, 100.0)

        # Backpropagation
        self.optimizer.zero_grad()  # Clear previous gradients
        loss.backward()  # Compute gradients

        # Layer 5: Gradient clipping to prevent exploding gradients
        torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), 0.5)

        self.optimizer.step()  # Update weights

        # Update priorities in replay buffer based on new TD errors
        td_errors_np = torch.clamp(td_errors, -10, 10).detach().cpu().numpy()
        self.memory.update_priorities(indices, np.abs(td_errors_np))

        # Soft update target network periodically
        self.steps += 1
        if self.steps % DRLConfig.TARGET_UPDATE_FREQUENCY == 0:
            self.soft_update_target_network()

        return loss.item()

    def soft_update_target_network(self):
        """
        Gradually update target network toward policy network.

        Uses exponential moving average instead of hard copying:
            θ_target ← τ·θ_policy + (1-τ)·θ_target

        With τ=0.005 (TAU in config):
            - 0.5% new policy weights
            - 99.5% old target weights

        This creates a slowly-moving target for stable learning,
        preventing the "chasing a moving target" problem.

        Called every TARGET_UPDATE_FREQUENCY steps (500 in config).
        """
        for target_param, policy_param in zip(
            self.target_net.parameters(), self.policy_net.parameters()
        ):
            target_param.data.copy_(
                DRLConfig.TAU * policy_param.data
                + (1 - DRLConfig.TAU) * target_param.data
            )

    def decay_epsilon(self):
        """
        Decay exploration rate (epsilon) after each episode.

        Implements exponential decay:
            ε ← max(ε_min, ε × decay_rate)

        Progression (with decay=0.995):
            Episode 1:   ε = 1.000 (100% random)
            Episode 100: ε = 0.606 (60% random)
            Episode 200: ε = 0.368 (37% random)
            Episode 500: ε = 0.082 (8% random)
            Episode 700: ε = 0.010 (1% random, minimum reached)

        Call this once per episode, typically after episode completes.
        """
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save(self, filepath):
        """
        Save complete agent state to checkpoint file.

        Saves everything needed to resume training:
        - Policy network weights
        - Target network weights
        - Optimizer state (momentum, learning rate schedule, etc.)
        - Current epsilon value
        - Training step counter
        - Episode counter

        Args:
            filepath (str): Path to save checkpoint (.pth file)

        Example:
            agent.save('models/checkpoint_ep500.pth')
        """
        checkpoint = {
            "policy_net_state_dict": self.policy_net.state_dict(),
            "target_net_state_dict": self.target_net.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "epsilon": self.epsilon,
            "steps": self.steps,
            "episode_count": self.episode_count,
        }
        torch.save(checkpoint, filepath)
        print(f"Model saved to {filepath}")

    def load(self, filepath):
        """
        Load agent state from checkpoint file.

        Restores complete training state including:
        - Network weights (policy and target)
        - Optimizer state
        - Exploration parameter (epsilon)
        - Training counters

        Args:
            filepath (str): Path to checkpoint file (.pth)

        Example:
            agent.load('models/checkpoint_ep500.pth')
            # Continue training from episode 500

            agent.load('models/final_model.pth')
            agent.set_eval_mode()
            # Use for testing
        """
        checkpoint = torch.load(filepath, map_location=self.device)
        self.policy_net.load_state_dict(checkpoint["policy_net_state_dict"])
        self.target_net.load_state_dict(checkpoint["target_net_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        self.epsilon = checkpoint["epsilon"]
        self.steps = checkpoint["steps"]
        self.episode_count = checkpoint["episode_count"]
        print(f"Model loaded from {filepath}")

    def set_eval_mode(self):
        """
        Set networks to evaluation mode for testing.

        Disables training-specific behaviors:
        - Dropout layers (if any)
        - Batch normalization updates (if any)

        Call before testing to ensure deterministic behavior.
        Set epsilon=0.0 separately for pure exploitation.

        Example:
            agent.set_eval_mode()
            agent.epsilon = 0.0
            # Now ready for testing
        """
        self.policy_net.eval()
        self.target_net.eval()

    def set_train_mode(self):
        """
        Set networks to training mode.

        Enables training-specific behaviors:
        - Dropout layers (if any)
        - Batch normalization updates (if any)

        Note: Target network always stays in eval mode
        (it's never trained directly, only updated via soft copying).

        Example:
            agent.set_train_mode()
            # Now ready for training episodes
        """
        self.policy_net.train()
        self.target_net.eval()  # Target network always in eval mode
