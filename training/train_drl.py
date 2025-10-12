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
from route_generator import generate_all_routes_developed
from common.utils import clean_route_directory

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
        """Log episode statistics and save immediately"""
        self.episode_rewards.append(reward)
        self.episode_losses.append(loss)
        self.episode_lengths.append(length)
        self.epsilon_history.append(epsilon)
        self.metrics_history.append(metrics)
        
        # Print progress IMMEDIATELY after each episode
        print(f"\n{'='*80}")
        print(f"Episode {episode} Complete:")
        loss_str = f"{loss:.4f}" if loss is not None else "N/A"
        print(f"  Reward: {reward:.4f} | Loss: {loss_str} | Steps: {length} | Epsilon: {epsilon:.3f}")
        print(f"  Avg Wait: {metrics['avg_waiting_time']:.2f}s | Sync Rate: {metrics['sync_success_rate']:.2%}")
        print(f"  Car: {metrics['waiting_time_car']:.2f}s | Bike: {metrics['waiting_time_bicycle']:.2f}s | Bus: {metrics['waiting_time_bus']:.2f}s")
        
        # NEW: Print reward component breakdown
        print(f"\n  Reward Components (avg per step):")
        print(f"    Waiting:    {metrics['reward_waiting_avg']:+.4f}")
        print(f"    Flow:       {metrics['reward_flow_avg']:+.4f}")
        print(f"    Sync:       {metrics['reward_sync_avg']:+.4f}")
        print(f"    CO2:        {metrics['reward_co2_avg']:+.4f}")
        print(f"    Equity:     {metrics['reward_equity_avg']:+.4f}")
        print(f"    Safety:     {metrics['reward_safety_avg']:+.4f}  ({metrics['safety_violation_count']} violations, {metrics['safety_violation_rate']:.1%} of steps)")
        print(f"    Pedestrian: {metrics['reward_pedestrian_avg']:+.4f}  ({metrics['ped_demand_ignored_count']} ignored, {metrics['ped_demand_ignored_rate']:.1%} of steps)")
        print(f"    TOTAL:      {reward:.4f}")
        print(f"{'='*80}")
    
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
    Main training function for DRL agent
    """
    print("\n" + "="*50)
    print("DRL TRAFFIC SIGNAL CONTROL - TRAINING")
    print("="*50 + "\n")
    
    # Print configuration
    print_config()
    
    # Verify we're in training mode
    if not is_training_mode():
        print(f"\n⚠️  WARNING: RUN_MODE is set to '{get_run_mode()}', not 'training'")
        print("To run training, set RUN_MODE=training in .env file")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Training cancelled.")
            return
    
    # STEP 1: Clean route directory before starting
    clean_route_directory()
    
    # STEP 2: Generate initial routes (needed for SUMO config)
    print("\nGenerating initial routes...")
    traffic_config = get_traffic_config()
    generate_all_routes_developed(traffic_config)
    
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
        # STEP 3: Generate new routes for each episode (skip episode 0, already generated)
        if episode > 0:
            traffic_config = get_traffic_config()
            generate_all_routes_developed(traffic_config)
        
        # Reset environment (SUMO loads fresh routes)
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
            'pedestrian_phase_count': 0,
            # NEW: Track reward components
            'reward_waiting': [],
            'reward_flow': [],
            'reward_sync': [],
            'reward_co2': [],
            'reward_equity': [],
            'reward_safety': [],
            'reward_pedestrian': [],
            'safety_violation_count': 0,
            'ped_demand_ignored_count': 0
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
            
            # NEW: Track reward components
            episode_metrics['reward_waiting'].append(info.get('reward_waiting', 0))
            episode_metrics['reward_flow'].append(info.get('reward_flow', 0))
            episode_metrics['reward_sync'].append(info.get('reward_sync', 0))
            episode_metrics['reward_co2'].append(info.get('reward_co2', 0))
            episode_metrics['reward_equity'].append(info.get('reward_equity', 0))
            episode_metrics['reward_safety'].append(info.get('reward_safety', 0))
            episode_metrics['reward_pedestrian'].append(info.get('reward_pedestrian', 0))
            if info.get('safety_violation', False):
                episode_metrics['safety_violation_count'] += 1
            if info.get('event_type') == 'ped_demand_ignored':
                episode_metrics['ped_demand_ignored_count'] += 1
            
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
            'pedestrian_phase_count': episode_metrics['pedestrian_phase_count'],
            # NEW: Average reward components per step
            'reward_waiting_avg': np.mean(episode_metrics['reward_waiting']),
            'reward_flow_avg': np.mean(episode_metrics['reward_flow']),
            'reward_sync_avg': np.mean(episode_metrics['reward_sync']),
            'reward_co2_avg': np.mean(episode_metrics['reward_co2']),
            'reward_equity_avg': np.mean(episode_metrics['reward_equity']),
            'reward_safety_avg': np.mean(episode_metrics['reward_safety']),
            'reward_pedestrian_avg': np.mean(episode_metrics['reward_pedestrian']),
            'safety_violation_count': episode_metrics['safety_violation_count'],
            'safety_violation_rate': episode_metrics['safety_violation_count'] / step_count if step_count > 0 else 0,
            'ped_demand_ignored_count': episode_metrics['ped_demand_ignored_count'],
            'ped_demand_ignored_rate': episode_metrics['ped_demand_ignored_count'] / step_count if step_count > 0 else 0
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
    logger.save_logs()
    logger.plot_training_progress()
    env.close()
    
    # STEP 4: Clean route directory after training completes
    print()
    clean_route_directory()
    
    print(f"\n{'='*50}")
    print("TRAINING COMPLETE!")
    print(f"{'='*50}")
    print(f"Final model saved to: {final_model_path}")
    print(f"Logs saved to: {log_dir}")
    print(f"Total episodes: {DRLConfig.NUM_EPISODES}")
    print(f"Final epsilon: {agent.epsilon:.4f}\n")


if __name__ == "__main__":
    train_drl_agent()
