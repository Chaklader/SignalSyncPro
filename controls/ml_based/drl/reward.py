import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.ml_based.drl.config import DRLConfig
from common.utils import get_vehicle_mode
from constants.constants import SAFE_HEADWAY, COLLISION_DISTANCE
from constants.developed.common.drl_tls_constants import action_names


class RewardCalculator:
    def __init__(self):
        self.prev_metrics = {}
        self.episode_step = 0
        self.phase_duration = {}

        self.total_headway_violations = 0
        self.total_distance_violations = 0

        self.action_counts = {0: 0, 1: 0, 2: 0}
        self.total_actions = 0

    def reset(self):
        if self.total_actions > 0:
            print("\n[ACTION DISTRIBUTION] Episode Summary:")
            for action_id, count in self.action_counts.items():
                pct = (count / self.total_actions) * 100
                print(
                    f"  {action_names[action_id]:12s}: {count:4d}/{self.total_actions} ({pct:5.1f}%)"
                )
            print()

        self.prev_metrics = {}
        self.episode_step = 0
        self.phase_duration = {}

        self.total_headway_violations = 0
        self.total_distance_violations = 0

        self.action_counts = {0: 0, 1: 0, 2: 0}
        self.total_actions = 0

        self.recent_phases = []

    def _collect_vehicle_metrics(self, traci):
        stopped_by_mode = {"car": 0, "bicycle": 0, "bus": 0}
        total_by_mode = {"car": 0, "bicycle": 0, "bus": 0}
        waiting_times_by_mode = {"car": [], "bicycle": [], "bus": []}
        total_co2 = 0.0

        for veh_id in traci.vehicle.getIDList():
            try:
                vtype = traci.vehicle.getTypeID(veh_id)
                speed = traci.vehicle.getSpeed(veh_id)
                wait_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
                co2 = traci.vehicle.getCO2Emission(veh_id)

                total_co2 += co2
                mode = get_vehicle_mode(vtype)

                total_by_mode[mode] += 1
                waiting_times_by_mode[mode].append(wait_time)

                if speed != -1 and speed < 0.1:
                    stopped_by_mode[mode] += 1
            except:  # noqa: E722
                continue

        return stopped_by_mode, total_by_mode, waiting_times_by_mode, total_co2

    def _collect_pedestrian_metrics(self, traci):
        stopped_count = 0
        total_count = 0
        waiting_times = []

        try:
            for ped_id in traci.person.getIDList():
                try:
                    wait_time = traci.person.getWaitingTime(ped_id)
                    speed = traci.person.getSpeed(ped_id)

                    total_count += 1
                    waiting_times.append(wait_time)

                    if speed != -1 and speed < 0.1:
                        stopped_count += 1
                except:  # noqa: E722
                    continue
        except:  # noqa: E722
            pass

        return stopped_count, total_count, waiting_times

    def _collect_all_metrics(self, traci):
        stopped_by_mode, total_by_mode, waiting_times_by_mode, total_co2 = (
            self._collect_vehicle_metrics(traci)
        )

        (
            stopped_by_mode["pedestrian"],
            total_by_mode["pedestrian"],
            waiting_times_by_mode["pedestrian"],
        ) = self._collect_pedestrian_metrics(traci)

        return (
            stopped_by_mode,
            total_by_mode,
            waiting_times_by_mode,
            total_co2 / 1_000_000.0,
        )

    def _calculate_excessive_wait_penalty(self, waiting_times_by_mode):
        car_wait_list = waiting_times_by_mode.get("car", [])
        bike_wait_list = waiting_times_by_mode.get("bicycle", [])

        car_wait = sum(car_wait_list) / len(car_wait_list) if car_wait_list else 0
        bike_wait = sum(bike_wait_list) / len(bike_wait_list) if bike_wait_list else 0

        excessive_penalty = 0

        if car_wait > 30:
            excessive_penalty += -1.5 * ((car_wait - 30) / 30)
        if car_wait > 40:
            excessive_penalty += -2.0 * ((car_wait - 40) / 40) ** 2

        if bike_wait > 25:
            excessive_penalty += -0.75 * ((bike_wait - 25) / 25)
        if bike_wait > 35:
            excessive_penalty += -2.0 * ((bike_wait - 35) / 35) ** 2

        return excessive_penalty

    def _calculate_waiting_component(self, waiting_times_by_mode, normalized_wait):
        base_wait_penalty = -DRLConfig.ALPHA_WAIT * normalized_wait
        excessive_penalty = self._calculate_excessive_wait_penalty(
            waiting_times_by_mode
        )

        return base_wait_penalty + excessive_penalty

    def _calculate_flow_component(self, normalized_wait):
        return (1.0 - normalized_wait) * 0.5

    def _calculate_co2_component(self, total_by_mode, total_co2_kg):
        weights = {
            "car": DRLConfig.WEIGHT_CAR,
            "bicycle": DRLConfig.WEIGHT_BICYCLE,
            "bus": DRLConfig.WEIGHT_BUS,
            "pedestrian": DRLConfig.WEIGHT_PEDESTRIAN,
        }

        weighted_total = sum(total_by_mode[m] * weights[m] for m in total_by_mode)

        co2_per_vehicle_kg = 0.0

        if weighted_total > 0:
            co2_per_vehicle_kg = total_co2_kg / weighted_total
            co2_reward = -DRLConfig.ALPHA_EMISSION * co2_per_vehicle_kg
        else:
            co2_reward = 0.0

        return co2_reward

    def _calculate_equity_component(self, waiting_times_by_mode):
        equity_penalty = self._calculate_equity_penalty(waiting_times_by_mode)
        equity_reward = -DRLConfig.ALPHA_EQUITY * equity_penalty
        return equity_reward, equity_penalty

    def _calculate_safety_component(
        self, traci, tls_ids, current_phases, phase_durations
    ):
        # TODO: Use number of safety violations as a metrics for reward calculation
        safety_violation = self._check_safety_violations(
            traci, tls_ids, current_phases, phase_durations
        )
        safety_reward = -DRLConfig.ALPHA_SAFETY if safety_violation else 0.0
        return safety_reward, safety_violation

    def _calculate_diversity_component(self, action, blocked_penalty):
        diversity_reward = 0.0

        if action in [1, 2] and blocked_penalty == 0:
            diversity_reward += 0.2

        if action is not None:
            self.action_counts[action] += 1
            self.total_actions += 1

            expected_freq = self.total_actions / 3.0
            actual_freq = self.action_counts[action]

            if self.total_actions > 30:
                if actual_freq >= expected_freq * 1.5:
                    overuse_ratio = (actual_freq - expected_freq) / expected_freq
                    diversity_reward -= min(0.05 * overuse_ratio, 0.2)

                    if self.episode_step % 200 == 0 and overuse_ratio > 0.5:
                        print(
                            f"[DIVERSITY WARNING] Step {self.episode_step}: {action_names.get(action, action)} overused "
                            f"({actual_freq}/{self.total_actions} = {actual_freq / self.total_actions * 100:.1f}%, "
                            f"expected 33.33%, penalty: {diversity_reward:.3f})"
                        )

                elif actual_freq <= expected_freq * 0.5:
                    underuse_ratio = (expected_freq - actual_freq) / expected_freq
                    diversity_reward += min(0.05 * underuse_ratio, 0.1)

                    if self.episode_step % 200 == 0 and underuse_ratio > 0.5:
                        print(
                            f"[DIVERSITY BONUS] Action {action_names.get(action, action)} underused "
                            f"({actual_freq:.0f} vs {expected_freq:.0f} expected), bonus: +{diversity_reward:.2f}"
                        )

        return diversity_reward

    def _calculate_consecutive_continue_component(
        self, action, tls_ids, current_phases
    ):
        consecutive_penalty = 0.0

        if not hasattr(self, "continue_streak"):
            self.continue_streak = {tls_id: 0 for tls_id in tls_ids}

        if action == 0:
            for tls_id in tls_ids:
                self.continue_streak[tls_id] += 1

                phase = current_phases.get(tls_id, 1)
                threshold = self.get_threshold(
                    DRLConfig.max_green_time.get(phase, 44),
                    DRLConfig.CONSECUTIVE_CONTINUE_THRESHOLD_RATIO,
                )

                if self.continue_streak[tls_id] >= threshold:
                    penalty = -(self.continue_streak[tls_id] - (threshold - 1)) * 0.1
                    consecutive_penalty += penalty

                    if (
                        self.continue_streak[tls_id] % 20 == 0
                        or self.continue_streak[tls_id] == threshold
                    ):
                        print(
                            f"[CONTINUE SPAM] TLS {tls_id} Phase {phase}: {self.continue_streak[tls_id]} consecutive Continue "
                            f"(threshold: {threshold}), penalty: {penalty:.2f}"
                        )
        else:
            for tls_id in tls_ids:
                self.continue_streak[tls_id] = 0

        return consecutive_penalty

    def _calculate_excessive_continue_component(
        self, stuck_durations, current_phases, tls_ids
    ):
        excessive_penalty = 0.0

        if stuck_durations:
            for tls_id in tls_ids:
                if tls_id not in stuck_durations:
                    continue

                duration = stuck_durations[tls_id]
                phase = current_phases.get(tls_id, 1)

                threshold = self.get_threshold(
                    DRLConfig.max_green_time.get(phase, 44),
                    DRLConfig.STUCK_PENALTY_THRESHOLD_RATIO,
                )

                if duration > threshold:
                    penalty = -(duration - threshold) * DRLConfig.STUCK_PENALTY_RATE
                    excessive_penalty += penalty

                    if duration % 20 == 0 or duration == (threshold + 1):
                        print(
                            f"[STUCK WARNING] TLS {tls_id} Phase {phase}: {duration}s without phase change "
                            f"(threshold: {threshold}s), penalty: {penalty:.2f}"
                        )

        return excessive_penalty

    def _calculate_bus_assistance_bonus(
        self, tls_ids, action, blocked_penalty, bus_waiting_data
    ):
        """
        Reward successful Skip2P1 actions that help waiting buses.

        Provides positive reinforcement when agent uses Skip2P1 to prioritize
        buses on major roads (Phase 1).

        Args:
            tls_ids: List of traffic light IDs
            action: Action taken (0=Continue, 1=Skip2P1, 2=Next)
            blocked_penalty: Penalty from blocked action (0 if not blocked)
            bus_waiting_data: Dict mapping tls_id to bus waiting time in seconds

        Returns:
            float: Bonus reward (0 or +0.3)
        """
        if action != 1 or blocked_penalty < 0:
            return 0.0

        if not bus_waiting_data:
            return 0.0

        for tls_id in tls_ids:
            avg_wait = bus_waiting_data.get(tls_id, 0.0)
            if avg_wait > 9.0:
                if self.episode_step % 100 == 0:
                    print(
                        f"[BUS ASSIST BONUS] TLS {tls_id}: Skip2P1 helped bus waiting {avg_wait:.1f}s, bonus: +0.3 🚌✨"
                    )
                return 0.3

        return 0.0

    def calculate_reward(
        self,
        traci,
        tls_ids,
        action,
        current_phases,
        phase_durations=None,
        blocked_penalty=0.0,
        stuck_durations=None,
        bus_waiting_data=None,
    ):
        self.episode_step += 1

        reward_components = {}

        stopped_by_mode, total_by_mode, waiting_times_by_mode, total_co2_kg = (
            self._collect_all_metrics(traci)
        )
        normalized_wait = self._calculate_weighted_waiting(waiting_times_by_mode)

        reward_components["flow"] = self._calculate_flow_component(normalized_wait)
        reward_components["waiting"] = self._calculate_waiting_component(
            waiting_times_by_mode, normalized_wait
        )
        reward_components["blocked"] = blocked_penalty

        reward_components["co2"] = self._calculate_co2_component(
            total_by_mode, total_co2_kg
        )
        reward_components["equity"], equity_penalty = self._calculate_equity_component(
            waiting_times_by_mode
        )
        reward_components["safety"], safety_violation = (
            self._calculate_safety_component(
                traci, tls_ids, current_phases, phase_durations
            )
        )
        reward_components["diversity"] = self._calculate_diversity_component(
            action, blocked_penalty
        )
        reward_components["consecutive_continue"] = (
            self._calculate_consecutive_continue_component(
                action, tls_ids, current_phases
            )
        )
        reward_components["excessive_continue"] = (
            self._calculate_excessive_continue_component(
                stuck_durations, current_phases, tls_ids
            )
        )
        reward_components["bus_assistance"] = self._calculate_bus_assistance_bonus(
            tls_ids, action, blocked_penalty, bus_waiting_data
        )

        reward = sum(reward_components.values())
        reward_before_clip = reward

        reward = np.clip(reward, -10.0, 10.0)

        avg_waiting_by_mode = {
            "car": np.mean(waiting_times_by_mode["car"])
            if waiting_times_by_mode["car"]
            else 0,
            "bicycle": (
                np.mean(waiting_times_by_mode["bicycle"])
                if waiting_times_by_mode["bicycle"]
                else 0
            ),
            "bus": np.mean(waiting_times_by_mode["bus"])
            if waiting_times_by_mode["bus"]
            else 0,
            "pedestrian": (
                np.mean(waiting_times_by_mode["pedestrian"])
                if waiting_times_by_mode["pedestrian"]
                else 0
            ),
        }

        if safety_violation:
            event_type = "safety_violation"
        else:
            event_type = "normal"

        info = {
            "stopped_by_mode": stopped_by_mode,
            "total_by_mode": total_by_mode,
            "waiting_time": normalized_wait * 60.0,
            "waiting_time_car": avg_waiting_by_mode["car"],
            "waiting_time_bicycle": avg_waiting_by_mode["bicycle"],
            "waiting_time_bus": avg_waiting_by_mode["bus"],
            "waiting_time_pedestrian": avg_waiting_by_mode["pedestrian"],
            "co2_total_kg": total_co2_kg,
            "equity_penalty": equity_penalty,
            "event_type": event_type,
            "reward_waiting": reward_components["waiting"],
            "reward_flow": reward_components["flow"],
            "reward_co2": reward_components["co2"],
            "reward_equity": reward_components["equity"],
            "reward_safety": reward_components["safety"],
            "reward_blocked": reward_components["blocked"],
            "reward_diversity": reward_components["diversity"],
            "reward_excessive_continue": reward_components["excessive_continue"],
            "reward_consecutive_continue": reward_components["consecutive_continue"],
            "reward_bus_assistance": reward_components["bus_assistance"],
            "reward_before_clip": reward_before_clip,
            "reward_clipped": reward,
            "reward_components_sum": sum(reward_components.values()),
            "normalized_wait": normalized_wait,
        }

        return reward, info

    def _get_instantaneous_waiting_times(self, traci):
        waiting_times = {"car": [], "bicycle": [], "pedestrian": [], "bus": []}

        for veh_id in traci.vehicle.getIDList():
            try:
                vtype = traci.vehicle.getTypeID(veh_id)

                wait_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
                speed = traci.vehicle.getSpeed(veh_id)

                if speed < 0.1:
                    if "Volkswagen" in vtype or "passenger" in vtype.lower():
                        waiting_times["car"].append(wait_time)
                    elif "Raleigh" in vtype or "bicycle" in vtype.lower():
                        waiting_times["bicycle"].append(wait_time)
                    elif "bus" in vtype.lower():
                        waiting_times["bus"].append(wait_time)
            except:  # noqa: E722
                continue

        for mode in waiting_times:
            if waiting_times[mode]:
                waiting_times[mode] = np.mean(waiting_times[mode])
            else:
                waiting_times[mode] = 0.0

        return waiting_times

    def _calculate_weighted_waiting(self, waiting_times_by_mode):
        weighted_sum = 0.0
        weighted_count = 0.0

        weights = {
            "car": DRLConfig.WEIGHT_CAR,
            "bicycle": DRLConfig.WEIGHT_BICYCLE,
            "pedestrian": DRLConfig.WEIGHT_PEDESTRIAN,
            "bus": DRLConfig.WEIGHT_BUS,
        }

        for mode, times in waiting_times_by_mode.items():
            if times:
                avg_wait = np.mean(times)
                count = len(times)
                weight = weights[mode]

                weighted_sum += weight * avg_wait * count
                weighted_count += weight * count

        weighted_wait = weighted_sum / weighted_count if weighted_count > 0 else 0.0
        return self._normalize_wait(weighted_wait)

    def _normalize_wait(self, weighted_wait):
        return min(weighted_wait / 60.0, 1.0)

    def _calculate_equity_penalty(self, waiting_times_by_mode):
        avg_waits = []
        for mode in ["car", "bicycle"]:
            if waiting_times_by_mode[mode]:
                avg_waits.append(np.mean(waiting_times_by_mode[mode]))

        if len(avg_waits) < 2:
            return 0.0

        mean_wait = np.mean(avg_waits)
        std_wait = np.std(avg_waits)

        if mean_wait < 0.1:
            return 0.0

        cv = std_wait / mean_wait

        equity_penalty = min(cv, 1.0)

        return equity_penalty

    def _check_vehicle_pair_safety(self, traci, lead_vehicle_id, follow_vehicle_id):
        lead_position = traci.vehicle.getLanePosition(lead_vehicle_id)
        follow_position = traci.vehicle.getLanePosition(follow_vehicle_id)
        follow_speed = traci.vehicle.getSpeed(follow_vehicle_id)

        distance_between = abs(lead_position - follow_position)
        time_headway = distance_between / follow_speed if follow_speed > 0.1 else 999.0

        has_headway_violation = time_headway < SAFE_HEADWAY and follow_speed > 8.0
        has_distance_violation = (
            distance_between < COLLISION_DISTANCE and follow_speed > 1.0
        )

        return (
            has_headway_violation,
            has_distance_violation,
            time_headway,
            distance_between,
            follow_speed,
        )

    def _check_near_collision_violations(self, traci, tls_ids):
        headway_violations = 0
        distance_violations = 0

        for tls_id in tls_ids:
            try:
                controlled_links = traci.trafficlight.getControlledLinks(tls_id)

                for link_group in controlled_links:
                    for link_tuple in link_group:
                        # [0] is Lane before intersection where vehicles approach
                        # We're checking for collision risk BEFORE vehicles enter
                        # the intersection, so we need to check vehicles for [0]
                        incoming_lane_id = link_tuple[0]
                        vehicle_ids = traci.lane.getLastStepVehicleIDs(incoming_lane_id)

                        if len(vehicle_ids) < 2:
                            continue

                        for idx in range(len(vehicle_ids) - 1):
                            try:
                                lead_veh = vehicle_ids[idx]
                                follow_veh = vehicle_ids[idx + 1]

                                (
                                    has_headway_violation,
                                    has_distance_violation,
                                    time_headway,
                                    distance,
                                    speed,
                                ) = self._check_vehicle_pair_safety(
                                    traci, lead_veh, follow_veh
                                )

                                if has_headway_violation:
                                    headway_violations += 1
                                    self.total_headway_violations += 1
                                    if headway_violations <= 3:
                                        print(
                                            f"[SAFETY-DEBUG] Headway: {time_headway:.2f}s < {SAFE_HEADWAY}s (FAST: speed={speed:.1f}m/s, dist={distance:.1f}m)"
                                        )
                                    return True, headway_violations, distance_violations

                                if has_distance_violation:
                                    distance_violations += 1
                                    self.total_distance_violations += 1
                                    if distance_violations <= 3:
                                        print(
                                            f"[SAFETY-DEBUG] Distance: {distance:.1f}m < {COLLISION_DISTANCE}m (MOVING: speed={speed:.1f}m/s)"
                                        )
                                    return True, headway_violations, distance_violations

                            except:  # noqa: E722
                                continue
            except:  # noqa: E722
                continue

        return False, headway_violations, distance_violations

    def _check_safety_violations(
        self, traci, tls_ids, current_phases, phase_durations=None
    ):
        has_collision_violation, headway_violations, distance_violations = (
            self._check_near_collision_violations(traci, tls_ids)
        )
        if has_collision_violation:
            return True

        if self.episode_step % 100 == 0 and self.episode_step > 0:
            print(f"\n[SAFETY SUMMARY] Step {self.episode_step}:")
            print(
                f"  Headway violations: {headway_violations} (FAST vehicles only: speed > 8.0 m/s)"
            )
            print(
                f"  Distance violations: {distance_violations} (MOVING only: speed > 1.0 m/s)"
            )
            print(
                f"  Episode totals - Headway: {self.total_headway_violations}, Distance: {self.total_distance_violations}\n"
            )

        return False

    def get_threshold(self, max_green_for_current_phase, ratio):
        return int(max_green_for_current_phase * ratio)

    def print_safety_summary(self):
        total_violations = (
            self.total_headway_violations + self.total_distance_violations
        )

        print(f"\n{'=' * 80}")
        print("[FINAL SAFETY SUMMARY] Episode Complete")
        print(f"{'=' * 80}")
        print(f"  Total Headway Violations:    {self.total_headway_violations}")
        print(f"  Total Distance Violations:   {self.total_distance_violations}")
        print(f"  {'─' * 76}")
        print(f"  TOTAL SAFETY VIOLATIONS:     {total_violations}")

        if self.episode_step > 0:
            violation_rate = (total_violations / self.episode_step) * 100
            print(f"  Violation Rate:              {violation_rate:.2f}% of steps")

        print(f"{'=' * 80}\n")
