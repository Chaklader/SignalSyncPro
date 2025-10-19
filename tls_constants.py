NUM_PHASES = 18
initialPhase = 0
majorThroughPhase = 1

busPriorityLane = {0: ("2_3_0", "4_3_0"), 1: ("5_6_0", "7_6_0")}

(
    leadingGreenOne,
    pOne,
    pcOne,
    pOneRed,
    leadingGreenTwo,
    pTwo,
    pcTwo,
    pTwoRed,
    leadingGreenThree,
    pThree,
    pcThree,
    pThreeRed,
    leadingGreenFour,
    pFour,
    pcFour,
    pFourRed,
    pFive,
    pFiveRed,
) = range(NUM_PHASES)


def next_phase(index):
    return (index + 1) % NUM_PHASES


def is_green(phase):
    return phase == pOne or phase == pTwo or phase == pThree or phase == pFour


def is_yellow(yellowPhase):
    return (
        yellowPhase == pcOne
        or yellowPhase == pcTwo
        or yellowPhase == pcThree
        or yellowPhase == pcFour
    )


def is_red(red):
    return red == pOneRed or red == pTwoRed or red == pThreeRed or red == pFourRed


def is_bus_priority(index):
    return index == pTwo or index == pThree or index == pFour


def is_pedestrian_priority(index):
    return index == pFourRed


# p1 = 0.9 = straightTrafficRatio + turnRatio
# p2 = 0.1 = turnRatio
# p3 = 0.45 (= 0.9 * minorToMajorTrafficRatio )
# p4 = 0.05 (= 0.1 * minorToMajorTrafficRatio )


gmax_p1 = 44
gmax_p2 = 12
gmax_p3 = 24
gmax_p4 = 10

maxGreen = {pOne: gmax_p1, pTwo: gmax_p2, pThree: gmax_p3, pFour: gmax_p4}

# cycle time = 44 + 12 + 24 + 10 = 90
