import traci

from constants.developed.multi_agent.drl_tls_constants import (
    TLS_IDS,
    bus_signals_emit_lanes,
    p1_main_green,
    PRIORITY_ACTION_HOLD,
    PRIORITY_ACTION_CYCLE,
    PRIORITY_ACTION_SKIP,
)
from controls.rule_based.developed.five_intersections.common import (
    WARNING_TIME,
    HOLD_THRESHOLD,
)


class BusPriorityManager:
    def __init__(self):
        self.tracked_buses = {tls_id: {} for tls_id in TLS_IDS}
        self.bus_priority_active = {tls_id: False for tls_id in TLS_IDS}

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
            except traci.exceptions.TraCIException:
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
            elif time_to_arrival <= WARNING_TIME:
                priority_active = True

        for veh_id in expired_buses:
            del self.tracked_buses[tls_id][veh_id]

        self.bus_priority_active[tls_id] = priority_active

    def is_priority_active(self, tls_id):
        return self.bus_priority_active.get(tls_id, False)

    def get_priority_action(self, tls_id, current_phase, green_duration):
        if not self.is_priority_active(tls_id):
            return None

        if current_phase == p1_main_green:
            if green_duration < HOLD_THRESHOLD:
                return PRIORITY_ACTION_HOLD
            else:
                return PRIORITY_ACTION_CYCLE
        else:
            return PRIORITY_ACTION_SKIP

    def clear_priority(self, tls_id):
        self.tracked_buses[tls_id] = {}
        self.bus_priority_active[tls_id] = False
