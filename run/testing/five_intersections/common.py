"""Common utilities for 5-intersection testing."""

import os
import sys
import time
from datetime import datetime

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
    def __init__(self, output_dir, control_type):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_file = os.path.join(
            output_dir, f"{control_type}_test_results_{timestamp}.csv"
        )

        with open(self.results_file, "w") as f:
            f.write(
                "scenario,cars_per_hr,bikes_per_hr,peds_per_hr,buses,simulation_time\n"
            )

    def log_episode(self, scenario_name, traffic_config, sim_time):
        with open(self.results_file, "a") as f:
            f.write(
                f"{scenario_name},{traffic_config['cars']},{traffic_config['bicycles']},"
                f"{traffic_config['pedestrians']},{traffic_config['buses']},{sim_time}\n"
            )

        print(
            f"  Scenario: {scenario_name} | Cars: {traffic_config['cars']}/hr | "
            f"Bikes: {traffic_config['bicycles']}/hr | Peds: {traffic_config['pedestrians']}/hr | "
            f"Sim time: {sim_time:.1f}s"
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
    print("=" * 70)
    print(f"5-INTERSECTION {control_type.upper()} CONTROL - TESTING")
    print("=" * 70)

    if scenarios is None:
        scenarios = parse_scenarios("all")

    clean_route_directory("infrastructure/developed/drl/multi_agent/routes")

    output_dir = f"results/five_intersections/{control_type}_testing"
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
            start_time = time.time()
            run_func(gui=False, max_steps=max_steps, verbose=False)
            sim_time = time.time() - start_time

            logger.log_episode(scenario_name, traffic_config, sim_time)
            progress_bar.update(1)

    progress_bar.close()

    print("\n" + "=" * 70)
    print("TESTING COMPLETE!")
    print("=" * 70)
    print(f"\nResults saved to: {logger.results_file}")
    print(f"Total scenarios tested: {total_scenarios}")

    return logger.results_file
