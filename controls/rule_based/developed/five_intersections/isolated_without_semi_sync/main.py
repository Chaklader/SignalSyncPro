import os
import sys

import traci

project_root = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
    )
)
sys.path.insert(0, project_root)

from constants.developed.multi_agent.constants import SIMULATION_LIMIT_TEST  # noqa: E402
from controls.rule_based.developed.five_intersections.isolated_without_semi_sync.controller import (  # noqa: E402
    IsolatedTLSController,
)
from run.testing.five_intersections.metrics_collector import MetricsCollector  # noqa: E402


SUMO_CONFIG = "configurations/developed/drl/multi_agent/signal_sync.sumocfg"


def run(gui=False, max_steps=3600, verbose=False, collect_metrics=True):
    """
    Run the isolated TLS control simulation.

    Args:
        gui: Whether to use SUMO GUI
        max_steps: Maximum simulation steps
        verbose: Print status every 100 steps
        collect_metrics: Whether to collect detailed traffic metrics

    Returns:
        dict: Dictionary containing metrics if collect_metrics=True, else step count
    """
    sumo_binary = "sumo-gui" if gui else "sumo"

    if "SUMO_HOME" in os.environ:
        sumo_binary = os.path.join(os.environ["SUMO_HOME"], "bin", sumo_binary)

    config_path = os.path.join(project_root, SUMO_CONFIG)

    sumo_cmd = [sumo_binary, "-c", config_path]

    traci.start(sumo_cmd)

    controller = IsolatedTLSController()

    # Initialize metrics collector if needed
    metrics_collector = MetricsCollector() if collect_metrics else None

    step = 0
    while step < max_steps:
        traci.simulationStep()
        controller.step()
        step += 1

        # Collect metrics for this step
        if collect_metrics and metrics_collector:
            metrics_collector.collect_step_metrics(traci)

        if traci.simulation.getMinExpectedNumber() == 0:
            break

        # Log progress every 100 steps
        if step % 100 == 0:
            vehicle_count = traci.vehicle.getIDCount()
            person_count = traci.person.getIDCount()
            waiting_vehicles = sum(
                1 for v in traci.vehicle.getIDList() if traci.vehicle.getSpeed(v) < 0.1
            )

            print(f"\n[STEP {step}] Progress Update:")
            print(f"  Active vehicles: {vehicle_count}")
            print(f"  Active pedestrians: {person_count}")
            print(f"  Waiting vehicles (speed < 0.1): {waiting_vehicles}")

            if collect_metrics and metrics_collector:
                current_metrics = metrics_collector.get_current_summary()
                print(f"  Avg car wait: {current_metrics.get('avg_car_wait', 0):.1f}s")
                print(
                    f"  Avg bike wait: {current_metrics.get('avg_bike_wait', 0):.1f}s"
                )
                print(f"  Avg ped wait: {current_metrics.get('avg_ped_wait', 0):.1f}s")

            if verbose:
                stats = controller.get_stats()
                print(f"  Controller stats: {stats}")

            sys.stdout.flush()

    traci.close()

    print(f"Simulation completed after {step} steps")

    if collect_metrics and metrics_collector:
        return metrics_collector.get_episode_metrics()
    return {"step_count": step}


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
