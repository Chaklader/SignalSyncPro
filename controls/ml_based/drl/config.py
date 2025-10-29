from constants.developed.common.drl_tls_constants import (
    p1_main_green,
    p2_main_green,
    p3_main_green,
    p4_main_green,
)


class DRLConfig:
    STATE_DIM = 32
    ACTION_DIM = 3
    HIDDEN_LAYERS = [256, 256, 128]

    LEARNING_RATE = 0.00001
    GAMMA = 0.95
    EPSILON_START = 1.0
    EPSILON_END = 0.05
    EPSILON_DECAY = 0.995
    TAU = 0.005

    BUFFER_SIZE = 50000
    BATCH_SIZE = 64
    MIN_BUFFER_SIZE = 1000

    ALPHA = 0.6
    BETA_START = 0.4
    BETA_FRAMES = 50000
    EPSILON_PER = 0.01

    ALPHA_WAIT = 2.5
    ALPHA_EMISSION = 0.05
    ALPHA_EQUITY = 0.5
    ALPHA_SAFETY = 2.0
    ALPHA_BLOCKED = 1.0
    ALPHA_NEXT_BONUS = 0.05
    ALPHA_STABILITY = 0.3
    ALPHA_SKIP_OVERUSE = 0.1

    EXPECTED_ACTION_FREQUENCIES = {
        0: 0.85,
        1: 0.125,
        2: 0.025,
    }

    SKIP2P1_MAX_RATE = 0.15

    max_green_time = {
        p1_main_green: 44,
        p2_main_green: 15,
        p3_main_green: 24,
        p4_main_green: 12,
    }

    MIN_PHASE_DURATION_FOR_STABILITY = {
        p1_main_green: 20,
        p2_main_green: 8,
        p3_main_green: 10,
        p4_main_green: 6,
    }

    min_phase_durations_for_next_bonus = {
        p1_main_green: 25,
        p2_main_green: 10,
        p3_main_green: 15,
        p4_main_green: 8,
    }

    STUCK_PENALTY_RATE = 0.10

    """
    Thresholds derived from ratios × max_green_time (seconds):
    - p1_main_green: 35 (0.80 × 44)
    - p2_main_green: 12 (0.80 × 15)
    - p3_main_green: 18 (0.75 × 24)
    - p4_main_green: 10 (0.85 × 12)
    """
    STUCK_PENALTY_THRESHOLD_RATIO = {
        p1_main_green: 0.80,
        p2_main_green: 0.80,
        p3_main_green: 0.75,
        p4_main_green: 0.85,
    }

    """
    Consecutive-Continue thresholds (seconds before penalty):
    - p1_main_green: 35 (0.80 × 44)
    - p2_main_green: 12 (0.80 × 15)
    - p3_main_green: 18 (0.75 × 24)
    - p4_main_green: 10 (0.85 × 12)
    """
    CONSECUTIVE_CONTINUE_THRESHOLD_RATIO = {
        p1_main_green: 0.80,
        p2_main_green: 0.80,
        p3_main_green: 0.75,
        p4_main_green: 0.85,
    }

    SAFETY_VIOLATION_THRESHOLD = 3.0

    WEIGHT_CAR = 1.3
    WEIGHT_BICYCLE = 1.0
    WEIGHT_PEDESTRIAN = 1.0
    WEIGHT_BUS = 2.0
