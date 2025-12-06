import sys

import traci

from constants.developed.multi_agent.drl_tls_constants import (
    PHASE_NAMES,
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
        self.total_gap_outs = 0
        self.gap_outs_by_tls = {tls_id: 0 for tls_id in TLS_IDS}
        self.last_log_time = 0

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

        gap_out = vehicle_gap_out and bicycle_gap_out
        if gap_out:
            self.total_gap_outs += 1
            self.gap_outs_by_tls[tls_id] += 1
            phase_name = PHASE_NAMES.get(phase, f"P{phase}")
            print(
                f"[GAP-OUT] TLS {tls_id}: {phase_name} terminated by gap-out "
                f"(no traffic for {GAP_OUT_THRESHOLD}s) ⏱️"
            )
            sys.stdout.flush()
        return gap_out

    def print_summary(self, current_time):
        """Print periodic summary of gap-out activity."""
        if current_time - self.last_log_time >= 1000:
            print(f"\n[GAP-OUT SUMMARY @ {current_time}s]")
            print(f"  Total gap-outs: {self.total_gap_outs}")
            for tls_id in TLS_IDS:
                if self.gap_outs_by_tls[tls_id] > 0:
                    print(f"  TLS {tls_id}: {self.gap_outs_by_tls[tls_id]} gap-outs")
            sys.stdout.flush()
            self.last_log_time = current_time

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
        # Phase transition counters for logging
        self.phase_transitions = {tls_id: 0 for tls_id in TLS_IDS}
        self.max_green_terminations = {tls_id: 0 for tls_id in TLS_IDS}
        self.skip_to_p1_count = {tls_id: 0 for tls_id in TLS_IDS}
        self.last_log_time = 0

    def init_tls(self):
        for tls_id in TLS_IDS:
            traci.trafficlight.setPhase(tls_id, p1_leading_green)
            self.current_phase[tls_id] = p1_leading_green
            self.phase_duration[tls_id] = 0

    def update_phases(self):
        for tls_id in TLS_IDS:
            self.current_phase[tls_id] = traci.trafficlight.getPhase(tls_id)

    def terminate_phase(self, tls_id, phase, reason="normal"):
        next_p = next_phase(phase)
        traci.trafficlight.setPhase(tls_id, next_p)
        duration = self.phase_duration[tls_id]
        self.phase_duration[tls_id] = 0
        self.phase_transitions[tls_id] += 1

        phase_name = PHASE_NAMES.get(phase, f"P{phase}")
        next_name = PHASE_NAMES.get(next_p, f"P{next_p}")
        print(
            f"[PHASE CHANGE] TLS {tls_id}: {phase_name} → {next_name} "
            f"(duration={duration}s, reason={reason})"
        )
        sys.stdout.flush()

    def skip_to_p1_phase(self, tls_id, phase):
        self.skip_to_p1[tls_id] = True
        next_p = next_phase(phase)
        traci.trafficlight.setPhase(tls_id, next_p)
        duration = self.phase_duration[tls_id]
        self.phase_duration[tls_id] = 0
        self.skip_to_p1_count[tls_id] += 1

        phase_name = PHASE_NAMES.get(phase, f"P{phase}")
        print(
            f"[SKIP TO P1] TLS {tls_id}: {phase_name} → P1 "
            f"(duration={duration}s, skipping remaining phases) 🔄"
        )
        sys.stdout.flush()

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
                "total_transitions": self.phase_transitions[tls_id],
                "max_green_terminations": self.max_green_terminations[tls_id],
                "skip_to_p1_count": self.skip_to_p1_count[tls_id],
            }
            for tls_id in TLS_IDS
        }

    def print_controller_summary(self, current_time):
        """Print periodic summary of controller activity."""
        if current_time - self.last_log_time >= 1000:
            print(f"\n[CONTROLLER SUMMARY @ {current_time}s]")
            total_transitions = sum(self.phase_transitions.values())
            total_max_green = sum(self.max_green_terminations.values())
            total_skip_p1 = sum(self.skip_to_p1_count.values())
            print(f"  Total phase transitions: {total_transitions}")
            print(f"  Max-green terminations: {total_max_green}")
            print(f"  Skip-to-P1 actions: {total_skip_p1}")
            for tls_id in TLS_IDS:
                phase_name = PHASE_NAMES.get(self.current_phase[tls_id], "?")
                print(
                    f"  TLS {tls_id}: Phase={phase_name}, "
                    f"Duration={self.phase_duration[tls_id]}s, "
                    f"Transitions={self.phase_transitions[tls_id]}"
                )
            # Print gap-out summary
            self.gap_out_detector.print_summary(current_time)
            sys.stdout.flush()
            self.last_log_time = current_time
