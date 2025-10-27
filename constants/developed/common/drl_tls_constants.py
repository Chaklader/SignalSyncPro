num_phases = 16

initial_phase = 0
major_through_phase = 1

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
) = range(num_phases)


def next_phase(index):
    return (index + 1) % num_phases


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


MAX_GREEN = {
    p1_main_green: 44,
    p2_main_green: 12,
    p3_main_green: 24,
    p4_main_green: 10,
}
