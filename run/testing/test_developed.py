"""
Test script for rule-based developed control across 30 traffic scenarios.
Mirrors the DRL testing approach for fair comparison.
"""

import sys
import os

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
from datetime import datetime  # noqa: E402
from tqdm import tqdm  # noqa: E402

from route_generator.traffic_config import get_traffic_config, TEST_SCENARIOS  # noqa: E402
from route_generator import generate_all_routes_developed  # noqa: E402
from common.utils import clean_route_directory  # noqa: E402
from controls.rule_based.developed.main import run  # noqa: E402


class TestLogger:
    """Logger for developed control testing results"""

    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_file = os.path.join(
            output_dir, f"developed_test_results_{timestamp}.csv"
        )

        # Write header
        with open(self.results_file, "w") as f:
            f.write(
                "scenario,cars_per_hr,bikes_per_hr,peds_per_hr,buses,simulation_time\n"
            )

    def log_episode(self, scenario_name, traffic_config, sim_time):
        """Log episode results"""
        with open(self.results_file, "a") as f:
            f.write(
                f"{scenario_name},{traffic_config['cars']},{traffic_config['bicycles']},"
                f"{traffic_config['pedestrians']},{traffic_config['buses']},{sim_time}\n"
            )

        print(
            f"  Scenario: {scenario_name} | Cars: {traffic_config['cars']}/hr | "
            f"Bikes: {traffic_config['bicycles']}/hr | Peds: {traffic_config['pedestrians']}/hr | "
            f"Sim time: {sim_time}s"
        )


def test_developed_control(scenarios=None):
    """
    Test rule-based developed control across multiple traffic scenarios.

    Args:
        scenarios: Dict of scenarios to test (default: all 30 TEST_SCENARIOS)

    Returns:
        Path to results file
    """
    print("=" * 70)
    print("RULE-BASED DEVELOPED CONTROL - TESTING")
    print("=" * 70)

    if scenarios is None:
        scenarios = TEST_SCENARIOS

    # STEP 1: Clean route directory before starting
    clean_route_directory()

    # Initialize logger
    output_dir = "results/developed_testing"
    logger = TestLogger(output_dir)

    print(
        f"\nTesting developed control on {sum(len(v) for v in scenarios.values())} scenarios..."
    )
    print(f"Results will be saved to: {logger.results_file}\n")

    # Test each scenario
    total_scenarios = sum(len(v) for v in scenarios.values())
    progress_bar = tqdm(total=total_scenarios, desc="Testing scenarios")

    for scenario_type, scenario_list in scenarios.items():
        for scenario_num in scenario_list:
            scenario_name = f"{scenario_type}_{scenario_num}"

            # Generate routes for this scenario
            traffic_config = get_traffic_config(mode="test", scenario=scenario_name)
            generate_all_routes_developed(traffic_config)

            # Run simulation
            print(f"\n{'=' * 70}")
            print(f"Scenario: {scenario_name}")
            print(f"  Cars: {traffic_config['cars']}/hr")
            print(f"  Bicycles: {traffic_config['bicycles']}/hr")
            print(f"  Pedestrians: {traffic_config['pedestrians']}/hr")
            print(f"  Buses: {traffic_config['buses']}")
            print(f"{'=' * 70}")

            # Run developed control (uses signal_sync.sumocfg)
            sumo_exe = "sumo"  # Use headless for testing
            if "SUMO_HOME" in os.environ:
                sumo_exe = os.path.join(os.environ["SUMO_HOME"], "bin", sumo_exe)

            # Get simulation limit from traffic config or use default
            max_steps = traffic_config.get("simulation_limit", 10000)

            # Run the simulation
            import time

            start_time = time.time()
            run(sumo_exe, max_steps)
            sim_time = time.time() - start_time

            # Log results
            logger.log_episode(scenario_name, traffic_config, sim_time)

            progress_bar.update(1)

    progress_bar.close()

    print("\n" + "=" * 70)
    print("TESTING COMPLETE!")
    print("=" * 70)
    print(f"\nResults saved to: {logger.results_file}")
    print(f"Total scenarios tested: {total_scenarios}")

    return logger.results_file


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Test rule-based developed control across traffic scenarios"
    )
    parser.add_argument(
        "--scenarios",
        type=str,
        default="all",
        help="Scenarios to test: 'all', 'Pr', 'Bi', 'Pe', or comma-separated list (e.g., 'Pr_0,Bi_5')",
    )

    args = parser.parse_args()

    # Parse scenarios
    if args.scenarios == "all":
        scenarios = TEST_SCENARIOS
    elif args.scenarios in ["Pr", "Bi", "Pe"]:
        scenarios = {args.scenarios: TEST_SCENARIOS[args.scenarios]}
    else:
        # Parse comma-separated list
        scenario_list = args.scenarios.split(",")
        scenarios = {}
        for s in scenario_list:
            s = s.strip()
            scenario_type = s.split("_")[0]
            scenario_num = int(s.split("_")[1])
            if scenario_type not in scenarios:
                scenarios[scenario_type] = []
            scenarios[scenario_type].append(scenario_num)

    test_developed_control(scenarios)


if __name__ == "__main__":
    main()
