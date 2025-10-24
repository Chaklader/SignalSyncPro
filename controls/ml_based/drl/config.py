"""
DRL Configuration Parameters

Note: Training constants (NUM_EPISODES_TRAIN, SIMULATION_LIMIT_TRAIN, etc.)
and safety thresholds (MIN_GREEN_TIME, SAFE_HEADWAY, etc.) are now in
constants/constants.py and should be imported directly where needed.
"""


class DRLConfig:
    """
    Deep Reinforcement Learning Configuration Parameters

    Hyperparameters for DQN agent training on traffic signal control.
    Optimized for multimodal traffic management with focus on vehicle waiting time.

    Architecture:
        STATE_DIM: Dimensionality of state space (traffic features)
        ACTION_DIM: Number of discrete actions available to agent
        HIDDEN_LAYERS: Neural network architecture (layer sizes)

    DQN Hyperparameters:
        LEARNING_RATE: Step size for gradient descent optimization
        GAMMA: Discount factor for future rewards (0.95 = 5% discount per step)
        EPSILON_START: Initial exploration rate (100% random actions)
        EPSILON_END: Minimum exploration rate after decay
        EPSILON_DECAY: Exponential decay rate per episode
        TAU: Soft update rate for target network (0.005 = 0.5% update per step)

    Replay Buffer:
        BUFFER_SIZE: Maximum number of experiences stored
        BATCH_SIZE: Number of experiences sampled per training step
        MIN_BUFFER_SIZE: Minimum experiences before training begins

    Prioritized Experience Replay:
        ALPHA: Prioritization exponent (0 = uniform, 1 = full prioritization)
        BETA_START: Initial importance sampling correction
        BETA_FRAMES: Number of frames to anneal beta to 1.0
        EPSILON_PER: Small constant added to priorities for numerical stability

    Reward Weights (Multi-Objective Optimization):
        ALPHA_WAIT: Weight for vehicle waiting time penalty (dominant factor)
        ALPHA_EMISSION: Weight for CO2 emission penalty
        ALPHA_EQUITY: Weight for modal equity (fairness across vehicle types)
        ALPHA_SAFETY: Weight for safety violation penalty
        ALPHA_PED_DEMAND: Weight for pedestrian demand satisfaction
        ALPHA_BLOCKED: Penalty for blocked actions (min green time violations)
        ALPHA_CONTINUE: Bonus for strategic phase continuation

    Phase Duration Constraints (Hybrid Approach - Oct 21, 2025):
        MAX_GREEN_TIME: Phase-specific maximum green times (from MSc thesis)
            - Phase 0 (Major N-S): 44s (major arterial, high capacity)
            - Phase 1 (Minor E-W): 12s (minor road, lower demand)
            - Phase 2 (Left turns): 24s (medium priority)
            - Phase 3 (Pedestrian): 10s (fixed crossing time)
        STUCK_PENALTY_START: Duration when progressive stuck penalty begins (30s)
        STUCK_PENALTY_RATE: Penalty rate per second over threshold (0.3 = 15x increase)
        STUCK_PENALTY_WARNING_THRESHOLD: Fraction of MAX_GREEN to start warning (0.7)
        DIVERSITY_BONUS: Reward for using non-Continue actions (encourages exploration)

    Implementation Strategy:
        - Hard Constraint: Force phase change at MAX_GREEN (safety net)
        - Soft Penalty: Progressive penalty starting at STUCK_PENALTY_START
        - Early Warning: Stronger penalty at 70% of MAX_GREEN
        - Diversity Incentive: Small bonus for phase changes

    Multimodal Weights:
        WEIGHT_CAR: Relative priority for private cars
        WEIGHT_BICYCLE: Relative priority for bicycles
        WEIGHT_PEDESTRIAN: Relative priority for pedestrians
        WEIGHT_BUS: Relative priority for buses (public transport)

    Notes:
        - Training constants (NUM_EPISODES_TRAIN, SIMULATION_LIMIT_TRAIN, etc.) are in constants/constants.py
        - Testing constants (NUM_EPISODES_TEST, SIMULATION_LIMIT_TEST, etc.) are in constants/constants.py
        - Safety thresholds (MIN_GREEN_TIME, SAFE_HEADWAY, etc.) are in constants/constants.py
        - Current configuration optimized to prevent sync bonus from dominating reward
    """

    STATE_DIM = 45
    ACTION_DIM = 4
    HIDDEN_LAYERS = [256, 256, 128]

    LEARNING_RATE = 0.00001
    GAMMA = 0.95
    EPSILON_START = 1.0
    EPSILON_END = 0.005
    EPSILON_DECAY = 0.995  # CHANGED: 0.98 → 0.995 (Phase 4 - Oct 24, 2025)
    # Rationale: Agent needs more exploration time to learn all 4 actions.
    # With 0.995: Episode 30 will have ε=0.86 (86% exploration)
    # With 0.98:  Episode 30 would have ε=0.54 (only 54% exploration)
    TAU = 0.005

    BUFFER_SIZE = 50000
    BATCH_SIZE = 32
    MIN_BUFFER_SIZE = 500

    ALPHA = 0.6
    BETA_START = 0.4
    BETA_FRAMES = 50000
    EPSILON_PER = 0.01

    ALPHA_WAIT = 5.0
    # ALPHA_SYNC removed - sync emerges naturally from waiting time minimization (Phase 4 - Oct 24, 2025)
    ALPHA_EMISSION = 0.03
    ALPHA_EQUITY = 0.03
    ALPHA_SAFETY = 5.0
    ALPHA_PED_DEMAND = 4.0
    ALPHA_BLOCKED = 3.0  # CHANGED: 0.5 → 3.0 (Phase 4 - Oct 24, 2025)
    # Rationale: Blocked actions indicate poor decision-making. With 56% block rate,
    # this creates strong penalty to prevent Continue spam. Expected: -2.0 × 4038 = -8076/episode

    ALPHA_CONTINUE = 0.02

    # NEW: Pedestrian phase activation bonus (positive reward for serving peds)
    # Increased from 2.0 to 3.0 to overcome blocked penalty (Phase 4 - Oct 24, 2025)
    PED_PHASE_ACTIVATION_BONUS = 3.0  # CHANGED: 2.0 → 3.0

    # NEW: Excessive continue penalty (encourage adaptive behavior)
    EXCESSIVE_CONTINUE_PENALTY = -0.5  # Penalty for staying stuck too long
    EXCESSIVE_CONTINUE_THRESHOLD = 35  # Seconds before penalty applies

    WEIGHT_CAR = 1.3
    WEIGHT_BICYCLE = 1.0
    WEIGHT_PEDESTRIAN = 1.0
    WEIGHT_BUS = 1.5

    # ========================================================================
    # Phase Duration Constraints (Hybrid Approach) - Oct 21, 2025
    # ========================================================================
    # Based on MSc thesis classical control values
    # Implements both hard constraints (force change) and soft penalties (train agent)
    # FIXED: Map ALL SUMO indices (0-15, 16) to their phase group's MAX_GREEN
    MAX_GREEN_TIME = {
        # Phase 1 group (Major N-S through + left) - SUMO indices 0-3
        0: 44,  # Leading green
        1: 44,  # Green
        2: 44,  # Yellow
        3: 44,  # All-red
        # Phase 2 group (Major left turns) - SUMO indices 4-7
        4: 12,  # Leading green
        5: 12,  # Green
        6: 12,  # Yellow
        7: 12,  # All-red
        # Phase 3 group (Minor E-W through + left) - SUMO indices 8-11
        8: 24,  # Leading green
        9: 24,  # Green
        10: 24,  # Yellow
        11: 24,  # All-red
        # Phase 4 group (Minor left turns) - SUMO indices 12-15
        12: 12,  # Leading green
        13: 12,  # Green
        14: 12,  # Yellow
        15: 12,  # All-red
        # Pedestrian exclusive phase - SUMO index 16
        16: 10,  # Fixed time for pedestrian crossing
    }

    # Progressive stuck penalty parameters
    STUCK_PENALTY_START = 30  # Start penalty at 30s (before MAX_GREEN)
    STUCK_PENALTY_RATE = 0.3  # Penalty per second (15x increase from 0.02)
    STUCK_PENALTY_WARNING_THRESHOLD = 0.7  # Start strong penalty at 70% of MAX_GREEN
