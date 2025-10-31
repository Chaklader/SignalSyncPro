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
    main_controllable_phases,
    phase_names,
    p1_red,
    p2_red,
    p3_red,
)

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)

import traci

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.ml_based.drl.config import DRLConfig
from controls.ml_based.drl.reward import RewardCalculator
from constants.constants import MIN_GREEN_TIME, YELLOW_TIME, ALL_RED_TIME
from constants.developed.common.drl_tls_constants import (
    p1_main_green,
    p2_main_green,
    p3_main_green,
    p4_main_green,
)
from constants.developed.common.phase_transitions import (
    get_next_phase_in_sequence,
    main_to_leading,
)

from constants.developed.common.drl_tls_constants import (
    p2_yellow,
    p3_yellow,
    p4_yellow,
)

from detectors.developed.drl.detectors import detectors
from constants.developed.common.drl_tls_constants import bus_priority_lanes


class TrafficManagement:
    def __init__(
        self,
        sumo_config_file,
        tls_ids,
        gui=False,
        simulation_limit=3600,
        is_training=True,
    ):
        self.sumo_config_file = sumo_config_file
        self.tls_ids = tls_ids
        self.gui = gui
        self.simulation_limit = simulation_limit
        self.is_training = is_training
        self.reward_calculator = RewardCalculator()

        self.current_phase = {tls_id: p1_leading_green for tls_id in tls_ids}
        self.phase_duration = {tls_id: 0 for tls_id in tls_ids}

        self.stuck_duration = {tls_id: 0 for tls_id in tls_ids}
        self.skip_to_p1_mode = {tls_id: False for tls_id in tls_ids}
        self.next_main_phase = {tls_id: None for tls_id in tls_ids}

        self.phase_change_count = 0
        self.blocked_action_count = 0
        self.total_action_count = 0

        self.action_history = []
        self.max_history_length = 1000

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
        from constants.developed.common.drl_tls_constants import p1_main_green

        any_in_p1 = any(
            self.current_phase[tls_id] == p1_main_green for tls_id in self.tls_ids
        )

        if any_in_p1:
            return [0, 2]
        else:
            return [0, 1, 2]

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

    def step(self, action, epsilon=0.0, was_exploration=False):
        step_time = traci.simulation.getTime()

        self.action_history.append(action)
        if len(self.action_history) > self.max_history_length:
            self.action_history.pop(0)

        action_counts = {0: 0, 1: 0, 2: 0}
        for a in self.action_history:
            if a in action_counts:
                action_counts[a] += 1

        blocked_penalties = []
        action_changed = False
        action_results = []

        for tls_id in self.tls_ids:
            current_phase = self.current_phase[tls_id]
            duration = self.phase_duration[tls_id]

            forced = self._handle_main_green_phases(tls_id, current_phase, duration)
            if forced:
                blocked_penalties.append(0.0)
                action_changed = True
                continue

            if current_phase not in [
                p1_main_green,
                p2_main_green,
                p3_main_green,
                p4_main_green,
            ]:
                self._handle_non_green_phases(tls_id, current_phase, duration)
                blocked_penalties.append(0.0)
                continue

            result = self._execute_action_for_tls(tls_id, action, step_time)
            action_results.append(result)

            blocked_penalties.append(result["blocked_penalty"])
            action_changed |= result["action_changed"]

        self._log_consolidated_action(action_results, epsilon, was_exploration)

        traci.simulationStep()

        for tls_id in self.tls_ids:
            self.phase_duration[tls_id] += 1
            current_phase = self.current_phase[tls_id]

            if action_changed or current_phase not in main_controllable_phases:
                self.stuck_duration[tls_id] = 0
            else:
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
            action_counts=action_counts,
            epsilon=epsilon,
            is_training=self.is_training,
        )

        done = traci.simulation.getMinExpectedNumber() == 0

        return next_state, reward, done, info

    def _log_consolidated_action(self, action_results, epsilon, was_exploration):
        results_with_logs = [r for r in action_results if r["log_type"] is not None]

        if not results_with_logs:
            return

        if len(results_with_logs) == 1:
            result = results_with_logs[0]
            log_type = result["log_type"]
            log_data = result["log_data"]

            exploration_pct = epsilon * 100
            exploitation_pct = (1 - epsilon) * 100
            mode = "Exploration ACT" if was_exploration else "Exploitation ACT"

            if log_type == "PHASE_CHANGE":
                print(
                    f"[PHASE CHANGE] TLS [{log_data['tls_id']}], "
                    f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                    f"{mode}: {log_data['from_phase']} → {log_data['to_phase']} "
                    f"(Action: {log_data['action_name']}), Duration: {log_data['duration']}s"
                )
            elif log_type == "BLOCKED":
                print(
                    f"[BLOCKED] TLS [{log_data['tls_id']}], "
                    f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                    f"{mode}: {log_data['reason']} "
                    f"(duration={log_data['duration']}s < MIN_GREEN={log_data['min_green']}s) ⚠️"
                )
            elif log_type == "BLOCKED_BUS":
                print(
                    f"[BLOCKED - BUS WAIT] TLS [{log_data['tls_id']}], "
                    f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                    f"{mode}: {log_data['reason']} "
                    f"(duration={log_data['duration']}s < MIN_GREEN={log_data['min_green']}s), "
                    f"bus waiting {log_data['bus_wait']:.1f}s, light penalty: {log_data['penalty']:.2f} 🚌"
                )
            elif log_type == "INVALID":
                print(
                    f"[INVALID] TLS [{log_data['tls_id']}], "
                    f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                    f"{mode}: {log_data['reason']} ⚠️"
                )

        elif len(results_with_logs) == 2:
            if results_with_logs[0]["log_type"] == results_with_logs[1]["log_type"]:
                log_type = results_with_logs[0]["log_type"]
                log_data_0 = results_with_logs[0]["log_data"]
                log_data_1 = results_with_logs[1]["log_data"]

                tls_list = [log_data_0["tls_id"], log_data_1["tls_id"]]

                exploration_pct = epsilon * 100
                exploitation_pct = (1 - epsilon) * 100
                mode = "Exploration ACT" if was_exploration else "Exploitation ACT"

                if log_type == "PHASE_CHANGE":
                    print(
                        f"[PHASE CHANGE] TLS {tls_list}, "
                        f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                        f"{mode}: {log_data_0['from_phase']} → {log_data_0['to_phase']} "
                        f"(Action: {log_data_0['action_name']}), Duration: {log_data_0['duration']}s"
                    )
                elif log_type == "BLOCKED":
                    print(
                        f"[BLOCKED] TLS {tls_list}, "
                        f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                        f"{mode}: {log_data_0['reason']} "
                        f"(duration={log_data_0['duration']}s < MIN_GREEN={log_data_0['min_green']}s) ⚠️"
                    )
                elif log_type == "BLOCKED_BUS":
                    print(
                        f"[BLOCKED - BUS WAIT] TLS {tls_list}, "
                        f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                        f"{mode}: {log_data_0['reason']} "
                        f"(duration={log_data_0['duration']}s < MIN_GREEN={log_data_0['min_green']}s), "
                        f"bus waiting {log_data_0['bus_wait']:.1f}s, light penalty: {log_data_0['penalty']:.2f} 🚌"
                    )
                elif log_type == "INVALID":
                    print(
                        f"[INVALID] TLS {tls_list}, "
                        f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                        f"{mode}: {log_data_0['reason']} ⚠️"
                    )
            else:
                for result in results_with_logs:
                    log_type = result["log_type"]
                    log_data = result["log_data"]

                    exploration_pct = epsilon * 100
                    exploitation_pct = (1 - epsilon) * 100
                    mode = "Exploration ACT" if was_exploration else "Exploitation ACT"

                    if log_type == "PHASE_CHANGE":
                        print(
                            f"[PHASE CHANGE] TLS [{log_data['tls_id']}], "
                            f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                            f"{mode}: {log_data['from_phase']} → {log_data['to_phase']} "
                            f"(Action: {log_data['action_name']}), Duration: {log_data['duration']}s"
                        )
                    elif log_type == "BLOCKED":
                        print(
                            f"[BLOCKED] TLS [{log_data['tls_id']}], "
                            f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                            f"{mode}: {log_data['reason']} "
                            f"(duration={log_data['duration']}s < MIN_GREEN={log_data['min_green']}s) ⚠️"
                        )
                    elif log_type == "BLOCKED_BUS":
                        print(
                            f"[BLOCKED - BUS WAIT] TLS [{log_data['tls_id']}], "
                            f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                            f"{mode}: {log_data['reason']} "
                            f"(duration={log_data['duration']}s < MIN_GREEN={log_data['min_green']}s), "
                            f"bus waiting {log_data['bus_wait']:.1f}s, light penalty: {log_data['penalty']:.2f} 🚌"
                        )
                    elif log_type == "INVALID":
                        print(
                            f"[INVALID] TLS [{log_data['tls_id']}], "
                            f"[Exploration {exploration_pct:.0f}%, Exploitation {exploitation_pct:.0f}%], "
                            f"{mode}: {log_data['reason']} ⚠️"
                        )

    def _execute_action_for_tls(self, tls_id, action, step_time):
        """
        Execute the action for a specific TLS:

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
        log_type = None
        log_data = {}

        if action == 0:
            pass

        elif action == 1:
            duration = self.phase_duration[tls_id]

            if (
                current_phase == p2_main_green
                or current_phase == p3_main_green
                or current_phase == p4_main_green
            ):
                phase_min_green = DRLConfig.phase_min_green_time.get(
                    current_phase, MIN_GREEN_TIME
                )

                if duration >= phase_min_green:
                    yellow_phase = self._get_next_phase(current_phase)
                    traci.trafficlight.setPhase(tls_id, yellow_phase)

                    self.current_phase[tls_id] = yellow_phase
                    self.phase_duration[tls_id] = 0
                    self.phase_change_count += 1
                    self.skip_to_p1_mode[tls_id] = True

                    action_changed = True

                    log_type = "PHASE_CHANGE"
                    log_data = {
                        "tls_id": tls_id,
                        "from_phase": self._get_phase_name(current_phase),
                        "to_phase": "P1",
                        "action_name": "Skip to P1",
                        "duration": duration,
                    }
                else:
                    self.blocked_action_count += 1

                    if bus_waiting_time > 0.15:
                        blocked_penalty = -DRLConfig.ALPHA_BLOCKED * 0.1
                        phase_min_green = DRLConfig.phase_min_green_time.get(
                            current_phase, MIN_GREEN_TIME
                        )
                        log_type = "BLOCKED_BUS"
                        log_data = {
                            "tls_id": tls_id,
                            "reason": "Cannot skip to P1",
                            "duration": duration,
                            "min_green": phase_min_green,
                            "bus_wait": bus_waiting_time * 60,
                            "penalty": blocked_penalty,
                        }
                    else:
                        blocked_penalty = -DRLConfig.ALPHA_BLOCKED
                        phase_min_green = DRLConfig.phase_min_green_time.get(
                            current_phase, MIN_GREEN_TIME
                        )
                        log_type = "BLOCKED"
                        log_data = {
                            "tls_id": tls_id,
                            "reason": "Cannot skip to P1",
                            "duration": duration,
                            "min_green": phase_min_green,
                        }
            else:
                self.blocked_action_count += 1
                blocked_penalty = -DRLConfig.ALPHA_BLOCKED * 0.5

                log_type = "INVALID"
                log_data = {
                    "tls_id": tls_id,
                    "reason": "Already in Phase 1, Skip2P1 is invalid",
                }

        elif action == 2:
            duration = self.phase_duration[tls_id]
            phase_min_green = DRLConfig.phase_min_green_time.get(
                current_phase, MIN_GREEN_TIME
            )

            if duration >= phase_min_green:
                next_main_phase = get_next_phase_in_sequence(current_phase)
                yellow_phase = self._get_yellow_phase(current_phase)
                traci.trafficlight.setPhase(tls_id, yellow_phase)

                self.current_phase[tls_id] = yellow_phase
                self.phase_duration[tls_id] = 0
                self.phase_change_count += 1
                self.next_main_phase[tls_id] = next_main_phase

                action_changed = True

                next_phase_name = phase_names.get(
                    next_main_phase, f"P{next_main_phase}"
                )
                log_type = "PHASE_CHANGE"
                log_data = {
                    "tls_id": tls_id,
                    "from_phase": self._get_phase_name(current_phase),
                    "to_phase": next_phase_name,
                    "action_name": "Next",
                    "duration": duration,
                }

            else:
                self.blocked_action_count += 1
                blocked_penalty = -DRLConfig.ALPHA_BLOCKED

                log_type = "BLOCKED"
                log_data = {
                    "tls_id": tls_id,
                    "reason": "Cannot advance phase",
                    "duration": duration,
                    "min_green": phase_min_green,
                }

        return {
            "blocked_penalty": blocked_penalty,
            "action_changed": action_changed,
            "log_type": log_type,
            "log_data": log_data,
        }

    def _handle_main_green_phases(self, tls_id, current_phase, duration):
        if (
            self.next_main_phase[tls_id]
            and current_phase in [p1_red, p2_red, p3_red, p4_red]
            and duration >= ALL_RED_TIME
        ):
            next_phase = main_to_leading[self.next_main_phase[tls_id]]
            traci.trafficlight.setPhase(tls_id, next_phase)

            self.current_phase[tls_id] = next_phase
            self.phase_duration[tls_id] = 0
            self.phase_change_count += 1
            self.next_main_phase[tls_id] = None
            return True

        if current_phase not in DRLConfig.max_green_time:
            return False

        max_green = DRLConfig.max_green_time[current_phase]

        if duration >= max_green:
            next_phase = self._get_next_phase(current_phase)
            traci.trafficlight.setPhase(tls_id, next_phase)

            self.current_phase[tls_id] = next_phase
            self.phase_duration[tls_id] = 0
            self.phase_change_count += 1

            print(
                f"[MAX_GREEN FORCED] TLS {tls_id}: Phase {self._get_phase_name(current_phase)} → {self._get_phase_name(next_phase)} "
                f"(duration {duration}s >= MAX {max_green}s) 🔴 FORCED CHANGE"
            )
            return True

        return False

    def _handle_non_green_phases(self, tls_id, current_phase, duration):
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
            return

        if (
            current_phase in auto_durations
            and duration >= auto_durations[current_phase]
        ):
            next_phase = self._get_next_phase(current_phase)
            traci.trafficlight.setPhase(tls_id, next_phase)

            self.current_phase[tls_id] = next_phase
            self.phase_duration[tls_id] = 0

    def _get_next_phase(self, current_phase):
        return (current_phase + 1) % num_phases

    def _get_yellow_phase(self, current_phase):
        """Get the yellow phase after current main phase"""
        if current_phase in main_controllable_phases:
            return current_phase + 1  # Yellow is always +1 from main phase
        return current_phase

    def _get_phase_name(self, phase):
        """
        Returns the human-readable phase name for any phase.
        """
        return phase_names.get(phase, f"Phase_{phase}")

    def _get_next_main_phase_name(self, current_phase):
        """
        Returns the next main controllable phase name.
        P1 → P2 → P3 → P4 → P1 (cycles through main phases only)
        """
        phase_keys = list(phase_names.keys())
        for idx, phase in enumerate(phase_keys):
            if phase == current_phase:
                next_idx = (idx + 1) % len(phase_keys)
                return phase_names[phase_keys[next_idx]]
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
