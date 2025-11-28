"""
Multi-Agent Detector Configuration for 5-TLS network.

Each TLS has its own set of detectors organized by phase.
Detector naming: {from_node}_{to_node}_{lane}_{distance}

Network topology:
   a────[3]────[6]────[17]────[18]────[19]────b
         │      │       │       │       │
         c/d    e/f     g/h     i/j     k/l
"""

from constants.developed.multi_agent.drl_tls_constants import (
    p1_main_green,
    p2_main_green,
    p3_main_green,
    p4_main_green,
)

#                     c              e              g              i              k
#                     │              │              │              │              │
#                     9             13             26             30             34
#                     │              │              │              │              │
#                    10             14             27             31             35
#                     │              │              │              │              │
#    a────1────2────[3]────4────5──[6]────7───20─[17]───21───22─[18]───23───24─[19]───25────8────b
#                     │              │              │              │              │
#                    11             15             28             32             36
#                     │              │              │              │              │
#                    12             16             29             33             37
#                     │              │              │              │              │
#                     d              f              h              j              l


#    x=-1100        x=0          x=1000         x=2000         x=3000         x=4000        x=5100
#    (Entry)      TLS-1          TLS-2          TLS-3          TLS-4          TLS-5         (Exit)

p1_detectors = {
    "3": {  # TLS-1
        "vehicle": ["2_3_0_30", "4_3_0_30"],
        "bicycle": ["a_3_1_15", "6_3_1_15"],
    },
    "6": {  # TLS-2
        "vehicle": ["5_6_0_30", "7_6_0_30"],
        "bicycle": ["3_6_1_15", "17_6_1_15"],
    },
    "17": {  # TLS-3
        "vehicle": ["20_17_0_30", "21_17_0_30"],
        "bicycle": ["6_17_1_15", "18_17_1_15"],
    },
    "18": {  # TLS-4
        "vehicle": ["22_18_0_30", "23_18_0_30"],
        "bicycle": ["17_18_1_15", "19_18_1_15"],
    },
    "19": {  # TLS-5
        "vehicle": ["24_19_0_30", "25_19_0_30"],
        "bicycle": ["18_19_1_15", "b_19_1_15"],
    },
}

# ============================================================
# P2 Detectors - Horizontal turn traffic (lane 1)
# ============================================================
p2_detectors = {
    "3": {  # TLS-1
        "vehicle": ["2_3_1_30", "4_3_1_30"],
        "bicycle": ["a_3_2_15", "6_3_2_15"],
    },
    "6": {  # TLS-2
        "vehicle": ["5_6_1_30", "7_6_1_30"],
        "bicycle": ["3_6_2_15", "17_6_2_15"],
    },
    "17": {  # TLS-3
        "vehicle": ["20_17_1_30", "21_17_1_30"],
        "bicycle": ["6_17_2_15", "18_17_2_15"],
    },
    "18": {  # TLS-4
        "vehicle": ["22_18_1_30", "23_18_1_30"],
        "bicycle": ["17_18_2_15", "19_18_2_15"],
    },
    "19": {  # TLS-5
        "vehicle": ["24_19_1_30", "25_19_1_30"],
        "bicycle": ["18_19_2_15", "b_19_2_15"],
    },
}

# ============================================================
# P3 Detectors - Vertical through traffic (lane 0)
# ============================================================
p3_detectors = {
    "3": {  # TLS-1
        "vehicle": ["10_3_0_30", "11_3_0_30"],
        "bicycle": ["c_3_1_15", "d_3_1_15"],
    },
    "6": {  # TLS-2
        "vehicle": ["14_6_0_30", "15_6_0_30"],
        "bicycle": ["e_6_1_15", "f_6_1_15"],
    },
    "17": {  # TLS-3
        "vehicle": ["27_17_0_30", "28_17_0_30"],
        "bicycle": ["g_17_1_15", "h_17_1_15"],
    },
    "18": {  # TLS-4
        "vehicle": ["31_18_0_30", "32_18_0_30"],
        "bicycle": ["i_18_1_15", "j_18_1_15"],
    },
    "19": {  # TLS-5
        "vehicle": ["35_19_0_30", "36_19_0_30"],
        "bicycle": ["k_19_1_15", "l_19_1_15"],
    },
}

# ============================================================
# P4 Detectors - Vertical turn traffic (lane 1)
# ============================================================
p4_detectors = {
    "3": {  # TLS-1
        "vehicle": ["10_3_1_30", "11_3_1_30"],
        "bicycle": ["c_3_2_15", "d_3_2_15"],
    },
    "6": {  # TLS-2
        "vehicle": ["14_6_1_30", "15_6_1_30"],
        "bicycle": ["e_6_2_15", "f_6_2_15"],
    },
    "17": {  # TLS-3
        "vehicle": ["27_17_1_30", "28_17_1_30"],
        "bicycle": ["g_17_2_15", "h_17_2_15"],
    },
    "18": {  # TLS-4
        "vehicle": ["31_18_1_30", "32_18_1_30"],
        "bicycle": ["i_18_2_15", "j_18_2_15"],
    },
    "19": {  # TLS-5
        "vehicle": ["35_19_1_30", "36_19_1_30"],
        "bicycle": ["k_19_2_15", "l_19_2_15"],
    },
}

# ============================================================
# Combined detector mapping by phase
# ============================================================
detectors = {
    p1_main_green: p1_detectors,
    p2_main_green: p2_detectors,
    p3_main_green: p3_detectors,
    p4_main_green: p4_detectors,
}


def get_detectors_for_tls(tls_id, phase):
    """
    Get detectors for a specific TLS and phase.

    Args:
        tls_id: TLS ID string ("3", "6", "17", "18", "19")
        phase: Phase number (p1_main_green, p2_main_green, etc.)

    Returns:
        dict with "vehicle" and "bicycle" detector lists
    """
    if phase in detectors and tls_id in detectors[phase]:
        return detectors[phase][tls_id]
    return {"vehicle": [], "bicycle": []}


def get_all_detectors_for_tls(tls_id):
    """
    Get all detectors for a specific TLS across all phases.

    Args:
        tls_id: TLS ID string

    Returns:
        dict mapping phase to detector dict
    """
    return {
        phase: get_detectors_for_tls(tls_id, phase)
        for phase in [p1_main_green, p2_main_green, p3_main_green, p4_main_green]
    }
