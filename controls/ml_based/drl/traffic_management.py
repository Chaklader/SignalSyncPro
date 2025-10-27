import numpy as np
import subprocess
import sys
import time
import os

from constants.developed.common.drl_tls_constants import (
    p1_leading_green,
    num_phases,
    p4_red,
    auto_durations,
)

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)

import traci

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.ml_based.drl.config import DRLConfig
from controls.ml_based.drl.reward import RewardCalculator
from constants.constants import MIN_GREEN_TIME, YELLOW_TIME
from constants.developed.common.drl_tls_constants import (
    p1_main_green,
    p2_main_green,
    p3_main_green,
    p4_main_green,
    p2_yellow,
    p3_yellow,
    p4_yellow,
)

from detectors.developed.drl.detectors import detectors
from constants.developed.common.drl_tls_constants import bus_priority_lanes


class TrafficManagement:
    def __init__(self, sumo_config_file, tls_ids, gui=False, simulation_limit=3600):
        self.sumo_config_file = sumo_config_file
        self.tls_ids = tls_ids
        self.gui = gui
        self.simulation_limit = simulation_limit
        self.reward_calculator = RewardCalculator()

        self.current_phase = {tls_id: p1_leading_green for tls_id in tls_ids}
        self.phase_duration = {tls_id: 0 for tls_id in tls_ids}

        self.stuck_duration = {tls_id: 0 for tls_id in tls_ids}
        self.skip_to_p1_mode = {tls_id: False for tls_id in tls_ids}

        self.phase_change_count = 0
        self.blocked_action_count = 0
        self.total_action_count = 0

        self.detector_info = detectors

    def reset(self):
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
            traci.trafficlight.setPhase(tls_id, p1_leading_green)
            self.current_phase[tls_id] = p1_leading_green
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

            vehicle_queues = self._get_detector_queues(current_phase, "vehicle")
            bicycle_queues = self._get_detector_queues(current_phase, "bicycle")

            state_features.extend(vehicle_queues)
            state_features.extend(bicycle_queues)

            bus_present = self._check_bus_presence_in_lanes(node_idx)
            state_features.append(float(bus_present))

            bus_normalized_wait = self._get_bus_normalized_wait(node_idx)
            state_features.append(bus_normalized_wait)

            sim_time = traci.simulation.getTime()
            time_normalized = min(sim_time / self.simulation_limit, 1.0)
            state_features.append(time_normalized)

        return np.array(state_features, dtype=np.float32)

    def get_valid_actions(self):
        """
        Return list of valid actions based on current traffic light phases.

        Action masking: Skip2P1 (action 1) is only valid when NOT already in Phase 1.
        This prevents invalid attempts and reduces blocking penalties.

        Returns:
            list: Valid action indices
                - Always valid: [0 (Continue), 2 (Next)]
                - Skip2P1 valid only when: current_phase != P1 for any TLS
        """
        from constants.developed.common.drl_tls_constants import p1_main_green

        for tls_id in self.tls_ids:
            if self.current_phase[tls_id] != p1_main_green:
                return [0, 1, 2]

        return [0, 2]

    def _encode_phase(self, phase):
        phases = [
            p1_main_green,
            p2_main_green,
            p3_main_green,
            p4_main_green,
        ]
        encoding = [0.0] * len(phases)

        if phase == p1_main_green:
            encoding[0] = 1.0
        elif phase == p2_main_green:
            encoding[1] = 1.0
        elif phase == p3_main_green:
            encoding[2] = 1.0
        elif phase == p4_main_green:
            encoding[3] = 1.0

        return encoding

    def _get_detector_queues(self, current_phase, vehicle_type):
        queues = []

        try:
            if current_phase not in [
                p1_main_green,
                p2_main_green,
                p3_main_green,
                p4_main_green,
            ]:
                return [0.0] * 4

            phase_detectors = self.detector_info[current_phase]
            detector_list = phase_detectors.get(vehicle_type, [])

            for det_id in detector_list:
                try:
                    last_detection = traci.inductionloop.getTimeSinceDetection(det_id)
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

    def _get_buses_in_priority_lanes(self, node_idx):
        try:
            bus_lanes = bus_priority_lanes[node_idx]
            buses = []

            for lane_id in bus_lanes:
                for veh_id in traci.lane.getLastStepVehicleIDs(lane_id):
                    if traci.vehicle.getTypeID(veh_id) == "bus":
                        buses.append(veh_id)

            return buses
        except:  # noqa: E722
            return []

    def _check_bus_presence_in_lanes(self, node_idx):
        return len(self._get_buses_in_priority_lanes(node_idx)) > 0

    def _get_bus_avg_wait(self, node_idx):
        buses = self._get_buses_in_priority_lanes(node_idx)

        if not buses:
            return 0.0

        try:
            waiting_times = [
                traci.vehicle.getAccumulatedWaitingTime(veh_id) for veh_id in buses
            ]
            return sum(waiting_times) / len(waiting_times)
        except:  # noqa: E722
            return 0.0

    def _get_bus_normalized_wait(self, node_idx):
        avg_wait = self._get_bus_avg_wait(node_idx)
        return min(avg_wait / 60.0, 1.0)

    def step(self, action):
        step_time = traci.simulation.getTime()

        forced_changes = {}

        for tls_id in self.tls_ids:
            current_phase = self.current_phase[tls_id]
            duration = self.phase_duration[tls_id]

            if (
                self.skip_to_p1_mode[tls_id]
                and current_phase in [p2_yellow, p3_yellow, p4_yellow]
                and duration >= YELLOW_TIME
            ):
                traci.trafficlight.setPhase(tls_id, p4_red)

                self.current_phase[tls_id] = p4_red
                self.phase_duration[tls_id] = 0
                self.phase_change_count += 1
                self.skip_to_p1_mode[tls_id] = False

                forced_changes[tls_id] = True
                continue

            if current_phase not in DRLConfig.max_green_time:
                forced_changes[tls_id] = False
                continue

            max_green = DRLConfig.max_green_time[current_phase]

            if duration >= max_green:
                next_phase = self._get_next_phase(current_phase)
                traci.trafficlight.setPhase(tls_id, next_phase)

                self.current_phase[tls_id] = next_phase
                self.phase_duration[tls_id] = 0
                self.phase_change_count += 1

                forced_changes[tls_id] = True

                print(
                    f"[MAX_GREEN FORCED] TLS {tls_id}: Phase {self._get_phase_name(current_phase)} → {self._get_phase_name(next_phase)} "
                    f"(duration {duration}s >= MAX {max_green}s) 🔴 FORCED CHANGE"
                )
            else:
                forced_changes[tls_id] = False

        blocked_penalties = []
        action_changed = False

        for tls_id in self.tls_ids:
            current_phase = self.current_phase[tls_id]

            if current_phase not in [
                p1_main_green,
                p2_main_green,
                p3_main_green,
                p4_main_green,
            ]:
                duration = self.phase_duration[tls_id]

                if (
                    current_phase in auto_durations
                    and duration >= auto_durations[current_phase]
                ):
                    next_phase = self._get_next_phase(current_phase)
                    traci.trafficlight.setPhase(tls_id, next_phase)

                    self.current_phase[tls_id] = next_phase
                    self.phase_duration[tls_id] = 0

                blocked_penalties.append(0.0)
                continue

            if forced_changes[tls_id]:
                blocked_penalties.append(0.0)
                action_changed = True
                continue

            penalty, changed = self._execute_action_for_tls(tls_id, action, step_time)

            blocked_penalties.append(penalty)
            action_changed |= changed

        traci.simulationStep()

        for tls_id in self.tls_ids:
            self.phase_duration[tls_id] += 1

            if action_changed:
                self.stuck_duration[tls_id] = 0
                continue

            self.stuck_duration[tls_id] += 1

        next_state = self._get_state()

        avg_blocked_penalty = (
            sum(blocked_penalties) / len(blocked_penalties)
            if blocked_penalties
            else 0.0
        )

        bus_waiting_data = {
            tls_id: self._get_bus_avg_wait(node_idx)
            for node_idx, tls_id in enumerate(self.tls_ids)
        }

        reward, info = self.reward_calculator.calculate_reward(
            traci,
            self.tls_ids,
            action,
            self.current_phase,
            self.phase_duration,
            blocked_penalty=avg_blocked_penalty,
            stuck_durations=self.stuck_duration,
            bus_waiting_data=bus_waiting_data,
        )

        done = traci.simulation.getMinExpectedNumber() == 0

        return next_state, reward, done, info

    def _execute_action_for_tls(self, tls_id, action, step_time):
        """
        Execute the action for a specific TLS

        Action ID 0 -> CONTINUE
        Action ID 1 -> SKIP TO P1
        Action ID 2 -> Next Phase
        """
        current_phase = self.current_phase[tls_id]
        self.total_action_count += 1

        node_idx = self.tls_ids.index(tls_id)
        bus_waiting_time = self._get_bus_normalized_wait(node_idx)

        blocked_penalty = 0.0
        action_changed = False

        if action == 0:
            pass

        elif action == 1:
            duration = self.phase_duration[tls_id]

            if (
                current_phase == p2_main_green
                or current_phase == p3_main_green
                or current_phase == p4_main_green
            ):
                if duration >= MIN_GREEN_TIME:
                    yellow_phase = self._get_next_phase(current_phase)
                    traci.trafficlight.setPhase(tls_id, yellow_phase)

                    self.current_phase[tls_id] = yellow_phase
                    self.phase_duration[tls_id] = 0
                    self.phase_change_count += 1
                    self.skip_to_p1_mode[tls_id] = True

                    action_changed = True

                    print(
                        f"[PHASE CHANGE] TLS {tls_id}: {self._get_phase_name(current_phase)} → P1 (Action: Skip to P1), Duration: {duration}s ✓"
                    )
                else:
                    self.blocked_action_count += 1

                    if bus_waiting_time > 0.15:
                        blocked_penalty = -DRLConfig.ALPHA_BLOCKED * 0.1
                        print(
                            f"[BLOCKED - BUS WAIT] TLS {tls_id}: Cannot skip to P1 (duration={duration}s < MIN_GREEN_TIME={MIN_GREEN_TIME}s), "
                            f"bus waiting {bus_waiting_time * 60:.1f}s, light penalty: {blocked_penalty:.2f} 🚌"
                        )
                    else:
                        blocked_penalty = -DRLConfig.ALPHA_BLOCKED
                        print(
                            f"[BLOCKED] TLS {tls_id}: Cannot skip to P1 (duration={duration}s < MIN_GREEN_TIME={MIN_GREEN_TIME}s) ⚠️"
                        )
            else:
                self.blocked_action_count += 1
                blocked_penalty = -DRLConfig.ALPHA_BLOCKED * 0.5

                print(
                    f"[INVALID] TLS {tls_id}: Already in Phase 1, Skip2P1 is invalid ⚠️"
                )

        elif action == 2:
            duration = self.phase_duration[tls_id]

            if duration >= MIN_GREEN_TIME:
                next_phase = self._get_next_phase(current_phase)
                traci.trafficlight.setPhase(tls_id, next_phase)

                self.current_phase[tls_id] = next_phase
                self.phase_duration[tls_id] = 0
                self.phase_change_count += 1

                action_changed = True

                print(
                    f"[PHASE CHANGE] TLS {tls_id}: {self._get_phase_name(current_phase)} → {self._get_next_main_phase_name(current_phase)} (Action: Next), Duration: {duration}s ✓"
                )

            else:
                self.blocked_action_count += 1
                blocked_penalty = -DRLConfig.ALPHA_BLOCKED

                print(
                    f"[BLOCKED] TLS {tls_id}: Cannot advance phase (duration={duration}s < MIN_GREEN_TIME={MIN_GREEN_TIME}s) ⚠️"
                )

        return blocked_penalty, action_changed

    def _get_next_phase(self, current_phase):
        return (current_phase + 1) % num_phases

    def _get_phase_name(self, phase):
        """
        Returns the human-readable phase name for any phase.
        """
        phase_names = {
            p1_main_green: "P1",
            p2_main_green: "P2",
            p3_main_green: "P3",
            p4_main_green: "P4",
        }

        return phase_names.get(phase, f"Phase_{phase}")

    def _get_next_main_phase_name(self, current_phase):
        """
        Returns the next main controllable phase name.
        P1 → P2 → P3 → P4 → P1 (cycles through main phases only)
        """
        if current_phase == p1_main_green:
            return "P2"
        elif current_phase == p2_main_green:
            return "P3"
        elif current_phase == p3_main_green:
            return "P4"
        elif current_phase == p4_main_green:
            return "P1"
        else:
            return "Unknown"

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
