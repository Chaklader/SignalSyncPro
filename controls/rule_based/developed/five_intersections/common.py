import traci

from constants.developed.multi_agent.drl_tls_constants import (
    TLS_IDS,
    p1_leading_green,
    auto_durations,
    next_phase,
    MAIN_GREEN_PHASES,
    RED_PHASES,
    GAP_OUT_THRESHOLD,
)
from controls.ml_based.drl.multi_agent.config import DRLConfig
from detectors.developed.drl.multi_agent.detectors import get_detectors_for_tls


MIN_GREEN = DRLConfig.phase_min_green_time
MAX_GREEN = DRLConfig.max_green_time


class GapOutDetector:
    def __init__(self):
        self.last_detection_time = {}

    def update(self, tls_id, phase, current_time):
        if phase not in MAIN_GREEN_PHASES:
            return

        detectors = get_detectors_for_tls(tls_id, phase)

        for det_id in detectors.get("vehicle", []) + detectors.get("bicycle", []):
            try:
                count = traci.inductionloop.getLastStepVehicleNumber(det_id)
                if count > 0:
                    self.last_detection_time[det_id] = current_time
            except traci.exceptions.TraCIException:
                pass

    def check_gap_out(self, tls_id, phase, current_time):
        detectors = get_detectors_for_tls(tls_id, phase)

        vehicle_dets = detectors.get("vehicle", [])
        bicycle_dets = detectors.get("bicycle", [])

        vehicle_gap_out = self._all_detectors_gap_out(vehicle_dets, current_time)
        bicycle_gap_out = self._all_detectors_gap_out(bicycle_dets, current_time)

        return vehicle_gap_out and bicycle_gap_out

    def _all_detectors_gap_out(self, detector_ids, current_time):
        if not detector_ids:
            return True

        for det_id in detector_ids:
            last_time = self.last_detection_time.get(det_id, 0)
            if current_time - last_time < GAP_OUT_THRESHOLD:
                return False
        return True


class BaseTLSController:
    def __init__(self):
        self.current_phase = {tls_id: 0 for tls_id in TLS_IDS}
        self.phase_duration = {tls_id: 0 for tls_id in TLS_IDS}
        self.skip_to_p1 = {tls_id: False for tls_id in TLS_IDS}
        self.gap_out_detector = GapOutDetector()

    def init_tls(self):
        for tls_id in TLS_IDS:
            traci.trafficlight.setPhase(tls_id, p1_leading_green)
            self.current_phase[tls_id] = p1_leading_green
            self.phase_duration[tls_id] = 0

    def update_phases(self):
        for tls_id in TLS_IDS:
            self.current_phase[tls_id] = traci.trafficlight.getPhase(tls_id)

    def terminate_phase(self, tls_id, phase):
        next_p = next_phase(phase)
        traci.trafficlight.setPhase(tls_id, next_p)
        self.phase_duration[tls_id] = 0

    def skip_to_p1_phase(self, tls_id, phase):
        self.skip_to_p1[tls_id] = True
        next_p = next_phase(phase)
        traci.trafficlight.setPhase(tls_id, next_p)
        self.phase_duration[tls_id] = 0

    def advance_phase(self, tls_id, phase):
        self.phase_duration[tls_id] = 0

        if phase in RED_PHASES and self.skip_to_p1[tls_id]:
            traci.trafficlight.setPhase(tls_id, p1_leading_green)
            self.skip_to_p1[tls_id] = False
            return

        next_p = next_phase(phase)
        traci.trafficlight.setPhase(tls_id, next_p)

    """
        handle the non-actuated phases (leading green, yellow, and red)
        These phases are managed automatically based on fixed durations.
    """

    def handle_transition_phase(self, tls_id, phase):
        self.phase_duration[tls_id] += 1
        duration = self.phase_duration[tls_id]
        required_duration = auto_durations.get(phase, 1)

        if duration >= required_duration:
            self.advance_phase(tls_id, phase)

    def get_stats(self):
        return {
            tls_id: {
                "phase": self.current_phase[tls_id],
                "duration": self.phase_duration[tls_id],
            }
            for tls_id in TLS_IDS
        }
