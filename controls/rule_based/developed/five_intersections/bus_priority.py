import traci
import sys

from constants.developed.multi_agent.drl_tls_constants import (
    TLS_IDS,
    bus_signals_emit_lanes,
    HEADWAY_TIME_FOR_SIGNAL_CONTROL,
    get_priority_action,
)

SPEED_THRESHOLD = 2.0
LANE_SPEED = 13.89
PRIORITY_BUFFER = 1
WEIGHTED_SPEED_RECENT_WEIGHT = 0.7
WEIGHTED_SPEED_WINDOW = 5


class BusPriorityManager:
    def __init__(self):
        self.tracked_buses = {tls_id: {} for tls_id in TLS_IDS}
        self.bus_priority_active = {tls_id: False for tls_id in TLS_IDS}
        self.total_buses_detected = 0
        self.total_priority_activations = 0
        self.total_priority_actions = {"HOLD": 0, "CYCLE": 0, "SKIP": 0}
        self.last_log_time = 0

    def update(self, current_time):
        for idx, tls_id in enumerate(TLS_IDS):
            self._check_bus_emit_lanes(idx, tls_id, current_time)
            self._update_bus_positions(tls_id, current_time)
            self._update_priority_status(tls_id, current_time)

    def _check_bus_emit_lanes(self, idx, tls_id, current_time):
        emit_lanes = bus_signals_emit_lanes.get(idx, ())

        for lane_id in emit_lanes:
            try:
                vehicles = traci.lane.getLastStepVehicleIDs(lane_id)
                buses = [v for v in vehicles if traci.vehicle.getTypeID(v) == "bus"]
                for veh_id in buses:
                    if veh_id in self.tracked_buses[tls_id]:
                        continue

                    entry_position = traci.vehicle.getLanePosition(veh_id)
                    lane_length = traci.lane.getLength(lane_id)

                    self.tracked_buses[tls_id][veh_id] = {
                        "detected_time": current_time,
                        "lane_id": lane_id,
                        "lane_length": lane_length,
                        "entry_position": entry_position,
                        "current_position": entry_position,
                        "moving_time": 0,
                        "position_history": [],
                    }
                    self.total_buses_detected += 1

                    distance_to_signal = lane_length - entry_position
                    theoretical_eta = distance_to_signal / LANE_SPEED

                    print(
                        f"[BUS DETECTED] TLS {tls_id}: Bus {veh_id} detected on {lane_id}, "
                        f"distance: {distance_to_signal:.0f}m, theoretical ETA: {theoretical_eta:.0f}s 🚌"
                    )
                    sys.stdout.flush()
            except traci.exceptions.TraCIException as e:
                if current_time < 10:
                    print(
                        f"[BUS PRIORITY WARNING] TLS {tls_id}: Cannot access lane {lane_id}: {e}"
                    )
                    sys.stdout.flush()
                continue

    def _update_bus_positions(self, tls_id, current_time):
        """Update bus positions and calculate moving time for dynamic ETA."""
        buses_to_remove = []

        for veh_id, bus_info in self.tracked_buses[tls_id].items():
            try:
                current_lane = traci.vehicle.getLaneID(veh_id)
                if current_lane != bus_info["lane_id"]:
                    buses_to_remove.append(veh_id)
                    continue

                current_position = traci.vehicle.getLanePosition(veh_id)
                current_speed = traci.vehicle.getSpeed(veh_id)

                bus_info["current_position"] = current_position

                if current_speed >= SPEED_THRESHOLD:
                    bus_info["moving_time"] += 1

                bus_info["position_history"].append(
                    {"time": current_time, "position": current_position}
                )

                if len(bus_info["position_history"]) > WEIGHTED_SPEED_WINDOW + 1:
                    bus_info["position_history"].pop(0)

            except traci.exceptions.TraCIException:
                buses_to_remove.append(veh_id)

        for veh_id in buses_to_remove:
            del self.tracked_buses[tls_id][veh_id]

    def _calculate_weighted_speed(self, bus_info):
        """Calculate weighted average speed (recent speed weighted more heavily)."""
        moving_time = bus_info["moving_time"]
        history = bus_info["position_history"]

        if moving_time < 3:
            return LANE_SPEED

        distance_traveled = bus_info["current_position"] - bus_info["entry_position"]
        total_avg_speed = (
            distance_traveled / moving_time if moving_time > 0 else LANE_SPEED
        )

        if len(history) >= 2:
            recent_distance = history[-1]["position"] - history[0]["position"]
            recent_time = len(history) - 1
            recent_speed = (
                recent_distance / recent_time if recent_time > 0 else total_avg_speed
            )
        else:
            recent_speed = total_avg_speed

        if moving_time >= WEIGHTED_SPEED_WINDOW:
            weighted_speed = (
                WEIGHTED_SPEED_RECENT_WEIGHT * recent_speed
                + (1 - WEIGHTED_SPEED_RECENT_WEIGHT) * total_avg_speed
            )
        else:
            weighted_speed = total_avg_speed

        return max(SPEED_THRESHOLD, min(weighted_speed, LANE_SPEED))

    def _calculate_dynamic_eta(self, bus_info):
        """Calculate dynamic ETA based on weighted speed and remaining distance."""
        distance_to_signal = bus_info["lane_length"] - bus_info["current_position"]
        weighted_speed = self._calculate_weighted_speed(bus_info)

        if weighted_speed <= 0:
            return float("inf")

        return distance_to_signal / weighted_speed

    def _update_priority_status(self, tls_id, current_time):
        if not self.tracked_buses[tls_id]:
            self.bus_priority_active[tls_id] = False
            return

        expired_buses = []
        priority_active = False

        for veh_id, bus_info in self.tracked_buses[tls_id].items():
            dynamic_eta = self._calculate_dynamic_eta(bus_info)
            distance_to_signal = bus_info["lane_length"] - bus_info["current_position"]

            if distance_to_signal <= 5:
                expired_buses.append(veh_id)
            elif dynamic_eta <= HEADWAY_TIME_FOR_SIGNAL_CONTROL + PRIORITY_BUFFER:
                priority_active = True

        for veh_id in expired_buses:
            del self.tracked_buses[tls_id][veh_id]

        was_active = self.bus_priority_active[tls_id]
        self.bus_priority_active[tls_id] = priority_active

        if priority_active and not was_active:
            self.total_priority_activations += 1

            for veh_id, bus_info in self.tracked_buses[tls_id].items():
                eta = self._calculate_dynamic_eta(bus_info)
                speed = self._calculate_weighted_speed(bus_info)
                dist = bus_info["lane_length"] - bus_info["current_position"]
                print(
                    f"[BUS PRIORITY ACTIVATED] TLS {tls_id}: Bus {veh_id} - "
                    f"ETA: {eta:.1f}s, speed: {speed:.1f}m/s, distance: {dist:.0f}m 🚨"
                )
            sys.stdout.flush()
        elif not priority_active and was_active:
            print(f"[BUS PRIORITY DEACTIVATED] TLS {tls_id}: Bus has passed ✓")
            sys.stdout.flush()

    def is_priority_active(self, tls_id):
        return self.bus_priority_active.get(tls_id, False)

    def get_bus_priority_action(self, tls_id, current_phase, green_duration):
        if not self.is_priority_active(tls_id):
            return None
        action = get_priority_action(current_phase, green_duration)
        if action:
            self.total_priority_actions[action] += 1
            print(
                f"[BUS PRIORITY ACTION] TLS {tls_id}: Phase {current_phase}, Duration {green_duration}s → {action}"
            )
            sys.stdout.flush()
        return action

    def clear_priority(self, tls_id):
        self.tracked_buses[tls_id] = {}
        self.bus_priority_active[tls_id] = False

    def print_summary(self, current_time):
        """Print periodic summary of bus priority activity."""
        if current_time - self.last_log_time >= 1000:
            print(f"\n[BUS PRIORITY SUMMARY @ {current_time}s]")
            print(f"  Total buses detected: {self.total_buses_detected}")
            print(f"  Total priority activations: {self.total_priority_activations}")
            print(
                f"  Actions taken: HOLD={self.total_priority_actions['HOLD']}, "
                f"CYCLE={self.total_priority_actions['CYCLE']}, "
                f"SKIP={self.total_priority_actions['SKIP']}"
            )
            for tls_id in TLS_IDS:
                tracked = len(self.tracked_buses[tls_id])
                active = self.bus_priority_active[tls_id]
                if tracked > 0 or active:
                    print(
                        f"  TLS {tls_id}: {tracked} buses tracked, priority={'ACTIVE' if active else 'inactive'}"
                    )
            sys.stdout.flush()
            self.last_log_time = current_time
