"""
Testing script for DRL traffic signal control
"""

import argparse
import os
import sys
from datetime import datetime

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.insert(0, project_root)

from common.sumo_utils import setup_environment  # noqa: E402

setup_environment()
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from tqdm import tqdm  # noqa: E402

from controls.ml_based.drl.agent import DQNAgent  # noqa: E402
from controls.ml_based.drl.traffic_management import TrafficManagement  # noqa: E402
from controls.ml_based.drl.config import DRLConfig  # noqa: E402
from route_generator.traffic_config import get_traffic_config  # noqa: E402
from route_generator import generate_all_routes_developed  # noqa: E402
from common.utils import clean_route_directory  # noqa: E402
from constants.constants import SIMULATION_LIMIT_TEST  # noqa: E402

TEST_SCENARIOS = {
    "Pr": list(range(10)),
    "Bi": list(range(10)),
    "Pe": list(range(10)),
}


class TestLogger:
    """
    Logger for test results
    """

    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.results = []

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_path = os.path.join(
            self.output_dir, f"drl_test_results_{timestamp}.csv"
        )

        with open(self.csv_path, "w") as f:
            f.write(
                "scenario,car_wait_time,bike_wait_time,ped_wait_time,bus_wait_time,"
            )
            f.write("sync_success_rate,co2_emission_kg,pedestrian_phase_count,")
            f.write("safety_violation_count,safety_violation_rate,")
            f.write("ped_demand_ignored_count,ped_demand_ignored_rate,total_steps\n")

    def log_scenario(self, scenario_name, metrics):
        """Log scenario results and save immediately to CSV"""
        result = {"scenario": scenario_name}
        result.update(metrics)
        self.results.append(result)

        with open(self.csv_path, "a") as f:
            f.write(f"{scenario_name},")
            f.write(f"{metrics['car_wait_time']:.4f},")
            f.write(f"{metrics['bike_wait_time']:.4f},")
            f.write(f"{metrics['ped_wait_time']:.4f},")
            f.write(f"{metrics['bus_wait_time']:.4f},")
            f.write(f"{metrics['sync_success_rate']:.6f},")
            f.write(f"{metrics['co2_emission_kg']:.4f},")
            f.write(f"{metrics['pedestrian_phase_count']},")
            f.write(f"{metrics['safety_violation_count']},")
            f.write(f"{metrics['safety_violation_rate']:.6f},")
            f.write(f"{metrics['ped_demand_ignored_count']},")
            f.write(f"{metrics['ped_demand_ignored_rate']:.6f},")
            f.write(f"{metrics['total_steps']}\n")

        print(f"✓ Results for {scenario_name} saved to: {self.csv_path}")

    def save_results(self):
        """Return DataFrame of all results (CSV already saved incrementally)"""
        df = pd.DataFrame(self.results)
        print(f"\nAll results saved to: {self.csv_path}")
        return df

    def print_summary(self):
        """Print summary statistics"""
        df = pd.DataFrame(self.results)

        print("\n" + "=" * 80)
        print("DRL TEST RESULTS SUMMARY")
        print("=" * 80)

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
    Test trained DRL agent on ALL 30 test scenarios.

    Agent has seen all 30 scenarios during training (every 4th episode),
    so this evaluates learned performance, not generalization to unseen scenarios.
    """
    if scenarios is None:
        scenarios = TEST_SCENARIOS
        print("\n" + "=" * 70)
        print("TESTING ON ALL 30 SCENARIOS (same as training):")
        print("  Pr: 0-9, Bi: 0-9, Pe: 0-9 (30 scenarios total)")
        print("=" * 70 + "\n")

    clean_route_directory()

    print("\nGenerating initial routes...")
    traffic_config = get_traffic_config(scenario="Pr_0")
    generate_all_routes_developed(traffic_config, SIMULATION_LIMIT_TEST)

    sumo_config = "configurations/developed/drl/single_agent/common/signal_sync.sumocfg"
    tls_ids = ["3", "6"]
    env = TrafficManagement(sumo_config, tls_ids, gui=False)

    initial_state = env.reset()
    state_dim = len(initial_state)
    action_dim = DRLConfig.ACTION_DIM
    env.close()

    agent = DQNAgent(state_dim, action_dim)
    agent.load(model_path)
    agent.set_eval_mode()
    agent.epsilon = 0.0
    output_dir = "results"
    logger = TestLogger(output_dir)

    print(
        f"\nTesting DRL agent on {sum(len(v) for v in scenarios.values())} scenarios..."
    )
    print(f"Model: {model_path}")
    print(f"Agent epsilon: {agent.epsilon} (pure exploitation mode)")
    print(f"Episode count from training: {agent.episode_count}")
    print(f"Total training steps: {agent.steps}\n")

    total_scenarios = sum(len(v) for v in scenarios.values())
    progress_bar = tqdm(total=total_scenarios, desc="Testing scenarios")

    scenario_count = 0
    for scenario_type, scenario_list in scenarios.items():
        for scenario_num in scenario_list:
            scenario_name = f"{scenario_type}_{scenario_num}"

            if scenario_count > 0:
                traffic_config = get_traffic_config(scenario=scenario_name)
                generate_all_routes_developed(traffic_config, SIMULATION_LIMIT_TEST)

            scenario_count += 1
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
                "safety_violation_count": 0,
                "ped_demand_ignored_count": 0,
                "ped_phase_count": 0,
            }

            action_counts = {0: 0, 1: 0, 2: 0, 3: 0}

            for step in range(SIMULATION_LIMIT_TEST):
                action = agent.select_action(state, explore=False, step=step)
                action_counts[action] += 1

                if step > 0 and step % 1000 == 0:
                    current_phases = [
                        env.current_phase.get(tls_id, -1) for tls_id in env.tls_ids
                    ]
                    print(
                        f"  Step {step} - Actions: Continue={action_counts[0]}, Skip2P1={action_counts[1]}, Next={action_counts[2]}, Ped={action_counts[3]}"
                    )
                    print(
                        f"           - Current phases: TLS_1={current_phases[0]}, TLS_2={current_phases[1] if len(current_phases) > 1 else 'N/A'}"
                    )

                next_state, reward, done, info = env.step(action)

                episode_metrics["step_count"] += 1

                episode_metrics["car_wait_times"].append(
                    info.get("waiting_time_car", 0)
                )
                episode_metrics["bike_wait_times"].append(
                    info.get("waiting_time_bicycle", 0)
                )
                episode_metrics["ped_wait_times"].append(
                    info.get("waiting_time_pedestrian", 0)
                )
                episode_metrics["bus_wait_times"].append(
                    info.get("waiting_time_bus", 0)
                )

                if info.get("sync_achieved", False):
                    episode_metrics["sync_success_count"] += 1
                episode_metrics["co2_emission"] += info.get("co2_emission", 0)

                if info.get("safety_violation", False):
                    episode_metrics["safety_violation_count"] += 1
                if info.get("event_type") == "ped_demand_ignored":
                    episode_metrics["ped_demand_ignored_count"] += 1
                if info.get("ped_phase_active", False):
                    episode_metrics["ped_phase_count"] += 1

                state = next_state

                if done:
                    break

            total_actions = sum(action_counts.values())
            print(f"\n[ACTION SUMMARY] {scenario_name}:")
            print(f"  Total actions: {total_actions}")
            print(
                f"  Continue (0): {action_counts[0]} ({action_counts[0] / total_actions * 100:.1f}%)"
            )
            print(
                f"  Skip to P1 (1): {action_counts[1]} ({action_counts[1] / total_actions * 100:.1f}%)"
            )
            print(
                f"  Next Phase (2): {action_counts[2]} ({action_counts[2] / total_actions * 100:.1f}%)"
            )
            print(
                f"  Pedestrian (3): {action_counts[3]} ({action_counts[3] / total_actions * 100:.1f}%)\n"
            )

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
                "co2_emission_kg": episode_metrics["co2_emission"],  # CO2 in kilograms
                "pedestrian_phase_count": episode_metrics["ped_phase_count"],
                "safety_violation_count": episode_metrics["safety_violation_count"],
                "safety_violation_rate": (
                    episode_metrics["safety_violation_count"]
                    / episode_metrics["step_count"]
                    if episode_metrics["step_count"] > 0
                    else 0
                ),
                "ped_demand_ignored_count": episode_metrics["ped_demand_ignored_count"],
                "ped_demand_ignored_rate": (
                    episode_metrics["ped_demand_ignored_count"]
                    / episode_metrics["step_count"]
                    if episode_metrics["step_count"] > 0
                    else 0
                ),
                "total_steps": episode_metrics["step_count"],
            }

            logger.log_scenario(scenario_name, final_metrics)

            env.close()

            progress_bar.update(1)
            progress_bar.set_postfix({"scenario": scenario_name})

    progress_bar.close()

    results_df = logger.save_results()
    logger.print_summary()

    print()
    clean_route_directory()

    print(f"\n{'=' * 50}")
    print("TESTING COMPLETE!")
    print(f"{'=' * 50}")
    print(f"Results saved to: {logger.csv_path}\n")

    return results_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test DRL traffic signal control")
    parser.add_argument(
        "--model", type=str, required=True, help="Path to trained model"
    )
    args = parser.parse_args()

    test_drl_agent(args.model)
