from constants.developed.common.tls_constants import (
    PHASE_ONE,
    PHASE_TWO,
    PHASE_THREE,
    PHASE_FOUR,
)

PHASE_ONE_DETECTORS = [
    [["2_3_0_30", "4_3_0_30"], ["a_3_1_15", "a_3_2_15", "6_3_1_15", "6_3_2_15"]],
    [["5_6_0_30", "7_6_0_30"], ["3_6_1_15", "3_6_2_15", "b_6_1_15", "b_6_2_15"]],
]
PHASE_TWO_DETECTORS = (
    [["2_3_1_30", "4_3_1_30"], ["a_3_2_15", "6_3_2_15"]],
    [
        ["5_6_1_30", "7_6_1_30"],
        ["3_6_2_15", "b_6_2_15"],
    ],
)
PHASE_THREE_DETECTORS = [
    [["11_3_0_30", "10_3_0_30"], ["d_3_1_15", "d_3_2_15", "c_3_1_15", "c_3_2_15"]],
    [["15_6_0_30", "14_6_0_30"], ["f_6_1_15", "f_6_2_15", "e_6_1_15", "e_6_2_15"]],
]
PHASE_FOUR_DETECTORS = [
    [["11_3_1_30", "10_3_1_30"], ["d_3_2_15", "c_3_2_15"]],
    [["15_6_1_30", "14_6_1_30"], ["f_6_2_15", "e_6_2_15"]],
]
PEDESTRIAN_DETECTORS = [
    ["a_3_0_ped", "c_3_0_ped", "6_3_0_ped", "d_3_0_ped"],
    ["3_6_0_ped", "e_6_0_ped", "b_6_0_ped", "f_6_0_ped"],
]


DETECTORS_INFO = {
    PHASE_ONE: PHASE_ONE_DETECTORS,
    PHASE_TWO: PHASE_TWO_DETECTORS,
    PHASE_THREE: PHASE_THREE_DETECTORS,
    PHASE_FOUR: PHASE_FOUR_DETECTORS,
}
