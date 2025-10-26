"""
Multi-Objective Reward Function for Deep Reinforcement Learning Traffic Control

This module implements the reward calculation system that provides feedback to the DRL
agent about traffic control performance. The reward balances multiple objectives including
efficiency (waiting time), equity (fairness across modes), and coordination (synchronization).

===================================================================================
REWARD FUNCTION PHILOSOPHY
===================================================================================

The reward function is the "objective function" the agent optimizes. It must:
    1. Be computable at every timestep (real-time feedback)
    2. Balance multiple competing objectives (efficiency, equity, safety)
    3. Provide meaningful learning signal (not too sparse, not too dense)
    4. Align with real-world traffic management goals
    5. Enable fair comparison with baseline systems

Key Design Principles:
    - Modal equity: Different road users weighted by priority
    - Instantaneous measurement: Current conditions, not cumulative
    - Normalized scale: Bounded rewards prevent training instability
    - Interpretable components: Each term has clear traffic meaning
    - Sparse bonuses: Special rewards for coordination achievements

===================================================================================
MATHEMATICAL FORMULATION
===================================================================================

1. PRIMARY REWARD COMPONENT: WEIGHTED STOPPED RATIO
----------------------------------------------------
The main reward is based on proportion of stopped vehicles, weighted by mode:

    weighted_stopped = Σ (stopped_count[mode] × weight[mode])
    weighted_total = Σ (total_count[mode] × weight[mode])

    stopped_ratio = weighted_stopped / weighted_total

    R_stopped = -stopped_ratio  ∈ [-1, 0]

Modal Weights (from config):
    W_car = 1.2        (baseline priority)
    W_bicycle = 1.0    (equal to cars)
    W_pedestrian = 1.0 (equal to cars)
    W_bus = 1.5        (highest - public transit priority)

Interpretation:
    - stopped_ratio = 0.0 → All vehicles moving → R_stopped = 0.0
    - stopped_ratio = 1.0 → All vehicles stopped → R_stopped = -1.0
    - stopped_ratio = 0.3 → 30% stopped → R_stopped = -0.3

Example Calculation:
    At intersection:
        Cars: 10 total, 3 stopped
        Bicycles: 5 total, 2 stopped
        Buses: 1 total, 1 stopped

    weighted_stopped = (3 × 1.2) + (2 × 1.0) + (1 × 1.5)
                     = 3.6 + 2.0 + 1.5 = 7.1

    weighted_total = (10 × 1.2) + (5 × 1.0) + (1 × 1.5)
                   = 12.0 + 5.0 + 1.5 = 18.5

    stopped_ratio = 7.1 / 18.5 = 0.384
    R_stopped = -0.384

2. FLOW BONUS: MOVEMENT REWARD
-------------------------------
Positive reinforcement for vehicles in motion:

    R_flow = (1 - stopped_ratio) × 0.5  ∈ [0, 0.5]

Interpretation:
    - All moving (stopped_ratio = 0): R_flow = 0.5
    - All stopped (stopped_ratio = 1): R_flow = 0.0
    - 30% stopped: R_flow = 0.7 × 0.5 = 0.35

Purpose:
    - Encourages maintaining traffic flow
    - Balances negative penalty with positive incentive
    - Amplifies difference between good and bad control

3. SYNCHRONIZATION BONUS
-------------------------
Special reward for achieving green wave coordination:

    R_sync = +0.15  if both intersections in Phase 1 simultaneously
    R_sync = 0.0    otherwise

Condition:
    both_in_phase_1 = (phase_3 ∈ {0,1}) AND (phase_6 ∈ {0,1})

Purpose:
    - Moderate incentive for coordination (ALPHA_SYNC=0.15)
    - Enables green wave progression
    - Matches thesis semi-synchronization objective
    - Does NOT dominate waiting time penalty (ALPHA_WAIT=6.0)
    - Sparse bonus (only when aligned)

Why Phase 1?
    - Major arterial through movement
    - Highest traffic volume
    - Green wave most beneficial here
    - Travel time: 22 seconds between intersections

4. TIERED EXCESSIVE WAITING PENALTIES
---------------------------------------
Additional penalties for extreme waiting times (CUMULATIVE):

Car Penalties:
    if car_wait > 30s:
        penalty += -1.5 × (car_wait - 30) / 30
    if car_wait > 40s:  # ADDITIONAL (cumulative!)
        penalty += -2.0 × ((car_wait - 40) / 40)²

Bicycle Penalties:
    if bike_wait > 25s:
        penalty += -0.75 × (bike_wait - 25) / 25
    if bike_wait > 35s:  # ADDITIONAL (cumulative!)
        penalty += -2.0 × ((bike_wait - 35) / 35)²

Purpose:
    - Strongly discourage extreme waiting times
    - Nuclear penalty (squared term) at 40s/35s thresholds
    - Faster learning: agent quickly learns 40s+ is very bad
    - Cumulative structure: both penalties apply if both thresholds exceeded

Example:
    Car wait = 50s:
        Base: -6.0 × (50/60) = -5.0
        Tier 1 (>30s): -1.5 × (20/30) = -1.0
        Tier 2 (>40s): -2.0 × (10/40)² = -0.125
        Total waiting penalty: -6.125

5. TOTAL REWARD FUNCTION
-------------------------
Combined reward with clipping:

    R_total = R_wait + R_excessive + R_flow + R_sync + R_co2 + R_equity + R_safety + R_ped
    R_total = clip(R_total, -10.0, 10.0)

Typical Range (with current config):
    Worst case:  R ≈ -8.0  (50s+ wait, violations, no sync)
    Poor:        R ≈ -3.0  (35s wait, some violations)
    Good:        R ≈ -0.5  (20s wait, minimal violations)
    Excellent:   R ≈ +0.2  (10s wait, synced, no violations)
    Best case:   R ≈ +0.5  (5s wait, synced, flowing)

Clipping to [-10, 10]:
    - Prevents extreme values from rare events
    - Ensures stable Q-value learning
    - Wider range than original [-2, 2] for clearer signals

===================================================================================
WAITING TIME MEASUREMENT
===================================================================================

Two Types of Waiting Time Tracked:

1. ACCUMULATED WAITING TIME (Cumulative)
    - SUMO built-in: traci.vehicle.getAccumulatedWaitingTime()
    - Total seconds vehicle has been stopped during entire trip
    - Used for: final episode statistics, comparison with thesis
    - NOT used for: immediate reward (would reward late trips!)

2. INSTANTANEOUS WAITING TIME (Current)
    - Only vehicles currently stopped (speed < 0.1 m/s)
    - Immediate feedback on current signal control
    - Used for: reward calculation
    - More responsive to agent actions

Why Instantaneous?
    Accumulated waiting time has lag problem:
        - Vehicle waits 60 sec, then departs
        - Agent gets same accumulated time for next 10 steps
        - Doesn't reflect current control quality

    Instantaneous captures current state:
        - Red light: many vehicles with waiting time
        - Green light: fewer vehicles with waiting time
        - Immediate feedback on signal timing decision

===================================================================================
MODAL PRIORITY WEIGHTS
===================================================================================

Different road users have different priorities in reward function:

Modal Weight Rationale:
    Cars (1.2):
        - Baseline priority
        - Largest traffic volume
        - Capacity considerations

    Bicycles (1.0):
        - Equal priority to cars
        - Vulnerable road users
        - Environmental benefits

    Pedestrians (1.0):
        - Equal priority to cars
        - Vulnerable road users
        - Safety critical
        - Dedicated phase available

    Buses (1.5):
        - HIGHEST priority
        - Public transit efficiency
        - Passenger capacity (30-50 people per bus)
        - Schedule reliability
        - Environmental benefits

Impact on Learning:
    - Agent learns to minimize bus delays
    - Balances car throughput with bicycle safety
    - Considers pedestrian demand for Phase 5 activation
    - Encourages multimodal optimization

Example Scenario:
    Option A: Clear 5 cars (5 × 1.2 = 6.0 weighted)
    Option B: Clear 1 bus (1 × 1.5 = 1.5 weighted) + 4 cars (4 × 1.2 = 4.8)
              = 6.3 weighted

    Agent learns: Option B is better (higher total weighted flow)

===================================================================================
EVENT CLASSIFICATION FOR PRIORITIZED EXPERIENCE REPLAY
===================================================================================

Events are classified to assign priority in replay buffer:

Event Types:
    'normal':              Regular traffic control decision
                          Priority: 1x (baseline)

    'sync_success':       Both intersections achieved Phase 1
                          Priority: 3x
                          Learn coordination patterns

    'sync_attempt':       Agent tried to skip to Phase 1 (Action 1)
                          Priority: 2x
                          Learn when synchronization is beneficial

    'pedestrian_phase':   Pedestrian phase activated (Action 3)
                          Priority: 5x
                          Learn pedestrian demand recognition

    'bus_conflict':       Bus present but delayed
                          Priority: 4x
                          Learn bus priority strategies

    'safety_violation':   Near-collision or safety issue
                          Priority: 10x
                          Critical to avoid

Classification Logic:
    if pedestrian_phase_active:
        event_type = 'pedestrian_phase'  # Highest priority for learning
    elif sync_achieved:
        event_type = 'sync_success'       # Learn successful coordination
    elif action == 1:
        event_type = 'sync_attempt'       # Learn when to coordinate
    else:
        event_type = 'normal'             # Routine decision

===================================================================================
COMPARISON WITH THESIS METRICS
===================================================================================

Thesis Evaluation Metrics (Testing Phase):
    - Average waiting time per mode (cars, bicycles, pedestrians, buses)
    - Weighted average waiting time
    - Total CO₂ emissions
    - Pedestrian phase usage frequency
    - Synchronization success rate

Reward Function Alignment:
    ✓ Waiting time: Core component of reward (ALPHA_WAIT = 6.0 - DOMINANT)
    ✓ Modal weighting: Same weights as thesis (1.3, 1.0, 1.0, 1.5)
    ✓ Synchronization: Explicit bonus (ALPHA_SYNC = 0.15 - balanced)
    ✓ CO₂: Enabled with small weight (ALPHA_EMISSION = 0.03)
    ✓ Equity: Enabled with small weight (ALPHA_EQUITY = 0.03)
    ✓ Safety: Important priority (ALPHA_SAFETY = 1.0)
    ✓ Pedestrian demand: Moderate weight (ALPHA_PED_DEMAND = 0.8)
    ✓ Tiered penalties: Excessive waiting at 30s/40s (cars), 25s/35s (bikes)

Simplification Rationale:
    - Start with core objective: minimize weighted waiting
    - Add synchronization for coordination learning
    - Simpler reward = faster initial learning
    - Can incrementally add complexity

===================================================================================
REWARD SHAPING CONSIDERATIONS
===================================================================================

Good Reward Properties:
    ✓ Markovian: Depends only on current state/action
    ✓ Bounded: Clipped to [-10, 10]
    ✓ Dense: Non-zero reward at every timestep
    ✓ Interpretable: Each component has clear meaning
    ✓ Differentiating: Distinguishes good from bad control
    ✓ Prioritized: Waiting time (6.0) >> Sync (0.15) prevents gaming

Potential Issues Addressed:
    ✗ Sparse rewards: Flow bonus ensures frequent positive feedback
    ✗ Delayed feedback: Instantaneous measurement, not cumulative
    ✗ Scale variance: Normalized ratios and clipping
    ✗ Mode imbalance: Explicit modal weighting
    ✗ Local optima: Sync bonus encourages global coordination

Reward Debugging:
    - Monitor reward distribution during training
    - Track component contributions (stopped, flow, sync)
    - Check modal balance (are buses being prioritized?)
    - Verify sync bonus triggers correctly
    - Ensure rewards stay within bounds

===================================================================================
"""

import numpy as np
import sys
import os

# Add parent directory to path for common imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controls.ml_based.drl.config import DRLConfig
from common.utils import get_vehicle_mode
from constants.constants import SAFE_HEADWAY, COLLISION_DISTANCE


class RewardCalculator:
    """
    Multi-Objective Reward Calculator for Traffic Signal Control

    Computes scalar reward signal for DRL agent based on current traffic conditions.
    Balances multiple objectives: efficiency (flow), equity (modal fairness), and
    coordination (synchronization between intersections).

    Reward Components:
        1. Stopped Ratio Penalty: -weighted_stopped_ratio ∈ [-1, 0]
           Penalizes proportion of stopped vehicles weighted by mode priority

        2. Flow Bonus: +(1 - stopped_ratio) × 0.5 ∈ [0, 0.5]
           Rewards vehicle movement and traffic flow

        3. Synchronization Bonus: +1.0 when both intersections in Phase 1
           Encourages green wave coordination

    Total Reward Range: [-2, 2] (clipped for stability)

    Modal Weights (Priority):
        - Cars: 1.2 (baseline)
        - Bicycles: 1.0 (equal priority)
        - Pedestrians: 1.0 (equal priority)
        - Buses: 1.5 (highest - public transit)

    Measurement Strategy:
        - Instantaneous: Current conditions only (not cumulative)
        - Per-timestep: Reward computed every simulation step
        - State-based: Reflects quality of current traffic state

    Event Classification:
        - Events tagged for Prioritized Experience Replay (PER)
        - High-priority: pedestrian phases, sync success, bus conflicts
        - Normal-priority: routine traffic control decisions

    Integration:
        - Called by TrafficManagement.step() every timestep
        - Returns (reward, info) tuple
        - Info dict contains detailed metrics for logging

    Usage:
        # Initialize
        reward_calc = RewardCalculator()

        # Compute reward
        reward, info = reward_calc.calculate_reward(
            traci, ['3', '6'], action, current_phases
        )

        print(f"Reward: {reward:.3f}")
        print(f"Stopped ratio: {info['weighted_stopped_ratio']:.3f}")
        print(f"Avg waiting time: {info['waiting_time']:.1f} sec")
        print(f"Sync achieved: {info['sync_achieved']}")

    Attributes:
        prev_metrics (dict): Previous timestep metrics (for delta calculation)
        episode_step (int): Current step count in episode
    """

    def __init__(self):
        """
        Initialize Reward Calculator.

        Sets up tracking variables for episode-level statistics and
        previous timestep comparisons.

        Attributes Initialized:
            prev_metrics (dict): Stores previous timestep measurements
                - Used for computing deltas (change in waiting time)
                - Currently empty (future feature for incremental rewards)

            episode_step (int): Counter for current episode timestep
                - Incremented in calculate_reward()
                - Used for episode statistics
                - Reset to 0 at episode start

            phase_duration (dict): Tracks phase duration for safety checks
                - Maps tls_id to seconds in current phase
                - Used to detect MIN_GREEN_TIME violations

        Example:
            reward_calc = RewardCalculator()
            # Ready to compute rewards

            # At episode start
            reward_calc.reset()
        """
        self.prev_metrics = {}
        self.episode_step = 0
        self.phase_duration = {}  # Track phase durations for safety checks

        # DEBUG: Safety violation tracking (near-collisions only)
        self.total_headway_violations = 0
        self.total_distance_violations = 0

        # Action diversity tracking (Phase 3 - Oct 23, 2025)
        self.action_counts = {0: 0, 1: 0, 2: 0, 3: 0}  # Count each action usage
        self.total_actions = 0

    def reset(self):
        """
        Reset calculator for new episode.

        Clears accumulated metrics and counters to prepare for new episode.
        Should be called by environment's reset() method.

        Resets:
            - prev_metrics: Clears stored previous measurements
            - episode_step: Resets timestep counter to 0
            - phase_duration: Clears phase duration tracking
            - action_counts: Resets action frequency tracking

        Example:
            # Start new training episode
            state = env.reset()
            reward_calc.reset()  # Clear previous episode data

            for step in range(3600):
                reward, info = reward_calc.calculate_reward(...)
                # Fresh metrics each episode
        """
        # Print action distribution summary before reset (Phase 4 - Oct 24, 2025)
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

        # DEBUG: Reset safety violation tracking (near-collisions only)
        self.total_headway_violations = 0
        self.total_distance_violations = 0

        # Reset action diversity tracking (Phase 3 - Oct 23, 2025)
        self.action_counts = {0: 0, 1: 0, 2: 0, 3: 0}
        self.total_actions = 0

        # Reset phase history tracking (Phase 4 - Oct 24, 2025)
        self.recent_phases = []

    def calculate_reward(
        self,
        traci,
        tls_ids,
        action,
        current_phases,
        phase_durations=None,
        blocked_penalty=0.0,
        stuck_durations=None,  # NEW: Time since last meaningful action
    ):
        """
        Calculate multi-objective reward for current timestep.

        PRIMARY METRIC: Weighted average waiting time (not stopped ratio)
        SECONDARY: CO₂ emissions, equity, safety, pedestrian demand
        BONUS: Synchronization achievement

        Core reward computation combining waiting time penalty, flow bonus,
        strong synchronization bonus, and secondary objectives. Returns detailed
        info dict with per-mode statistics for logging and analysis.

        Reward Calculation Steps:
            1. Count vehicles and collect metrics by mode (car, bicycle, bus, pedestrian)
            2. Calculate weighted average waiting time (PRIMARY METRIC)
            3. Normalize waiting time to [0, 1] range (assume max 60 seconds)
            4. Calculate base reward: -ALPHA_WAIT (6.0) × normalized_wait
            5. Add tiered excessive waiting penalties:
               - Cars: -1.5×(wait-30)/30 if >30s, PLUS -2.0×((wait-40)/40)² if >40s
               - Bikes: -0.75×(wait-25)/25 if >25s, PLUS -2.0×((wait-35)/35)² if >35s
            6. Add flow bonus: +(1 - normalized_wait) × 0.5
            7. Add sync bonus: +ALPHA_SYNC (0.15) if both in Phase 1
            8. Add small CO₂ emissions penalty: -ALPHA_EMISSION × co2_per_vehicle
            9. Add small equity penalty: -ALPHA_EQUITY × variance_across_modes
            10. Add safety penalty: -ALPHA_SAFETY (1.0) if violations
            11. Add pedestrian demand handling: penalty/bonus based on response
            12. Clip final reward to [-10, 10] (wider range for clearer signals)
            13. Classify event type for PER
            14. Return (reward, info)

        Modal Counting:
            For each vehicle in simulation:
                - Get vehicle type ID from SUMO
                - Classify using get_vehicle_mode() utility
                - Track total count per mode
                - Check if stopped (speed < 0.1 m/s)
                - Record accumulated waiting time
                - Track CO₂ emissions

        Weighted Average Waiting Time (PRIMARY METRIC):
            weighted_wait = Σ (mean_wait[mode] × weight[mode] × count[mode]) / Σ (weight[mode] × count[mode])
            normalized_wait = min(weighted_wait / 60.0, 1.0)

            This is more meaningful than stopped ratio for traffic control evaluation
            and matches thesis evaluation metrics.

        Synchronization Detection:
            - Both intersections must be in Phase 1 (indices 0 or 1)
            - Bonus only when simultaneously coordinated
            - Encourages green wave timing
            - Small bonus (0.15) encourages coordination without dominating waiting time penalty
            - Waiting time (ALPHA_WAIT=6.0) is THE dominant factor in reward structure

        Args:
            traci: SUMO TraCI connection object
                Used to query vehicle states, speeds, waiting times

            tls_ids (list of str): Traffic light IDs ['3', '6']
                Currently not directly used (future: per-intersection rewards)

            action (int): Action taken this timestep (0-3)
                Used for event classification (sync attempt detection)

            current_phases (dict): Current phase for each intersection
                Format: {'3': 0, '6': 1}
                Used for synchronization detection

        Returns:
            tuple: (reward, info)

            reward (float): Scalar reward signal
                Range: [-10.0, 10.0] (clipped) - wider range for clearer learning signals
                Typical: -2.0 to +3.5
                Worst case: -7.0 (safety violation + all penalties)
                Best case: +3.5 (low wait + sync + good flow)
                Negative: Poor performance (high waiting time)
                Positive: Good performance (low wait + coordinated)

            info (dict): Detailed metrics for logging
                Keys:
                    'stopped_by_mode': dict
                        {'car': int, 'bicycle': int, 'bus': int, 'pedestrian': int}
                        Count of stopped vehicles per mode

                    'total_by_mode': dict
                        Total vehicle count per mode

                    'waiting_time': float
                        PRIMARY METRIC: Weighted average waiting time (seconds)
                        This is the main evaluation metric matching thesis

                    'waiting_time_car': float
                        Average waiting time for cars (seconds)

                    'waiting_time_bicycle': float
                        Average waiting time for bicycles (seconds)

                    'waiting_time_bus': float
                        Average waiting time for buses (seconds)

                    'waiting_time_pedestrian': float
                        Average waiting time for pedestrians (seconds)

                    'sync_achieved': bool
                        True if both intersections in Phase 1

                    'co2_emission': float
                        Total CO₂ emissions (grams)

                    'equity_penalty': float
                        Variance in waiting times across modes

                    'safety_violation': bool
                        True if safety constraints violated

                    'ped_demand_high': bool
                        True if ≥10 pedestrians waiting

                    'ped_phase_active': bool
                        True if pedestrian phase active

                    'event_type': str
                        Event classification for PER:
                        'safety_violation', 'ped_demand_ignored', 'pedestrian_phase',
                        'sync_success', 'sync_attempt', 'normal'

        Example Usage:
            # During training step
            reward, info = reward_calc.calculate_reward(
                traci=traci,
                tls_ids=['3', '6'],
                action=1,  # Skip to Phase 1
                current_phases={'3': 1, '6': 0}
            )

            print(f"Reward: {reward:.3f}")
            # Output: Reward: 3.200
            # (Low waiting time + synchronization achieved)

            # Log detailed metrics
            logger.log({
                'reward': reward,
                'waiting_time': info['waiting_time'],  # PRIMARY METRIC
                'car_wait': info['waiting_time_car'],
                'bike_wait': info['waiting_time_bicycle'],
                'bus_wait': info['waiting_time_bus'],
                'sync': info['sync_achieved'],
                'co2': info['co2_emission'],
                'safety': info['safety_violation']
            })

        Reward Interpretation:
            reward = -2.0  → High waiting time (40+ sec avg), poor control
            reward = -0.5  → Moderate waiting time (20-30 sec), acceptable control
            reward = +1.0  → Low waiting time (10-15 sec), good flow
            reward = +3.2  → Low waiting time + synchronization achieved
            reward = -7.0  → Safety violation + high waiting time (CRITICAL)

        Performance Indicators (Waiting Time):
            waiting_time < 10 sec: Excellent flow
            waiting_time 10-20 sec: Good flow
            waiting_time 20-40 sec: Moderate congestion
            waiting_time > 40 sec: Severe congestion

        Notes:
            - Called every simulation step (1 second)
            - Uses instantaneous measurements (not cumulative)
            - Modal weights from DRLConfig
            - Sync bonus matches thesis semi-synchronization objective
            - Event classification enables PER prioritization
        """
        self.episode_step += 1

        # ========================================================================
        # STEP 1: Count vehicles and collect metrics by mode
        # ========================================================================
        stopped_by_mode = {"car": 0, "bicycle": 0, "bus": 0, "pedestrian": 0}
        total_by_mode = {"car": 0, "bicycle": 0, "bus": 0, "pedestrian": 0}
        waiting_times_by_mode = {"car": [], "bicycle": [], "bus": [], "pedestrian": []}

        total_co2 = 0.0

        # Track VEHICLES (cars, bicycles, buses)
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

                # Check if stopped (speed < 0.1 m/s, but not -1 which means no data)
                if speed != -1 and speed < 0.1:
                    stopped_by_mode[mode] += 1
            except:  # noqa: E722
                continue

        # ========================================================================
        # Track PEDESTRIANS (separate SUMO API)
        # ========================================================================
        # CRITICAL: Pedestrians are NOT in traci.vehicle.getIDList()!
        # They use traci.person.getIDList() - separate API
        try:
            for ped_id in traci.person.getIDList():
                try:
                    # Get pedestrian metrics
                    wait_time = traci.person.getWaitingTime(ped_id)
                    speed = traci.person.getSpeed(ped_id)

                    # Track pedestrian data
                    total_by_mode["pedestrian"] += 1
                    waiting_times_by_mode["pedestrian"].append(wait_time)

                    # Check if stopped (waiting)
                    if speed != -1 and speed < 0.1:
                        stopped_by_mode["pedestrian"] += 1
                except:  # noqa: E722
                    # Skip individual pedestrian if query fails
                    continue
        except:  # noqa: E722
            # If pedestrian API fails entirely, continue without pedestrian data
            pass

        # ========================================================================
        # STEP 2: Calculate weighted average waiting time (PRIMARY METRIC)
        # ========================================================================
        weighted_wait = self._calculate_weighted_waiting(waiting_times_by_mode)

        # Normalize to [0, 1] range (assume max reasonable waiting = 60 seconds)
        normalized_wait = min(weighted_wait / 60.0, 1.0)

        # ========================================================================
        # STEP 3: REWARD CALCULATION (REBALANCED) - WITH DETAILED COMPONENT TRACKING
        # ========================================================================

        # Initialize reward components dictionary for debugging
        reward_components = {}

        # Component 1: Waiting time penalty (ENHANCED WITH THRESHOLD PENALTY)
        base_wait_penalty = -DRLConfig.ALPHA_WAIT * normalized_wait

        # NEW: Additional penalty for excessive waiting (>30s for cars/bikes)
        car_wait_list = waiting_times_by_mode.get("car", [])
        bike_wait_list = waiting_times_by_mode.get("bicycle", [])
        car_wait = sum(car_wait_list) / len(car_wait_list) if car_wait_list else 0
        bike_wait = sum(bike_wait_list) / len(bike_wait_list) if bike_wait_list else 0

        excessive_penalty = 0

        # Car waiting penalties (tiered and cumulative)
        if car_wait > 30:  # Standard excessive penalty
            excessive_penalty += -1.5 * ((car_wait - 30) / 30)
        if car_wait > 40:
            excessive_penalty += -2.0 * ((car_wait - 40) / 40) ** 2

        # Bike waiting penalties (tiered and cumulative)
        if bike_wait > 25:
            excessive_penalty += -0.75 * ((bike_wait - 25) / 25)
        if bike_wait > 35:
            excessive_penalty += -2.0 * ((bike_wait - 35) / 35) ** 2

        reward_components["waiting"] = base_wait_penalty + excessive_penalty

        # Component 2: Flow bonus (simple, no gaming)
        # Flow bonus based purely on normalized waiting time
        reward_components["flow"] = (1.0 - normalized_wait) * 0.5

        # Check if both signals in Phase 1 (for info tracking, no reward)
        phase_list = list(current_phases.values())
        both_phase_1 = len(phase_list) >= 2 and all(p in [0, 1] for p in phase_list)

        # Component 4: CO₂ emissions penalty (small but present)
        weights = {
            "car": DRLConfig.WEIGHT_CAR,
            "bicycle": DRLConfig.WEIGHT_BICYCLE,
            "bus": DRLConfig.WEIGHT_BUS,
            "pedestrian": DRLConfig.WEIGHT_PEDESTRIAN,
        }

        weighted_total = sum(total_by_mode[m] * weights[m] for m in total_by_mode)
        co2_per_vehicle = 0.0

        if weighted_total > 0:
            co2_per_vehicle = total_co2 / weighted_total / 1000.0  # mg to g
            reward_components["co2"] = -DRLConfig.ALPHA_EMISSION * co2_per_vehicle
        else:
            reward_components["co2"] = 0.0

        # Component: Equity penalty (small but present)
        equity_penalty = self._calculate_equity_penalty(waiting_times_by_mode)
        reward_components["equity"] = -DRLConfig.ALPHA_EQUITY * equity_penalty

        # Component: Safety violations
        safety_violation = self._check_safety_violations(
            traci, tls_ids, current_phases, phase_durations
        )
        reward_components["safety"] = (
            -DRLConfig.ALPHA_SAFETY if safety_violation else 0.0
        )

        # Component: Blocked action penalty
        reward_components["blocked"] = blocked_penalty

        # Component: True Action Diversity
        # Penalize overuse of any single action, reward balanced action distribution
        reward_components["diversity"] = 0.0
        if action is not None:
            # Track action usage
            self.action_counts[action] += 1
            self.total_actions += 1

            expected_freq = self.total_actions / 4.0
            actual_freq = self.action_counts[action]

            if actual_freq > expected_freq * 1.5:
                overuse_ratio = (actual_freq - expected_freq) / expected_freq
                reward_components["diversity"] = -0.25 * overuse_ratio
                # Log every 100 steps when overuse detected (changed from % 50 for better visibility)
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

        # Component: Pedestrian demand handling 1) state based reward 2) action based reward
        ped_demand_high = self._pedestrian_demand_high(traci, tls_ids)
        ped_phase_active = any(p == 16 for p in current_phases.values())

        reward_components["pedestrian"] = 0.0
        reward_components["ped_activation"] = 0.0

        if action == 3:  # Pedestrian action selected
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
                if self.episode_step % 100 == 0:  # Log every 100 steps
                    print(
                        f"[PED WEAK SIGNAL] Step {self.episode_step}: Ped phase active without high demand (small penalty: -0.05)"
                    )
            else:
                reward_components["pedestrian"] = 0.0

        # Component: Consecutive Continue Penalty 1) consecutive continue 2) excessive continue
        # Prevents policy collapse by penalizing repeated Continue actions
        reward_components["consecutive_continue"] = 0.0

        # Initialize tracking if not exists
        if not hasattr(self, "continue_streak"):
            self.continue_streak = {tls_id: 0 for tls_id in tls_ids}

        if action == 0:  # Continue action
            for tls_id in tls_ids:
                self.continue_streak[tls_id] += 1

                # we only penalize if agent takes 3 consecutive Continue ACTIONS (not time-based).
                # EXPONENTIAL penalty: 3rd=-1.0, 4th=-2.0, 5th=-4.0, 6th=-8.0 (Phase 4 emergency fix)
                if self.continue_streak[tls_id] >= 3:
                    # Exponential: 2^(streak-3) for streak >= 3
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
            # Reset streak when agent chooses another action
            for tls_id in tls_ids:
                self.continue_streak[tls_id] = 0

        reward_components["excessive_continue"] = 0.0

        # stuck_durations tracks how long since the agent
        # took a non-Continue action (Actions 1, 2, or 3).
        # Agent can get stuck in any phase P1, P2, P3, P4.
        if stuck_durations:
            for tls_id, duration in stuck_durations.items():
                # duration is the stuck_duration is tracked per traffic light (per TLS ID).
                if duration > DRLConfig.EXCESSIVE_CONTINUE_THRESHOLD:
                    current_phase = current_phases.get(tls_id, 0)
                    max_green = DRLConfig.MAX_GREEN_TIME.get(current_phase, 44)

                    # Penalize if stuck beyond threshold AND approaching max_green (80%)
                    # Has the agent been stuck (spamming Continue) for more than 80% of
                    # the phase's maximum allowed time? So this can be P1, P2, P3, P4.
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

        # ========================================================================
        # STEP 4: Calculate detailed metrics for logging
        # ========================================================================
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

        # Event classification for PER
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
            # Original metrics
            "stopped_by_mode": stopped_by_mode,
            "total_by_mode": total_by_mode,
            "waiting_time": weighted_wait,  # PRIMARY METRIC
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
            # NEW: ALL reward components for complete tracking (Phase 4 - Oct 24, 2025)
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
            "reward_consecutive_continue": reward_components[
                "consecutive_continue"
            ],  # NEW: Phase 4 - Oct 24, 2025
            "reward_before_clip": reward_before_clip,
            "reward_clipped": reward,
            "reward_components_sum": sum(reward_components.values()),
            # Additional debugging info
            "normalized_wait": normalized_wait,
            "co2_per_vehicle": co2_per_vehicle,
            "weighted_total_vehicles": weighted_total,
        }

        # DEBUG: Print pedestrian stats every 100 steps (moved to end - Phase 4 Oct 24, 2025)
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
        """
        Get current waiting times for stopped vehicles only.

        Measures instantaneous waiting time (vehicles currently stopped) rather
        than accumulated waiting time (total wait during entire trip).

        Instantaneous vs Accumulated:
            Instantaneous:
                - Only counts currently stopped vehicles (speed < 0.1)
                - Immediate feedback on current signal control
                - Changes rapidly with signal phases
                - Better for reward signal (responsive to actions)

            Accumulated (SUMO default):
                - Total wait time since vehicle entered network
                - Includes past delays no longer relevant
                - Lags behind current control decisions
                - Better for final episode statistics

        Measurement Process:
            For each vehicle in simulation:
                1. Get vehicle type and classify mode
                2. Get current speed
                3. If speed < 0.1 m/s (effectively stopped):
                    - Record accumulated waiting time
                    - Add to mode-specific list
                4. Skip moving vehicles

        Args:
            traci: SUMO TraCI connection

        Returns:
            dict: Average waiting time per mode (seconds)
                Format: {
                    'car': float,
                    'bicycle': float,
                    'pedestrian': float,
                    'bus': float
                }

                Values are averages across stopped vehicles of that mode
                Zero if no stopped vehicles of that mode

        Example:
            waiting_times = self._get_instantaneous_waiting_times(traci)

            # At red light:
            # {'car': 15.3, 'bicycle': 8.2, 'pedestrian': 0.0, 'bus': 22.1}
            # Cars waiting 15.3 sec average, bus waiting longest

            # At green light:
            # {'car': 2.1, 'bicycle': 1.5, 'pedestrian': 0.0, 'bus': 0.0}
            # Only stragglers still stopping

        Vehicle Classification:
            Uses vehicle type ID string matching:
                - 'Volkswagen' or 'passenger' → car
                - 'Raleigh' or 'bicycle' → bicycle
                - 'bus' → bus
                - Pedestrians not detected via vehicle API

        Notes:
            - Only counts stopped vehicles (speed < 0.1 m/s)
            - Returns mean waiting time per mode
            - Empty lists default to 0.0 (no waiting)
            - More responsive than accumulated waiting time
            - Better reflects current signal control quality
        """
        waiting_times = {"car": [], "bicycle": [], "pedestrian": [], "bus": []}

        # Get all vehicles currently in simulation
        for veh_id in traci.vehicle.getIDList():
            try:
                vtype = traci.vehicle.getTypeID(veh_id)

                # Get CURRENT waiting time (seconds stopped)
                wait_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
                speed = traci.vehicle.getSpeed(veh_id)

                # Only count if currently stopped
                if speed < 0.1:
                    if "Volkswagen" in vtype or "passenger" in vtype.lower():
                        waiting_times["car"].append(wait_time)
                    elif "Raleigh" in vtype or "bicycle" in vtype.lower():
                        waiting_times["bicycle"].append(wait_time)
                    elif "bus" in vtype.lower():
                        waiting_times["bus"].append(wait_time)
            except:  # noqa: E722
                continue

        # Calculate AVERAGE for this timestep
        for mode in waiting_times:
            if waiting_times[mode]:
                waiting_times[mode] = np.mean(waiting_times[mode])
            else:
                waiting_times[mode] = 0.0

        return waiting_times

    def _calculate_weighted_waiting(self, waiting_times_by_mode):
        """
        Calculate weighted average waiting time across all modes.

        Applies modal priority weights to compute overall system performance
        metric that emphasizes high-priority modes (buses, cars).

        Formula:
            For each mode: avg_wait[mode] = mean(waiting_times[mode])
            weighted_avg = Σ (weight[mode] × avg_wait[mode] × count[mode]) / Σ (weight[mode] × count[mode])

        Where:
            weight[mode] = priority weight from config
            avg_wait[mode] = average waiting time for that mode
            count[mode] = number of vehicles in that mode

        Args:
            waiting_times_by_mode (dict): Lists of waiting times by mode (seconds)
                Format: {
                    'car': [10.0, 15.0, 8.0, ...],
                    'bicycle': [5.0, 7.0, ...],
                    'pedestrian': [0.0, ...],
                    'bus': [20.0, 25.0, ...]
                }

        Returns:
            float: Weighted average waiting time (seconds)
                Higher values indicate worse performance
                Weighted by modal priorities and vehicle counts

        Example:
            waiting = {
                'car': [10.0, 12.0],      # 2 cars, avg 11 seconds
                'bicycle': [5.0],         # 1 bicycle, avg 5 seconds
                'pedestrian': [],         # 0 pedestrians
                'bus': [20.0, 24.0]       # 2 buses, avg 22 seconds (high priority!)
            }

            weighted = self._calculate_weighted_waiting(waiting)

            # Calculation:
            # car_avg = 11, bicycle_avg = 5, ped_avg = 0, bus_avg = 22
            # numerator = 1.2×11×2 + 1.0×5×1 + 1.0×0×0 + 1.5×22×2 = 26.4 + 5 + 0 + 66 = 97.4
            # denominator = 1.2×2 + 1.0×1 + 1.0×0 + 1.5×2 = 2.4 + 1 + 0 + 3 = 6.4
            # weighted = 97.4 / 6.4 = 15.2 seconds

            # Note: Bus waiting (22s) pulls average up due to 1.5 weight

        Interpretation:
            weighted_avg < 10 sec:  Excellent performance
            weighted_avg 10-20 sec: Good performance
            weighted_avg 20-40 sec: Acceptable performance
            weighted_avg > 40 sec: Poor performance

        Usage:
            - Primary metric for reward calculation
            - Compare different control strategies
            - Track episode performance
            - Align with thesis weighted average waiting time metric

        Notes:
            - Matches thesis evaluation methodology
            - Emphasizes high-priority mode delays
            - Zero if no vehicles present (division safe)
            - Accounts for both mode priority AND vehicle count
        """
        weighted_sum = 0.0
        weighted_count = 0.0

        weights = {
            "car": DRLConfig.WEIGHT_CAR,
            "bicycle": DRLConfig.WEIGHT_BICYCLE,
            "pedestrian": DRLConfig.WEIGHT_PEDESTRIAN,
            "bus": DRLConfig.WEIGHT_BUS,
        }

        for mode, times in waiting_times_by_mode.items():
            if times:  # Only process if there are vehicles of this mode
                avg_wait = np.mean(times)
                count = len(times)
                weight = weights[mode]

                weighted_sum += weight * avg_wait * count
                weighted_count += weight * count

        return weighted_sum / weighted_count if weighted_count > 0 else 0.0

    def _check_sync_success(self, current_phases):
        """
        Check if intersections achieved synchronization.

        Synchronization defined as both intersections simultaneously in Phase 1
        (major arterial through movement), enabling green wave progression.

        Synchronization Condition:
            - Both intersections must be in Phase 1
            - Phase 1 = SUMO phase indices 0 or 1 (leading green)
            - Simultaneous activation required (same timestep)

        Why Phase 1?
            - Major arterial through movement (highest volume)
            - Primary corridor for green wave
            - Matches thesis semi-synchronization objective
            - 300m spacing → 22 second travel time offset

        Args:
            current_phases (dict): Current phase for each intersection
                Format: {'3': 0, '6': 1}
                Keys: traffic light IDs
                Values: SUMO phase indices (0-19)

        Returns:
            bool: True if synchronized, False otherwise

        Example:
            # Both in Phase 1
            phases = {'3': 0, '6': 1}  # Both Phase 1 (leading green variants)
            sync = self._check_sync_success(phases)
            assert sync == True

            # Different phases
            phases = {'3': 0, '6': 4}  # P1 and P2
            sync = self._check_sync_success(phases)
            assert sync == False

            # One intersection only
            phases = {'3': 0}  # Missing second intersection
            sync = self._check_sync_success(phases)
            assert sync == False

        Green Wave Timing:
            Ideal sequence:
                t=0:  Intersection 3 activates Phase 1
                t=22: Intersection 6 activates Phase 1
                → Vehicles from Int 3 arrive at Int 6 during green

            Sync detection:
                - Both in Phase 1 at same time
                - Offset handled by agent learning
                - Reward bonus encourages coordination

        Notes:
            - Simple binary check (synchronized or not)
            - Could be extended to check offset timing
            - Matches existing Developed Control sync logic
            - Used for sync bonus (+1.0 reward)
        """
        phase_list = list(current_phases.values())
        if len(phase_list) >= 2:
            # Check if both are in Phase 1 (phases 0 or 1)
            return all(phase in [0, 1] for phase in phase_list)
        return False

    def _count_waiting_pedestrians_per_intersection(self, traci, tls_ids):
        """
        Count waiting pedestrians at each intersection using person API.

        Returns dict mapping tls_id to waiting pedestrian count.

        Args:
            traci: TraCI connection
            tls_ids: List of traffic light IDs (e.g., ["3", "6"])

        Returns:
            dict: {tls_id: waiting_count} for each intersection

        Example:
            {"3": 8, "6": 12}  # 8 peds at TLS 3, 12 at TLS 6
        """
        # Define edges near each intersection
        node3_edges = {"a_3", "6_3", "c_3", "d_3", "3_6", "3_a", "3_d", "3_c"}
        node6_edges = {"3_6", "b_6", "e_6", "f_6", "6_b", "6_3", "6_f", "6_e"}

        waiting_counts = {}

        try:
            # Get all pedestrians in simulation
            ped_ids = traci.person.getIDList()

            # Count waiting pedestrians per intersection
            for tls_id in tls_ids:
                waiting_count = 0

                # Determine which edges to check based on TLS ID
                if tls_id == "3":
                    relevant_edges = node3_edges
                elif tls_id == "6":
                    relevant_edges = node6_edges
                else:
                    continue

                # Count pedestrians near this intersection
                for ped_id in ped_ids:
                    try:
                        wait_time = traci.person.getWaitingTime(ped_id)
                        # Check if waiting (>2 seconds) and near this intersection
                        if wait_time > 2.0:
                            # Get pedestrian's current edge
                            edge = traci.person.getRoadID(ped_id)
                            if edge in relevant_edges:
                                waiting_count += 1
                    except:  # noqa: E722
                        # Skip failed reads
                        continue

                waiting_counts[tls_id] = waiting_count

        except:  # noqa: E722
            # Safe default if infrastructure fails
            pass

        return waiting_counts

    def _pedestrian_demand_high(self, traci, tls_ids):
        """
        Check if pedestrian demand justifies activating Phase 5.

        Implements pedestrian detection for prioritizing pedestrian phases.
        UPDATED: Now requires ≥1 waiting pedestrian to match MSc thesis baseline behavior.
        (Previously required ≥10, which was too strict compared to thesis)

        Detection Method:
            - Reads mean speed from pedestrian detectors
            - Speed < 0.1 m/s → pedestrians waiting (stopped/slow)
            - Counts pedestrians across all detectors at intersection
            - Threshold: ≥10 pedestrian waiting → demand detected (matches thesis)

        Detector Infrastructure:
            - Uses pedPhaseDetector from detectors.py
            - Virtual loop detectors at each crosswalk
            - 6m upstream from stop line
            - Covers entire crosswalk width

        Args:
            traci: SUMO TraCI connection
                Used to query pedestrian detectors via inductionloop API

            tls_ids (list): Traffic light IDs
                Identifies which intersections to check (e.g., ['3', '6'])

        Returns:
            bool: True if pedestrian demand detected (≥1 waiting), False otherwise

        Implementation Logic:
            1. Iterate through each intersection (node_idx)
            2. Get pedestrian detectors for that intersection
            3. For each detector, check mean speed and count
            4. If speed < 0.1 m/s, add vehicle count to total
            5. If total ≥ 12 pedestrian waiting, return True (matches thesis)
            6. Return False if no intersection has demand

        Usage in Reward Calculation:
            if self._pedestrian_demand_high(traci, tls_ids):
                event_type = 'pedestrian_phase'
                # High priority for Prioritized Experience Replay
                # Agent should learn to activate pedestrian phase

        Error Handling:
            - Try-except on each detector query
            - Failed reads skip to next detector
            - Returns False if all detectors fail (safe default)

        Notes:
            - Threshold (≥1) matches MSc thesis baseline behavior
            - Same logic as thesis: any(check_pedestrian()) → activate
            - Used for event classification in Prioritized Experience Replay
            - Agent learns when to activate based on reward feedback
        """
        # Use helper function to count waiting pedestrians per intersection
        waiting_counts = self._count_waiting_pedestrians_per_intersection(
            traci, tls_ids
        )

        # Check if any intersection has pedestrian demand (≥3 pedestrians waiting)
        # Further lowered from 6 to 3 to increase learning opportunities (Phase 4 - Oct 24, 2025)
        # Rationale: Agent needs more frequent positive feedback to learn pedestrian action value
        for tls_id, waiting_count in waiting_counts.items():
            if waiting_count >= 6:  # CHANGED: 6 → 3
                print(
                    f"[PED DEMAND] TLS {tls_id}: {waiting_count} pedestrians waiting (≥6 threshold) 🚶"
                )
                return True

        return False

    def _classify_event(
        self, action, sync_achieved, ped_phase_active, ped_demand_high=False
    ):
        """
        Classify event type for Prioritized Experience Replay.

        Assigns priority class to experience based on action taken and
        resulting state. Important events (sync, pedestrian, bus) receive
        higher priority for more frequent learning.

        Event Classification Hierarchy (highest to lowest priority):
            1. Safety violation: 'safety_violation' (priority 10x - CRITICAL)
            2. Pedestrian demand ignored: 'ped_demand_ignored' (priority 6x)
            3. Pedestrian phase: 'pedestrian_phase' (priority 5x)
            4. Sync success: 'sync_success' (priority 3x)
            5. Sync attempt: 'sync_attempt' (priority 2x)
            6. Normal: 'normal' (priority 1x)

        Classification Logic:
            if ped_demand_high and not ped_phase_active:
                → 'ped_demand_ignored'
                HIGHEST priority - agent must learn to avoid this

            elif ped_phase_active:
                → 'pedestrian_phase'
                High priority for vulnerable road user safety

            elif sync_achieved:
                → 'sync_success'
                Learn successful coordination patterns

            elif action == 1 (Skip to Phase 1):
                → 'sync_attempt'
                Learn when synchronization is beneficial

            else:
                → 'normal'
                Routine traffic control decision

        Args:
            action (int): Action taken (0-3)
                0: Continue
                1: Skip to Phase 1
                2: Next phase
                3: Pedestrian phase

            sync_achieved (bool): Whether synchronization achieved
                True if both intersections in Phase 1

            ped_phase_active (bool): Whether pedestrian phase active
                True if Phase 5 (pedestrian exclusive) active

            ped_demand_high (bool): Whether ≥10 pedestrians waiting
                True if high pedestrian demand detected

        Returns:
            str: Event type classification
                'safety_violation': Safety issue detected (CRITICAL - must avoid)
                'ped_demand_ignored': High ped demand but phase not activated (LEARN TO AVOID)
                'pedestrian_phase': Pedestrian phase activated
                'sync_success': Synchronization achieved
                'sync_attempt': Tried to synchronize (Action 1)
                'normal': Regular decision

        Example:
            # Pedestrian phase activated
            event = self._classify_event(
                action=3,
                sync_achieved=False,
                ped_phase_active=True
            )
            assert event == 'pedestrian_phase'

            # Synchronization achieved
            event = self._classify_event(
                action=1,
                sync_achieved=True,
                ped_phase_active=False
            )
            assert event == 'sync_success'

            # Sync attempt (may or may not succeed)
            event = self._classify_event(
                action=1,
                sync_achieved=False,
                ped_phase_active=False
            )
            assert event == 'sync_attempt'

            # Normal progression
            event = self._classify_event(
                action=2,
                sync_achieved=False,
                ped_phase_active=False
            )
            assert event == 'normal'

        PER Priority Multipliers:
            Event type → Priority in replay buffer:
                'safety_violation' → 10x (CRITICAL - must learn to avoid)
                'ped_demand_ignored' → 6x (HIGH - learn to avoid ignoring pedestrians)
                'pedestrian_phase' → 5x (learn pedestrian response)
                'sync_success' → 3x (learn coordination)
                'sync_attempt' → 2x (learn when to coordinate)
                'normal' → 1x (baseline learning)

        Usage in Agent:
            reward, info = reward_calc.calculate_reward(...)
            event_type = info['event_type']

            agent.store_experience(
                state, action, reward, next_state, done,
                info={'event_type': event_type}
            )

            # PER buffer uses event_type to set priority

        Notes:
            - Enables focused learning on important events
            - Addresses sparse reward problem (sync bonus rare)
            - Accelerates learning of coordination strategies
            - Compatible with DQN agent's PER implementation
            - 'ped_demand_ignored' gets highest priority to teach agent responsiveness
        """
        if ped_demand_high and not ped_phase_active:
            return "ped_demand_ignored"
        elif ped_phase_active:
            return "pedestrian_phase"
        elif sync_achieved:
            return "sync_success"
        elif action == 1:  # Skip to Phase 1
            return "sync_attempt"
        else:
            return "normal"

    def _calculate_equity_penalty(self, waiting_times_by_mode):
        """
        Calculate equity penalty based on variance in waiting times across modes.

        Measures fairness of traffic signal control by comparing average waiting
        times across different transportation modes. High variance indicates some
        modes are being unfairly prioritized over others.

        Equity Metric:
            - Uses Coefficient of Variation (CV = std / mean)
            - CV = 0: Perfect equity (all modes wait same time)
            - CV > 1: Very unfair (large disparities between modes)

        Calculation Steps:
            1. Compute average waiting time for each mode
            2. Calculate mean and std deviation across modes
            3. Compute CV = std / mean
            4. Normalize to [0, 1] range

        Args:
            waiting_times_by_mode (dict): Waiting times per mode
                Format: {'car': [10, 15, 20], 'bicycle': [5, 8], ...}

        Returns:
            float: Equity penalty [0, 1]
                0.0 = Perfectly fair (all modes treated equally)
                1.0 = Very unfair (large variance in waiting times)

        Example:
            # Fair scenario: all modes wait ~10 seconds
            waiting_times = {
                'car': [10, 11, 9],
                'bicycle': [10, 12],
                'bus': [11, 10],
                'pedestrian': [9, 10, 11]
            }
            penalty = self._calculate_equity_penalty(waiting_times)
            # penalty ≈ 0.1 (low - fairly equitable)

            # Unfair scenario: cars wait 5s, pedestrians wait 30s
            waiting_times = {
                'car': [5, 6, 4],
                'bicycle': [15, 18],
                'bus': [10, 12],
                'pedestrian': [30, 35, 28]
            }
            penalty = self._calculate_equity_penalty(waiting_times)
            # penalty ≈ 0.8 (high - very inequitable)

        Notes:
            - Requires ≥2 modes with vehicles to compute
            - Returns 0.0 if insufficient data
            - Returns 0.0 if mean waiting time < 0.1s (negligible)
            - Used with ALPHA_EQUITY weight in reward calculation
        """
        # Get average waiting time per mode (only continuous flow modes)
        avg_waits = []
        for mode in ["car", "bicycle"]:  # Exclude bus/ped (scheduled/intermittent)
            if waiting_times_by_mode[mode]:
                avg_waits.append(np.mean(waiting_times_by_mode[mode]))

        if len(avg_waits) < 2:
            return 0.0  # Can't measure fairness with <2 modes

        # Calculate coefficient of variation (normalized std dev)
        mean_wait = np.mean(avg_waits)
        std_wait = np.std(avg_waits)

        if mean_wait < 0.1:
            return 0.0  # Very low waiting times = fair enough

        # Coefficient of variation: higher = more unfair
        cv = std_wait / mean_wait

        # Normalize to [0, 1] range (cv > 1.0 is very unfair)
        equity_penalty = min(cv, 1.0)

        return equity_penalty

    def _check_near_collision_violations(self, traci, tls_ids):
        """
        Check for near-collision safety violations (headway and distance).

        Checks:
        1. Time Headway: < 1.0 seconds (only for fast vehicles: speed > 8.0 m/s)
        2. Following Distance: < 1.0 meters (only for moving vehicles: speed > 1.0 m/s)

        Args:
            traci: SUMO TraCI connection
            tls_ids (list): Traffic light IDs to check

        Returns:
            tuple: (has_violation: bool, headway_count: int, distance_count: int)
        """
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

                                    # Headway check (UPDATED: only enforce for fast vehicles)
                                    if time_headway < SAFE_HEADWAY:
                                        if (
                                            speed1 > 8.0
                                        ):  # Only enforce for fast vehicles (>28.8 km/h)
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

                                    # Distance check (FIXED: only for moving vehicles)
                                    if distance < COLLISION_DISTANCE:
                                        # CRITICAL FIX: Only flag if lead vehicle is MOVING
                                        if speed1 > 1.0:  # 1 m/s = 3.6 km/h (crawling)
                                            distance_violations += 1
                                            self.total_distance_violations += 1
                                            if distance_violations <= 3:
                                                print(
                                                    f"[SAFETY-DEBUG] Distance: {distance:.1f}m < {COLLISION_DISTANCE}m (MOVING: speed={speed1:.1f}m/s)"
                                                )
                                            # Found a real moving collision risk
                                            return (
                                                True,
                                                headway_violations,
                                                distance_violations,
                                            )
                                        # If stopped (speed <= 1.0), this is normal queuing - ignore
                                except:  # noqa: E722
                                    continue
            except:  # noqa: E722
                continue

        return False, headway_violations, distance_violations

    def _check_safety_violations(
        self, traci, tls_ids, current_phases, phase_durations=None
    ):
        """
        Check for near-collision safety violations (headway and distance).

        RATIONALE (Phase 4 - Oct 24, 2025):
        Red light violations removed from safety checks because:
        1. They are consequences of phase timing, not direct safety risks
        2. Agent doesn't control vehicles, only traffic light phases
        3. Red light violations are SUMO artifacts (dilemma zone problem)
        4. Including them created feedback loop preventing phase changes

        Now ONLY checks near-collisions between vehicles, which are:
        - Direct consequences of traffic congestion/flow
        - Influenced by agent's queue management and phase timing
        - Real safety metrics we want to minimize

        FIXED ISSUES:
        1. SAFE_HEADWAY reduced from 2.0s to 1.0s (per config update)
        2. Headway violations ONLY for fast vehicles (speed > 8.0 m/s = 28.8 km/h)
        3. COLLISION_DISTANCE reduced from 5.0m to 1.0m (per config update)
        4. Distance violations ONLY for moving vehicles (speed > 1.0 m/s)

        NOTE: MIN_GREEN_TIME enforcement is handled by _execute_action_for_tls()
        in traffic_management.py. That method blocks unsafe phase changes BEFORE
        they occur. We do NOT check phase_duration here because:
        1. Actions are already blocked if duration < MIN_GREEN_TIME
        2. Checking here creates false positives (flagging blocked attempts)
        3. The agent never actually makes unsafe phase changes

        Violation Types (Near-Collision Only):
            a) Unsafe headway (< SAFE_HEADWAY seconds):
               - Only flagged if speed > 8.0 m/s (fast vehicles)
               - Slow/stopped vehicles ignored (normal queuing)

            b) Vehicles too close (< COLLISION_DISTANCE meters):
               - Only flagged if speed > 1.0 m/s (moving vehicles)
               - Stopped queues (speed <= 1.0) ignored

        Args:
            traci: SUMO TraCI connection
            tls_ids (list): Traffic light IDs to check
            current_phases (dict): Current phase for each TLS
            phase_durations (dict, optional): NOT USED (kept for compatibility)

        Returns:
            bool: True if any safety violation detected, False otherwise

        Safety Thresholds (from constants.py):
            - SAFE_HEADWAY = 1.0 seconds (only enforced for speed > 8.0 m/s)
            - COLLISION_DISTANCE = 1.0 meters (only enforced for speed > 1.0 m/s)
        """
        # Check: Near-collisions (headway and distance violations)
        has_collision_violation, headway_violations, distance_violations = (
            self._check_near_collision_violations(traci, tls_ids)
        )
        if has_collision_violation:
            return True

        # Debug summary (every 100 steps)
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

        # Return False - violations already returned True immediately (early exit)
        return False

    def print_safety_summary(self):
        """
        Print final safety violation summary for the episode.
        Should be called at the end of each episode.
        """
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
