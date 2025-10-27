from constants.developed.common.drl_tls_constants import (
    p1_main_green,
    p2_main_green,
    p3_main_green,
    p4_main_green,
)

p1_detectors = {
    "vehicle": ["2_3_0_30", "4_3_0_30", "5_6_0_30", "7_6_0_30"],
    "bicycle": ["a_3_1_15", "6_3_1_15", "3_6_1_15", "b_6_1_15"],
}


p2_detectors = {
    "vehicle": ["2_3_1_30", "4_3_1_30", "5_6_1_30", "7_6_1_30"],
    "bicycle": ["a_3_2_15", "6_3_2_15", "3_6_2_15", "b_6_2_15"],
}


p3_detectors = {
    "vehicle": ["11_3_0_30", "10_3_0_30", "15_6_0_30", "14_6_0_30"],
    "bicycle": ["d_3_1_15", "c_3_1_15", "f_6_1_15", "e_6_1_15"],
}


p4_detectors = {
    "vehicle": ["11_3_1_30", "10_3_1_30", "15_6_1_30", "14_6_1_30"],
    "bicycle": ["d_3_2_15", "c_3_2_15", "f_6_2_15", "e_6_2_15"],
}

detectors = {
    p1_main_green: p1_detectors,
    p2_main_green: p2_detectors,
    p3_main_green: p3_detectors,
    p4_main_green: p4_detectors,
}
