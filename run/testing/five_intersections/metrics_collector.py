"""Metrics collector for rule-based traffic signal control testing."""

import numpy as np


def get_vehicle_mode(vtype):
    """Determine vehicle mode from vehicle type string."""
    vtype_lower = vtype.lower()
    if "bus" in vtype_lower:
        return "bus"
    elif "raleigh" in vtype_lower or "bicycle" in vtype_lower:
        return "bicycle"
    else:
        return "car"


class MetricsCollector:
    """Collects traffic metrics from SUMO simulation via TraCI."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all collected metrics."""
        self.car_wait_times = []
        self.bike_wait_times = []
        self.ped_wait_times = []
        self.bus_wait_times = []
        self.co2_per_step = []
        self.safety_violations = 0
        self.step_count = 0

    def collect_step_metrics(self, traci):
        """
        Collect metrics for the current simulation step.

        Args:
            traci: TraCI connection object
        """
        self.step_count += 1

        # Collect vehicle metrics
        waiting_times_by_mode = {"car": [], "bicycle": [], "bus": []}
        total_co2_mg = 0.0

        for veh_id in traci.vehicle.getIDList():
            try:
                vtype = traci.vehicle.getTypeID(veh_id)
                wait_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
                co2 = traci.vehicle.getCO2Emission(veh_id)

                total_co2_mg += co2
                mode = get_vehicle_mode(vtype)
                waiting_times_by_mode[mode].append(wait_time)
            except Exception:
                continue

        # Collect pedestrian metrics
        ped_waiting_times = []
        try:
            for ped_id in traci.person.getIDList():
                try:
                    wait_time = traci.person.getWaitingTime(ped_id)
                    ped_waiting_times.append(wait_time)
                except Exception:
                    continue
        except Exception:
            pass

        # Store step metrics
        if waiting_times_by_mode["car"]:
            self.car_wait_times.append(np.mean(waiting_times_by_mode["car"]))
        if waiting_times_by_mode["bicycle"]:
            self.bike_wait_times.append(np.mean(waiting_times_by_mode["bicycle"]))
        if waiting_times_by_mode["bus"]:
            self.bus_wait_times.append(np.mean(waiting_times_by_mode["bus"]))
        if ped_waiting_times:
            self.ped_wait_times.append(np.mean(ped_waiting_times))

        # Convert CO2 from mg/s to kg/s
        co2_kg_per_s = total_co2_mg / 1_000_000.0
        self.co2_per_step.append(co2_kg_per_s)

        # Safety violations - check for collisions
        try:
            collision_count = traci.simulation.getCollidingVehiclesNumber()
            self.safety_violations += collision_count
        except Exception:
            pass

    def get_current_summary(self):
        """
        Get current metrics summary for progress logging.

        Returns:
            dict: Dictionary with current average metrics
        """
        return {
            "avg_car_wait": np.mean(self.car_wait_times)
            if self.car_wait_times
            else 0.0,
            "avg_bike_wait": np.mean(self.bike_wait_times)
            if self.bike_wait_times
            else 0.0,
            "avg_ped_wait": np.mean(self.ped_wait_times)
            if self.ped_wait_times
            else 0.0,
            "avg_bus_wait": np.mean(self.bus_wait_times)
            if self.bus_wait_times
            else 0.0,
            "step_count": self.step_count,
        }

    def get_episode_metrics(self):
        """
        Calculate and return aggregated metrics for the episode.

        Returns:
            dict: Dictionary containing all aggregated metrics
        """
        avg_wait_car = np.mean(self.car_wait_times) if self.car_wait_times else 0.0
        avg_wait_bike = np.mean(self.bike_wait_times) if self.bike_wait_times else 0.0
        avg_wait_ped = np.mean(self.ped_wait_times) if self.ped_wait_times else 0.0
        avg_wait_bus = np.mean(self.bus_wait_times) if self.bus_wait_times else 0.0
        avg_co2_per_s = np.mean(self.co2_per_step) if self.co2_per_step else 0.0

        return {
            "avg_waiting_time_car": avg_wait_car,
            "avg_waiting_time_bicycle": avg_wait_bike,
            "avg_waiting_time_pedestrian": avg_wait_ped,
            "avg_waiting_time_bus": avg_wait_bus,
            "co2_total_kg_per_s": avg_co2_per_s,
            "co2_total_kg_per_hour": avg_co2_per_s * 3600,
            "safety_violations_total": self.safety_violations,
            "step_count": self.step_count,
        }
