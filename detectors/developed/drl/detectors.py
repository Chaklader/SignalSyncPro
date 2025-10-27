from constants.developed.common.drl_tls_constants import (
    p1_leading_green,
    p2_leading_green,
    p3_leading_green,
    p4_leading_green,
    p1_main_green,
    p2_main_green,
    p3_main_green,
    p4_main_green,
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

LEADING_GREEN_ONE_DETECTORS = [
    ["a_3_1_15", "a_3_2_15", "6_3_1_15", "6_3_2_15"],
    ["3_6_1_15", "3_6_2_15", "b_6_1_15", "b_6_2_15"],
]

LEADING_GREEN_TWO_DETECTORS = [
    ["a_3_2_15", "6_3_2_15"],
    ["3_6_2_15", "b_6_2_15"],
]

LEADING_GREEN_THREE_DETECTORS = [
    ["d_3_1_15", "d_3_2_15", "c_3_1_15", "c_3_2_15"],
    ["f_6_1_15", "f_6_2_15", "e_6_1_15", "e_6_2_15"],
]

LEADING_GREEN_FOUR_DETECTORS = [
    ["d_3_2_15", "c_3_2_15"],
    ["f_6_2_15", "e_6_2_15"],
]

DETECTORS_INFO = {
    p1_main_green: PHASE_ONE_DETECTORS,
    p2_main_green: PHASE_TWO_DETECTORS,
    p3_main_green: PHASE_THREE_DETECTORS,
    p4_main_green: PHASE_FOUR_DETECTORS,
    p1_leading_green: LEADING_GREEN_ONE_DETECTORS,
    p2_leading_green: LEADING_GREEN_TWO_DETECTORS,
    p3_leading_green: LEADING_GREEN_THREE_DETECTORS,
    p4_leading_green: LEADING_GREEN_FOUR_DETECTORS,
}
