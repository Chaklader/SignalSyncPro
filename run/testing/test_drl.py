"""
Testing script for DRL traffic signal control
"""

import os
import sys

# CRITICAL: Setup paths FIRST, before any other imports
# Temporarily add project root to import sumo_utils
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Use centralized path setup utility
from common.sumo_utils import setup_environment
setup_environment()

# Now safe to import everything else
import numpy as np
import pandas as pd
from tqdm import tqdm

from controls.ml_based.drl.agent import DQNAgent
from controls.ml_based.drl.traffic_management import TrafficManagement
from controls.ml_based.drl.config import DRLConfig
from route_generator.traffic_config import get_traffic_config
from route_generator import generate_all_routes_developed
from common.utils import clean_route_directory

# Test scenarios
TEST_SCENARIOS = {
    "Pr": list(range(10)),  # Pr_0 to Pr_9
    "Bi": list(range(10)),  # Bi_0 to Bi_9
    "Pe": list(range(10)),  # Pe_0 to Pe_9
}


class TestLogger:
    """
    Logger for test results
    """

    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.results = []

    def log_scenario(self, scenario_name, metrics):
        """Log scenario results"""
        result = {"scenario": scenario_name}
        result.update(metrics)
        self.results.append(result)

    def save_results(self):
        """Save all results to CSV"""
        df = pd.DataFrame(self.results)
        output_path = os.path.join(self.output_dir, "drl_test_results.csv")
        df.to_csv(output_path, index=False)
        print(f"\nResults saved to: {output_path}")
        return df

    def print_summary(self):
        """Print summary statistics"""
        df = pd.DataFrame(self.results)

        print("\n" + "=" * 80)
        print("DRL TEST RESULTS SUMMARY")
        print("=" * 80)

        # Group by scenario type
        for scenario_type in ["Pr", "Bi", "Pe"]:
            scenario_results = df[df["scenario"].str.startswith(scenario_type)]
            if len(scenario_results) > 0:
                print(f"\n{scenario_type} Scenarios (n={len(scenario_results)}):")
                print(
                    f"  Avg Car Wait Time:    {scenario_results['car_wait_time'].mean():.2f}s"
                )
                print(
                    f"  Avg Bike Wait Time:   {scenario_results['bike_wait_time'].mean():.2f}s"
                )
                print(
                    f"  Avg Ped Wait Time:    {scenario_results['ped_wait_time'].mean():.2f}s"
                )
                print(
                    f"  Avg Bus Wait Time:    {scenario_results['bus_wait_time'].mean():.2f}s"
                )
                print(
                    f"  Avg Sync Success:     {scenario_results['sync_success_rate'].mean() * 100:.1f}%"
                )
                print(
                    f"  Avg CO2 Emission:     {scenario_results['co2_emission'].mean():.2f} kg"
                )


def test_drl_agent(model_path, scenarios=None):
    """
    Test trained DRL agent on all scenarios
    """
    # Test mode - no configuration needed None

    if scenarios is None:
        scenarios = TEST_SCENARIOS

    # STEP 1: Clean route directory before starting
    clean_route_directory()

    # STEP 2: Generate initial routes (needed for SUMO config)
    print("\nGenerating initial routes...")
    traffic_config = get_traffic_config(mode='test', scenario='Pr_0')  # Initial dummy config
    generate_all_routes_developed(traffic_config)

    # Initialize environment and agent
    sumo_config = "configurations/developed/common/signal_sync.sumocfg"
    tls_ids = ["3", "6"]
    env = TrafficManagement(sumo_config, tls_ids, gui=False)

    # Get dimensions
    initial_state = env.reset()
    state_dim = len(initial_state)
    action_dim = DRLConfig.ACTION_DIM
    env.close()

    # Initialize agent and load model
    agent = DQNAgent(state_dim, action_dim)
    agent.load(model_path)
    agent.set_eval_mode()

    # Initialize logger
    output_dir = "results/drl_testing"
    logger = TestLogger(output_dir)

    print(
        f"\nTesting DRL agent on {sum(len(v) for v in scenarios.values())} scenarios..."
    )
    print(f"Model: {model_path}\n")

    # Test each scenario
    total_scenarios = sum(len(v) for v in scenarios.values())
    progress_bar = tqdm(total=total_scenarios, desc="Testing scenarios")

    scenario_count = 0
    for scenario_type, scenario_list in scenarios.items():
        for scenario_num in scenario_list:
            scenario_name = f"{scenario_type}_{scenario_num}"

            # STEP 3: Generate routes for each scenario (skip first, already generated)
            if scenario_count > 0:
                traffic_config = get_traffic_config(mode='test', scenario=scenario_name)
                generate_all_routes_developed(traffic_config)
            scenario_count += 1

            # 3. Run episode
            env = TrafficManagement(sumo_config, tls_ids, gui=False)
            state = env.reset()

            episode_metrics = {
                "car_wait_times": [],
                "bike_wait_times": [],
                "ped_wait_times": [],
                "bus_wait_times": [],
                "sync_success_count": 0,
                "step_count": 0,
                "co2_emission": 0,
            }

            done = False
            while not done:
                # Select action (no exploration)
                action = agent.select_action(state, explore=False)

                # Take step
                next_state, reward, done, info = env.step(action)

                # Track metrics
                episode_metrics["step_count"] += 1
                if info.get("sync_achieved", False):
                    episode_metrics["sync_success_count"] += 1
                episode_metrics["co2_emission"] += info.get("co2_emission", 0)

                # Update state
                state = next_state

            # Calculate final metrics
            final_metrics = {
                "car_wait_time": (
                    np.mean(episode_metrics["car_wait_times"])
                    if episode_metrics["car_wait_times"]
                    else 0
                ),
                "bike_wait_time": (
                    np.mean(episode_metrics["bike_wait_times"])
                    if episode_metrics["bike_wait_times"]
                    else 0
                ),
                "ped_wait_time": (
                    np.mean(episode_metrics["ped_wait_times"])
                    if episode_metrics["ped_wait_times"]
                    else 0
                ),
                "bus_wait_time": (
                    np.mean(episode_metrics["bus_wait_times"])
                    if episode_metrics["bus_wait_times"]
                    else 0
                ),
                "sync_success_rate": (
                    episode_metrics["sync_success_count"]
                    / episode_metrics["step_count"]
                    if episode_metrics["step_count"] > 0
                    else 0
                ),
                "co2_emission": episode_metrics["co2_emission"],
                "total_steps": episode_metrics["step_count"],
            }

            # Log results
            logger.log_scenario(scenario_name, final_metrics)

            # Close environment
            env.close()

            # Update progress
            progress_bar.update(1)
            progress_bar.set_postfix({"scenario": scenario_name})

    progress_bar.close()

    # Save and display results
    results_df = logger.save_results()
    logger.print_summary()

    # STEP 4: Clean route directory after testing completes
    print()
    clean_route_directory()

    print(f"\n{'=' * 50}")
    print("TESTING COMPLETE!")
    print(f"{'=' * 50}")
    print(f"Results saved to: {output_dir}\n")

    return results_df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test DRL traffic signal control")
    parser.add_argument(
        "--model", type=str, required=True, help="Path to trained model"
    )
    args = parser.parse_args()

    test_drl_agent(args.model)
