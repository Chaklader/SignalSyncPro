import numpy as np
import sys
import os

from constants.developed.common.tls_constants import PHASE_FOUR_RED

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)

import traci

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controls.ml_based.drl.config import DRLConfig
from controls.ml_based.drl.reward import RewardCalculator
from constants.constants import MIN_GREEN_TIME
from constants.developed.common.drl_tls_constants import (
    PHASE_ONE,
    PHASE_TWO,
    PHASE_THREE,
    PHASE_FOUR,
)
from detectors.developed.common.detectors import DETECTORS_INFO


class TrafficManagement:
    def __init__(self, sumo_config_file, tls_ids, gui=False):
        self.sumo_config_file = sumo_config_file
        self.tls_ids = tls_ids
        self.gui = gui
        self.reward_calculator = RewardCalculator()

        self.current_phase = {tls_id: PHASE_ONE for tls_id in tls_ids}
        self.phase_duration = {tls_id: 0 for tls_id in tls_ids}

        self.stuck_duration = {tls_id: 0 for tls_id in tls_ids}
        self.skip_to_p1_mode = {tls_id: False for tls_id in tls_ids}

        self.phase_change_count = 0
        self.blocked_action_count = 0
        self.total_action_count = 0

        self.detector_info = DETECTORS_INFO

    def reset(self):
        import subprocess
        import time

        sumo_binary = "sumo-gui" if self.gui else "sumo"

        if "SUMO_BINDIR" in os.environ:
            sumo_binary = os.path.join(os.environ["SUMO_BINDIR"], sumo_binary)

        sumo_cmd = [sumo_binary, "-c", self.sumo_config_file]
        self.sumo_process = subprocess.Popen(
            sumo_cmd, stdout=sys.stdout, stderr=sys.stderr
        )

        time.sleep(2)

        try:
            traci.init(8816)
        except Exception as e:
            print(f"Failed to connect to SUMO: {e}")
            if hasattr(self, "sumo_process"):
                self.sumo_process.terminate()
            raise

        for tls_id in self.tls_ids:
            traci.trafficlight.setPhase(tls_id, PHASE_ONE)
            self.current_phase[tls_id] = PHASE_ONE
            self.phase_duration[tls_id] = 0
            self.stuck_duration[tls_id] = 0
            self.skip_to_p1_mode[tls_id] = False

        return self._get_state()

    def _get_state(self):
        state_features = []

        for node_idx, tls_id in enumerate(self.tls_ids):
            current_phase = self.current_phase[tls_id]
            phase_duration = self.phase_duration[tls_id]

            phase_encoding = self._encode_phase(current_phase)
            state_features.extend(phase_encoding)

            state_features.append(min(phase_duration / 60.0, 1.0))

            vehicle_queues = self._get_detector_queues(
                node_idx, current_phase, "vehicle"
            )
            bicycle_queues = self._get_detector_queues(
                node_idx, current_phase, "bicycle"
            )

            state_features.extend(vehicle_queues)
            state_features.extend(bicycle_queues)

            bus_present = self._check_bus_presence_in_lanes(node_idx)
            state_features.append(float(bus_present))

            sim_time = traci.simulation.getTime()
            time_normalized = (sim_time % 3600) / 3600.0
            state_features.append(time_normalized)

        return np.array(state_features, dtype=np.float32)

    def _encode_phase(self, phase):
        phases = [
            PHASE_ONE,
            PHASE_TWO,
            PHASE_THREE,
            PHASE_FOUR,
        ]
        encoding = [0.0] * len(phases)

        if phase in [1]:
            encoding[0] = 1.0
        elif phase in [5]:
            encoding[1] = 1.0
        elif phase in [9]:
            encoding[2] = 1.0
        elif phase in [13]:
            encoding[3] = 1.0

        return encoding

    def _get_detector_queues(self, node_idx, current_phase, vehicle_type):
        queues = []

        try:
            if current_phase in [PHASE_ONE, PHASE_TWO, PHASE_THREE, PHASE_FOUR]:
                detector_list = self.detector_info[current_phase][node_idx]
            else:
                return [0.0] * 4

            for detector_group in detector_list:
                if isinstance(detector_group, list):
                    for det_id in detector_group:
                        try:
                            last_detection = traci.inductionloop.getTimeSinceDetection(
                                det_id
                            )
                            if last_detection < 3.0:
                                queues.append(1.0)
                            else:
                                queues.append(0.0)
                        except:  # noqa: E722
                            queues.append(0.0)
        except:  # noqa: E722
            queues = [0.0] * 4

        while len(queues) < 4:
            queues.append(0.0)
        return queues[:4]

    def _check_bus_presence_in_lanes(self, node_idx):
        from constants.developed.common.drl_tls_constants import BUS_PRIORITY_LANE

        try:
            bus_lanes = BUS_PRIORITY_LANE[node_idx]
            for lane_id in bus_lanes:
                for veh_id in traci.lane.getLastStepVehicleIDs(lane_id):
                    if traci.vehicle.getTypeID(veh_id) == "bus":
                        return True
        except:  # noqa: E722
            pass
        return False

    def step(self, action):
        step_time = traci.simulation.getTime()

        forced_changes = {}

        for tls_id in self.tls_ids:
            current_phase = self.current_phase[tls_id]
            duration = self.phase_duration[tls_id]

            if self.skip_to_p1_mode[tls_id] and current_phase in [6, 10, 14]:
                print(
                    f"[SKIP TO P1] TLS {tls_id}: Phase {current_phase} → 15 (all-red before P1) 🔴"
                )
                traci.trafficlight.setPhase(tls_id, 15)
                self.current_phase[tls_id] = PHASE_FOUR_RED
                self.phase_duration[tls_id] = 0
                self.phase_change_count += 1
                self.skip_to_p1_mode[tls_id] = False  # Clear flag
                forced_changes[tls_id] = True
                continue

            if current_phase in DRLConfig.MAX_GREEN_TIME:
                max_green = DRLConfig.MAX_GREEN_TIME[current_phase]
            else:
                forced_changes[tls_id] = False
                continue

            if duration >= max_green:
                next_phase = self._get_next_phase(current_phase)
                print(
                    f"[MAX_GREEN FORCED] TLS {tls_id}: Phase {current_phase} → {next_phase} "
                    f"(duration {duration}s >= MAX {max_green}s) 🔴 FORCED CHANGE"
                )
                traci.trafficlight.setPhase(tls_id, next_phase)
                self.current_phase[tls_id] = next_phase
                self.phase_duration[tls_id] = 0
                self.phase_change_count += 1
                forced_changes[tls_id] = True
            else:
                forced_changes[tls_id] = False

        blocked_penalties = []
        action_changed = False

        for tls_id in self.tls_ids:
            if not forced_changes[tls_id]:
                penalty, changed = self._execute_action_for_tls(
                    tls_id, action, step_time
                )
                blocked_penalties.append(penalty)
                if changed:
                    action_changed = True
            else:
                blocked_penalties.append(0.0)
                action_changed = True

        traci.simulationStep()

        for tls_id in self.tls_ids:
            self.phase_duration[tls_id] += 1

            if action_changed:
                self.stuck_duration[tls_id] = 0
            else:
                self.stuck_duration[tls_id] += 1

        next_state = self._get_state()

        avg_blocked_penalty = (
            sum(blocked_penalties) / len(blocked_penalties)
            if blocked_penalties
            else 0.0
        )

        reward, info = self.reward_calculator.calculate_reward(
            traci,
            self.tls_ids,
            action,
            self.current_phase,
            self.phase_duration,
            blocked_penalty=avg_blocked_penalty,
            stuck_durations=self.stuck_duration,
        )

        done = traci.simulation.getMinExpectedNumber() == 0

        return next_state, reward, done, info

    def _execute_action_for_tls(self, tls_id, action, step_time):
        current_phase = self.current_phase[tls_id]
        self.total_action_count += 1
        blocked_penalty = 0.0
        action_changed = False

        # continue action
        if action == 0:
            pass

        # skip to P1 action
        elif action == 1:
            duration = self.phase_duration[tls_id]
            if (
                current_phase in [PHASE_TWO, PHASE_THREE, PHASE_FOUR]
                and duration >= MIN_GREEN_TIME
            ):
                yellow_phase = self._get_next_phase(current_phase)

                print(
                    f"[PHASE CHANGE] TLS {tls_id}: Phase {current_phase} → {yellow_phase} (Skip to P1 - yellow clearance), Duration: {duration}s ✓"
                )
                traci.trafficlight.setPhase(tls_id, yellow_phase)
                self.current_phase[tls_id] = yellow_phase
                self.phase_duration[tls_id] = 0
                self.phase_change_count += 1
                action_changed = True

                self.skip_to_p1_mode[tls_id] = True

            #  can't skip to P1 within MIN_GREEN_TIME
            elif current_phase in [PHASE_TWO, PHASE_THREE, PHASE_FOUR]:
                print(
                    f"[BLOCKED] TLS {tls_id}: Cannot skip to P1 (duration={duration}s < MIN_GREEN_TIME={MIN_GREEN_TIME}s) ⚠️"
                )
                self.blocked_action_count += 1
                blocked_penalty = -DRLConfig.ALPHA_BLOCKED

            else:
                print(
                    f"[REDUNDANT] TLS {tls_id}: Already in Phase 1, Skip2P1 is redundant ⚠️"
                )
                self.blocked_action_count += 1
                blocked_penalty = -DRLConfig.ALPHA_BLOCKED

        # next action
        elif action == 2:
            duration = self.phase_duration[tls_id]

            if duration >= MIN_GREEN_TIME:
                next_phase = self._get_next_phase(current_phase)
                print(
                    f"[PHASE CHANGE] TLS {tls_id}: Phase {current_phase} → {next_phase} (Next), Duration: {duration}s ✓"
                )
                traci.trafficlight.setPhase(tls_id, next_phase)
                self.current_phase[tls_id] = next_phase
                self.phase_duration[tls_id] = 0
                self.phase_change_count += 1
                action_changed = True
            else:
                print(
                    f"[BLOCKED] TLS {tls_id}: Cannot advance phase (duration={duration}s < MIN_GREEN_TIME={MIN_GREEN_TIME}s) ⚠️"
                )
                self.blocked_action_count += 1
                blocked_penalty = -DRLConfig.ALPHA_BLOCKED

        return blocked_penalty, action_changed

    def _get_next_phase(self, current_phase):
        return (current_phase + 1) % 16

    def close(self):
        print(f"\n{'=' * 80}")
        print("[EPISODE SUMMARY] Phase Change Statistics:")
        print(f"  Total actions attempted: {self.total_action_count}")
        print(f"  Phase changes executed: {self.phase_change_count}")
        print(f"  Actions blocked (MIN_GREEN_TIME): {self.blocked_action_count}")
        if self.total_action_count > 0:
            change_rate = (self.phase_change_count / self.total_action_count) * 100
            block_rate = (self.blocked_action_count / self.total_action_count) * 100
            print(f"  Phase change rate: {change_rate:.1f}%")
            print(f"  Block rate: {block_rate:.1f}%")
        print(f"{'=' * 80}\n")

        self.reward_calculator.print_safety_summary()

        self.phase_change_count = 0
        self.blocked_action_count = 0
        self.total_action_count = 0

        try:
            traci.close()
        except:  # noqa: E722
            pass

        if hasattr(self, "sumo_process"):
            try:
                self.sumo_process.terminate()
                self.sumo_process.wait(timeout=5)
            except:  # noqa: E722
                try:
                    self.sumo_process.kill()
                except:  # noqa: E722
                    pass
