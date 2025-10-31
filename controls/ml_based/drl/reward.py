import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.ml_based.drl.config import DRLConfig
from common.utils import get_vehicle_mode
from constants.constants import SAFE_HEADWAY, COLLISION_DISTANCE
from constants.developed.common.drl_tls_constants import (
    action_names,
    phase_names,
    is_main_green_phases,
    p1_main_green,
    p2_main_green,
    p3_main_green,
    p4_main_green,
)


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

    # TODO: remove the mode weights from CO2 calculation
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

    # TODO: Count Red light violations, normalized it and add to the safety metrics
    def _calculate_safety_component(
        self, traci, tls_ids, current_phases, phase_durations
    ):
        has_violation, headway_count, distance_count = self._check_safety_violations(
            traci, tls_ids, current_phases, phase_durations
        )
        total_violations = headway_count + distance_count
        safety_reward = (
            0.05
            if total_violations == 0
            else -DRLConfig.ALPHA_SAFETY
            * min(total_violations / DRLConfig.SAFETY_VIOLATION_THRESHOLD, 1.0)
        )

        return (
            safety_reward,
            has_violation,
            total_violations,
            headway_count,
            distance_count,
        )

    def _calculate_diversity_component(self, action, blocked_penalty, epsilon):
        # Track action counts
        if action in self.action_counts:
            self.action_counts[action] += 1
            self.total_actions += 1

        if self.total_actions <= 100:
            return 0.0

        diversity_reward = 0.0
        diversity_scale = 1.0 - epsilon

        expected_ratio = DRLConfig.expected_action_frequencies.get(action, 0)
        actual_ratio = self.action_counts.get(action, 0) / self.total_actions

        # Action 0: Continue
        if action == 0:
            if actual_ratio < expected_ratio * 0.8:
                underuse_ratio = (expected_ratio - actual_ratio) / expected_ratio
                diversity_reward += min(0.1 * underuse_ratio * diversity_scale, 0.05)

                if self.episode_step % 200 == 0:
                    print(
                        f"[CONTINUE UNDERUSED] {actual_ratio:.1%} vs {expected_ratio:.1%} expected, bonus: +{diversity_reward:.3f}"
                    )

        # Action 1: Skip2P1
        elif action == 1:
            if actual_ratio < expected_ratio:
                underuse_ratio = (expected_ratio - actual_ratio) / expected_ratio
                # Stronger bonus for underused Skip2P1
                diversity_reward += min(0.5 * underuse_ratio * diversity_scale, 0.25)
                if self.episode_step % 100 == 0:
                    print(
                        f"[SKIP2P1 UNDERUSED] {actual_ratio:.1%} vs {expected_ratio:.1%} expected, bonus: +{diversity_reward:.3f}"
                    )
            elif actual_ratio > expected_ratio * 3.0:  # More lenient threshold
                overuse_ratio = (actual_ratio - expected_ratio) / expected_ratio
                diversity_reward -= min(0.05 * overuse_ratio * diversity_scale, 0.02)

        # Action 2: Next
        elif action == 2:
            if actual_ratio > expected_ratio * 1.5:
                overuse_ratio = (actual_ratio - expected_ratio) / expected_ratio
                diversity_reward -= min(0.15 * overuse_ratio * diversity_scale, 0.1)

                if self.episode_step % 200 == 0 and actual_ratio > expected_ratio * 2.0:
                    print(
                        f"[ACTION {action} OVERUSED] {actual_ratio:.1%} vs {expected_ratio:.1%} expected, penalty: -{abs(diversity_reward):.3f}"
                    )

        skip_rate = self.action_counts[1] / max(self.total_actions, 1)

        if skip_rate > DRLConfig.SKIP2P1_MAX_RATE and self.total_actions > 100:
            skip_penalty = (
                -DRLConfig.ALPHA_SKIP_OVERUSE
                * (skip_rate - DRLConfig.SKIP2P1_MAX_RATE)
                / DRLConfig.SKIP2P1_MAX_RATE
                * diversity_scale
            )
            diversity_reward += skip_penalty

            if self.episode_step % 200 == 0:
                print(
                    f"[SKIP2P1 OVERUSE] Rate: {skip_rate * 100:.1f}% (max {DRLConfig.SKIP2P1_MAX_RATE * 100:.1f}%), "
                    f"penalty: {skip_penalty:.3f}"
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

                # min Green < stability threshold < next bonus threshold < consecutive continue threshold < max green
                threshold = DRLConfig.consecutive_continue_threshold.get(phase, 20)

                if self.continue_streak[tls_id] >= threshold:
                    penalty = -(self.continue_streak[tls_id] - (threshold - 1)) * 0.01
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

    def _calculate_bus_assistance_bonus(
        self, tls_ids, action, blocked_penalty, bus_waiting_data
    ):
        bonus = 0.0

        if bus_waiting_data:
            for tls_id in tls_ids:
                avg_wait = bus_waiting_data.get(tls_id, 0.0)

                if avg_wait > 20.0:
                    # Heavy penalty for very long bus waits
                    penalty = -0.2 * (avg_wait - 20.0) / 20.0
                    bonus += penalty
                    if self.episode_step % 100 == 0:
                        print(
                            f"[BUS PENALTY] TLS {tls_id}: Bus waiting {avg_wait:.1f}s > 20s, penalty: {penalty:.3f} 🚌❌"
                        )

                elif avg_wait < 5.0:
                    # Reward excellent bus service
                    good_bonus = 0.15
                    bonus += good_bonus
                    if self.episode_step % 200 == 0:
                        print(
                            f"[BUS EXCELLENT] TLS {tls_id}: Bus waiting {avg_wait:.1f}s < 5s, bonus: +{good_bonus:.2f} 🚌✅"
                        )

                elif action == 1 and blocked_penalty == 0.0:
                    # Skip2P1 bonus based on effectiveness
                    if avg_wait > 10.0:
                        skip_bonus = 0.3
                    elif avg_wait > 5.0:
                        skip_bonus = 0.2
                    else:
                        skip_bonus = 0.1

                    bonus += skip_bonus
                    if self.episode_step % 100 == 0:
                        print(
                            f"[SKIP2P1 BONUS] TLS {tls_id}: Skip helped bus (wait={avg_wait:.1f}s), bonus: +{skip_bonus:.2f} 🚌✨"
                        )

        return bonus

    def _calculate_exploration_bonus(self, action, action_counts, epsilon):
        if epsilon < 0.1:
            return 0.0

        total_actions = sum(action_counts.values())

        if total_actions < 100:
            return 0.0

        action_freq = action_counts[action] / total_actions
        expected_freq = DRLConfig.expected_action_frequencies.get(action, 0.333)

        if action_freq < expected_freq * 0.5:
            underuse_ratio = (expected_freq - action_freq) / expected_freq
            bonus = underuse_ratio * epsilon * 0.1

            if self.episode_step % 100 == 0:
                action_names = {0: "Continue", 1: "Skip2P1", 2: "Next"}
                print(
                    f"[EXPLORATION BONUS] {action_names[action]} used {action_freq:.1%} "
                    f"(expected {expected_freq:.1%}), ε={epsilon:.2f}, bonus: +{bonus:.3f}"
                )

            return bonus

        return 0.0

    def _calculate_skip2p1_effectiveness_bonus(
        self, action, current_phases, phase_durations
    ):
        """Reward successful Skip2P1 actions that improve traffic flow"""
        if action != 1:
            return 0.0

        bonus = 0.0

        for tls_id, phase in current_phases.items():
            if phase == p1_main_green or not is_main_green_phases(phase):
                continue

            duration = phase_durations.get(tls_id, 0)
            min_green = DRLConfig.phase_min_green_time.get(phase, 0)

            if phase == p2_main_green and duration >= min_green:
                bonus += 0.25
            elif phase == p3_main_green and duration >= min_green:
                bonus += 0.3
            elif phase == p4_main_green and duration >= min_green:
                bonus += 0.2

            if self.episode_step % 100 == 0 and bonus > 0:
                phase_name = phase_names.get(phase, f"P{phase}")
                print(
                    f"[SKIP2P1 EFFECTIVE] From {phase_name} after {duration}s, bonus: +{bonus:.2f}"
                )

        return bonus

    def _calculate_next_phase_bonus(self, action, phase_durations, current_phases):
        if action != 2 or not phase_durations:
            return 0.0

        for tls_id, phase in current_phases.items():
            if not is_main_green_phases(phase):
                continue

            duration = phase_durations.get(tls_id, 0)
            min_duration_for_next = DRLConfig.min_phase_durations_for_next_bonus[phase]

            consecutive_threshold = DRLConfig.consecutive_continue_threshold.get(
                phase, 20
            )

            if duration >= min_duration_for_next and duration < consecutive_threshold:
                bonus = DRLConfig.ALPHA_NEXT_BONUS

                max_green = DRLConfig.max_green_time.get(phase, 44)
                optimal_ratio = min(duration / (max_green * 0.5), 1.0)
                bonus *= 1.0 + optimal_ratio

                if self.episode_step % 100 == 0:
                    phase_name = phase_names.get(phase, f"P{phase}")
                    print(
                        f"[NEXT BONUS] Next from {phase_name} after {duration}s (min {min_duration_for_next}s), bonus: +{bonus:.3f}"
                    )
                return bonus

        return 0.0

    def _calculate_stability_bonus(self, action, phase_durations, current_phases):
        if action != 0 or not phase_durations:
            return 0.0

        bonus = 0.0

        for tls_id, phase in current_phases.items():
            if not is_main_green_phases(phase):
                continue

            duration = phase_durations.get(tls_id, 0)

            min_duration_for_stability = DRLConfig.min_phase_duration_for_stability.get(
                phase, 10
            )
            consecutive_threshold = DRLConfig.consecutive_continue_threshold.get(
                phase, 20
            )
            max_green = DRLConfig.max_green_time.get(phase, 44)

            if (
                duration >= min_duration_for_stability
                and duration < consecutive_threshold
            ):
                phase_bonus = DRLConfig.ALPHA_STABILITY
                duration_ratio = duration / max_green
                phase_bonus *= 1.0 + duration_ratio
                bonus += phase_bonus

                if self.episode_step % 100 == 0:
                    phase_name = phase_names.get(phase, f"P{phase}")
                    print(
                        f"[STABILITY BONUS] Continue in {phase_name} for {duration}s (min {min_duration_for_stability}s), bonus: +{phase_bonus:.3f}"
                    )

        return bonus

    def _calculate_early_change_penalty(self, action, phase_durations, current_phases):
        if action == 0 or not phase_durations:
            return 0.0

        penalty = 0.0

        for tls_id, phase in current_phases.items():
            if not is_main_green_phases(phase):
                continue

            duration = phase_durations.get(tls_id, 0)

            optimal_duration = DRLConfig.min_phase_durations_for_next_bonus.get(
                phase, 15
            )

            if duration < optimal_duration:
                shortfall_ratio = 1.0 - (duration / optimal_duration)
                penalty -= shortfall_ratio * 0.5

                if self.episode_step % 100 == 0 and shortfall_ratio > 0.3:
                    phase_name = phase_names.get(phase, f"P{phase}")
                    print(
                        f"[EARLY CHANGE] {phase_name} changed after {duration}s "
                        f"(optimal {optimal_duration}s), penalty: {penalty:.3f}"
                    )

        return penalty

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
        action_counts=None,
        epsilon=0.0,
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
        (
            reward_components["safety"],
            safety_violation,
            total_violations,
            headway_violations,
            distance_violations,
        ) = self._calculate_safety_component(
            traci, tls_ids, current_phases, phase_durations
        )

        reward_components["diversity"] = self._calculate_diversity_component(
            action, blocked_penalty, epsilon
        )

        reward_components["consecutive_continue"] = (
            self._calculate_consecutive_continue_component(
                action, tls_ids, current_phases
            )
        )

        reward_components["bus_assistance"] = self._calculate_bus_assistance_bonus(
            tls_ids, action, blocked_penalty, bus_waiting_data
        )

        reward_components["exploration"] = (
            self._calculate_exploration_bonus(action, action_counts, epsilon)
            if action_counts
            else 0.0
        )

        reward_components["next_bonus"] = self._calculate_next_phase_bonus(
            action, current_phases, phase_durations
        )

        reward_components["skip2p1_effectiveness"] = (
            self._calculate_skip2p1_effectiveness_bonus(
                action, current_phases, phase_durations
            )
        )

        reward_components["stability"] = self._calculate_stability_bonus(
            action, phase_durations, current_phases
        )

        reward_components["early_change_penalty"] = (
            self._calculate_early_change_penalty(
                action, phase_durations, current_phases
            )
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
            "safety_violation": safety_violation,
            "safety_violations_total": total_violations,
            "safety_violations_headway": headway_violations,
            "safety_violations_distance": distance_violations,
            "reward_waiting": reward_components["waiting"],
            "reward_flow": reward_components["flow"],
            "reward_co2": reward_components["co2"],
            "reward_equity": reward_components["equity"],
            "reward_safety": reward_components["safety"],
            "reward_blocked": reward_components["blocked"],
            "reward_diversity": reward_components["diversity"],
            "reward_consecutive_continue": reward_components["consecutive_continue"],
            "reward_bus_assistance": reward_components["bus_assistance"],
            "reward_exploration": reward_components["exploration"],
            "reward_next_bonus": reward_components["next_bonus"],
            "reward_skip2p1_effectiveness": reward_components["skip2p1_effectiveness"],
            "reward_stability": reward_components["stability"],
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

        avg_waiting_times = {}

        for mode in waiting_times:
            if waiting_times[mode]:
                avg_waiting_times[mode] = np.mean(waiting_times[mode])
            else:
                avg_waiting_times[mode] = 0.0

        return avg_waiting_times

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

        mean_wait = float(np.mean(avg_waits))
        std_wait = float(np.std(avg_waits))

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

    def _record_headway_violation(
        self, headway_violations, time_headway, speed, distance
    ):
        headway_violations += 1
        self.total_headway_violations += 1
        if headway_violations <= 3:
            print(
                f"[SAFETY-DEBUG] Headway: {time_headway:.2f}s < {SAFE_HEADWAY}s "
                f"(FAST: speed={speed:.1f}m/s, dist={distance:.1f}m)"
            )
        return headway_violations

    def _record_distance_violation(self, distance_violations, distance, speed):
        distance_violations += 1
        self.total_distance_violations += 1
        if distance_violations <= 3:
            print(
                f"[SAFETY-DEBUG] Distance: {distance:.1f}m < {COLLISION_DISTANCE}m "
                f"(MOVING: speed={speed:.1f}m/s)"
            )
        return distance_violations

    def _check_lane_vehicle_pairs(
        self, traci, vehicle_ids, headway_violations, distance_violations
    ):
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
                ) = self._check_vehicle_pair_safety(traci, lead_veh, follow_veh)

                if has_headway_violation:
                    headway_violations = self._record_headway_violation(
                        headway_violations, time_headway, speed, distance
                    )
                    return True, headway_violations, distance_violations

                if has_distance_violation:
                    distance_violations = self._record_distance_violation(
                        distance_violations, distance, speed
                    )
                    return True, headway_violations, distance_violations

            except:  # noqa: E722
                continue

        return False, headway_violations, distance_violations

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

                        has_violation, headway_violations, distance_violations = (
                            self._check_lane_vehicle_pairs(
                                traci,
                                vehicle_ids,
                                headway_violations,
                                distance_violations,
                            )
                        )

                        if has_violation:
                            return True, headway_violations, distance_violations
            except:  # noqa: E722
                continue

        return False, headway_violations, distance_violations

    def _check_safety_violations(
        self, traci, tls_ids, current_phases, phase_durations=None
    ):
        has_collision_violation, headway_violations, distance_violations = (
            self._check_near_collision_violations(traci, tls_ids)
        )

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

        return has_collision_violation, headway_violations, distance_violations

    def get_threshold(
        self, max_green_for_current_phase, ratio_dict_or_value, phase=None
    ):
        if isinstance(ratio_dict_or_value, dict) and phase is not None:
            ratio = ratio_dict_or_value.get(phase, 0.8)
        else:
            ratio = (
                ratio_dict_or_value
                if not isinstance(ratio_dict_or_value, dict)
                else 0.8
            )
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
