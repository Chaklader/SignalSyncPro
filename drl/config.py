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
    NUM_EPISODES = 25  # Quick test with 10 episodes
    MAX_STEPS_PER_EPISODE = 3600  # 2000 seconds simulation (33 minutes)
    UPDATE_FREQUENCY = 4  # Update every N steps
    TARGET_UPDATE_FREQUENCY = 500  # REDUCED from 1000
    SAVE_FREQUENCY = 5  # Save more frequently (every 5 episodes)
    
    # Reward Weights (SIMPLIFIED)
    ALPHA_WAIT = 1.0  # Main component
    ALPHA_EMISSION = 0.1  # Add small emission penalty
    ALPHA_SYNC = 0.5  # Bonus
    ALPHA_EQUITY = 0.2  # Add small equity penalty
    ALPHA_SAFETY = 5.0  # Keep high
    ALPHA_PED_DEMAND = 0.5  # Pedestrian demand penalty (high waiting pedestrians)
    
    # Multimodal Weights for waiting time
    WEIGHT_CAR = 1.2
    WEIGHT_BICYCLE = 1.0
    WEIGHT_PEDESTRIAN = 1.0
    WEIGHT_BUS = 1.5  # Slightly higher priority for public transport
