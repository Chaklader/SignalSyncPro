"""Common utilities for 5-intersection testing."""

import os
import sys
from datetime import datetime

import pandas as pd

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.insert(0, project_root)

from common.sumo_utils import setup_environment  # noqa: E402

setup_environment()

from tqdm import tqdm  # noqa: E402

from route_generator.traffic_config import (  # noqa: E402
    TEST_SCENARIOS_FIVE_INTERSECTIONS,
    get_test_scenario,
)
from route_generator.developed.drl.multi_agent import generate_all_routes  # noqa: E402
from common.utils import clean_route_directory  # noqa: E402
from constants.developed.multi_agent.constants import SIMULATION_LIMIT_TEST  # noqa: E402


class TestLogger:
    """Logger for 5-intersection testing with detailed metrics."""

    def __init__(self, output_dir, control_type):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.results = []

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_file = os.path.join(
            output_dir, f"{control_type}_test_results_{timestamp}.csv"
        )

        # Write CSV header matching DRL test output format
        with open(self.results_file, "w") as f:
            f.write("scenario,avg_waiting_time_car,avg_waiting_time_bicycle,")
            f.write("avg_waiting_time_pedestrian,avg_waiting_time_bus,")
            f.write(
                "co2_total_kg_per_s,co2_total_kg_per_hour,safety_violations_total\n"
            )

    def log_episode(self, scenario_name, metrics):
        """
        Log metrics for a scenario.

        Args:
            scenario_name: Name of the scenario (e.g., "Pr_0")
            metrics: Dictionary containing collected metrics
        """
        result = {"scenario": scenario_name}
        result.update(metrics)
        self.results.append(result)

        with open(self.results_file, "a") as f:
            f.write(f"{scenario_name},")
            f.write(f"{metrics.get('avg_waiting_time_car', 0):.2f},")
            f.write(f"{metrics.get('avg_waiting_time_bicycle', 0):.2f},")
            f.write(f"{metrics.get('avg_waiting_time_pedestrian', 0):.2f},")
            f.write(f"{metrics.get('avg_waiting_time_bus', 0):.2f},")
            f.write(f"{metrics.get('co2_total_kg_per_s', 0):.2f},")
            f.write(f"{metrics.get('co2_total_kg_per_hour', 0):.2f},")
            f.write(f"{metrics.get('safety_violations_total', 0)}\n")

        print(f"✓ Results for {scenario_name} saved to: {self.results_file}")

    def print_summary(self):
        """Print summary statistics for all tested scenarios."""
        df = pd.DataFrame(self.results)

        print("\n" + "=" * 80)
        print("5-TLS TEST RESULTS SUMMARY")
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


def parse_scenarios(scenarios_arg):
    if scenarios_arg == "all":
        scenarios = {}
        for name in TEST_SCENARIOS_FIVE_INTERSECTIONS.keys():
            scenario_type = name.split("_")[0]
            scenario_num = int(name.split("_")[1])
            if scenario_type not in scenarios:
                scenarios[scenario_type] = []
            scenarios[scenario_type].append(scenario_num)
        return scenarios

    if scenarios_arg in ["Pr", "Bi", "Pe"]:
        return {scenarios_arg: list(range(10))}

    scenario_list = scenarios_arg.split(",")
    scenarios = {}
    for s in scenario_list:
        s = s.strip()
        scenario_type = s.split("_")[0]
        scenario_num = int(s.split("_")[1])
        if scenario_type not in scenarios:
            scenarios[scenario_type] = []
        scenarios[scenario_type].append(scenario_num)
    return scenarios


def run_test_scenarios(run_func, control_type, scenarios=None):
    """
    Run test scenarios with detailed metrics collection.

    Args:
        run_func: Function to run simulation (must return metrics dict)
        control_type: Type of control (e.g., "isolated")
        scenarios: Dictionary of scenarios to test

    Returns:
        str: Path to results file
    """
    print("=" * 70)
    print(f"5-INTERSECTION {control_type.upper()} CONTROL - TESTING")
    print("=" * 70)

    if scenarios is None:
        scenarios = parse_scenarios("all")

    clean_route_directory("infrastructure/developed/drl/multi_agent/routes")

    output_dir = f"results_5/{control_type}_testing"
    logger = TestLogger(output_dir, control_type)

    total_scenarios = sum(len(v) for v in scenarios.values())
    print(f"\nTesting {control_type} control on {total_scenarios} scenarios...")
    print(f"Results will be saved to: {logger.results_file}\n")

    progress_bar = tqdm(total=total_scenarios, desc="Testing scenarios")

    for scenario_type, scenario_list in scenarios.items():
        for scenario_num in scenario_list:
            scenario_name = f"{scenario_type}_{scenario_num}"

            traffic_config = get_test_scenario(
                scenario_name, TEST_SCENARIOS_FIVE_INTERSECTIONS
            )
            generate_all_routes(traffic_config, SIMULATION_LIMIT_TEST)

            print(f"\n{'=' * 70}")
            print(f"Scenario: {scenario_name}")
            print(f"  Cars: {traffic_config['cars']}/hr")
            print(f"  Bicycles: {traffic_config['bicycles']}/hr")
            print(f"  Pedestrians: {traffic_config['pedestrians']}/hr")
            print(f"  Buses: {traffic_config['buses']}")
            print(f"{'=' * 70}")

            max_steps = traffic_config.get("simulation_limit", SIMULATION_LIMIT_TEST)

            # Run simulation and collect metrics
            metrics = run_func(
                gui=False, max_steps=max_steps, verbose=False, collect_metrics=True
            )

            logger.log_episode(scenario_name, metrics)
            progress_bar.update(1)

    progress_bar.close()

    # Print summary statistics
    logger.print_summary()

    print("\n" + "=" * 70)
    print("TESTING COMPLETE!")
    print("=" * 70)
    print(f"\nResults saved to: {logger.results_file}")
    print(f"Total scenarios tested: {total_scenarios}")

    return logger.results_file
