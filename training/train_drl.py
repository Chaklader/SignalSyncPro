"""
Training script for DRL traffic signal control
"""
import os
import sys
import numpy as np
import torch
from datetime import datetime
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add SUMO tools to path if SUMO_HOME is set
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    if tools not in sys.path:
        sys.path.append(tools)

from drl.agent import DQNAgent
from drl.traffic_management import TrafficManagement
from drl.config import DRLConfig
from env_config import get_run_mode, is_training_mode, is_test_mode, print_config
from traffic_config import get_traffic_config
from route_generator import generate_all_routes

class TrainingLogger:
    """
    Logger for training metrics
    """
    def __init__(self, log_dir):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        self.episode_rewards = []
        self.episode_losses = []
        self.episode_lengths = []
        self.epsilon_history = []
        self.metrics_history = []
        
    def log_episode(self, episode, reward, loss, length, epsilon, metrics):
        """Log episode statistics"""
        self.episode_rewards.append(reward)
        self.episode_losses.append(loss)
        self.episode_lengths.append(length)
        self.epsilon_history.append(epsilon)
        self.metrics_history.append(metrics)
        
        # Print progress
        if episode % 10 == 0:
            avg_reward = np.mean(self.episode_rewards[-10:])
            avg_loss = np.mean([l for l in self.episode_losses[-10:] if l is not None])
            print(f"Episode {episode} | Avg Reward: {avg_reward:.2f} | Avg Loss: {avg_loss:.4f} | Epsilon: {epsilon:.3f}")
    
    def save_logs(self):
        """Save training logs to CSV"""
        df = pd.DataFrame({
            'episode': range(len(self.episode_rewards)),
            'reward': self.episode_rewards,
            'loss': self.episode_losses,
            'length': self.episode_lengths,
            'epsilon': self.epsilon_history
        })
        df.to_csv(os.path.join(self.log_dir, 'training_log.csv'), index=False)
        
        # Save detailed metrics
        metrics_df = pd.DataFrame(self.metrics_history)
        metrics_df.to_csv(os.path.join(self.log_dir, 'training_metrics.csv'), index=False)
    
    def plot_training_progress(self):
        """Plot training curves"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Reward
        axes[0, 0].plot(self.episode_rewards)
        axes[0, 0].plot(pd.Series(self.episode_rewards).rolling(50).mean(), color='red', label='MA(50)')
        axes[0, 0].set_title('Episode Reward')
        axes[0, 0].set_xlabel('Episode')
        axes[0, 0].set_ylabel('Total Reward')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss
        losses = [l for l in self.episode_losses if l is not None]
        axes[0, 1].plot(losses)
        axes[0, 1].set_title('Training Loss')
        axes[0, 1].set_xlabel('Episode')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].grid(True)
        
        # Episode length
        axes[1, 0].plot(self.episode_lengths)
        axes[1, 0].set_title('Episode Length')
        axes[1, 0].set_xlabel('Episode')
        axes[1, 0].set_ylabel('Steps')
        axes[1, 0].grid(True)
        
        # Epsilon decay
        axes[1, 1].plot(self.epsilon_history)
        axes[1, 1].set_title('Exploration Rate (Epsilon)')
        axes[1, 1].set_xlabel('Episode')
        axes[1, 1].set_ylabel('Epsilon')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.log_dir, 'training_progress.png'))
        plt.close()

def train_drl_agent():
    """
    Main training function
    """
    # Print environment configuration
    print_config()
    
    # Check if in training mode
    if not is_training_mode():
        print(f"\n⚠️  WARNING: RUN_MODE is set to '{get_run_mode()}', not 'training'")
        print("To run training, set RUN_MODE=training in .env file")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Training cancelled.")
            return
    
    # Setup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = f"logs/training_{timestamp}"
    model_dir = f"models/training_{timestamp}"
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    
    # Initialize environment
    sumo_config = "test.sumocfg"
    tls_ids = ['3', '6']  # Traffic light IDs
    env = TrafficManagement(sumo_config, tls_ids, gui=False)
    
    # Get state dimension from initial reset
    initial_state = env.reset()
    state_dim = len(initial_state)
    action_dim = DRLConfig.ACTION_DIM
    env.close()
    
    print(f"State dimension: {state_dim}")
    print(f"Action dimension: {action_dim}")
    
    # Initialize agent
    agent = DQNAgent(state_dim, action_dim)
    logger = TrainingLogger(log_dir)
    
    # Training loop
    print(f"\nStarting training for {DRLConfig.NUM_EPISODES} episodes...")
    print(f"Logs will be saved to: {log_dir}")
    print(f"Models will be saved to: {model_dir}\n")
    
    for episode in tqdm(range(DRLConfig.NUM_EPISODES), desc="Training"):
        # 1. Get dynamic traffic configuration for this episode
        traffic_config = get_traffic_config()
        
        # 2. Generate route files with new traffic volumes
        generate_all_routes(traffic_config)
        
        # 3. Reset environment (SUMO loads fresh routes)
        state = env.reset()
        
        # IMPORTANT: Reset reward calculator for new episode
        env.reward_calculator.reset()
        
        episode_reward = 0
        episode_losses = []
        step_count = 0
        episode_metrics = {
            'avg_waiting_time': [],
            'waiting_time_car': [],
            'waiting_time_bicycle': [],
            'waiting_time_bus': [],
            'waiting_time_pedestrian': [],
            'sync_success_count': 0,
            'pedestrian_phase_count': 0
        }
        
        # Episode loop
        for step in range(DRLConfig.MAX_STEPS_PER_EPISODE):
            # Select action
            action = agent.select_action(state, explore=True)
            
            # Take step in environment
            next_state, reward, done, info = env.step(action)
            
            # Store experience
            agent.store_experience(state, action, reward, next_state, done, info)
            
            # Train agent
            if step % DRLConfig.UPDATE_FREQUENCY == 0:
                loss = agent.train()
                if loss is not None:
                    episode_losses.append(loss)
            
            # Update state and metrics
            state = next_state
            episode_reward += reward
            step_count += 1
            
            # Track metrics
            episode_metrics['avg_waiting_time'].append(info.get('waiting_time', 0))
            episode_metrics['waiting_time_car'].append(info.get('waiting_time_car', 0))
            episode_metrics['waiting_time_bicycle'].append(info.get('waiting_time_bicycle', 0))
            episode_metrics['waiting_time_bus'].append(info.get('waiting_time_bus', 0))
            episode_metrics['waiting_time_pedestrian'].append(info.get('waiting_time_pedestrian', 0))
            if info.get('sync_achieved', False):
                episode_metrics['sync_success_count'] += 1
            if info.get('event_type') == 'pedestrian_phase':
                episode_metrics['pedestrian_phase_count'] += 1
            
            # Check if done
            if done:
                break
        
        # Close environment
        env.close()
        
        # Decay epsilon
        agent.decay_epsilon()
        agent.episode_count += 1
        
        # Calculate episode statistics
        avg_loss = np.mean(episode_losses) if episode_losses else None
        avg_reward = episode_reward / step_count if step_count > 0 else 0  # Average reward per step
        final_metrics = {
            'avg_waiting_time': np.mean(episode_metrics['avg_waiting_time']),
            'waiting_time_car': np.mean(episode_metrics['waiting_time_car']),
            'waiting_time_bicycle': np.mean(episode_metrics['waiting_time_bicycle']),
            'waiting_time_bus': np.mean(episode_metrics['waiting_time_bus']),
            'waiting_time_pedestrian': np.mean(episode_metrics['waiting_time_pedestrian']),
            'sync_success_rate': episode_metrics['sync_success_count'] / step_count if step_count > 0 else 0,
            'pedestrian_phase_count': episode_metrics['pedestrian_phase_count']
        }
        
        # Log episode (using average reward per step)
        logger.log_episode(episode, avg_reward, avg_loss, step_count, agent.epsilon, final_metrics)
        
        # Save checkpoint
        if (episode + 1) % DRLConfig.SAVE_FREQUENCY == 0:
            checkpoint_path = os.path.join(model_dir, f"checkpoint_ep{episode+1}.pth")
            agent.save(checkpoint_path)
            logger.save_logs()
            logger.plot_training_progress()
    
    # Save final model
    final_model_path = os.path.join(model_dir, "final_model.pth")
    agent.save(final_model_path)
    
    # Save logs and plots
    logger.save_logs()
    logger.plot_training_progress()
    
    print(f"\nTraining complete!")
    print(f"Final model saved to: {final_model_path}")
    print(f"Training logs saved to: {log_dir}")

if __name__ == "__main__":
    train_drl_agent()
