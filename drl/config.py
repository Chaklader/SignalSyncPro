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
    EPSILON_DECAY = 0.97
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
    NUM_EPISODES = 50  # Test with 5 episodes to verify safety fix
    MAX_STEPS_PER_EPISODE = 3600  # 3600 seconds simulation (1 hour)
    UPDATE_FREQUENCY = 4  # Update every N steps
    TARGET_UPDATE_FREQUENCY = 500  # REDUCED from 1000
    
    # Save frequencies (separated for models vs logs)
    MODEL_SAVE_FREQUENCY = 50  # Save model checkpoints every 10 episodes
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

    # In drl/config.py - UPDATED CONFIGURATION (After Safety Fix)
    ALPHA_WAIT = 0.9  # INCREASED from 0.7 (prioritize traffic flow)
    ALPHA_SYNC = 0.6  # FURTHER REDUCED from 0.85 (sync less important than flow)
    ALPHA_EMISSION = 0.05  
    ALPHA_EQUITY = 0.05 
    ALPHA_SAFETY = 1.0     # RE-ENABLED (reduced from 5.0 for testing)
    ALPHA_PED_DEMAND = 0.3  # REDUCED from 0.5 (was causing over-activation)
    ALPHA_BLOCKED = 0.15   # NEW: Penalty for blocked actions (Fix 1)
    ALPHA_CONTINUE = 0.05  # NEW: Bonus for strategic Continue action (Fix 3)
    
    # Safety thresholds
    MIN_GREEN_TIME = 5  # Minimum green time (seconds)
    MAX_STRATEGIC_DURATION = 20  # Maximum duration for strategic continue bonus (seconds)
    SAFE_HEADWAY = 1.0  # Minimum time headway (seconds)
    COLLISION_DISTANCE = 1.0  # Near-collision distance (meters)
    
    # Multimodal Weights for waiting time
    # REBALANCED: Prioritize cars/bicycles more, reduce bus dominance
    WEIGHT_CAR = 1.5  # Increased from 1.3 (cars are majority traffic)
    WEIGHT_BICYCLE = 1.2  # Increased from 1.0 (sustainable transport)
    WEIGHT_PEDESTRIAN = 0.8  # Reduced from 1.0 (lower volume)
    WEIGHT_BUS = 1.0  # Reduced from 1.5 (was over-prioritized)
