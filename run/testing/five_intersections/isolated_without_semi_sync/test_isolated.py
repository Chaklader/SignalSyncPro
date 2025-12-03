"""Test script for isolated control (without semi-sync) across 30 traffic scenarios."""

import argparse
import sys
import os

project_root = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
sys.path.insert(0, project_root)

from run.testing.five_intersections.common import parse_scenarios, run_test_scenarios  # noqa: E402
from controls.rule_based.developed.five_intersections.isolated_without_semi_sync.main import (  # noqa: E402
    run,
)


def main():
    parser = argparse.ArgumentParser(
        description="Test isolated control (5-TLS) across traffic scenarios"
    )
    parser.add_argument(
        "--scenarios",
        type=str,
        default="all",
        help="Scenarios to test: 'all', 'Pr', 'Bi', 'Pe', or comma-separated (e.g., 'Pr_0,Bi_5')",
    )

    args = parser.parse_args()
    scenarios = parse_scenarios(args.scenarios)
    run_test_scenarios(run, "isolated", scenarios)


if __name__ == "__main__":
    main()
