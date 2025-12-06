import traci
import sys

from constants.developed.multi_agent.drl_tls_constants import (
    TLS_IDS,
    bus_signals_emit_lanes,
    HEADWAY_TIME_FOR_SIGNAL_CONTROL,
    get_priority_action,
)


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
                    travel_time = self._get_travel_time_for_lane(idx, lane_id)
                    self.tracked_buses[tls_id][veh_id] = {
                        "detected_time": current_time,
                        "travel_time": travel_time,
                    }
                    self.total_buses_detected += 1
                    print(
                        f"[BUS DETECTED] TLS {tls_id}: Bus {veh_id} detected on {lane_id}, ETA: {travel_time}s 🚌"
                    )
                    sys.stdout.flush()
            except traci.exceptions.TraCIException as e:
                # Log lane access errors once at startup
                if current_time < 10:
                    print(
                        f"[BUS PRIORITY WARNING] TLS {tls_id}: Cannot access lane {lane_id}: {e}"
                    )
                    sys.stdout.flush()
                continue

    def _get_travel_time_for_lane(self, idx, lane_id):
        if idx == 0:
            if "1_2" in lane_id:
                return 72
            return 64
        elif idx == 4:
            if "8_25" in lane_id:
                return 72
            return 64
        return 64

    def _update_priority_status(self, tls_id, current_time):
        if not self.tracked_buses[tls_id]:
            self.bus_priority_active[tls_id] = False
            return

        expired_buses = []
        priority_active = False

        for veh_id, bus_info in self.tracked_buses[tls_id].items():
            elapsed = current_time - bus_info["detected_time"]
            time_to_arrival = bus_info["travel_time"] - elapsed

            if time_to_arrival <= 0:
                expired_buses.append(veh_id)
            elif time_to_arrival <= HEADWAY_TIME_FOR_SIGNAL_CONTROL:
                priority_active = True

        for veh_id in expired_buses:
            del self.tracked_buses[tls_id][veh_id]

        was_active = self.bus_priority_active[tls_id]
        self.bus_priority_active[tls_id] = priority_active

        if priority_active and not was_active:
            self.total_priority_activations += 1
            print(
                f"[BUS PRIORITY ACTIVATED] TLS {tls_id}: Bus arriving soon (≤{HEADWAY_TIME_FOR_SIGNAL_CONTROL}s) 🚨"
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
        if current_time - self.last_log_time >= 1000:  # Every 1000 steps
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
