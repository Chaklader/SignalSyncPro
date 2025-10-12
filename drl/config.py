"""
DRL Configuration Parameters
"""

class DRLConfig:
    STATE_DIM = 45  # Will be calculated based on actual state features
    ACTION_DIM = 4  # Continue, Skip to Phase 1, Next Phase, Pedestrian Phase
    HIDDEN_LAYERS = [256, 256, 128]
    
    # DQN Hyperparameters
    LEARNING_RATE = 0.00001  # REDUCED from 0.0001 (10x smaller)
    GAMMA = 0.95  # REDUCED from 0.99
    EPSILON_START = 1.0
    EPSILON_END = 0.01
    EPSILON_DECAY = 0.995
    TAU = 0.005  # Target network soft update rate
    
    # Replay Buffer
    BUFFER_SIZE = 50000  # REDUCED from 100000
    BATCH_SIZE = 32  # REDUCED from 64
    MIN_BUFFER_SIZE = 500  # REDUCED from 1000
    
    # Prioritized Experience Replay
    ALPHA = 0.6  # Prioritization exponent
    BETA_START = 0.4
    BETA_FRAMES = 50000  # REDUCED from 100000
    EPSILON_PER = 0.01  # Small constant for priority
    
    # Training
    NUM_EPISODES = 30  # Quick test with 30 episodes
    MAX_STEPS_PER_EPISODE = 3600  # 3600 seconds simulation (1 hour)
    UPDATE_FREQUENCY = 4  # Update every N steps
    TARGET_UPDATE_FREQUENCY = 500  # REDUCED from 1000
    SAVE_FREQUENCY = 1  # Save after every episode for immediate logging
    
    # ========================================================================
    # REWARD WEIGHTS - REBALANCED FOR WAITING TIME METRIC
    # ========================================================================
    
    # Primary component: Waiting time (normalized to [0,1])
    ALPHA_WAIT = 0.5  # Waiting time penalty - allows positive rewards
    
    # Strong coordination incentive
    ALPHA_SYNC = 3.0  # Synchronization bonus (STRONG!) - overwhelms small penalties
    
    # Secondary components (small but present - sustainability & fairness)
    ALPHA_EMISSION = 0.01  # CO₂ emissions penalty (environmental sustainability)
    ALPHA_EQUITY = 0.05  # Fairness penalty across modes (multimodal equity)
    
    # Critical safety component (NON-NEGOTIABLE)
    ALPHA_SAFETY = 5.0  # Safety violations (HIGH PENALTY - prevents dangerous timings)
    
    # Pedestrian responsiveness
    ALPHA_PED_DEMAND = 1.0  # Penalty for ignoring high pedestrian demand
    
    # Safety thresholds
    MIN_GREEN_TIME = 5  # Minimum green time (seconds)
    SAFE_HEADWAY = 2.0  # Minimum time headway (seconds)
    COLLISION_DISTANCE = 5.0  # Near-collision distance (meters)
    
    # Multimodal Weights for waiting time
    WEIGHT_CAR = 1.2
    WEIGHT_BICYCLE = 1.0
    WEIGHT_PEDESTRIAN = 1.0
    WEIGHT_BUS = 1.5  # Slightly higher priority for public transport
