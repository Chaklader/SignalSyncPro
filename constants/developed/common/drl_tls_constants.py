NUM_PHASES = 16
INITIAL_PHASE = 0
MAJOR_THROUGH_PHASE = 1

BUS_PRIORITY_LANE = {0: ("2_3_0", "4_3_0"), 1: ("5_6_0", "7_6_0")}


(
    p1_leading_green,
    p1_main_green,
    p1_yellow,
    p1_red,

    p2_leading_green,
    p2_main_green,
    p2_yellow,
    p2_red,

    p3_leading_green,
    p3_main_green,
    p3_yellow,
    p3_red,

    p4_leading_green,
    p4_main_green,
    p4_yellow,
    p4_red,
) = range(NUM_PHASES)

def next_phase(index):
    return (index + 1) % NUM_PHASES


def is_green(phase):
    return phase in (p1_main_green, p2_main_green, p3_main_green, p4_main_green)


def is_yellow(yellowPhase):
    return yellowPhase in (
        p1_yellow,
        p2_yellow,
        p3_yellow,
        p4_yellow,
    )


def is_red(red):
    return red in (p1_red, p2_red, p3_red, p4_red)


def is_bus_priority(index):
    return index in (p2_main_green, p3_main_green, p4_main_green)


# p1 = 0.9 = STRAIGHT_TRAFFIC_RATIO + TURN_RATIO
# p2 = 0.1 = TURN_RATIO
# p3 = 0.45 (= 0.9 * MINOR_TO_MAJOR_TRAFFIC_RATIO )
# p4 = 0.05 (= 0.1 * MINOR_TO_MAJOR_TRAFFIC_RATIO )


MAX_GREEN_PHASE_ONE = 44
MAX_GREEN_PHASE_TWO = 12
MAX_GREEN_PHASE_THREE = 24
MAX_GREEN_PHASE_FOUR = 10

MAX_GREEN = {
    p1_main_green: MAX_GREEN_PHASE_ONE,
    p2_main_green: MAX_GREEN_PHASE_TWO,
    p3_main_green: MAX_GREEN_PHASE_THREE,
    p4_main_green: MAX_GREEN_PHASE_FOUR,
}

# cycle time = 44 + 12 + 24 + 10 = 90
