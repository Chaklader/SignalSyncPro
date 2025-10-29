"""
Training script for DRL traffic signal control
"""

import os
import sys

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)
from common.sumo_utils import setup_environment  # noqa: E402

setup_environment()

import numpy as np  # noqa: E402
import random  # noqa: E402
from datetime import datetime  # noqa: E402
from tqdm import tqdm  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import torch  # noqa: E402

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
from constants.developed.common.drl_tls_constants import TLS_IDS  # noqa: E402


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

        print(f"\n{'=' * 80}")
        print(f"Episode {episode} Complete:")
        loss_str = f"{loss:.4f}" if loss is not None else "N/A"
        print(
            f"  Reward: {reward:.4f} | Loss: {loss_str} | Steps: {length} | Epsilon: {epsilon:.3f}"
        )
        print(
            f"  Car: {metrics['avg_waiting_time_car']:.2f}s | Bike: {metrics['avg_waiting_time_bicycle']:.2f}s | Bus: {metrics['avg_waiting_time_bus']:.2f}s"
        )

        print("\n  Reward Components (avg per step):")
        print(f"    Waiting:           {metrics['reward_waiting_avg']:+.4f}")
        print(f"    Flow:              {metrics['reward_flow_avg']:+.4f}")
        print(f"    CO2:               {metrics['reward_co2_avg']:+.4f}")
        print(f"    Equity:            {metrics['reward_equity_avg']:+.4f}")
        print(
            f"    Safety:            {metrics['reward_safety_avg']:+.4f}  "
            f"({metrics['safety_violations_total']} violations)"
        )
        print(f"    Blocked:           {metrics['reward_blocked_avg']:+.4f}")
        print(f"    Diversity:         {metrics['reward_diversity_avg']:+.4f}")
        print(
            f"    Consecutive Cont:  {metrics['reward_consecutive_continue_avg']:+.4f}"
        )
        print(f"    Bus Assistance:    {metrics['reward_bus_assistance_avg']:+.4f}")
        print(f"    Exploration:       {metrics['reward_exploration_avg']:+.4f}")
        print(f"    Next Bonus:        {metrics['reward_next_bonus_avg']:+.4f}")
        print(f"    Stability:         {metrics['reward_stability_avg']:+.4f}")
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

        df = df.round({"reward": 4, "loss": 4, "epsilon": 4, "length": 0})
        df.to_csv(os.path.join(self.log_dir, "training_log.csv"), index=False)

        metrics_df = pd.DataFrame(self.metrics_history)
        metrics_df = metrics_df.round(2)
        metrics_df.to_csv(
            os.path.join(self.log_dir, "training_metrics.csv"), index=False
        )

    def plot_training_progress(self):
        """Plot training curves"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

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

        losses = [loss for loss in self.episode_losses if loss is not None]
        axes[0, 1].plot(losses)
        axes[0, 1].set_title("Training Loss")
        axes[0, 1].set_xlabel("Episode")
        axes[0, 1].set_ylabel("Loss")
        axes[0, 1].grid(True)

        axes[1, 0].plot(self.episode_lengths)
        axes[1, 0].set_title("Episode Length")
        axes[1, 0].set_xlabel("Episode")
        axes[1, 0].set_ylabel("Steps")
        axes[1, 0].grid(True)

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

    clean_route_directory()

    print("\nGenerating initial routes...")
    traffic_config = get_traffic_config()  # Random traffic
    generate_all_routes_developed(traffic_config, SIMULATION_LIMIT_TRAIN)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = f"logs/training_{timestamp}"
    model_dir = f"models/training_{timestamp}"
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    sumo_config = "configurations/developed/drl/single_agent/signal_sync.sumocfg"

    traffic_management = TrafficManagement(
        sumo_config, TLS_IDS, gui=False, simulation_limit=SIMULATION_LIMIT_TRAIN
    )

    initial_state = traffic_management.reset()
    state_dim = len(initial_state)
    action_dim = DRLConfig.ACTION_DIM

    traffic_management.close()

    print(f"State dimension: {state_dim}")
    print(f"Action dimension: {action_dim}")

    agent = DQNAgent(state_dim, action_dim)
    logger = TrainingLogger(log_dir)

    print(f"\nStarting training for {NUM_EPISODES_TRAIN} episodes...")
    print(f"Logs will be saved to: {log_dir}")
    print(f"Models will be saved to: {model_dir}\n")

    all_scenarios = [f"{t}_{n}" for t in ["Pr", "Bi", "Pe"] for n in range(10)]
    random.shuffle(all_scenarios)
    scenario_idx = 0
    test_episode_in_window = -1
    test_position_in_window = -1

    print(f"\n{'=' * 70}")
    print(f"TRAINING PLAN ({NUM_EPISODES_TRAIN} episodes total):")
    print("  - ~75% episodes: RANDOM traffic")
    print("  - ~25% episodes: TEST scenarios (1 per 4-episode window, random position)")
    print("  - All 30 scenarios will be used in shuffled order")
    print("  - Position within each 4-episode window is randomized")
    print(f"{'=' * 70}\n")

    for episode in tqdm(range(1, NUM_EPISODES_TRAIN + 1), desc="Training"):
        window_start = ((episode - 1) // 4) * 4 + 1
        is_window_start = episode == window_start

        if is_window_start:
            test_position_in_window = random.randint(0, 3)
            test_episode_in_window = window_start + test_position_in_window

        if episode == test_episode_in_window:
            scenario = all_scenarios[scenario_idx % 30]
            scenario_idx += 1

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

        state = traffic_management.reset()

        traffic_management.reward_calculator.reset()

        episode_reward = 0
        episode_losses = []
        step_count = 0
        episode_metrics = {
            "avg_waiting_time_car": [],
            "avg_waiting_time_bicycle": [],
            "avg_waiting_time_bus": [],
            "avg_waiting_time_pedestrian": [],
            "co2_total_kg": [],
            "reward_waiting": [],
            "reward_flow": [],
            "reward_co2": [],
            "reward_equity": [],
            "reward_safety": [],
            "reward_blocked": [],
            "reward_diversity": [],
            "reward_consecutive_continue": [],
            "reward_bus_assistance": [],
            "reward_exploration": [],
            "reward_next_bonus": [],
            "reward_stability": [],
            "safety_violations_total": 0,
        }

        for step in range(SIMULATION_LIMIT_TRAIN):
            valid_actions = traffic_management.get_valid_actions()
            action = agent.select_action(
                state, explore=True, valid_actions=valid_actions
            )
            next_state, reward, done, info = traffic_management.step(
                action, epsilon=agent.epsilon
            )

            agent.store_experience(state, action, reward, next_state, done, info)

            if step % UPDATE_FREQUENCY == 0:
                loss = agent.train()
                if loss is not None:
                    episode_losses.append(loss)

            state = next_state
            episode_reward += reward
            step_count += 1

            episode_metrics["avg_waiting_time_car"].append(
                info.get("waiting_time_car", 0)
            )
            episode_metrics["avg_waiting_time_bicycle"].append(
                info.get("waiting_time_bicycle", 0)
            )
            episode_metrics["avg_waiting_time_bus"].append(
                info.get("waiting_time_bus", 0)
            )
            episode_metrics["avg_waiting_time_pedestrian"].append(
                info.get("waiting_time_pedestrian", 0)
            )
            episode_metrics["co2_total_kg"].append(info.get("co2_total_kg", 0))
            episode_metrics["reward_waiting"].append(info.get("reward_waiting", 0))
            episode_metrics["reward_flow"].append(info.get("reward_flow", 0))
            episode_metrics["reward_co2"].append(info.get("reward_co2", 0))
            episode_metrics["reward_equity"].append(info.get("reward_equity", 0))
            episode_metrics["reward_safety"].append(info.get("reward_safety", 0))
            episode_metrics["reward_blocked"].append(info.get("reward_blocked", 0))
            episode_metrics["reward_diversity"].append(info.get("reward_diversity", 0))
            episode_metrics["reward_consecutive_continue"].append(
                info.get("reward_consecutive_continue", 0)
            )
            episode_metrics["reward_bus_assistance"].append(
                info.get("reward_bus_assistance", 0)
            )
            episode_metrics["reward_exploration"].append(
                info.get("reward_exploration", 0)
            )
            episode_metrics["reward_next_bonus"].append(
                info.get("reward_next_bonus", 0)
            )
            episode_metrics["reward_stability"].append(info.get("reward_stability", 0))

            episode_metrics["safety_violations_total"] += info.get(
                "safety_violations_total", 0
            )

            if done:
                break

        traffic_management.close()
        agent.decay_epsilon()
        agent.episode_count += 1

        avg_loss = np.mean(episode_losses) if episode_losses else None
        avg_reward = episode_reward / step_count if step_count > 0 else 0

        final_metrics = {
            "avg_waiting_time_car": np.mean(episode_metrics["avg_waiting_time_car"]),
            "avg_waiting_time_bicycle": np.mean(
                episode_metrics["avg_waiting_time_bicycle"]
            ),
            "avg_waiting_time_bus": np.mean(episode_metrics["avg_waiting_time_bus"]),
            "avg_waiting_time_pedestrian": np.mean(
                episode_metrics["avg_waiting_time_pedestrian"]
            ),
            "co2_total_kg": np.mean(episode_metrics["co2_total_kg"]),
            "reward_waiting_avg": np.mean(episode_metrics["reward_waiting"]),
            "reward_flow_avg": np.mean(episode_metrics["reward_flow"]),
            "reward_co2_avg": np.mean(episode_metrics["reward_co2"]),
            "reward_equity_avg": np.mean(episode_metrics["reward_equity"]),
            "reward_safety_avg": np.mean(episode_metrics["reward_safety"]),
            "reward_blocked_avg": np.mean(episode_metrics["reward_blocked"]),
            "reward_diversity_avg": np.mean(episode_metrics["reward_diversity"]),
            "reward_consecutive_continue_avg": np.mean(
                episode_metrics["reward_consecutive_continue"]
            ),
            "reward_bus_assistance_avg": np.mean(
                episode_metrics["reward_bus_assistance"]
            ),
            "reward_exploration_avg": np.mean(episode_metrics["reward_exploration"]),
            "reward_next_bonus_avg": np.mean(episode_metrics["reward_next_bonus"]),
            "reward_stability_avg": np.mean(episode_metrics["reward_stability"]),
            "safety_violations_total": episode_metrics["safety_violations_total"],
        }

        logger.log_episode(
            episode, avg_reward, avg_loss, step_count, agent.epsilon, final_metrics
        )

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

            sample_size = min(1000, len(agent.memory))
            batch, indices, weights = agent.memory.sample(sample_size)

            continue_q_values = []
            skip2p1_q_values = []
            next_q_values = []
            action_counts = {"Continue": 0, "Skip2P1": 0, "Next": 0}

            for i, (state, action, reward, next_state, done) in enumerate(batch):
                with torch.no_grad():
                    state_tensor = (
                        torch.FloatTensor(state).unsqueeze(0).to(agent.device)
                    )

                    q_vals = agent.policy_net(state_tensor).squeeze()
                    q_list = q_vals.tolist()

                    continue_q = q_list[0]
                    skip2p1_q = q_list[1]
                    next_q = q_list[2]

                    continue_q_values.append(continue_q)
                    skip2p1_q_values.append(skip2p1_q)
                    next_q_values.append(next_q)

                    best_action = ["Continue", "Skip2P1", "Next"][
                        q_vals.argmax().item()
                    ]
                    action_counts[best_action] += 1

                    if i < 100:
                        print(
                            f"  State {i + 1}: Continue={continue_q:+.3f} | Skip2P1={skip2p1_q:+.3f} | Next={next_q:+.3f} → Best: {best_action}"
                        )

            avg_continue_q = sum(continue_q_values) / len(continue_q_values)
            avg_skip2p1_q = sum(skip2p1_q_values) / len(skip2p1_q_values)
            avg_next_q = sum(next_q_values) / len(next_q_values)

            q_value_spread = max(avg_continue_q, avg_skip2p1_q, avg_next_q) - min(
                avg_continue_q, avg_skip2p1_q, avg_next_q
            )

            print(f"\n  Summary (from {sample_size} sampled states):")
            print(f"    Avg Continue Q-value: {avg_continue_q:+.3f}")
            print(f"    Avg Skip2P1 Q-value:  {avg_skip2p1_q:+.3f}")
            print(f"    Avg Next Q-value:     {avg_next_q:+.3f}")
            print(f"    Q-value Spread:       {q_value_spread:.3f}")
            print("\n  Best Action Distribution:")
            for action, count in action_counts.items():
                pct = (count / sample_size) * 100
                print(f"    {action:12s}: {count:3d}/{sample_size} ({pct:5.1f}%)")

            if q_value_spread < 0.3:
                print("    ✅ GOOD! Q-values well-balanced (spread < 0.3)")
            elif q_value_spread < 0.8:
                print("    ⚠️  WARNING: Q-values moderately imbalanced (spread 0.3-0.8)")
            else:
                print("    ❌ PROBLEM: Q-values highly imbalanced (spread > 0.8)")

            print(f"{'=' * 70}\n")

        if episode % LOG_SAVE_FREQUENCY == 0:
            logger.save_logs()

        if episode % MODEL_SAVE_FREQUENCY == 0:
            checkpoint_path = os.path.join(model_dir, f"checkpoint_ep{episode}.pth")
            agent.save(checkpoint_path)
            logger.plot_training_progress()

    final_model_path = os.path.join(model_dir, "final_model.pth")
    agent.save(final_model_path)
    logger.save_logs()
    logger.plot_training_progress()
    traffic_management.close()

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
