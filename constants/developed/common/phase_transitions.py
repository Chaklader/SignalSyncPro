"""
P1 -> P2 | Act [0, 2]
P2 -> P1, P3 | Act [0, 1, 2]
P3 -> P1, P4 | Act [0, 1, 2]
P4 -> P1, P3 | Act [0, 1, 2]
"""

VALID_PHASE_TRANSITIONS = {
    1: [5],
    5: [1, 9],
    9: [1, 13],
    13: [1, 9],
}

PHASE_MIN_GREEN_TIME = {
    1: 10,
    5: 5,
    9: 8,
    13: 5,
}

main_to_leading = {1: 0, 5: 4, 9: 8, 13: 12}


def get_next_phase_in_sequence(current_phase):
    valid_transitions = VALID_PHASE_TRANSITIONS.get(current_phase, [1])

    if len(valid_transitions) == 1:
        return valid_transitions[0]
    else:
        return [t for t in valid_transitions if t != 1][0]


def is_valid_transition(current_phase, next_phase):
    return next_phase in VALID_PHASE_TRANSITIONS.get(current_phase, [])
