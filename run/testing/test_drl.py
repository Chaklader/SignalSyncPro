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

from controls.ml_based.drl import DQNAgent  # noqa: E402
from controls.ml_based.drl import TrafficManagement  # noqa: E402
from controls.ml_based.drl.single_agent.config import DRLConfig  # noqa: E402
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
    def __init__(self, output_dir, save_states_for_analysis=True):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.results = []
        self.save_states_for_analysis = save_states_for_analysis

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_path = os.path.join(
            self.output_dir, f"drl_test_results_{timestamp}.csv"
        )

        if self.save_states_for_analysis:
            self.states_path = os.path.join(
                self.output_dir, f"test_states_{timestamp}.npz"
            )
            self.all_states = []
            self.all_actions = []
            self.all_scenarios = []
            print("\n📊 State collection ENABLED for explainability analysis")
            print(f"   States will be saved to: {self.states_path}")
            print("   Target: ~300,000 states (ALL states from 30 scenarios)")
            print("   Expected file size: ~75 MB\n")

        with open(self.csv_path, "w") as f:
            f.write("scenario,avg_waiting_time_car,avg_waiting_time_bicycle,")
            f.write("avg_waiting_time_pedestrian,avg_waiting_time_bus,")
            f.write(
                "co2_total_kg_per_s,co2_total_kg_per_hour,safety_violations_total\n"
            )

    def log_scenario(self, scenario_name, metrics):
        result = {"scenario": scenario_name}
        result.update(metrics)
        self.results.append(result)

        with open(self.csv_path, "a") as f:
            f.write(f"{scenario_name},")
            f.write(f"{metrics['avg_waiting_time_car']:.2f},")
            f.write(f"{metrics['avg_waiting_time_bicycle']:.2f},")
            f.write(f"{metrics['avg_waiting_time_pedestrian']:.2f},")
            f.write(f"{metrics['avg_waiting_time_bus']:.2f},")
            f.write(f"{metrics['co2_total_kg_per_s']:.2f},")
            f.write(f"{metrics['co2_total_kg_per_hour']:.2f},")
            f.write(f"{metrics['safety_violations_total']}\n")

        print(f"✓ Results for {scenario_name} saved to: {self.csv_path}")

    def collect_state(self, state, action, scenario_name):
        """
        Collect state-action pair for explainability analysis.

        Args:
            state: State vector (numpy array)
            action: Action taken (int)
            scenario_name: Name of current scenario (str)
        """
        if self.save_states_for_analysis:
            self.all_states.append(state.copy())
            self.all_actions.append(action)
            self.all_scenarios.append(scenario_name)

    def save_collected_states(self):
        """
        Save all collected states to numpy file for later analysis.
        """
        if self.save_states_for_analysis and len(self.all_states) > 0:
            states_array = np.array(self.all_states)
            actions_array = np.array(self.all_actions)
            scenarios_array = np.array(self.all_scenarios)

            np.savez_compressed(
                self.states_path,
                states=states_array,
                actions=actions_array,
                scenarios=scenarios_array,
            )

            print("\n✅ Collected states saved successfully!")
            print(f"   File: {self.states_path}")
            print(f"   Total states: {len(self.all_states):,}")
            print(f"   State shape: {states_array.shape}")
            print("   Action distribution:")
            unique, counts = np.unique(actions_array, return_counts=True)
            action_names = {0: "Continue", 1: "Skip2P1", 2: "Next"}  # 3 actions only
            for action_id, count in zip(unique, counts):
                percentage = (count / len(actions_array)) * 100
                print(
                    f"     {action_names.get(action_id, f'Action_{action_id}')}: {count:,} ({percentage:.1f}%)"
                )
            print()

    def save_results(self):
        df = pd.DataFrame(self.results)
        print(f"\nAll results saved to: {self.csv_path}")

        self.save_collected_states()
        return df

    def print_summary(self):
        df = pd.DataFrame(self.results)

        print("\n" + "=" * 80)
        print("DRL TEST RESULTS SUMMARY")
        print("=" * 80)

        for scenario_type in ["Pr", "Bi", "Pe"]:
            scenario_results = df[df["scenario"].str.startswith(scenario_type)]
            if len(scenario_results) > 0:
                print(f"\n{scenario_type} Scenarios (n={len(scenario_results)}):")
                print(
                    f"  Avg Car Wait Time:    {scenario_results['avg_waiting_time_car'].mean():.2f}s"
                )
                print(
                    f"  Avg Bike Wait Time:   {scenario_results['avg_waiting_time_bicycle'].mean():.2f}s"
                )
                print(
                    f"  Avg Ped Wait Time:    {scenario_results['avg_waiting_time_pedestrian'].mean():.2f}s"
                )
                print(
                    f"  Avg Bus Wait Time:    {scenario_results['avg_waiting_time_bus'].mean():.2f}s"
                )
                print(
                    f"  Avg CO2 per hour:     {scenario_results['co2_total_kg_per_hour'].mean():.2f} kg/hr"
                )
                print(
                    f"  Total Safety Violations: {scenario_results['safety_violations_total'].sum()}"
                )


def test_drl_agent(model_path, scenarios=None):
    if scenarios is None:
        scenarios = TEST_SCENARIOS
        print("\n" + "=" * 70)
        print("TESTING ON ALL 30 SCENARIOS (same as training):")
        print("  Pr: 0-9, Bi: 0-9, Pe: 0-9 (30 scenarios total)")
        print("=" * 70 + "\n")
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

    sumo_config = "configurations/developed/drl/single_agent/signal_sync.sumocfg"
    tls_ids = ["3", "6"]
    traffic_management = TrafficManagement(
        sumo_config,
        tls_ids,
        gui=False,
        simulation_limit=SIMULATION_LIMIT_TEST,
        is_training=False,
    )

    initial_state = traffic_management.reset()
    state_dim = len(initial_state)
    action_dim = DRLConfig.ACTION_DIM
    traffic_management.close()

    agent = DQNAgent(state_dim, action_dim)
    agent.load(model_path)
    agent.set_eval_mode()
    agent.epsilon = 0.0
    output_dir = "results"
    logger = TestLogger(output_dir, save_states_for_analysis=True)

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
            traffic_management = TrafficManagement(
                sumo_config,
                tls_ids,
                gui=False,
                simulation_limit=SIMULATION_LIMIT_TEST,
                is_training=False,
            )
            state = traffic_management.reset()

            episode_metrics = {
                "car_wait_times": [],
                "bike_wait_times": [],
                "ped_wait_times": [],
                "bus_wait_times": [],
                "co2_per_s": [],
                "co2_per_hour": [],
                "step_count": 0,
                "safety_violations": 0,
            }

            action_counts = {0: 0, 1: 0, 2: 0}

            state_sample_interval = 1

            for step in range(SIMULATION_LIMIT_TEST):
                valid_actions = traffic_management.get_valid_actions()
                action, was_exploration = agent.select_action(
                    state, explore=False, step=step, valid_actions=valid_actions
                )
                action_counts[action] += 1

                if step % state_sample_interval == 0:
                    logger.collect_state(state, action, scenario_name)

                if step > 0 and step % 1000 == 0:
                    current_phases = [
                        traffic_management.current_phase.get(tls_id, -1)
                        for tls_id in traffic_management.tls_ids
                    ]
                    print(
                        f"  Step {step} - Actions: Continue={action_counts[0]}, Skip2P1={action_counts[1]}, Next={action_counts[2]}"
                    )
                    print(
                        f"           - Current phases: TLS_1={current_phases[0]}, TLS_2={current_phases[1] if len(current_phases) > 1 else 'N/A'}"
                    )

                next_state, reward, done, info = traffic_management.step(action)

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

                episode_metrics["co2_per_s"].append(info.get("co2_total_kg_per_s", 0))
                episode_metrics["co2_per_hour"].append(
                    info.get("co2_total_kg_per_hour", 0)
                )
                episode_metrics["safety_violations"] += info.get(
                    "safety_violations_total", 0
                )

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
                f"  Next Phase (2): {action_counts[2]} ({action_counts[2] / total_actions * 100:.1f}%)\n"
            )

            final_metrics = {
                "avg_waiting_time_car": (
                    np.mean(episode_metrics["car_wait_times"])
                    if episode_metrics["car_wait_times"]
                    else 0
                ),
                "avg_waiting_time_bicycle": (
                    np.mean(episode_metrics["bike_wait_times"])
                    if episode_metrics["bike_wait_times"]
                    else 0
                ),
                "avg_waiting_time_pedestrian": (
                    np.mean(episode_metrics["ped_wait_times"])
                    if episode_metrics["ped_wait_times"]
                    else 0
                ),
                "avg_waiting_time_bus": (
                    np.mean(episode_metrics["bus_wait_times"])
                    if episode_metrics["bus_wait_times"]
                    else 0
                ),
                "co2_total_kg_per_s": (
                    np.mean(episode_metrics["co2_per_s"])
                    if episode_metrics["co2_per_s"]
                    else 0
                ),
                "co2_total_kg_per_hour": (
                    np.mean(episode_metrics["co2_per_hour"])
                    if episode_metrics["co2_per_hour"]
                    else 0
                ),
                "safety_violations_total": episode_metrics["safety_violations"],
            }

            logger.log_scenario(scenario_name, final_metrics)

            traffic_management.close()

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
