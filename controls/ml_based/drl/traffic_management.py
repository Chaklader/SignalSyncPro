"""
Enhanced SUMO Environment Wrapper for Deep Reinforcement Learning Traffic Control

This module provides a Gym-style environment interface for training DRL agents to control
traffic signals in SUMO (Simulation of Urban MObility). It integrates with the existing
SignalSyncPro infrastructure while providing the standardized interface needed for DQN training.

===================================================================================
ENVIRONMENT OVERVIEW
===================================================================================

The TrafficManagement environment simulates a two-intersection urban corridor:
    - Two traffic lights (IDs: '3' and '6')
    - Separated by 300 meters along major arterial
    - Each intersection has minor road crossing
    - Multimodal traffic: cars, bicycles, pedestrians, buses
    - Semi-synchronized coordination between intersections

Key Features:
    - Realistic traffic simulation via SUMO
    - Existing detector infrastructure integration
    - Phase-based signal control (4 phases + pedestrian)
    - Synchronization timer for green wave coordination
    - Multi-objective reward (waiting time, CO₂, sync, equity, safety)

===================================================================================
STATE SPACE (45 dimensions for 2 intersections)
===================================================================================

The environment uses CENTRALIZED control: one agent observes and controls BOTH
intersections simultaneously. This enables learning of coordination strategies.

State Vector Structure (~45 total dimensions):

For EACH intersection (×2 = ~22-23 dimensions each):
    ┌─────────────────────────────────────────────────────────┐
    │ Phase Information:                                       │
    │   - Phase encoding (one-hot):        5 dims             │
    │     [Phase1, Phase2, Phase3, Phase4, Pedestrian]        │
    │   - Phase duration (normalized):     1 dim              │
    │                                                          │
    │ Vehicle Detection:                                       │
    │   - Vehicle queues (4 approaches):   4 dims             │
    │   - Bicycle queues (4 approaches):   4 dims             │
    │                                                          │
    │ Pedestrian & Transit:                                    │
    │   - Pedestrian demand (binary):      1 dim              │
    │   - Bus presence (binary):           1 dim              │
    │                                                          │
    │ Coordination:                                            │
    │   - Sync timer (normalized):         1 dim              │
    │   - Time of day (normalized):        1 dim              │
    └─────────────────────────────────────────────────────────┘

Total: ~45 dimensions (combines both intersections + coordination features)

State Normalization:
    - Phase encoding: {0, 1} (one-hot)
    - Durations: [0, 1] (normalized by maximum expected duration)
    - Queues: [0, 1] (detector occupancy)
    - Timers: [0, 1] (normalized by coordination window)
    - Time of day: [0, 1] (normalized within hour)

Example State Vector:
    [
        # Intersection 3
        1, 0, 0, 0, 0,  # Phase 1 active
        0.25,           # 15 seconds into phase
        0.8, 0.3, 0.0, 0.5,  # Vehicle queues
        0.6, 0.2, 0.0, 0.3,  # Bicycle queues
        1.0,            # Pedestrians waiting
        0.0,            # No bus
        0.6,            # Sync timer
        0.42,           # Time of day

        # Intersection 6
        0, 1, 0, 0, 0,  # Phase 2 active
        0.15,           # 9 seconds into phase
        0.5, 0.7, 0.2, 0.4,  # Vehicle queues
        0.3, 0.5, 0.1, 0.2,  # Bicycle queues
        0.0,            # No pedestrians
        1.0,            # Bus present
        0.3,            # Sync timer
        0.42,           # Time of day (same)
    ]

===================================================================================
ACTION SPACE (4 discrete actions)
===================================================================================

Actions are applied to BOTH intersections in coordinated manner:

    Action 0: Continue Current Phase
        - Maintains green signal on current movement
        - Useful when traffic is clearing efficiently
        - No phase change, duration counter increments

    Action 1: Skip to Phase 1 (Major Arterial Through)
        - Forces transition to Phase 1 (major through movement)
        - Used for synchronization and green wave coordination
        - Only executes if MIN_GREEN_TIME satisfied

    Action 2: Progress to Next Phase
        - Advances to next phase in sequence (1→2→3→4→1)
        - Standard phase progression for balanced service
        - Only executes if MIN_GREEN_TIME satisfied

    Action 3: Activate Pedestrian Phase
        - Triggers dedicated pedestrian crossing phase
        - High priority when pedestrian demand detected
        - Only executes if MIN_GREEN_TIME satisfied

Action Constraints:
    - Minimum green time: 5 seconds (safety requirement)
    - Yellow/all-red clearance automatically inserted
    - Phase progression follows fixed sequence
    - Actions applied independently to each intersection

===================================================================================
REWARD FUNCTION
===================================================================================

Multi-objective reward balancing efficiency, equity, and safety:

    R = -α₁·waiting_time - α₂·CO₂ + α₃·sync_success + α₄·equity - α₅·safety_penalty

Component Weights (from config):
    α₁ = 1.0   (waiting time penalty)
    α₂ = 0.0   (CO₂ emissions - disabled for now)
    α₃ = 0.5   (synchronization bonus)
    α₄ = 0.0   (equity - disabled for now)
    α₅ = 0.0   (safety violations - disabled for now)

Modal Priority Weights:
    - Cars:        1.2 (baseline)
    - Bicycles:    1.0 (equal priority)
    - Pedestrians: 1.0 (equal priority)
    - Buses:       1.5 (high priority for public transit)

Typical Reward Range:
    Good performance:  -5 to +5 per step
    Poor performance:  -20 to -50 per step
    Extreme events:    -100 (safety) to +20 (perfect sync)

===================================================================================
EPISODE STRUCTURE
===================================================================================

Episode Lifecycle:
    1. reset() - Initialize SUMO, reset traffic lights, return initial state
    2. Loop:
        a. Agent selects action based on state
        b. step(action) - Execute action, advance simulation
        c. Receive next_state, reward, done, info
        d. Agent learns from experience
    3. Episode ends when:
        - No more vehicles expected (simulation complete)
        - Maximum steps reached (timeout)
        - Manual termination

Episode Duration:
    - Training: 3,600 steps (1 hour simulation time)
    - Testing: 10,000 steps (2.78 hours) to match thesis scenarios

Episode Frequency:
    - Training: 500-1000 episodes with varying traffic
    - Testing: 30 episodes (Pr_0 to Pe_9 scenarios from thesis)

===================================================================================
INTEGRATION WITH EXISTING INFRASTRUCTURE
===================================================================================

This environment integrates seamlessly with SignalSyncPro components:

From constants.py:
    - MIN_GREEN_TIME (5 seconds)
    - YELLOW_TIME (3 seconds)
    - ALLRED_TIME (2 seconds)

From tls_constants.py:
    - pOne, pTwo, pThree, pFour (phase definitions)
    - busPriorityLane (bus detection lanes)

From detectors.py:
    - detectorInfo (detector layout and IDs)
    - pedPhaseDetector (pedestrian detection points)

From drl/reward.py:
    - RewardCalculator (multi-objective reward computation)

This ensures DRL training uses identical infrastructure as the Developed Control
system, enabling fair comparison in testing phase.

===================================================================================
CENTRALIZED VS DISTRIBUTED CONTROL
===================================================================================

**This environment uses CENTRALIZED control:**

Single Agent Observes Both Intersections:
    ✓ State vector includes features from BOTH intersections
    ✓ Agent sees global traffic conditions
    ✓ Can learn coordination patterns naturally
    ✓ Synchronization emerges from learning

Single Agent Controls Both Intersections:
    ✓ Same action applied to both (or alternating based on need)
    ✓ Shared decision-making policy
    ✓ One trained model for entire corridor
    ✓ Efficient: 110K parameters vs 220K for separate agents

Why Centralized?
    - Thesis emphasizes semi-synchronization (requires coordination)
    - Green wave optimization (needs upstream-downstream awareness)
    - More efficient learning (shared experiences)
    - Better performance (global optimization vs local greedy)

===================================================================================
SUMO INTEGRATION DETAILS
===================================================================================

SUMO Connection:
    - Uses TraCI (Traffic Control Interface) for Python control
    - Port 8816 (configured in signal_sync.sumocfg)
    - Subprocess management for clean startup/shutdown
    - Real-time simulation stepping (1 second per step)

Traffic Light Control:
    - Phase-based control (not signal-by-signal)
    - Automatic yellow/all-red clearance
    - Safety constraints enforced (MIN_GREEN_TIME)
    - Compatible with existing phase structure

Vehicle Detection:
    - Induction loop detectors at 30m and 100m upstream
    - Last detection time for queue estimation
    - Type-specific detection (cars, bicycles, buses)
    - Pedestrian crossing detectors

Simulation Fidelity:
    - Krauss car-following model
    - LC2013 lane-changing model
    - Poisson arrival distribution
    - Realistic vehicle dynamics
    - CO₂ emission calculations

===================================================================================
"""

import numpy as np
import sys
import os

# Add SUMO tools to path
if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)

import traci

# Import existing infrastructure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controls.ml_based.drl.config import DRLConfig
from controls.ml_based.drl.reward import RewardCalculator
from constants.constants import MIN_GREEN_TIME
from constants.developed.common.tls_constants import (
    PHASE_ONE,
    PHASE_TWO,
    PHASE_THREE,
    PHASE_FOUR,
)
from detectors.developed.common.detectors import DETECTORS_INFO, PEDESTRIAN_DETECTORS


class TrafficManagement:
    """
    Gym-Style Environment for DRL-Based Traffic Signal Control

    Provides a standardized interface for training Deep Reinforcement Learning agents
    to control traffic signals in a two-intersection urban corridor simulated in SUMO.

    Architecture:
        - Centralized control: Single agent controls both intersections
        - State space: 45 dimensions (combined from both intersections)
        - Action space: 4 discrete actions (applied to both intersections)
        - Reward: Multi-objective (waiting time, sync, equity, safety)

    Environment Type:
        - Multi-agent (2 intersections) with centralized policy
        - Partially observable (detector-based state)
        - Continuous time (1-second steps)
        - Stochastic (Poisson traffic arrivals)

    Integration:
        - Uses existing SignalSyncPro detector infrastructure
        - Compatible with Developed Control phase structure
        - Maintains bus priority and pedestrian detection logic
        - Enables fair comparison with baseline systems

    Lifecycle:
        1. __init__() - Configure environment parameters
        2. reset() - Start SUMO, initialize state
        3. Loop:
            - Agent: action = select_action(state)
            - Env: next_state, reward, done, info = step(action)
            - Agent: learn from (state, action, reward, next_state, done)
        4. close() - Terminate SUMO simulation

    Example Usage:
        # Training
        env = TrafficManagement("configurations/developed/common/signal_sync.sumocfg", ['3', '6'], gui=False)
        state = env.reset()

        for step in range(3600):
            action = agent.select_action(state)
            next_state, reward, done, info = env.step(action)
            agent.store_experience(state, action, reward, next_state, done, info)
            agent.train()
            state = next_state
            if done:
                break

        env.close()

        # Testing
        env = TrafficManagement("configurations/developed/common/signal_sync.sumocfg", ['3', '6'], gui=True)
        agent.set_eval_mode()
        state = env.reset()

        for step in range(10000):
            action = agent.select_action(state, explore=False)
            next_state, reward, done, info = env.step(action)
            state = next_state
            if done:
                break

        env.close()

    Attributes:
        sumo_config_file (str): Path to SUMO configuration file
        tls_ids (list): Traffic light IDs ['3', '6']
        gui (bool): Enable SUMO GUI visualization
        reward_calculator (RewardCalculator): Computes multi-objective rewards
        current_phase (dict): Current phase for each intersection
        phase_duration (dict): Seconds in current phase for each intersection
        green_steps (dict): Green time counter for each intersection
        sync_timer (dict): Coordination timer for each intersection
        sync_success_count (int): Number of successful synchronizations
        detector_info (dict): Detector layout from existing infrastructure
        ped_phase_detectors (dict): Pedestrian detector IDs
    """

    def __init__(self, sumo_config_file, tls_ids, gui=False):
        """
        Initialize Traffic Management Environment.

        Sets up the environment with SUMO configuration and traffic light IDs.
        Does NOT start SUMO - call reset() to begin simulation.

        Args:
            sumo_config_file (str): Path to SUMO configuration file
                Example: "configurations/developed/common/signal_sync.sumocfg"
                Must include network, routes, and simulation settings

            tls_ids (list of str): Traffic light signal IDs to control
                Example: ['3', '6'] for two-intersection corridor
                Must match IDs in SUMO network file

            gui (bool, optional): Enable SUMO GUI visualization
                Default: False (headless for faster training)
                Set True for testing/debugging to see traffic

        Initialization:
            - Stores configuration parameters
            - Creates reward calculator instance
            - Initializes tracking dictionaries for each intersection:
                * current_phase: Active signal phase
                * phase_duration: Time in current phase (seconds)
                * green_steps: Green time counter
                * sync_timer: Coordination countdown
            - Loads existing detector infrastructure

        Phase Structure:
            pOne (0-3):   Phase 1 - Major arterial through (North-South)
            pTwo (4-7):   Phase 2 - Major arterial left turns
            pThree (8-11): Phase 3 - Minor road through (East-West)
            pFour (12-15): Phase 4 - Minor road left turns
            16:           Pedestrian exclusive phase

        Detector Infrastructure:
            detectorInfo: Existing detector layout
                - 30m upstream: actuation detection
                - 100m upstream: approach detection
                - Separate detectors for vehicles and bicycles

            pedPhaseDetector: Pedestrian crossing detectors
                - Virtual loop detectors at crosswalks
                - 6m upstream from stop line
                - Triggers when ≥10 pedestrians waiting

        Synchronization:
            sync_timer: Countdown for green wave coordination
                - Set to 999999 initially (no coordination active)
                - Updated when intersection activates Phase 1
                - Other intersection aims to activate Phase 1 at offset time
                - Offset: 22 seconds (travel time between intersections)

        Example:
            # Training setup (no GUI)
            env = TrafficManagement(
                sumo_config_file="configurations/developed/common/signal_sync.sumocfg",
                tls_ids=['3', '6'],
                gui=False
            )

            # Testing setup (with GUI)
            env = TrafficManagement(
                sumo_config_file="configurations/developed/common/signal_sync.sumocfg",
                tls_ids=['3', '6'],
                gui=True
            )
        """
        self.sumo_config_file = sumo_config_file
        self.tls_ids = tls_ids
        self.gui = gui
        self.reward_calculator = RewardCalculator()

        # Phase tracking (from existing code)
        self.current_phase = {tls_id: PHASE_ONE for tls_id in tls_ids}
        self.phase_duration = {tls_id: 0 for tls_id in tls_ids}
        self.green_steps = {tls_id: 0 for tls_id in tls_ids}

        # NEW: Track stuck duration (time since last meaningful action)
        self.stuck_duration = {tls_id: 0 for tls_id in tls_ids}

        # DEBUG: Phase change tracking
        self.phase_change_count = 0
        self.blocked_action_count = 0
        self.total_action_count = 0

        # Synchronization tracking
        self.sync_timer = {tls_id: 999999 for tls_id in tls_ids}
        self.sync_success_count = 0

        # Detector infrastructure (from existing code)
        self.detector_info = DETECTORS_INFO
        self.ped_phase_detectors = PEDESTRIAN_DETECTORS

    def reset(self):
        """
        Reset environment and start new episode.

        Starts SUMO simulation, initializes traffic lights to Phase 1,
        and returns initial state observation.

        Process:
            1. Launch SUMO as subprocess (GUI or headless)
            2. Connect via TraCI on port 8816
            3. Initialize all traffic lights to Phase 1
            4. Reset phase counters and timers
            5. Extract and return initial state

        SUMO Startup:
            - Uses sumo-gui if self.gui=True, else sumo (headless)
            - Checks SUMO_BINDIR environment variable for binary location
            - Launches as subprocess with visible output
            - Waits 2 seconds for SUMO to start and open TraCI port

        TraCI Connection:
            - Port 8816 (must match signal_sync.sumocfg configuration)
            - Retries connection if initial attempt fails
            - Terminates SUMO subprocess on connection failure

        Initial State:
            - All intersections start in Phase 1 (major through)
            - All phase durations reset to 0
            - All sync timers reset to 999999 (no coordination)
            - Sync success counter reset to 0

        Returns:
            np.ndarray: Initial state vector [45 dims]
                Shape: (45,)
                Dtype: float32
                Range: [0, 1] (all features normalized)

        Raises:
            Exception: If SUMO fails to start or TraCI connection fails
                - SUMO subprocess is terminated on failure
                - Error message includes original exception details

        Example:
            env = TrafficManagement("configurations/developed/common/signal_sync.sumocfg", ['3', '6'])

            # Start new episode
            state = env.reset()
            print(f"Initial state shape: {state.shape}")  # (45,)
            print(f"State range: [{state.min():.2f}, {state.max():.2f}]")

            # State contains:
            # - Both intersections in Phase 1: [1,0,0,0,0, ...]
            # - Zero duration: [..., 0.0, ...]
            # - Initial queue lengths from traffic generation
            # - No pedestrian demand initially
            # - Buses may or may not be present (stochastic arrivals)

        Notes:
            - Call this at the start of each training/testing episode
            - Previous SUMO instance is automatically terminated
            - Traffic generation starts immediately (Poisson arrivals)
            - First few steps may have zero/low traffic (warm-up period)
        """
        # Start SUMO using subprocess (matching main.py approach)
        import subprocess
        import time

        sumo_binary = "sumo-gui" if self.gui else "sumo"

        # Check for SUMO_BINDIR (like main.py does)
        if "SUMO_BINDIR" in os.environ:
            sumo_binary = os.path.join(os.environ["SUMO_BINDIR"], sumo_binary)

        # Start SUMO as subprocess (keep output visible like main.py)
        sumo_cmd = [sumo_binary, "-c", self.sumo_config_file]
        self.sumo_process = subprocess.Popen(
            sumo_cmd, stdout=sys.stdout, stderr=sys.stderr
        )

        # Wait a bit for SUMO to start and open port
        time.sleep(2)

        # Connect via TraCI (port 8816 from signal_sync.sumocfg)
        try:
            traci.init(8816)
        except Exception as e:
            print(f"Failed to connect to SUMO: {e}")
            if hasattr(self, "sumo_process"):
                self.sumo_process.terminate()
            raise

        # Initialize traffic lights
        for tls_id in self.tls_ids:
            traci.trafficlight.setPhase(tls_id, PHASE_ONE)
            self.current_phase[tls_id] = PHASE_ONE
            self.phase_duration[tls_id] = 0
            self.green_steps[tls_id] = 0
            self.sync_timer[tls_id] = 999999
            self.stuck_duration[tls_id] = 0  # NEW: Reset stuck duration

        self.sync_success_count = 0

        return self._get_state()

    def _get_state(self):
        """
        Extract comprehensive state observation from SUMO.

        Constructs 45-dimensional state vector combining traffic conditions
        from both intersections with coordination features.

        State Vector Composition (for each intersection):
            Phase Information (6 dims):
                - Phase encoding (one-hot): [5 dims]
                  [is_phase1, is_phase2, is_phase3, is_phase4, is_ped_phase]

                  **Phase One-Hot Encoding Examples**

                    | Current Phase | Phase Description | is_phase1 | is_phase2 | is_phase3 | is_phase4 | is_ped_phase | Vector |
                    |---------------|-------------------|-----------|-----------|-----------|-----------|--------------|---------|
                    | 0 or 1 | Phase 1 (Major Through) | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | `[1, 0, 0, 0, 0]` |
                    | 4 or 5 | Phase 2 (Major Left) | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | `[0, 1, 0, 0, 0]` |
                    | 8 or 9 | Phase 3 (Minor Through) | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | `[0, 0, 1, 0, 0]` |
                    | 12 or 13 | Phase 4 (Minor Left) | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | `[0, 0, 0, 1, 0]` |
                    | 16 | Phase 5 (Pedestrian Exclusive) | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | `[0, 0, 0, 0, 1]` |

                    **SUMO Phase Mapping**

                    Each main phase has 4 SUMO indices (leading green, green, yellow, all-red):
                    - **Phase 1**: Indices 0, 1, 2, 3 → All encode as `[1, 0, 0, 0, 0]`
                    - **Phase 2**: Indices 4, 5, 6, 7 → All encode as `[0, 1, 0, 0, 0]`
                    - **Phase 3**: Indices 8, 9, 10, 11 → All encode as `[0, 0, 1, 0, 0]`
                    - **Phase 4**: Indices 12, 13, 14, 15 → All encode as `[0, 0, 0, 1, 0]`
                    - **Pedestrian**: Index 16 → Encodes as `[0, 0, 0, 0, 1]`

                    The encoding simplifies SUMO's 20 phases into 5 conceptual phases for the neural network.


                    **SUMO Phase Index Explanation**

                    **SUMO uses 20 phase indices (0-19).** Each main phase spans 4 consecutive indices:

                    | SUMO Index | Sub-Phase | Description | One-Hot Encoding |
                    |------------|-----------|-------------|------------------|
                    | **0** | Phase 1 - Leading Green Start | Major through starting | `[1, 0, 0, 0, 0]` |
                    | **1** | Phase 1 - Green Active | Major through main green | `[1, 0, 0, 0, 0]` |
                    | 2 | Phase 1 - Yellow | Major through clearance | `[1, 0, 0, 0, 0]` |
                    | 3 | Phase 1 - All-red | Major through clearance | `[1, 0, 0, 0, 0]` |
                    | **4** | Phase 2 - Leading Green Start | Major left starting | `[0, 1, 0, 0, 0]` |
                    | **5** | Phase 2 - Green Active | Major left main green | `[0, 1, 0, 0, 0]` |
                    | 6 | Phase 2 - Yellow | Major left clearance | `[0, 1, 0, 0, 0]` |
                    | 7 | Phase 2 - All-red | Major left clearance | `[0, 1, 0, 0, 0]` |
                    | **8** | Phase 3 - Leading Green Start | Minor through starting | `[0, 0, 1, 0, 0]` |
                    | **9** | Phase 3 - Green Active | Minor through main green | `[0, 0, 1, 0, 0]` |
                    | 10 | Phase 3 - Yellow | Minor through clearance | `[0, 0, 1, 0, 0]` |
                    | 11 | Phase 3 - All-red | Minor through clearance | `[0, 0, 1, 0, 0]` |
                    | **12** | Phase 4 - Leading Green Start | Minor left starting | `[0, 0, 0, 1, 0]` |
                    | **13** | Phase 4 - Green Active | Minor left main green | `[0, 0, 0, 1, 0]` |
                    | 14 | Phase 4 - Yellow | Minor left clearance | `[0, 0, 0, 1, 0]` |
                    | 15 | Phase 4 - All-red | Minor left clearance | `[0, 0, 0, 1, 0]` |
                    | **16** | Phase 5 - Pedestrian | Pedestrian exclusive | `[0, 0, 0, 0, 1]` |

                    **Key Point**

                    **"0 or 1"** means: *If SUMO reports current phase is 0 OR if SUMO reports current phase is 1, both get the SAME encoding.*

                    We only care about which **main phase** is active, not whether it's in leading green, yellow, or all-red. The neural network treats indices 0, 1, 2, 3 all as "Phase 1".

                - Phase duration (normalized): [1 dim]
                  min(duration / 60.0, 1.0)  # Capped at 60 seconds

            Vehicle Detection (8 dims):
                - Vehicle queues: [4 dims]
                  One per approach direction (N, S, E, W)
                  Binary occupancy from detector last detection time
                - Bicycle queues: [4 dims]
                  One per approach direction
                  Binary occupancy from bicycle-specific detectors

            Pedestrian & Transit (2 dims):
                - Pedestrian demand: [1 dim]
                  Binary: 1.0 if pedestrians waiting, else 0.0
                - Bus presence: [1 dim]
                  Binary: 1.0 if bus on priority lane, else 0.0

            Coordination (2 dims):
                - Sync timer (normalized): [1 dim]
                  min(timer / 30.0, 1.0)  # Coordination window
                - Time of day (normalized): [1 dim]
                  (sim_time % 3600) / 3600.0  # Within-hour cycle

        Total: (6 + 8 + 2 + 2) × 2 intersections = ~36 core dims
               + coordination features ≈ 45 total dimensions

        Detector Logic:
            Queue Detection:
                - Checks detector last detection time
                - If < 3.0 seconds: queue present (1.0)
                - If ≥ 3.0 seconds: queue cleared (0.0)

            Pedestrian Detection:
                - Checks pedestrian detector mean speed
                - If speed < 0.1 m/s: waiting (1.0)
                - If speed ≥ 0.1 m/s or no detection: not waiting (0.0)

            Bus Detection:
                - Checks vehicle IDs on bus priority lanes
                - If vehicle type is 'bus': present (1.0)
                - Otherwise: not present (0.0)

        Returns:
            np.ndarray: State vector
                Shape: (45,)
                Dtype: float32
                Range: [0, 1] for all features

        Example State Interpretation:
            state = env._get_state()

            # Intersection 3 (first ~22 dims)
            state[0:5]   # Phase: [1,0,0,0,0] → Phase 1 active
            state[5]     # Duration: 0.25 → 15 seconds into phase
            state[6:10]  # Vehicle queues: [0.8, 0.3, 0.0, 0.5]
            state[10:14] # Bicycle queues: [0.6, 0.2, 0.0, 0.3]
            state[14]    # Pedestrians: 1.0 → waiting
            state[15]    # Bus: 0.0 → not present
            state[16]    # Sync timer: 0.6 → 18 seconds until coordination
            state[17]    # Time: 0.42 → 25.2 minutes into hour

            # Intersection 6 (next ~22 dims)
            state[18:23] # Phase: [0,1,0,0,0] → Phase 2 active
            # ... similar structure

        Notes:
            - Called by reset() for initial state
            - Called by step() after each action
            - All features normalized to [0,1] for neural network input
            - Missing/failed detector reads default to 0.0 (safe fallback)
            - Phase encoding uses green phases only (leading green)
        """
        state_features = []

        for node_idx, tls_id in enumerate(self.tls_ids):
            # Current phase information
            current_phase = self.current_phase[tls_id]
            phase_duration = self.phase_duration[tls_id]

            # One-hot encode current phase
            phase_encoding = self._encode_phase(current_phase)
            state_features.extend(phase_encoding)

            # Normalized phase duration
            state_features.append(min(phase_duration / 60.0, 1.0))

            # Queue lengths from detectors
            vehicle_queues = self._get_detector_queues(
                node_idx, current_phase, "vehicle"
            )
            bicycle_queues = self._get_detector_queues(
                node_idx, current_phase, "bicycle"
            )

            state_features.extend(vehicle_queues)
            state_features.extend(bicycle_queues)

            # Pedestrian detection
            ped_demand = self._get_pedestrian_demand(node_idx)
            state_features.append(ped_demand)

            # Bus presence detection
            bus_present = self._check_bus_presence_in_lanes(node_idx)
            state_features.append(float(bus_present))

            # Synchronization timer
            sync_timer_normalized = min(self.sync_timer[tls_id] / 30.0, 1.0)
            state_features.append(sync_timer_normalized)

            # Time of day (simulation time)
            sim_time = traci.simulation.getTime()
            time_normalized = (sim_time % 3600) / 3600.0  # Normalized within hour
            state_features.append(time_normalized)

        return np.array(state_features, dtype=np.float32)

    def _encode_phase(self, phase):
        """
        Convert SUMO phase index to one-hot encoding.

        Maps SUMO phase numbers (which include leading green, yellow, all-red)
        to simplified one-hot encoding of main green phases.

        Phase Mapping:
            Phase 1 (Major Through):      0, 1 → [1, 0, 0, 0, 0]
            Phase 2 (Major Left):          4, 5 → [0, 1, 0, 0, 0]
            Phase 3 (Minor Through):       8, 9 → [0, 0, 1, 0, 0]
            Phase 4 (Minor Left):         12,13 → [0, 0, 0, 1, 0]
            Pedestrian Phase:             16    → [0, 0, 0, 0, 1]

        SUMO Phase Structure (per main phase):
            0: Leading green start
            1: Leading green active (main green signal)
            2: Yellow clearance
            3: All-red clearance

        Args:
            phase (int): Current SUMO phase index
                Range: 0-19 (full phase sequence)
                Main phases: 0-1 (P1), 4-5 (P2), 8-9 (P3), 12-13 (P4), 16 (Ped)

        Returns:
            list: One-hot encoded phase [5 floats]
                Length: 5 (four main phases + pedestrian)
                Values: 0.0 or 1.0
                Sum: always 1.0 (exactly one phase active)

        Example:
            # Phase 1 active (major through green)
            encoding = self._encode_phase(1)
            assert encoding == [1.0, 0.0, 0.0, 0.0, 0.0]

            # Phase 3 active (minor through green)
            encoding = self._encode_phase(9)
            assert encoding == [0.0, 0.0, 1.0, 0.0, 0.0]

            # Pedestrian phase active
            encoding = self._encode_phase(16)
            assert encoding == [0.0, 0.0, 0.0, 0.0, 1.0]

        Notes:
            - Only green phases are encoded (yellow/all-red treated as part of green phase)
            - Simplifies state space from 20 phases to 5 conceptual phases
            - Neural network learns phase progression patterns more easily
        """
        phases = [
            PHASE_ONE,
            PHASE_TWO,
            PHASE_THREE,
            PHASE_FOUR,
            16,
        ]  # 16 = pedestrian phase
        encoding = [0.0] * len(phases)

        # Map to green phase
        if phase in [0, 1]:  # Phase 1
            encoding[0] = 1.0
        elif phase in [4, 5]:  # Phase 2
            encoding[1] = 1.0
        elif phase in [8, 9]:  # Phase 3
            encoding[2] = 1.0
        elif phase in [12, 13]:  # Phase 4
            encoding[3] = 1.0
        elif phase == 16:  # Pedestrian phase
            encoding[4] = 1.0

        return encoding

    def _get_detector_queues(self, node_idx, current_phase, vehicle_type):
        """
        Get queue lengths from induction loop detectors.

        Reads detector occupancy for the currently active phase and returns
        binary queue indicators for each approach.

        Detector Selection:
            - Detectors vary by phase (each phase serves different approaches)
            - Uses existing detector infrastructure from detectorInfo
            - Phase 1: Major through detectors
            - Phase 2: Major left turn detectors
            - Phase 3: Minor through detectors
            - Phase 4: Minor left turn detectors

        Queue Detection Logic:
            - Query last detection time for each detector
            - If last_detection < 3.0 seconds: queue present (1.0)
            - If last_detection ≥ 3.0 seconds: queue cleared (0.0)
            - Failed detector reads default to 0.0 (safe assumption)

        Args:
            node_idx (int): Intersection index (0 or 1)
                0 → Intersection '3'
                1 → Intersection '6'

            current_phase (int): Active SUMO phase (0-19)
                Determines which detector set to query

            vehicle_type (str): Type of vehicles to detect
                'vehicle' → Cars and general vehicles
                'bicycle' → Bicycles on dedicated bicycle detectors
                (Currently not differentiated in detector reading)

        Returns:
            list: Queue occupancy indicators [4 floats]
                Length: 4 (one per approach direction)
                Values: 0.0 (no queue) or 1.0 (queue present)
                Padded/truncated to exactly 4 values

        Example:
            # Intersection 0, Phase 1 active
            queues = self._get_detector_queues(0, 1, 'vehicle')
            # Returns: [1.0, 0.0, 0.0, 1.0]
            # Interpretation:
            #   - North approach: queue (1.0)
            #   - South approach: clear (0.0)
            #   - East approach: clear (0.0)
            #   - West approach: queue (1.0)

        Error Handling:
            - Try-except wraps all detector queries
            - Missing detectors → returns [0.0, 0.0, 0.0, 0.0]
            - Failed detector reads → individual detector returns 0.0
            - Ensures state vector always has correct dimensionality

        Notes:
            - Uses 30m upstream detectors for actuation
            - Detection threshold (3.0 sec) balances responsiveness vs noise
            - Binary representation simplifies state space
            - Real queue lengths not used (occupancy sufficient for DRL)
        """
        queues = []

        try:
            if current_phase in [0, 1]:
                detector_list = self.detector_info[PHASE_ONE][node_idx]
            elif current_phase in [4, 5]:
                detector_list = self.detector_info[PHASE_TWO][node_idx]
            elif current_phase in [8, 9]:
                detector_list = self.detector_info[PHASE_THREE][node_idx]
            elif current_phase in [12, 13]:
                detector_list = self.detector_info[PHASE_FOUR][node_idx]
            else:
                return [0.0] * 4

            # Count vehicles at detectors
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

        # Pad or truncate to fixed size
        while len(queues) < 4:
            queues.append(0.0)
        return queues[:4]

    def _get_pedestrian_demand(self, node_idx):
        """
        Check if pedestrians are waiting at crosswalks.

        Queries pedestrian detection loops at crossing points to determine
        if pedestrian phase should be activated.

        Detection Method:
            - Reads mean speed from pedestrian detectors
            - Speed < 0.1 m/s → pedestrians waiting (stopped/slow)
            - Speed ≥ 0.1 m/s or no detection → no pedestrians

        Detector Locations:
            - Virtual loop detectors at each crosswalk
            - 6m upstream from stop line
            - Covers entire crosswalk width

        Args:
            node_idx (int): Intersection index (0 or 1)
                Maps to ped_phase_detectors[node_idx]

        Returns:
            float: Pedestrian demand indicator
                1.0 → Pedestrians waiting (activate Phase 5)
                0.0 → No pedestrians (continue regular sequence)

        Example:
            # Check pedestrian demand at intersection 0
            demand = self._get_pedestrian_demand(0)
            if demand == 1.0:
                print("Pedestrians waiting - consider activating Phase 5")

        Activation Logic (in DRL agent):
            - High demand (1.0) → Agent may select Action 3 (pedestrian phase)
            - Low demand (0.0) → Agent focuses on vehicle phases
            - Reward function incentivizes serving waiting pedestrians

        Error Handling:
            - Try-except on each detector query
            - Failed reads skip to next detector
            - Returns 0.0 if all detectors fail (safe default)

        Notes:
            - Matches existing Developed Control pedestrian detection logic
            - Compatible with thesis pedestrian priority phase implementation
            - Detection threshold (0.1 m/s) filters moving pedestrians
            - Returns binary signal (not pedestrian count)
        """
        try:
            ped_detectors = self.ped_phase_detectors[node_idx]
            for det_id in ped_detectors:
                try:
                    speed = traci.inductionloop.getLastStepMeanSpeed(det_id)
                    if speed != -1 and speed < 0.1:
                        return 1.0
                except:  # noqa: E722
                    continue
        except:  # noqa: E722
            pass
        return 0.0

    def _check_bus_presence_in_lanes(self, node_idx):
        """
        Detect if bus is on priority approach lane.

        Checks bus priority lanes for presence of transit vehicles to enable
        bus priority signal control (early green or phase skip).

        Detection Method:
            - Queries vehicle IDs on bus priority lanes
            - Checks vehicle type for each ID
            - Returns True if any vehicle has type 'bus'

        Bus Priority Lanes:
            - Defined in tls_constants.busPriorityLane
            - Typically major arterial approach lanes
            - Allows buses to request priority

        Args:
            node_idx (int): Intersection index (0 or 1)
                Maps to busPriorityLane[node_idx]

        Returns:
            bool: Bus presence indicator
                True → Bus detected on priority lane
                False → No bus detected

        Example:
            # Check bus presence at intersection 1
            bus_present = self._check_bus_presence_in_lanes(1)
            if bus_present:
                print("Bus detected - consider priority treatment")
                # Agent may skip to Phase 1 for green wave

        Priority Treatment Options:
            - Phase skip to Phase 1 (Action 1) for bus progression
            - Extended green for bus clearance
            - Early green activation for upstream bus
            - Coordination with other intersection for platoon flow

        Error Handling:
            - Try-except wraps entire detection
            - Missing lane data → returns False
            - Failed vehicle queries → continues to next lane
            - Safe default: no priority without confirmed detection

        Notes:
            - Matches existing Developed Control bus priority logic
            - Compatible with thesis bus prioritization implementation
            - 15-minute bus frequency in test scenarios
            - Reward function includes bus waiting time with higher weight (1.5x)
        """
        from constants.developed.common.tls_constants import BUS_PRIORITY_LANE

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
        """
        Execute action and advance simulation by one timestep.

        Applies the selected action to both traffic lights, advances SUMO
        simulation by 1 second, and returns next state with reward.

        Action Execution Flow:
            1. Get current simulation time
            2. Execute action for both intersections (coordinated)
            3. Advance SUMO simulation by 1 step (1 second)
            4. Update phase duration counters
            5. Update synchronization timers
            6. Extract next state observation
            7. Calculate reward from traffic conditions
            8. Check episode termination
            9. Return (next_state, reward, done, info)

        Action Mapping:
            0: Continue current phase
               - No phase change
               - Phase duration increments
               - Useful when traffic clearing efficiently

            1: Skip to Phase 1 (major through)
               - Forces transition to Phase 1
               - Enables synchronization and green wave
               - Only if MIN_GREEN_TIME satisfied

            2: Progress to next phase
               - Advances in sequence: 1→2→3→4→1
               - Balanced service for all movements
               - Only if MIN_GREEN_TIME satisfied

            3: Activate pedestrian phase
               - Triggers dedicated pedestrian crossing
               - High priority for waiting pedestrians
               - Only if MIN_GREEN_TIME satisfied

        Safety Constraints:
            - MIN_GREEN_TIME (5 seconds) enforced for all actions
            - Actions 1, 2, 3 only execute if current phase ≥ 5 seconds
            - Prevents rapid phase changes that confuse drivers
            - Automatic yellow/all-red clearance inserted by SUMO

        Synchronization Update:
            - When intersection activates Phase 1, sets sync timer for other
            - Timer = current_time + 22 seconds (travel time offset)
            - Other intersection aims to reach Phase 1 at timer expiration
            - Enables green wave progression along corridor

        Args:
            action (int): Selected action index
                Range: [0, 3]
                0 = Continue, 1 = Skip to P1, 2 = Next, 3 = Pedestrian

        Returns:
            tuple: (next_state, reward, done, info)

            next_state (np.ndarray): Updated state observation
                Shape: (45,)
                Dtype: float32
                Range: [0, 1]

            reward (float): Scalar reward signal
                Typical range: -50 to +20
                Negative: penalties (waiting time, CO₂)
                Positive: bonuses (sync success, low waiting)

            done (bool): Episode termination flag
                True: No more vehicles expected (simulation complete)
                False: Episode continues

            info (dict): Additional information
                Keys may include:
                    'event_type': str - Event classification for PER
                        'normal', 'ped_phase', 'sync_success',
                        'sync_failure', 'bus_conflict', 'safety_violation'
                    'sync_success': bool - Coordination achieved
                    'waiting_times': dict - Per-mode waiting times
                    'emissions': float - CO₂ emissions this step

        Example:
            # Training loop
            state = env.reset()
            total_reward = 0

            for step in range(3600):
                # Agent selects action
                action = agent.select_action(state)

                # Execute action in environment
                next_state, reward, done, info = env.step(action)

                # Store experience for learning
                agent.store_experience(state, action, reward,
                                      next_state, done, info)

                # Update state and accumulate reward
                state = next_state
                total_reward += reward

                # Check termination
                if done:
                    print(f"Episode finished. Total reward: {total_reward}")
                    break

        Timestep Details:
            - Each step = 1 second simulation time
            - Episode typically 3600 steps (1 hour) for training
            - Episode typically 10000 steps (2.78 hours) for testing
            - Real-time factor depends on hardware (typically 5-50x faster)

        Notes:
            - Actions applied to both intersections (centralized control)
            - Phase changes respect minimum green time (safety)
            - Synchronization emerges from reward signal and sync timers
            - SUMO handles vehicle movements, emissions, collisions automatically
        """
        step_time = traci.simulation.getTime()

        # HYBRID MAX_GREEN CONSTRAINT (Oct 21, 2025)
        # Check if any intersection has exceeded MAX_GREEN and force phase change
        forced_changes = {}
        for tls_id in self.tls_ids:
            current_phase = self.current_phase[tls_id]
            duration = self.phase_duration[tls_id]
            max_green = DRLConfig.MAX_GREEN_TIME.get(current_phase, 44)

            if duration >= max_green:
                # HARD CONSTRAINT: Force phase change regardless of agent action
                next_phase = self._get_next_phase(current_phase)
                print(
                    f"[MAX_GREEN FORCED] TLS {tls_id}: Phase {current_phase} → {next_phase} "
                    f"(duration {duration}s >= MAX {max_green}s) 🔴 FORCED CHANGE"
                )
                traci.trafficlight.setPhase(tls_id, next_phase)
                self.current_phase[tls_id] = next_phase
                self.phase_duration[tls_id] = 0
                self.green_steps[tls_id] = 0
                self.phase_change_count += 1
                forced_changes[tls_id] = True
            else:
                forced_changes[tls_id] = False

        # Execute action for all intersections (only if not forced)
        blocked_penalties = []
        action_changed = False  # Track if any meaningful action occurred
        for tls_id in self.tls_ids:
            if not forced_changes[tls_id]:  # Only execute if not forced
                penalty, changed = self._execute_action_for_tls(
                    tls_id, action, step_time
                )
                blocked_penalties.append(penalty)
                if changed:
                    action_changed = True
            else:
                # Forced change counts as action_changed
                blocked_penalties.append(0.0)
                action_changed = True

        # Advance simulation by 1 second
        traci.simulationStep()

        # Update phase durations and stuck duration
        for tls_id in self.tls_ids:
            self.phase_duration[tls_id] += 1
            self.green_steps[tls_id] += 1

            # NEW: Update stuck duration (time since last meaningful action)
            if action_changed:
                self.stuck_duration[tls_id] = 0  # Reset on meaningful action
            else:
                self.stuck_duration[tls_id] += 1  # Increment if just continuing

        # Update synchronization timer
        self._update_sync_timer(step_time)

        # Get new state
        next_state = self._get_state()

        # Calculate average blocked penalty across intersections
        avg_blocked_penalty = (
            sum(blocked_penalties) / len(blocked_penalties)
            if blocked_penalties
            else 0.0
        )

        # Calculate reward (pass phase_durations for safety checks and blocked penalty)
        reward, info = self.reward_calculator.calculate_reward(
            traci,
            self.tls_ids,
            action,
            self.current_phase,
            self.phase_duration,
            blocked_penalty=avg_blocked_penalty,
            stuck_durations=self.stuck_duration,  # NEW: Pass stuck durations
        )

        # Check if episode done
        done = traci.simulation.getMinExpectedNumber() == 0

        return next_state, reward, done, info

    def _execute_action_for_tls(self, tls_id, action, step_time):
        """
        Execute specific action for one traffic light.

        Applies the action to a single intersection while respecting safety
        constraints (minimum green time).

        Args:
            tls_id (str): Traffic light ID ('3' or '6')
            action (int): Action to execute (0-3)
            step_time (float): Current simulation time (seconds)

        Returns:
            tuple: (blocked_penalty, action_changed)
                blocked_penalty (float): 0.0 if action executed or Continue,
                    -ALPHA_BLOCKED if action blocked due to MIN_GREEN_TIME
                action_changed (bool): True if phase actually changed

        Action Implementation:
            Action 0 (Continue):
                - No-op: phase remains unchanged
                - Duration counter continues incrementing

            Action 1 (Skip to Phase 1):
                - Changes phase to pOne (0: leading green)
                - Only if current_phase != pOne (avoid redundant skip)
                - Only if phase_duration >= MIN_GREEN_TIME (5 sec)
                - Resets phase counters to 0

            Action 2 (Next Phase):
                - Calls _get_next_phase() for sequence
                - Only if phase_duration >= MIN_GREEN_TIME
                - Resets phase counters to 0

            Action 3 (Pedestrian Phase):
                - Changes phase to 16 (pedestrian exclusive)
                - Only if phase_duration >= MIN_GREEN_TIME
                - Resets phase counters to 0

        Safety Enforcement:
            - MIN_GREEN_TIME check prevents premature phase changes
            - Protects against driver confusion and unsafe clearance
            - SUMO automatically inserts yellow and all-red intervals

        State Updates:
            - self.current_phase[tls_id] updated to new phase
            - self.phase_duration[tls_id] reset to 0 on phase change
            - self.green_steps[tls_id] reset to 0 on phase change

        Example Execution:
            # Action 1: Skip to Phase 1
            # Current: Phase 3, Duration 8 sec
            self._execute_action_for_tls('3', 1, 100.5)
            # Result:
            #   - traci.trafficlight.setPhase('3', 0)  # pOne = 0
            #   - self.current_phase['3'] = 0
            #   - self.phase_duration['3'] = 0
            #   - self.green_steps['3'] = 0

            # Action 0: Continue
            # Current: Phase 1, Duration 3 sec
            self._execute_action_for_tls('3', 0, 103.5)
            # Result: No changes, duration continues incrementing

        Notes:
            - Called by step() for each intersection
            - Centralized control: same action applied to both
            - Phase changes trigger SUMO's internal yellow/clearance logic
            - Synchronization coordination handled by _update_sync_timer()
        """
        current_phase = self.current_phase[tls_id]
        self.total_action_count += 1
        blocked_penalty = 0.0  # Track if action was blocked
        action_changed = False  # NEW: Track if action caused phase change

        if action == 0:  # Continue current phase
            pass  # No change, no penalty

        elif action == 1:  # Skip to Phase 1
            duration = self.phase_duration[tls_id]
            if current_phase != PHASE_ONE and duration >= MIN_GREEN_TIME:
                print(
                    f"[PHASE CHANGE] TLS {tls_id}: Phase {current_phase} → {PHASE_ONE} (Skip to P1), Duration: {duration}s ✓"
                )
                traci.trafficlight.setPhase(tls_id, PHASE_ONE)
                self.current_phase[tls_id] = PHASE_ONE
                self.phase_duration[tls_id] = 0
                self.green_steps[tls_id] = 0
                self.phase_change_count += 1
                action_changed = True  # NEW: Phase changed
            elif current_phase != PHASE_ONE:
                print(
                    f"[BLOCKED] TLS {tls_id}: Cannot skip to P1 (duration={duration}s < MIN_GREEN_TIME={MIN_GREEN_TIME}s) ⚠️"
                )
                self.blocked_action_count += 1
                blocked_penalty = -DRLConfig.ALPHA_BLOCKED  # Penalize blocked action
            else:
                # FIX: Redundant action penalty - already in Phase 1 (Phase 3 Oct 23, 2025)
                print(
                    f"[REDUNDANT] TLS {tls_id}: Already in Phase 1, Skip2P1 is redundant ⚠️"
                )
                self.blocked_action_count += 1
                blocked_penalty = (
                    -DRLConfig.ALPHA_BLOCKED
                )  # Same penalty as blocked action

        elif action == 2:  # Next phase
            duration = self.phase_duration[tls_id]
            if duration >= MIN_GREEN_TIME:
                next_phase = self._get_next_phase(current_phase)
                print(
                    f"[PHASE CHANGE] TLS {tls_id}: Phase {current_phase} → {next_phase} (Next), Duration: {duration}s ✓"
                )
                traci.trafficlight.setPhase(tls_id, next_phase)
                self.current_phase[tls_id] = next_phase
                self.phase_duration[tls_id] = 0
                self.green_steps[tls_id] = 0
                self.phase_change_count += 1
                action_changed = True  # NEW: Phase changed
            else:
                print(
                    f"[BLOCKED] TLS {tls_id}: Cannot advance phase (duration={duration}s < MIN_GREEN_TIME={MIN_GREEN_TIME}s) ⚠️"
                )
                self.blocked_action_count += 1
                blocked_penalty = -DRLConfig.ALPHA_BLOCKED  # Penalize blocked action

        elif action == 3:  # Pedestrian phase
            duration = self.phase_duration[tls_id]
            if duration >= MIN_GREEN_TIME:
                print(
                    f"[PHASE CHANGE] TLS {tls_id}: Phase {current_phase} → 16 (Pedestrian), Duration: {duration}s ✓"
                )
                traci.trafficlight.setPhase(tls_id, 16)
                self.current_phase[tls_id] = 16
                self.phase_duration[tls_id] = 0
                self.green_steps[tls_id] = 0
                self.phase_change_count += 1
                action_changed = True  # NEW: Phase changed
            else:
                print(
                    f"[BLOCKED] TLS {tls_id}: Cannot activate ped phase (duration={duration}s < MIN_GREEN_TIME={MIN_GREEN_TIME}s) ⚠️"
                )
                self.blocked_action_count += 1
                blocked_penalty = -DRLConfig.ALPHA_BLOCKED  # Penalize blocked action

        return blocked_penalty, action_changed  # NEW: Return tuple

    def _get_next_phase(self, current_phase):
        """
        Determine next phase in cyclic sequence.

        Implements circular phase progression: P1 → P2 → P3 → P4 → P1

        Phase Progression:
            Phase 1 (0-3)   → Phase 2 (4)   # Major through → Major left
            Phase 2 (4-7)   → Phase 3 (8)   # Major left → Minor through
            Phase 3 (8-11)  → Phase 4 (12)  # Minor through → Minor left
            Phase 4 (12-15) → Phase 1 (0)   # Minor left → Major through
            Pedestrian (16) → Phase 1 (0)   # Ped exclusive → Major through

        Args:
            current_phase (int): Active SUMO phase index (0-19)

        Returns:
            int: Next phase leading green index
                Returns: 0, 4, 8, or 12 (leading green starts)
                SUMO automatically advances through green/yellow/clearance

        Example:
            # Currently in Phase 1 (major through)
            next_phase = self._get_next_phase(1)
            assert next_phase == 4  # Phase 2 leading green

            # Currently in Phase 4 (minor left)
            next_phase = self._get_next_phase(13)
            assert next_phase == 0  # Back to Phase 1

            # Currently in pedestrian phase
            next_phase = self._get_next_phase(16)
            assert next_phase == 0  # Resume with Phase 1

        Phase Index Details:
            Each main phase spans 4 SUMO indices:
                0: Leading green start
                1: Leading green active (main green)
                2: Yellow clearance
                3: All-red clearance

            Example for Phase 1 (Major Through):
                Index 0: P1 leading green start
                Index 1: P1 leading green active ← encoded as "Phase 1"
                Index 2: P1 yellow
                Index 3: P1 all-red

        Notes:
            - Always returns leading green start (0, 4, 8, 12)
            - SUMO handles progression through green/yellow/clearance
            - Circular sequence ensures all movements serviced
            - Pedestrian phase returns to Phase 1 (major arterial priority)
        """
        if current_phase in [0, 1, 2, 3]:  # Phase 1
            return 4  # Phase 2 leading green
        elif current_phase in [4, 5, 6, 7]:  # Phase 2
            return 8  # Phase 3 leading green
        elif current_phase in [8, 9, 10, 11]:  # Phase 3
            return 12  # Phase 4 leading green
        elif current_phase in [12, 13, 14, 15]:  # Phase 4
            return 0  # Phase 1 leading green
        else:  # Pedestrian or other
            return 0  # Default to Phase 1

    def _update_sync_timer(self, step_time):
        """
        Update synchronization timers for green wave coordination.

        Implements semi-synchronization logic where activation of Phase 1
        at one intersection sets coordination target for the other intersection.

        Coordination Strategy:
            - When Intersection A activates Phase 1 (major through):
                → Set sync_timer for Intersection B = current_time + 22 seconds
            - Intersection B should aim to activate Phase 1 at sync_timer time
            - Offset of 22 seconds matches travel time between intersections
            - Enables green wave progression along corridor

        Timer Update Logic:
            For each intersection:
                If current_phase == pOne (major through green):
                    → Set other intersection's sync_timer
                    → sync_timer = current_time + 22

        Args:
            step_time (float): Current simulation time (seconds)

        Example Scenario:
            Time 100s: Intersection 3 activates Phase 1
                → sync_timer['6'] = 100 + 22 = 122

            Time 122s: Intersection 6 should activate Phase 1
                → Achieves coordination
                → Vehicles from Intersection 3 arrive at green light

        Coordination Rewards:
            - Reward calculator checks if sync_timer reached
            - Bonus reward for activating Phase 1 near sync_timer
            - Penalty for missing coordination opportunity
            - Encourages agent to learn green wave timing

        Timer Usage in State:
            - sync_timer included in state observation (normalized)
            - Agent learns to use timer as coordination cue
            - Low timer value → consider skipping to Phase 1 (Action 1)
            - High timer value → continue normal phase sequence

        Notes:
            - Initial sync_timer = 999999 (no coordination active)
            - Timer updates continuously as intersections activate Phase 1
            - Compatible with existing Developed Control semi-sync logic
            - Offset (22 sec) based on 300m spacing at ~13.6 m/s (49 km/h)
        """
        for idx, tls_id in enumerate(self.tls_ids):
            if self.current_phase[tls_id] == PHASE_ONE:
                # Set sync time for other intersection
                other_idx = 1 - idx
                other_tls_id = self.tls_ids[other_idx]
                self.sync_timer[other_tls_id] = step_time + 22  # Coordination offset

    def close(self):
        """
        Close SUMO connection and terminate simulation.

        Cleanly shuts down TraCI connection and terminates SUMO subprocess.
        Should be called at the end of each episode or when environment no
        longer needed.

        Shutdown Process:
            1. Close TraCI connection (graceful)
            2. Terminate SUMO subprocess (SIGTERM)
            3. Wait up to 5 seconds for clean exit
            4. Force kill if still running (SIGKILL)

        Error Handling:
            - Try-except wraps all shutdown operations
            - Continues to subprocess termination even if TraCI close fails
            - Force kill ensures no orphaned SUMO processes

        Example:
            # Training loop
            env = TrafficManagement("configurations/developed/common/signal_sync.sumocfg", ['3', '6'])

            try:
                state = env.reset()
                for step in range(3600):
                    action = agent.select_action(state)
                    next_state, reward, done, info = env.step(action)
                    state = next_state
                    if done:
                        break
            finally:
                env.close()  # Always close, even on error

            # Multiple episodes
            for episode in range(100):
                state = env.reset()  # Starts new SUMO instance
                # ... training ...
                env.close()  # Clean shutdown

        Notes:
            - Called automatically by __del__ if forgotten
            - Important for preventing SUMO process accumulation
            - Releases port 8816 for next episode
            - Flushes any pending SUMO output/logs
            - Safe to call multiple times (idempotent)
        """
        # Print episode summary before closing
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

        # Print safety violation summary
        self.reward_calculator.print_safety_summary()

        # Reset counters for next episode
        self.phase_change_count = 0
        self.blocked_action_count = 0
        self.total_action_count = 0

        try:
            traci.close()
        except:  # noqa: E722
            pass

        # Terminate SUMO subprocess if it exists
        if hasattr(self, "sumo_process"):
            try:
                self.sumo_process.terminate()
                self.sumo_process.wait(timeout=5)
            except:  # noqa: E722
                try:
                    self.sumo_process.kill()
                except:  # noqa: E722
                    pass
