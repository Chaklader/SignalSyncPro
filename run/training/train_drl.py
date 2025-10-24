"""
Training script for DRL traffic signal control
"""

import os
import sys

# CRITICAL: Setup paths FIRST, before any other imports
# Temporarily add project root to import sumo_utils
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)

# Use centralized path setup utility
from common.sumo_utils import setup_environment  # noqa: E402

setup_environment()

# Now safe to import everything else
import numpy as np  # noqa: E402
import random  # noqa: E402
from datetime import datetime  # noqa: E402
from tqdm import tqdm  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from controls.ml_based.drl.agent import DQNAgent  # noqa: E402
from controls.ml_based.drl.traffic_management import TrafficManagement  # noqa: E402
from controls.ml_based.drl.config import DRLConfig  # noqa: E402
from route_generator.traffic_config import get_traffic_config  # noqa: E402
from route_generator import generate_all_routes_developed  # noqa: E402
from common.utils import clean_route_directory  # noqa: E402
from constants.constants import (  # noqa: E402
    NUM_EPISODES_TRAIN,
    SIMULATION_LIMIT_TRAIN,
    UPDATE_FREQUENCY,
    MODEL_SAVE_FREQUENCY,
    LOG_SAVE_FREQUENCY,
)


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
        print(f"\n{'=' * 80}")
        print(f"Episode {episode} Complete:")
        loss_str = f"{loss:.4f}" if loss is not None else "N/A"
        print(
            f"  Reward: {reward:.4f} | Loss: {loss_str} | Steps: {length} | Epsilon: {epsilon:.3f}"
        )
        print(
            f"  Avg Wait: {metrics['avg_waiting_time']:.2f}s | Sync Rate: {metrics['sync_success_rate']:.2%}"
        )
        print(
            f"  Car: {metrics['waiting_time_car']:.2f}s | Bike: {metrics['waiting_time_bicycle']:.2f}s | Bus: {metrics['waiting_time_bus']:.2f}s"
        )

        # NEW: Print ALL reward component breakdown (Phase 4 - Oct 24, 2025)
        print("\n  Reward Components (avg per step):")
        print(f"    Waiting:           {metrics['reward_waiting_avg']:+.4f}")
        print(f"    Flow:              {metrics['reward_flow_avg']:+.4f}")
        print(f"    CO2:               {metrics['reward_co2_avg']:+.4f}")
        print(f"    Equity:            {metrics['reward_equity_avg']:+.4f}")
        print(
            f"    Safety:            {metrics['reward_safety_avg']:+.4f}  ({metrics['safety_violation_count']} violations, {metrics['safety_violation_rate']:.1%} of steps)"
        )
        print(
            f"    Pedestrian:        {metrics['reward_pedestrian_avg']:+.4f}  ({metrics['ped_demand_ignored_count']} ignored, {metrics['ped_demand_ignored_rate']:.1%} of steps)"
        )
        print(f"    Blocked:           {metrics['reward_blocked_avg']:+.4f}")
        print(f"    Diversity:         {metrics['reward_diversity_avg']:+.4f}")
        print(f"    Ped Activation:    {metrics['reward_ped_activation_avg']:+.4f}")
        print(f"    Excessive Cont:    {metrics['reward_excessive_continue_avg']:+.4f}")
        print(
            f"    Consecutive Cont:  {metrics['reward_consecutive_continue_avg']:+.4f}"
        )
        print(f"    {'─' * 40}")
        print(f"    TOTAL:             {reward:.4f}")
        print(f"{'=' * 80}")

    def save_logs(self):
        """Save training logs to CSV"""
        df = pd.DataFrame(
            {
                "episode": range(
                    1, len(self.episode_rewards) + 1
                ),  # Start from 1, not 0
                "reward": self.episode_rewards,
                "loss": self.episode_losses,
                "length": self.episode_lengths,
                "epsilon": self.epsilon_history,
            }
        )
        df.to_csv(os.path.join(self.log_dir, "training_log.csv"), index=False)

        # Save detailed metrics
        metrics_df = pd.DataFrame(self.metrics_history)
        metrics_df.to_csv(
            os.path.join(self.log_dir, "training_metrics.csv"), index=False
        )

    def plot_training_progress(self):
        """Plot training curves"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        # Reward
        axes[0, 0].plot(self.episode_rewards)
        axes[0, 0].plot(
            pd.Series(self.episode_rewards).rolling(50).mean(),
            color="red",
            label="MA(50)",
        )
        axes[0, 0].set_title("Episode Reward")
        axes[0, 0].set_xlabel("Episode")
        axes[0, 0].set_ylabel("Total Reward")
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        # Loss
        losses = [loss for loss in self.episode_losses if loss is not None]
        axes[0, 1].plot(losses)
        axes[0, 1].set_title("Training Loss")
        axes[0, 1].set_xlabel("Episode")
        axes[0, 1].set_ylabel("Loss")
        axes[0, 1].grid(True)

        # Episode length
        axes[1, 0].plot(self.episode_lengths)
        axes[1, 0].set_title("Episode Length")
        axes[1, 0].set_xlabel("Episode")
        axes[1, 0].set_ylabel("Steps")
        axes[1, 0].grid(True)

        # Epsilon decay
        axes[1, 1].plot(self.epsilon_history)
        axes[1, 1].set_title("Exploration Rate (Epsilon)")
        axes[1, 1].set_xlabel("Episode")
        axes[1, 1].set_ylabel("Epsilon")
        axes[1, 1].grid(True)

        plt.tight_layout()
        plt.savefig(os.path.join(self.log_dir, "training_progress.png"))
        plt.close()


def train_drl_agent():
    """
    Main training function for DRL agent
    """
    print("\n" + "=" * 50)
    print("DRL TRAFFIC SIGNAL CONTROL - TRAINING")
    print("=" * 50 + "\n")

    # Training mode - no configuration needed

    # STEP 1: Clean route directory before starting
    clean_route_directory()

    # STEP 2: Generate initial routes (needed for SUMO config)
    print("\nGenerating initial routes...")
    traffic_config = get_traffic_config()  # Random traffic
    generate_all_routes_developed(traffic_config, SIMULATION_LIMIT_TRAIN)

    # Setup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = f"logs/training_{timestamp}"
    model_dir = f"models/training_{timestamp}"
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    # Initialize environment
    sumo_config = "configurations/developed/common/signal_sync.sumocfg"
    tls_ids = ["3", "6"]  # Traffic light IDs
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
    print(f"\nStarting training for {NUM_EPISODES_TRAIN} episodes...")
    print(f"Logs will be saved to: {log_dir}")
    print(f"Models will be saved to: {model_dir}\n")

    # Randomized test scenario scheduling to prevent gaming
    # Strategy: In every 4-episode window, use exactly 1 test scenario at random position
    all_scenarios = [f"{t}_{n}" for t in ["Pr", "Bi", "Pe"] for n in range(10)]
    random.shuffle(all_scenarios)  # Shuffle all 30 scenarios
    scenario_idx = 0  # Track which scenario to use next

    print(f"\n{'=' * 70}")
    print(f"TRAINING PLAN ({NUM_EPISODES_TRAIN} episodes total):")
    print("  - ~75% episodes: RANDOM traffic")
    print("  - ~25% episodes: TEST scenarios (1 per 4-episode window, random position)")
    print("  - All 30 scenarios will be used in shuffled order")
    print("  - Position within each 4-episode window is randomized")
    print(f"{'=' * 70}\n")

    for episode in tqdm(range(1, NUM_EPISODES_TRAIN + 1), desc="Training"):
        # STEP 3: Generate new routes for each episode
        # Determine if this is the start of a new 4-episode window
        window_start = ((episode - 1) // 4) * 4 + 1  # Episodes 1, 5, 9, 13, ...
        is_window_start = episode == window_start

        # At start of each 4-episode window, randomly pick which position gets test scenario
        if is_window_start:
            # Randomly choose position 0, 1, 2, or 3 within this window
            test_position_in_window = random.randint(0, 3)
            # Mark which episode in this window gets the test scenario
            test_episode_in_window = window_start + test_position_in_window

        # Check if current episode is the chosen one for test scenario
        if episode == test_episode_in_window:
            # Use next test scenario from shuffled list
            scenario = all_scenarios[scenario_idx % 30]
            scenario_idx += 1

            # If we've used all 30 scenarios, reshuffle for next cycle
            if scenario_idx % 30 == 0:
                random.shuffle(all_scenarios)
                print(f"\n{'=' * 70}")
                print(
                    "[CYCLE COMPLETE] All 30 scenarios used. Reshuffling for next cycle..."
                )
                print(f"{'=' * 70}\n")

            traffic_config = get_traffic_config(scenario=scenario)
            print(f"\n{'=' * 70}")
            print(
                f"Episode {episode} - Using TEST scenario: {scenario} (#{scenario_idx}, pos {test_position_in_window + 1}/4 in window)"
            )
            print(f"  Cars: {traffic_config['cars']}/hr")
            print(f"  Bicycles: {traffic_config['bicycles']}/hr")
            print(f"  Pedestrians: {traffic_config['pedestrians']}/hr")
            print(f"  Buses: {traffic_config['buses']}")
            print(f"{'=' * 70}")
        else:
            traffic_config = get_traffic_config()  # Random traffic
            print(f"\n{'=' * 70}")
            print(f"Episode {episode} - Generating RANDOM routes:")
            print(f"  Cars: {traffic_config['cars']}/hr")
            print(f"  Bicycles: {traffic_config['bicycles']}/hr")
            print(f"  Pedestrians: {traffic_config['pedestrians']}/hr")
            print(f"  Buses: {traffic_config['buses']}")
            print(f"{'=' * 70}")

        generate_all_routes_developed(traffic_config, SIMULATION_LIMIT_TRAIN)

        # Reset environment (SUMO loads fresh routes)
        state = env.reset()

        # IMPORTANT: Reset reward calculator for new episode
        env.reward_calculator.reset()

        episode_reward = 0
        episode_losses = []
        step_count = 0
        episode_metrics = {
            "avg_waiting_time": [],
            "waiting_time_car": [],
            "waiting_time_bicycle": [],
            "waiting_time_bus": [],
            "waiting_time_pedestrian": [],
            "sync_success_count": 0,
            "pedestrian_phase_count": 0,
            # NEW: Track ALL reward components (Phase 4 - Oct 24, 2025)
            "reward_waiting": [],
            "reward_flow": [],
            "reward_co2": [],
            "reward_equity": [],
            "reward_safety": [],
            "reward_pedestrian": [],
            "reward_blocked": [],
            "reward_diversity": [],
            "reward_ped_activation": [],
            "reward_excessive_continue": [],
            "reward_consecutive_continue": [],
            "safety_violation_count": 0,
            "ped_demand_ignored_count": 0,
        }

        # Episode loop
        for step in range(SIMULATION_LIMIT_TRAIN):
            # Select action
            action = agent.select_action(state, explore=True)

            # Take step in environment
            next_state, reward, done, info = env.step(action)

            # Store experience
            agent.store_experience(state, action, reward, next_state, done, info)

            # Train agent
            if step % UPDATE_FREQUENCY == 0:
                loss = agent.train()
                if loss is not None:
                    episode_losses.append(loss)

            # Update state and metrics
            state = next_state
            episode_reward += reward
            step_count += 1

            # Track metrics
            episode_metrics["avg_waiting_time"].append(info.get("waiting_time", 0))
            episode_metrics["waiting_time_car"].append(info.get("waiting_time_car", 0))
            episode_metrics["waiting_time_bicycle"].append(
                info.get("waiting_time_bicycle", 0)
            )
            episode_metrics["waiting_time_bus"].append(info.get("waiting_time_bus", 0))
            episode_metrics["waiting_time_pedestrian"].append(
                info.get("waiting_time_pedestrian", 0)
            )
            if info.get("sync_achieved", False):
                episode_metrics["sync_success_count"] += 1
            if info.get("event_type") == "pedestrian_phase":
                episode_metrics["pedestrian_phase_count"] += 1

            # NEW: Track ALL reward components (Phase 4 - Oct 24, 2025)
            episode_metrics["reward_waiting"].append(info.get("reward_waiting", 0))
            episode_metrics["reward_flow"].append(info.get("reward_flow", 0))
            episode_metrics["reward_co2"].append(info.get("reward_co2", 0))
            episode_metrics["reward_equity"].append(info.get("reward_equity", 0))
            episode_metrics["reward_safety"].append(info.get("reward_safety", 0))
            episode_metrics["reward_pedestrian"].append(
                info.get("reward_pedestrian", 0)
            )
            episode_metrics["reward_blocked"].append(info.get("reward_blocked", 0))
            episode_metrics["reward_diversity"].append(info.get("reward_diversity", 0))
            episode_metrics["reward_ped_activation"].append(
                info.get("reward_ped_activation", 0)
            )
            episode_metrics["reward_excessive_continue"].append(
                info.get("reward_excessive_continue", 0)
            )
            episode_metrics["reward_consecutive_continue"].append(
                info.get("reward_consecutive_continue", 0)
            )
            if info.get("safety_violation", False):
                episode_metrics["safety_violation_count"] += 1
            if info.get("event_type") == "ped_demand_ignored":
                episode_metrics["ped_demand_ignored_count"] += 1

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
        avg_reward = (
            episode_reward / step_count if step_count > 0 else 0
        )  # Average reward per step
        final_metrics = {
            "avg_waiting_time": np.mean(episode_metrics["avg_waiting_time"]),
            "waiting_time_car": np.mean(episode_metrics["waiting_time_car"]),
            "waiting_time_bicycle": np.mean(episode_metrics["waiting_time_bicycle"]),
            "waiting_time_bus": np.mean(episode_metrics["waiting_time_bus"]),
            "waiting_time_pedestrian": np.mean(
                episode_metrics["waiting_time_pedestrian"]
            ),
            "sync_success_rate": (
                episode_metrics["sync_success_count"] / step_count
                if step_count > 0
                else 0
            ),
            "pedestrian_phase_count": episode_metrics["pedestrian_phase_count"],
            # NEW: Average ALL reward components per step (Phase 4 - Oct 24, 2025)
            "reward_waiting_avg": np.mean(episode_metrics["reward_waiting"]),
            "reward_flow_avg": np.mean(episode_metrics["reward_flow"]),
            "reward_co2_avg": np.mean(episode_metrics["reward_co2"]),
            "reward_equity_avg": np.mean(episode_metrics["reward_equity"]),
            "reward_safety_avg": np.mean(episode_metrics["reward_safety"]),
            "reward_pedestrian_avg": np.mean(episode_metrics["reward_pedestrian"]),
            "reward_blocked_avg": np.mean(episode_metrics["reward_blocked"]),
            "reward_diversity_avg": np.mean(episode_metrics["reward_diversity"]),
            "reward_ped_activation_avg": np.mean(
                episode_metrics["reward_ped_activation"]
            ),
            "reward_excessive_continue_avg": np.mean(
                episode_metrics["reward_excessive_continue"]
            ),
            "reward_consecutive_continue_avg": np.mean(
                episode_metrics["reward_consecutive_continue"]
            ),
            "safety_violation_count": episode_metrics["safety_violation_count"],
            "safety_violation_rate": (
                episode_metrics["safety_violation_count"] / step_count
                if step_count > 0
                else 0
            ),
            "ped_demand_ignored_count": episode_metrics["ped_demand_ignored_count"],
            "ped_demand_ignored_rate": (
                episode_metrics["ped_demand_ignored_count"] / step_count
                if step_count > 0
                else 0
            ),
        }

        # Log episode (using average reward per step)
        logger.log_episode(
            episode, avg_reward, avg_loss, step_count, agent.epsilon, final_metrics
        )

        # Q-value Debugging: Track pedestrian Q-values (NEW - Phase 3 Oct 22, 2025)
        # Monitor if ped Q-values are improving during training
        # Changed to EVERY episode for detailed tracking (Phase 3 - Oct 23, 2025)
        # Removed minimum memory check - sample whatever is available (Phase 3 - Oct 23, 2025)
        if len(agent.memory) > 0:
            print(f"\n{'=' * 70}")
            print(f"[Q-VALUE CHECK] Episode {episode} - Pedestrian Q-value Analysis")
            print(f"{'=' * 70}")
            print("  Current Episode Traffic:")
            print(f"    Cars:        {traffic_config['cars']}/hr")
            print(f"    Bicycles:    {traffic_config['bicycles']}/hr")
            print(f"    Pedestrians: {traffic_config['pedestrians']}/hr")
            print(f"    Buses:       {traffic_config['buses']}")
            print(
                f"\n  Note: Sampled states below are from replay buffer (Episodes 1-{episode})"
            )
            print("        and represent a mix of different traffic conditions.")
            print(f"{'=' * 70}")

            # Sample up to 1000 random states from replay buffer for robust statistics
            # Will use whatever is available if < 1000 (Phase 3 - Oct 23, 2025)
            import torch

            sample_size = min(1000, len(agent.memory))
            batch, indices, weights = agent.memory.sample(sample_size)

            ped_q_values = []
            continue_q_values = []
            skip2p1_q_values = []
            next_q_values = []
            action_counts = {"Continue": 0, "Skip2P1": 0, "Next": 0, "Pedestrian": 0}

            for i, (state, action, reward, next_state, done) in enumerate(batch):
                with torch.no_grad():
                    # Convert numpy state to tensor
                    state_tensor = (
                        torch.FloatTensor(state).unsqueeze(0).to(agent.device)
                    )

                    # Get Q-values for this state
                    q_vals = agent.policy_net(state_tensor).squeeze()
                    q_list = q_vals.tolist()

                    continue_q = q_list[0]
                    skip2p1_q = q_list[1]
                    next_q = q_list[2]
                    ped_q = q_list[3]

                    ped_q_values.append(ped_q)
                    continue_q_values.append(continue_q)
                    skip2p1_q_values.append(skip2p1_q)
                    next_q_values.append(next_q)

                    # Determine which action has highest Q-value
                    best_action = ["Continue", "Skip2P1", "Next", "Pedestrian"][
                        q_vals.argmax().item()
                    ]
                    action_counts[best_action] += 1

                    # Print first 100 states as examples
                    # Increased from 5 to 100 for detailed inspection (Phase 3 - Oct 23, 2025)
                    if i < 100:
                        print(
                            f"  State {i + 1}: Continue={continue_q:+.3f} | Skip2P1={skip2p1_q:+.3f} | Next={next_q:+.3f} | Ped={ped_q:+.3f} → Best: {best_action}"
                        )

            # Calculate statistics from sampled states
            avg_ped_q = sum(ped_q_values) / len(ped_q_values)
            avg_continue_q = sum(continue_q_values) / len(continue_q_values)
            avg_skip2p1_q = sum(skip2p1_q_values) / len(skip2p1_q_values)
            avg_next_q = sum(next_q_values) / len(next_q_values)
            ped_q_gap = avg_ped_q - avg_continue_q

            print(f"\n  Summary (from {sample_size} sampled states):")
            print(f"    Avg Continue Q-value: {avg_continue_q:+.3f}")
            print(f"    Avg Skip2P1 Q-value:  {avg_skip2p1_q:+.3f}")
            print(f"    Avg Next Q-value:     {avg_next_q:+.3f}")
            print(f"    Avg Ped Q-value:      {avg_ped_q:+.3f}")
            print(f"    Gap (Ped - Continue): {ped_q_gap:+.3f}")
            print("\n  Best Action Distribution:")
            for action, count in action_counts.items():
                pct = (count / sample_size) * 100
                print(f"    {action:12s}: {count:3d}/{sample_size} ({pct:5.1f}%)")

            if ped_q_gap > -0.5:
                print("    ✅ GOOD! Ped Q-values competitive (gap < 0.5)")
            elif ped_q_gap > -1.5:
                print("    ⚠️  WARNING: Ped Q-values still low (gap -0.5 to -1.5)")
            else:
                print("    ❌ PROBLEM: Ped Q-values very low (gap > -1.5)")

            print(f"{'=' * 70}\n")

        # Save logs after every episode (immediate monitoring)
        if episode % LOG_SAVE_FREQUENCY == 0:
            logger.save_logs()

        # Save model checkpoint less frequently
        if episode % MODEL_SAVE_FREQUENCY == 0:
            checkpoint_path = os.path.join(model_dir, f"checkpoint_ep{episode}.pth")
            agent.save(checkpoint_path)
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

    print(f"\n{'=' * 50}")
    print("TRAINING COMPLETE!")
    print(f"{'=' * 50}")
    print(f"Final model saved to: {final_model_path}")
    print(f"Logs saved to: {log_dir}")
    print(f"Total episodes: {NUM_EPISODES_TRAIN}")
    print(f"Final epsilon: {agent.epsilon:.4f}\n")


if __name__ == "__main__":
    train_drl_agent()
