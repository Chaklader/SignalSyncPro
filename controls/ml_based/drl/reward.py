import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.ml_based.drl.config import DRLConfig
from common.utils import get_vehicle_mode
from constants.constants import SAFE_HEADWAY, COLLISION_DISTANCE


class RewardCalculator:
    def __init__(self):
        self.prev_metrics = {}
        self.episode_step = 0
        self.phase_duration = {}

        self.total_headway_violations = 0
        self.total_distance_violations = 0

        self.action_counts = {0: 0, 1: 0, 2: 0, 3: 0}
        self.total_actions = 0

    def reset(self):
        if self.total_actions > 0:
            action_names = {0: "Continue", 1: "Skip2P1", 2: "Next", 3: "Pedestrian"}
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

        self.action_counts = {0: 0, 1: 0, 2: 0, 3: 0}
        self.total_actions = 0

        self.recent_phases = []

    def calculate_reward(
        self,
        traci,
        tls_ids,
        action,
        current_phases,
        phase_durations=None,
        blocked_penalty=0.0,
        stuck_durations=None,
    ):
        self.episode_step += 1

        stopped_by_mode = {"car": 0, "bicycle": 0, "bus": 0, "pedestrian": 0}
        total_by_mode = {"car": 0, "bicycle": 0, "bus": 0, "pedestrian": 0}
        waiting_times_by_mode = {"car": [], "bicycle": [], "bus": [], "pedestrian": []}

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

        try:
            for ped_id in traci.person.getIDList():
                try:
                    wait_time = traci.person.getWaitingTime(ped_id)
                    speed = traci.person.getSpeed(ped_id)

                    total_by_mode["pedestrian"] += 1
                    waiting_times_by_mode["pedestrian"].append(wait_time)

                    if speed != -1 and speed < 0.1:
                        stopped_by_mode["pedestrian"] += 1
                except:  # noqa: E722
                    continue
        except:  # noqa: E722
            pass

        weighted_wait = self._calculate_weighted_waiting(waiting_times_by_mode)

        normalized_wait = min(weighted_wait / 60.0, 1.0)

        reward_components = {}

        base_wait_penalty = -DRLConfig.ALPHA_WAIT * normalized_wait

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

        reward_components["waiting"] = base_wait_penalty + excessive_penalty

        reward_components["flow"] = (1.0 - normalized_wait) * 0.5

        phase_list = list(current_phases.values())
        both_phase_1 = len(phase_list) >= 2 and all(p in [0, 1] for p in phase_list)

        weights = {
            "car": DRLConfig.WEIGHT_CAR,
            "bicycle": DRLConfig.WEIGHT_BICYCLE,
            "bus": DRLConfig.WEIGHT_BUS,
            "pedestrian": DRLConfig.WEIGHT_PEDESTRIAN,
        }

        weighted_total = sum(total_by_mode[m] * weights[m] for m in total_by_mode)
        co2_per_vehicle = 0.0

        if weighted_total > 0:
            co2_per_vehicle = total_co2 / weighted_total / 1000.0
            reward_components["co2"] = -DRLConfig.ALPHA_EMISSION * co2_per_vehicle
        else:
            reward_components["co2"] = 0.0

        equity_penalty = self._calculate_equity_penalty(waiting_times_by_mode)
        reward_components["equity"] = -DRLConfig.ALPHA_EQUITY * equity_penalty

        safety_violation = self._check_safety_violations(
            traci, tls_ids, current_phases, phase_durations
        )
        reward_components["safety"] = (
            -DRLConfig.ALPHA_SAFETY if safety_violation else 0.0
        )

        reward_components["blocked"] = blocked_penalty

        reward_components["diversity"] = 0.0
        if action is not None:
            self.action_counts[action] += 1
            self.total_actions += 1

            expected_freq = self.total_actions / 4.0
            actual_freq = self.action_counts[action]

            if actual_freq > expected_freq * 1.5:
                overuse_ratio = (actual_freq - expected_freq) / expected_freq
                reward_components["diversity"] = -0.25 * overuse_ratio
                if self.episode_step % 100 == 0 and overuse_ratio > 0.3:
                    action_names = {
                        0: "Continue",
                        1: "Skip2P1",
                        2: "Next",
                        3: "Pedestrian",
                    }
                    print(
                        f"[DIVERSITY WARNING] Step {self.episode_step}: {action_names.get(action, action)} overused "
                        f"({actual_freq}/{self.total_actions} = {actual_freq / self.total_actions * 100:.1f}%, "
                        f"expected 25%, penalty: {reward_components['diversity']:.3f})"
                    )
            elif actual_freq < expected_freq * 0.5 and self.total_actions > 20:
                underuse_ratio = (expected_freq - actual_freq) / expected_freq
                reward_components["diversity"] = +0.5 * underuse_ratio

                if underuse_ratio > 0.7:
                    action_names = {
                        0: "Continue",
                        1: "Skip2P1",
                        2: "Next",
                        3: "Pedestrian",
                    }
                    print(
                        f"[DIVERSITY BONUS] Action {action_names.get(action, action)} underused "
                        f"({actual_freq:.0f} vs {expected_freq:.0f} expected), bonus: +{0.5 * underuse_ratio:.2f}"
                    )

        ped_demand_high = self._pedestrian_demand_high(traci, tls_ids)
        ped_phase_active = any(p == 16 for p in current_phases.values())

        reward_components["pedestrian"] = 0.0
        reward_components["ped_activation"] = 0.0

        if action == 3:
            if self._pedestrian_demand_high(traci, tls_ids):
                reward_components["ped_activation"] = (
                    DRLConfig.PED_PHASE_ACTIVATION_BONUS
                )
                print(
                    f"[PED BONUS] Activated ped phase with demand: +{DRLConfig.PED_PHASE_ACTIVATION_BONUS:.2f}"
                )
            else:
                reward_components["ped_activation"] = 0.0
                print("[PED EXPLORATION] Activated ped phase with low demand: -0.5")
        else:
            if ped_demand_high and not ped_phase_active:
                reward_components["pedestrian"] = -DRLConfig.ALPHA_PED_DEMAND
            elif ped_phase_active and ped_demand_high:
                reward_components["pedestrian"] = DRLConfig.ALPHA_PED_DEMAND * 2.0
            elif ped_phase_active and not ped_demand_high:
                reward_components["pedestrian"] = -0.05
                if self.episode_step % 100 == 0:
                    print(
                        f"[PED WEAK SIGNAL] Step {self.episode_step}: Ped phase active without high demand (small penalty: -0.05)"
                    )
            else:
                reward_components["pedestrian"] = 0.0

        reward_components["consecutive_continue"] = 0.0

        if not hasattr(self, "continue_streak"):
            self.continue_streak = {tls_id: 0 for tls_id in tls_ids}

        if action == 0:
            for tls_id in tls_ids:
                self.continue_streak[tls_id] += 1

                if self.continue_streak[tls_id] >= 3:
                    penalty = -(2 ** (self.continue_streak[tls_id] - 3))
                    reward_components["consecutive_continue"] += penalty

                    if (
                        self.continue_streak[tls_id] % 5 == 0
                        or self.continue_streak[tls_id] == 3
                    ):
                        print(
                            f"[CONTINUE SPAM] TLS {tls_id}: {self.continue_streak[tls_id]} consecutive Continue, penalty: {penalty:.2f}"
                        )
        else:
            for tls_id in tls_ids:
                self.continue_streak[tls_id] = 0

        reward_components["excessive_continue"] = 0.0

        if stuck_durations:
            for tls_id, duration in stuck_durations.items():
                if duration > DRLConfig.EXCESSIVE_CONTINUE_THRESHOLD:
                    current_phase = current_phases.get(tls_id, 0)
                    max_green = DRLConfig.MAX_GREEN_TIME.get(current_phase, 44)

                    if duration > (max_green * 0.8):
                        reward_components["excessive_continue"] -= (
                            DRLConfig.EXCESSIVE_CONTINUE_PENALTY
                        )

                        if duration % 10 == 0:
                            print(
                                f"[EXCESSIVE CONTINUE] TLS {tls_id}: {duration}s stuck (>{max_green * 0.8:.1f}s = 80% of max), penalty: -{DRLConfig.EXCESSIVE_CONTINUE_PENALTY}"
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
        elif ped_phase_active:
            event_type = "pedestrian_phase"
        elif ped_demand_high and not ped_phase_active:
            event_type = "ped_demand_ignored"
        elif both_phase_1:
            event_type = "sync_success"
        elif action == 1:
            event_type = "sync_attempt"
        else:
            event_type = "normal"

        info = {
            "stopped_by_mode": stopped_by_mode,
            "total_by_mode": total_by_mode,
            "waiting_time": weighted_wait,
            "waiting_time_car": avg_waiting_by_mode["car"],
            "waiting_time_bicycle": avg_waiting_by_mode["bicycle"],
            "waiting_time_bus": avg_waiting_by_mode["bus"],
            "waiting_time_pedestrian": avg_waiting_by_mode["pedestrian"],
            "sync_achieved": both_phase_1,
            "co2_emission": total_co2 / 1000.0,
            "equity_penalty": equity_penalty,
            "safety_violation": safety_violation,
            "ped_demand_high": ped_demand_high,
            "ped_phase_active": ped_phase_active,
            "event_type": event_type,
            "reward_waiting": reward_components["waiting"],
            "reward_flow": reward_components["flow"],
            "reward_co2": reward_components["co2"],
            "reward_equity": reward_components["equity"],
            "reward_safety": reward_components["safety"],
            "reward_pedestrian": reward_components["pedestrian"],
            "reward_blocked": reward_components["blocked"],
            "reward_diversity": reward_components["diversity"],
            "reward_ped_activation": reward_components["ped_activation"],
            "reward_excessive_continue": reward_components["excessive_continue"],
            "reward_consecutive_continue": reward_components["consecutive_continue"],
            "reward_before_clip": reward_before_clip,
            "reward_clipped": reward,
            "reward_components_sum": sum(reward_components.values()),
            "normalized_wait": normalized_wait,
            "co2_per_vehicle": co2_per_vehicle,
            "weighted_total_vehicles": weighted_total,
        }

        if self.episode_step % 100 == 0 and self.episode_step > 0:
            print(f"\n[PEDESTRIAN DEBUG] Step {self.episode_step}:")
            print(f"  Total pedestrians: {total_by_mode['pedestrian']}")
            print(f"  Stopped pedestrians: {stopped_by_mode['pedestrian']}")
            if waiting_times_by_mode["pedestrian"]:
                print(
                    f"  Avg waiting time: {np.mean(waiting_times_by_mode['pedestrian']):.2f}s"
                )
            else:
                print("  Avg waiting time: 0.0s (no pedestrians)")

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

        return weighted_sum / weighted_count if weighted_count > 0 else 0.0

    def _check_sync_success(self, current_phases):
        phase_list = list(current_phases.values())
        if len(phase_list) >= 2:
            return all(phase in [0, 1] for phase in phase_list)
        return False

    def _count_waiting_pedestrians_per_intersection(self, traci, tls_ids):
        node3_edges = {"a_3", "6_3", "c_3", "d_3", "3_6", "3_a", "3_d", "3_c"}
        node6_edges = {"3_6", "b_6", "e_6", "f_6", "6_b", "6_3", "6_f", "6_e"}

        waiting_counts = {}

        try:
            ped_ids = traci.person.getIDList()

            for tls_id in tls_ids:
                waiting_count = 0

                if tls_id == "3":
                    relevant_edges = node3_edges
                elif tls_id == "6":
                    relevant_edges = node6_edges
                else:
                    continue

                for ped_id in ped_ids:
                    try:
                        wait_time = traci.person.getWaitingTime(ped_id)
                        if wait_time > 2.0:
                            edge = traci.person.getRoadID(ped_id)
                            if edge in relevant_edges:
                                waiting_count += 1
                    except:  # noqa: E722
                        continue

                waiting_counts[tls_id] = waiting_count

        except:  # noqa: E722
            pass

        return waiting_counts

    def _pedestrian_demand_high(self, traci, tls_ids):
        waiting_counts = self._count_waiting_pedestrians_per_intersection(
            traci, tls_ids
        )

        for tls_id, waiting_count in waiting_counts.items():
            if waiting_count >= 6:
                print(
                    f"[PED DEMAND] TLS {tls_id}: {waiting_count} pedestrians waiting (≥6 threshold) 🚶"
                )
                return True

        return False

    def _classify_event(
        self, action, sync_achieved, ped_phase_active, ped_demand_high=False
    ):
        if ped_demand_high and not ped_phase_active:
            return "ped_demand_ignored"
        elif ped_phase_active:
            return "pedestrian_phase"
        elif sync_achieved:
            return "sync_success"
        elif action == 1:
            return "sync_attempt"
        else:
            return "normal"

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

    def _check_near_collision_violations(self, traci, tls_ids):
        headway_violations = 0
        distance_violations = 0

        for tls_id in tls_ids:
            try:
                controlled_links = traci.trafficlight.getControlledLinks(tls_id)

                for link_list in controlled_links:
                    for link in link_list:
                        incoming_lane = link[0]
                        vehicle_ids = traci.lane.getLastStepVehicleIDs(incoming_lane)

                        if len(vehicle_ids) >= 2:
                            for i in range(len(vehicle_ids) - 1):
                                try:
                                    pos1 = traci.vehicle.getLanePosition(vehicle_ids[i])
                                    pos2 = traci.vehicle.getLanePosition(
                                        vehicle_ids[i + 1]
                                    )
                                    speed1 = traci.vehicle.getSpeed(vehicle_ids[i])

                                    distance = abs(pos1 - pos2)
                                    time_headway = (
                                        distance / speed1 if speed1 > 0.1 else 999
                                    )

                                    if time_headway < SAFE_HEADWAY:
                                        if speed1 > 8.0:
                                            headway_violations += 1
                                            self.total_headway_violations += 1
                                            if headway_violations <= 3:
                                                print(
                                                    f"[SAFETY-DEBUG] Headway: {time_headway:.2f}s < {SAFE_HEADWAY}s (FAST: speed={speed1:.1f}m/s, dist={distance:.1f}m)"
                                                )
                                            return (
                                                True,
                                                headway_violations,
                                                distance_violations,
                                            )

                                    if distance < COLLISION_DISTANCE:
                                        if speed1 > 1.0:
                                            distance_violations += 1
                                            self.total_distance_violations += 1
                                            if distance_violations <= 3:
                                                print(
                                                    f"[SAFETY-DEBUG] Distance: {distance:.1f}m < {COLLISION_DISTANCE}m (MOVING: speed={speed1:.1f}m/s)"
                                                )
                                            return (
                                                True,
                                                headway_violations,
                                                distance_violations,
                                            )
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
