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
    EPSILON_END = 0.005  # REDUCED from 0.01 - lower exploration floor
    EPSILON_DECAY = 0.98  # INCREASED from 0.97 - slower decay for better convergence
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
    NUM_EPISODES = 100  # Test with 5 episodes to verify safety fix
    MAX_STEPS_PER_EPISODE = 3600  # 3600 seconds simulation (1 hour)
    UPDATE_FREQUENCY = 4  # Update every N steps
    TARGET_UPDATE_FREQUENCY = 500  # REDUCED from 1000
    
    # Save frequencies (separated for models vs logs)
    MODEL_SAVE_FREQUENCY = 25  # Save model checkpoints every 10 episodes
    LOG_SAVE_FREQUENCY = 1  # Save CSV logs after every episode for immediate monitoring
    
    # ========================================================================
    # REWARD WEIGHTS - REBALANCED FOR WAITING TIME METRIC
    # ========================================================================
    
    # Primary component: Waiting time (normalized to [0,1])
    # ALPHA_WAIT = 0.5  
    # ALPHA_SYNC = 3.0  
    # ALPHA_EMISSION = 0.01  
    # ALPHA_EQUITY = 0.05  
    # ALPHA_SAFETY = 5.0  
    # ALPHA_PED_DEMAND = 1.0

    # In drl/config.py - REBALANCED FOR VEHICLE WAITING TIME FOCUS
    ALPHA_WAIT = 6.0       # DOUBLED from 3.0 - Make car waiting time THE DOMINANT factor
    ALPHA_SYNC = 0.15      # HALVED from 0.35 - Prevent sync bonus from dominating reward
    ALPHA_EMISSION = 0.03  # Reduced - less important than waiting
    ALPHA_EQUITY = 0.03    # Reduced - less important than waiting  
    ALPHA_SAFETY = 1.0     # Keep safety important
    ALPHA_PED_DEMAND = 0.8 # INCREASED from 0.3 - Prevent ped over-serving
    ALPHA_BLOCKED = 0.1    # Reduced slightly
    ALPHA_CONTINUE = 0.02  # Reduced - was encouraging too much continuation
    
    # Safety thresholds
    MIN_GREEN_TIME = 5  # Minimum green time (seconds)
    MAX_STRATEGIC_DURATION = 20  # Maximum duration for strategic continue bonus (seconds)
    SAFE_HEADWAY = 1.0  # Minimum time headway (seconds)
    COLLISION_DISTANCE = 1.0  # Near-collision distance (meters)
    
    # Multimodal Weights for waiting time
    WEIGHT_CAR = 1.3
    WEIGHT_BICYCLE = 1.0
    WEIGHT_PEDESTRIAN = 1.0
    WEIGHT_BUS = 1.5  # Slightly higher priority for public transport
