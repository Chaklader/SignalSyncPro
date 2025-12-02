import os
import sys
import subprocess

import traci

from constants.developed.multi_agent.constants import SIMULATION_LIMIT_TEST
from controls.rule_based.developed.five_intersections.isolated_without_semi_sync.controller import (
    IsolatedTLSController,
)


SUMO_CONFIG = "configurations/developed/drl/multi_agent/signal_sync.sumocfg"
PORT = 8816


def run(gui=False, max_steps=3600, verbose=False):
    sumo_binary = "sumo-gui" if gui else "sumo"

    if "SUMO_HOME" in os.environ:
        sumo_binary = os.path.join(os.environ["SUMO_HOME"], "bin", sumo_binary)

    project_root = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
            )
        )
    )

    config_path = os.path.join(project_root, SUMO_CONFIG)

    sumo_cmd = [sumo_binary, "-c", config_path]

    subprocess.Popen(
        sumo_cmd,
        stdout=subprocess.DEVNULL if not verbose else sys.stdout,
        stderr=subprocess.DEVNULL if not verbose else sys.stderr,
    )

    traci.init(PORT)

    controller = IsolatedTLSController()

    step = 0
    while step < max_steps:
        traci.simulationStep()
        controller.step()
        step += 1

        if traci.simulation.getMinExpectedNumber() == 0:
            break

        if verbose and step % 100 == 0:
            stats = controller.get_stats()
            print(f"Step {step}: {stats}")

    traci.close()

    print(f"Simulation completed after {step} steps")
    return step


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Isolated TLS Control (5-TLS Network)")
    parser.add_argument("--gui", action="store_true", help="Use SUMO GUI")
    parser.add_argument(
        "--steps", type=int, default=SIMULATION_LIMIT_TEST, help="Max simulation steps"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print status every 100 steps"
    )

    args = parser.parse_args()

    run(gui=args.gui, max_steps=args.steps, verbose=args.verbose)


if __name__ == "__main__":
    main()
