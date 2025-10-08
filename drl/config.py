"""
DRL Configuration Parameters
"""

class DRLConfig:
    # Neural Network Architecture
    STATE_DIM = 45  # Will be calculated based on actual state features
    ACTION_DIM = 4  # Continue, Skip to Phase 1, Next Phase, Pedestrian Phase
    HIDDEN_LAYERS = [256, 256, 128]
    
    # DQN Hyperparameters
    LEARNING_RATE = 0.0001
    GAMMA = 0.99  # Discount factor
    EPSILON_START = 1.0
    EPSILON_END = 0.01
    EPSILON_DECAY = 0.995
    TAU = 0.005  # Target network soft update rate
    
    # Replay Buffer
    BUFFER_SIZE = 100000
    BATCH_SIZE = 64
    MIN_BUFFER_SIZE = 1000
    
    # Prioritized Experience Replay
    ALPHA = 0.6  # Prioritization exponent
    BETA_START = 0.4
    BETA_FRAMES = 100000
    EPSILON_PER = 0.01  # Small constant for priority
    
    # Training
    NUM_EPISODES = 1000
    MAX_STEPS_PER_EPISODE = 3600  # 1 hour simulation
    UPDATE_FREQUENCY = 4  # Update every N steps
    TARGET_UPDATE_FREQUENCY = 1000  # Copy to target network every N steps
    SAVE_FREQUENCY = 50  # Save model every N episodes
    
    # Reward Weights
    ALPHA_WAIT = 0.1  # Waiting time penalty
    ALPHA_EMISSION = 0.05  # Emission penalty
    ALPHA_SYNC = 5.0  # Synchronization bonus
    ALPHA_EQUITY = 2.0  # Equity bonus
    ALPHA_SAFETY = 100.0  # Safety penalty
    
    # Multimodal Weights for waiting time
    WEIGHT_CAR = 1.0
    WEIGHT_BICYCLE = 1.5  # Higher priority for vulnerable modes
    WEIGHT_PEDESTRIAN = 2.0
    WEIGHT_BUS = 1.2
