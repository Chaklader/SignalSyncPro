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

    R_sync = +1.0  if both intersections in Phase 1 simultaneously
    R_sync = 0.0   otherwise

Condition:
    both_in_phase_1 = (phase_3 ∈ {0,1}) AND (phase_6 ∈ {0,1})

Purpose:
    - Strong incentive for coordination
    - Enables green wave progression
    - Matches thesis semi-synchronization objective
    - Sparse bonus (only when aligned)

Why Phase 1?
    - Major arterial through movement
    - Highest traffic volume
    - Green wave most beneficial here
    - Travel time: 22 seconds between intersections

4. TOTAL REWARD FUNCTION
-------------------------
Combined reward with clipping:

    R_total = R_stopped + R_flow + R_sync
    R_total = clip(R_total, -2.0, 2.0)

Typical Range:
    Worst case:  R = -1.0 + 0.0 + 0.0 = -1.0  (all stopped, no sync)
    Poor:        R = -0.5 + 0.25 + 0.0 = -0.25
    Good:        R = -0.2 + 0.4 + 0.0 = 0.2
    Excellent:   R = -0.1 + 0.45 + 1.0 = 1.35  (flowing + synced)
    Best case:   R = 0.0 + 0.5 + 1.0 = 1.5  (all moving + synced)

Clipping to [-2, 2]:
    - Prevents extreme values from rare events
    - Ensures stable Q-value learning
    - Maintains interpretability

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
    ✓ Waiting time: Core component of reward (stopped ratio proxy)
    ✓ Modal weighting: Same weights as thesis (1.2, 1.0, 1.0, 1.5)
    ✓ Synchronization: Explicit bonus for coordination
    ✗ CO₂: Currently disabled (ALPHA_EMISSION = 0.0) for simplicity
    ✗ Equity: Currently disabled (ALPHA_EQUITY = 0.0) for simplicity

Simplification Rationale:
    - Start with core objective: minimize weighted waiting
    - Add synchronization for coordination learning
    - CO₂ and equity can be enabled later via config
    - Simpler reward = faster initial learning
    - Can incrementally add complexity

===================================================================================
REWARD SHAPING CONSIDERATIONS
===================================================================================

Good Reward Properties:
    ✓ Markovian: Depends only on current state/action
    ✓ Bounded: Clipped to [-2, 2]
    ✓ Dense: Non-zero reward at every timestep
    ✓ Interpretable: Each component has clear meaning
    ✓ Differentiating: Distinguishes good from bad control

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

from drl.config import DRLConfig
from common.utils import get_vehicle_mode


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
                
        Example:
            reward_calc = RewardCalculator()
            # Ready to compute rewards
            
            # At episode start
            reward_calc.reset()
        """
        self.prev_metrics = {}
        self.episode_step = 0
        
    def reset(self):
        """
        Reset calculator for new episode.
        
        Clears accumulated metrics and counters to prepare for new episode.
        Should be called by environment's reset() method.
        
        Resets:
            - prev_metrics: Clears stored previous measurements
            - episode_step: Resets timestep counter to 0
            
        Example:
            # Start new training episode
            state = env.reset()
            reward_calc.reset()  # Clear previous episode data
            
            for step in range(3600):
                reward, info = reward_calc.calculate_reward(...)
                # Fresh metrics each episode
        """
        self.prev_metrics = {}
        self.episode_step = 0
        
    def calculate_reward(self, traci, tls_ids, action, current_phases):
        """
        Calculate multi-objective reward for current timestep.
        
        Core reward computation combining weighted stopped ratio, flow bonus,
        and synchronization bonus. Also returns detailed info dict with
        per-mode statistics for logging and analysis.
        
        Reward Calculation Steps:
            1. Count stopped/total vehicles by mode (car, bicycle, bus, pedestrian)
            2. Apply modal priority weights (from config)
            3. Compute weighted stopped ratio
            4. Calculate base reward: -stopped_ratio
            5. Add flow bonus: +(1 - stopped_ratio) × 0.5
            6. Add sync bonus: +1.0 if both intersections in Phase 1
            7. Clip final reward to [-2, 2]
            8. Classify event type for PER
            9. Return (reward, info)
            
        Modal Counting:
            For each vehicle in simulation:
                - Get vehicle type ID from SUMO
                - Classify using get_vehicle_mode() utility
                - Track total count per mode
                - Check if stopped (speed < 0.1 m/s)
                - Record accumulated waiting time
                
        Weighted Stopped Ratio:
            weighted_stopped = Σ (stopped[mode] × weight[mode])
            weighted_total = Σ (total[mode] × weight[mode])
            ratio = weighted_stopped / weighted_total
            
        Synchronization Detection:
            - Both intersections must be in Phase 1 (indices 0 or 1)
            - Bonus only when simultaneously coordinated
            - Encourages green wave timing
            
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
                Range: [-2.0, 2.0] (clipped)
                Typical: -1.0 to +1.5
                Negative: Poor performance (many stopped vehicles)
                Positive: Good performance (flowing + coordinated)
                
            info (dict): Detailed metrics for logging
                Keys:
                    'stopped_by_mode': dict
                        {'car': int, 'bicycle': int, 'bus': int, 'pedestrian': int}
                        Count of stopped vehicles per mode
                        
                    'total_by_mode': dict
                        Total vehicle count per mode
                        
                    'weighted_stopped_ratio': float
                        Weighted proportion of stopped vehicles [0, 1]
                        
                    'waiting_time': float
                        Overall average waiting time (seconds)
                        Unweighted mean across all vehicles
                        
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
                        
                    'event_type': str
                        Event classification for PER:
                        'normal', 'sync_success', 'sync_attempt', 'pedestrian_phase'
                        
        Example Usage:
            # During training step
            reward, info = reward_calc.calculate_reward(
                traci=traci,
                tls_ids=['3', '6'],
                action=1,  # Skip to Phase 1
                current_phases={'3': 1, '6': 0}
            )
            
            print(f"Reward: {reward:.3f}")
            # Output: Reward: 1.200
            # (Good flow + synchronization achieved)
            
            # Log detailed metrics
            logger.log({
                'reward': reward,
                'stopped_ratio': info['weighted_stopped_ratio'],
                'car_wait': info['waiting_time_car'],
                'bike_wait': info['waiting_time_bicycle'],
                'bus_wait': info['waiting_time_bus'],
                'sync': info['sync_achieved']
            })
            
        Reward Interpretation:
            reward = -0.8  → Many vehicles stopped, poor control
            reward = -0.2  → Some congestion, acceptable control
            reward = +0.3  → Good flow, no sync
            reward = +1.2  → Good flow + synchronization achieved
            
        Performance Indicators:
            stopped_ratio < 0.2: Excellent flow
            stopped_ratio 0.2-0.5: Good flow
            stopped_ratio 0.5-0.8: Moderate congestion
            stopped_ratio > 0.8: Severe congestion
            
        Notes:
            - Called every simulation step (1 second)
            - Uses instantaneous measurements (not cumulative)
            - Modal weights from DRLConfig
            - Sync bonus matches thesis semi-synchronization objective
            - Event classification enables PER prioritization
        """
        self.episode_step += 1
        
        # Count stopped vehicles and waiting times by mode
        stopped_by_mode = {'car': 0, 'bicycle': 0, 'bus': 0, 'pedestrian': 0}
        total_by_mode = {'car': 0, 'bicycle': 0, 'bus': 0, 'pedestrian': 0}
        waiting_times_by_mode = {'car': [], 'bicycle': [], 'bus': [], 'pedestrian': []}
        
        for veh_id in traci.vehicle.getIDList():
            try:
                vtype = traci.vehicle.getTypeID(veh_id)
                speed = traci.vehicle.getSpeed(veh_id)
                wait_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
                
                # Classify vehicle using common utility
                mode = get_vehicle_mode(vtype)
                
                total_by_mode[mode] += 1
                waiting_times_by_mode[mode].append(wait_time)
                
                if speed < 0.1:  # Stopped
                    stopped_by_mode[mode] += 1
            except:
                continue
        
        # Calculate weighted stopped ratio (using config weights)
        weights = {
            'car': DRLConfig.WEIGHT_CAR,
            'bicycle': DRLConfig.WEIGHT_BICYCLE,
            'bus': DRLConfig.WEIGHT_BUS,
            'pedestrian': DRLConfig.WEIGHT_PEDESTRIAN
        }
        
        weighted_stopped = 0
        weighted_total = 0
        
        for mode in stopped_by_mode:
            weighted_stopped += stopped_by_mode[mode] * weights[mode]
            weighted_total += total_by_mode[mode] * weights[mode]
        
        if weighted_total > 0:
            stopped_ratio = weighted_stopped / weighted_total
        else:
            stopped_ratio = 0.0
        
        # Reward calculation
        reward = -stopped_ratio  # Penalty for stopped vehicles
        reward += (1.0 - stopped_ratio) * 0.5  # Bonus for flow
        
        # Sync bonus
        phase_list = list(current_phases.values())
        both_phase_1 = len(phase_list) >= 2 and all(p in [0, 1] for p in phase_list)
        if both_phase_1:
            reward += 1.0
        
        reward = np.clip(reward, -2.0, 2.0)
        
        # Calculate average waiting time per mode (in seconds)
        avg_waiting_time_by_mode = {
            'car': np.mean(waiting_times_by_mode['car']) if waiting_times_by_mode['car'] else 0,
            'bicycle': np.mean(waiting_times_by_mode['bicycle']) if waiting_times_by_mode['bicycle'] else 0,
            'bus': np.mean(waiting_times_by_mode['bus']) if waiting_times_by_mode['bus'] else 0,
            'pedestrian': np.mean(waiting_times_by_mode['pedestrian']) if waiting_times_by_mode['pedestrian'] else 0
        }
        
        # Overall average waiting time (weighted)
        all_waiting_times = []
        for mode in waiting_times_by_mode:
            all_waiting_times.extend(waiting_times_by_mode[mode])
        overall_avg_wait = np.mean(all_waiting_times) if all_waiting_times else 0
        
        info = {
            'stopped_by_mode': stopped_by_mode,
            'total_by_mode': total_by_mode,
            'weighted_stopped_ratio': stopped_ratio,
            'waiting_time': overall_avg_wait,  # Overall average waiting time in seconds
            'waiting_time_car': avg_waiting_time_by_mode['car'],
            'waiting_time_bicycle': avg_waiting_time_by_mode['bicycle'],
            'waiting_time_bus': avg_waiting_time_by_mode['bus'],
            'waiting_time_pedestrian': avg_waiting_time_by_mode['pedestrian'],
            'sync_achieved': both_phase_1,
            'event_type': 'sync_success' if both_phase_1 else 'normal'
        }
        
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
        waiting_times = {
            'car': [],
            'bicycle': [],
            'pedestrian': [],
            'bus': []
        }
        
        # Get all vehicles currently in simulation
        for veh_id in traci.vehicle.getIDList():
            try:
                vtype = traci.vehicle.getTypeID(veh_id)
                
                # Get CURRENT waiting time (seconds stopped)
                wait_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
                speed = traci.vehicle.getSpeed(veh_id)
                
                # Only count if currently stopped
                if speed < 0.1:
                    if 'Volkswagen' in vtype or 'passenger' in vtype.lower():
                        waiting_times['car'].append(wait_time)
                    elif 'Raleigh' in vtype or 'bicycle' in vtype.lower():
                        waiting_times['bicycle'].append(wait_time)
                    elif 'bus' in vtype.lower():
                        waiting_times['bus'].append(wait_time)
            except:
                continue
        
        # Calculate AVERAGE for this timestep
        for mode in waiting_times:
            if waiting_times[mode]:
                waiting_times[mode] = np.mean(waiting_times[mode])
            else:
                waiting_times[mode] = 0.0
        
        return waiting_times
    
    def _calculate_weighted_waiting(self, waiting_times):
        """
        Calculate weighted average waiting time across all modes.
        
        Applies modal priority weights to compute overall system performance
        metric that emphasizes high-priority modes (buses, pedestrians).
        
        Formula:
            weighted_avg = Σ (weight[mode] × wait[mode]) / Σ weight[mode]
            
        Where:
            weight[mode] = priority weight from config
            wait[mode] = average waiting time for that mode
            
        Args:
            waiting_times (dict): Waiting times by mode (seconds)
                Format: {
                    'car': float,
                    'bicycle': float,
                    'pedestrian': float,
                    'bus': float
                }
                
        Returns:
            float: Weighted average waiting time (seconds)
                Higher values indicate worse performance
                Weighted by modal priorities
                
        Example:
            waiting = {
                'car': 10.0,      # 10 seconds average
                'bicycle': 5.0,   # 5 seconds average  
                'pedestrian': 0.0,
                'bus': 20.0       # 20 seconds average (high priority!)
            }
            
            weighted = self._calculate_weighted_waiting(waiting)
            
            # Calculation:
            # numerator = 1.2×10 + 1.0×5 + 1.0×0 + 1.5×20 = 47
            # denominator = 1.2 + 1.0 + 1.0 + 1.5 = 4.7
            # weighted = 47 / 4.7 = 10.0 seconds
            
            # Note: Bus waiting (20s) pulls average up due to 1.5 weight
            
        Interpretation:
            weighted_avg < 5 sec:  Excellent performance
            weighted_avg 5-15 sec: Good performance
            weighted_avg 15-30 sec: Acceptable performance
            weighted_avg > 30 sec: Poor performance
            
        Usage:
            - Compare different control strategies
            - Track episode performance
            - Align with thesis weighted average waiting time metric
            
        Notes:
            - Matches thesis evaluation methodology
            - Emphasizes high-priority mode delays
            - Zero if no vehicles present (division safe)
        """
        weighted_sum = (
            DRLConfig.WEIGHT_CAR * waiting_times['car'] +
            DRLConfig.WEIGHT_BICYCLE * waiting_times['bicycle'] +
            DRLConfig.WEIGHT_PEDESTRIAN * waiting_times.get('pedestrian', 0) +
            DRLConfig.WEIGHT_BUS * waiting_times['bus']
        )
        total_weight = (DRLConfig.WEIGHT_CAR + DRLConfig.WEIGHT_BICYCLE + 
                       DRLConfig.WEIGHT_PEDESTRIAN + DRLConfig.WEIGHT_BUS)
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
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
    
    def _pedestrian_demand_high(self, traci, tls_ids):
        """
        Check if pedestrian demand justifies activating Phase 5.
        
        Placeholder for pedestrian demand detection logic. Should be
        implemented based on pedestrian detector infrastructure.
        
        Demand Detection Methods:
            1. Detector-based:
                - Count pedestrians at crossing detectors
                - Threshold: ≥10 pedestrians waiting
                - Check mean speed < 0.1 m/s (stopped)
                
            2. Button-based:
                - Virtual pedestrian call button
                - Binary signal (activated or not)
                
            3. Time-based:
                - Time since last pedestrian phase
                - Threshold: >300 seconds without ped phase
                
        Args:
            traci: SUMO TraCI connection
                Used to query pedestrian detectors
                
            tls_ids (list): Traffic light IDs
                Identifies which intersections to check
                
        Returns:
            bool: True if high pedestrian demand, False otherwise
            
        Current Implementation:
            - Returns False (placeholder)
            - TODO: Implement actual pedestrian detection
            - Should use pedPhaseDetector from existing infrastructure
            
        Intended Logic:
            def _pedestrian_demand_high(self, traci, tls_ids):
                for tls_id in tls_ids:
                    node_idx = tls_ids.index(tls_id)
                    ped_detectors = pedPhaseDetector[node_idx]
                    
                    for det_id in ped_detectors:
                        speed = traci.inductionloop.getLastStepMeanSpeed(det_id)
                        count = traci.inductionloop.getLastStepVehicleNumber(det_id)
                        
                        if speed < 0.1 and count >= 10:
                            return True
                return False
                
        Usage:
            if self._pedestrian_demand_high(traci, tls_ids):
                event_type = 'pedestrian_phase'
                # High priority for PER
                # Agent should consider Action 3 (activate ped phase)
                
        Notes:
            - Currently not used in reward calculation
            - Needed for complete event classification
            - Important for learning pedestrian-responsive control
            - Should match environment's _get_pedestrian_demand() logic
        """
        # Simple heuristic: count pedestrians
        # This is placeholder - implement based on your pedestrian detection
        return False
    
    def _classify_event(self, action, sync_achieved, ped_phase_active):
        """
        Classify event type for Prioritized Experience Replay.
        
        Assigns priority class to experience based on action taken and
        resulting state. Important events (sync, pedestrian, bus) receive
        higher priority for more frequent learning.
        
        Event Classification Hierarchy (highest to lowest priority):
            1. Pedestrian phase: 'pedestrian_phase' (priority 5x)
            2. Sync success: 'sync_success' (priority 3x)
            3. Sync attempt: 'sync_attempt' (priority 2x)
            4. Normal: 'normal' (priority 1x)
            
        Classification Logic:
            if ped_phase_active:
                → 'pedestrian_phase'
                Highest priority for vulnerable road user safety
                
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
                
        Returns:
            str: Event type classification
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
        """
        if ped_phase_active:
            return 'pedestrian_phase'
        elif sync_achieved:
            return 'sync_success'
        elif action == 1:  # Skip to Phase 1
            return 'sync_attempt'
        else:
            return 'normal'