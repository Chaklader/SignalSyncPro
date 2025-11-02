"""
P1 -> P2 | Act [0, 2]
P2 -> P1, P3 | Act [0, 1, 2]
P3 -> P1, P4 | Act [0, 1, 2]
P4 -> P1, P3 | Act [0, 1, 2]
"""

main_to_leading = {1: 0, 5: 4, 9: 8, 13: 12}


def get_next_phase_in_sequence(current_phase):
    """
    Simple cycle: P1 → P2 → P3 → P4 → P1
    This ensures proper phase rotation with Action 2 (Next).
    """
    cycle = list(main_to_leading.keys())  # [1, 5, 9, 13] derived from main_to_leading

    if current_phase in cycle:
        idx = cycle.index(current_phase)
        return cycle[(idx + 1) % len(cycle)]

    return 1
