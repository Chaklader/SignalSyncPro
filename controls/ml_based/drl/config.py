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
    ALPHA_BLOCKED = 0.3
    ALPHA_SKIP_OVERUSE = 0.15

    ALPHA_STABILITY = 2.5
    ALPHA_NEXT_BONUS = 3.0

    WEIGHT_CAR = 1.3
    WEIGHT_BICYCLE = 1.0
    WEIGHT_PEDESTRIAN = 1.0
    WEIGHT_BUS = 2.0

    SAFETY_VIOLATION_THRESHOLD = 3.0
    SKIP2P1_MAX_RATE = 0.04

    """
    Expected action frequencies

    0: Continue 85%
    1: Skip 2P1 2.5%
    2: Next 12.5%
    """
    expected_action_frequencies = {
        0: 0.85,
        1: 0.025,
        2: 0.125,
    }

    """
    Phase Aware Thresholds

        Min Green time < Stability threshold < Next bonus threshold < Consecutive continue threshold < Max green duration
    """
    phase_min_green_time = {
        p1_main_green: 10,
        p2_main_green: 4,
        p3_main_green: 6,
        p4_main_green: 3,
    }

    min_phase_duration_for_stability = {
        p1_main_green: 11,
        p2_main_green: 5,
        p3_main_green: 7,
        p4_main_green: 4,
    }

    min_phase_durations_for_next_bonus = {
        p1_main_green: 14,
        p2_main_green: 7,
        p3_main_green: 9,
        p4_main_green: 5,
    }

    consecutive_continue_threshold = {
        p1_main_green: 30,
        p2_main_green: 10,
        p3_main_green: 15,
        p4_main_green: 8,
    }

    max_green_time = {
        p1_main_green: 44,
        p2_main_green: 15,
        p3_main_green: 24,
        p4_main_green: 12,
    }
