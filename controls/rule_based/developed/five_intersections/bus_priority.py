import traci

from constants.developed.multi_agent.drl_tls_constants import (
    TLS_IDS,
    bus_signals_emit_lanes,
    p1_main_green,
)
from controls.rule_based.developed.five_intersections.common import (
    WARNING_TIME,
    HOLD_THRESHOLD,
)


class BusPriorityManager:
    def __init__(self):
        self.bus_detected = {tls_id: False for tls_id in TLS_IDS}
        self.bus_detected_time = {tls_id: None for tls_id in TLS_IDS}
        self.bus_travel_time = {tls_id: None for tls_id in TLS_IDS}
        self.bus_priority_active = {tls_id: False for tls_id in TLS_IDS}

    def update(self, current_time):
        for idx, tls_id in enumerate(TLS_IDS):
            self._check_bus_emit_lanes(idx, tls_id, current_time)
            self._update_priority_status(tls_id, current_time)

    def _check_bus_emit_lanes(self, idx, tls_id, current_time):
        if self.bus_detected[tls_id]:
            return

        emit_lanes = bus_signals_emit_lanes.get(idx, ())

        for lane_id in emit_lanes:
            try:
                vehicles = traci.lane.getLastStepVehicleIDs(lane_id)
                for veh_id in vehicles:
                    if traci.vehicle.getTypeID(veh_id) == "bus":
                        travel_time = self._get_travel_time_for_lane(idx, lane_id)
                        self.bus_detected[tls_id] = True
                        self.bus_detected_time[tls_id] = current_time
                        self.bus_travel_time[tls_id] = travel_time
                        return
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
        if not self.bus_detected[tls_id]:
            self.bus_priority_active[tls_id] = False
            return

        detection_time = self.bus_detected_time[tls_id]
        travel_time = self.bus_travel_time[tls_id]

        if detection_time is None or travel_time is None:
            return

        elapsed = current_time - detection_time
        time_to_arrival = travel_time - elapsed

        if time_to_arrival <= WARNING_TIME:
            self.bus_priority_active[tls_id] = True

        if time_to_arrival <= 0:
            self._clear_bus_detection(tls_id)

    def _clear_bus_detection(self, tls_id):
        self.bus_detected[tls_id] = False
        self.bus_detected_time[tls_id] = None
        self.bus_travel_time[tls_id] = None
        self.bus_priority_active[tls_id] = False

    def is_priority_active(self, tls_id):
        return self.bus_priority_active.get(tls_id, False)

    def get_priority_action(self, tls_id, current_phase, green_duration):
        if not self.is_priority_active(tls_id):
            return None

        if current_phase == p1_main_green:
            if green_duration < HOLD_THRESHOLD:
                return "HOLD"
            else:
                return "CYCLE"
        else:
            return "SKIP"

    def clear_priority(self, tls_id):
        self._clear_bus_detection(tls_id)
