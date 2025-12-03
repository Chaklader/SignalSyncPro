"""
Multi-Agent DRL TLS Constants for 5-intersection network.

Network topology:
   a────[3]────[6]────[17]────[18]────[19]────b
         │      │       │       │       │
         c/d    e/f     g/h     i/j     k/l
"""

num_phases = 16

initial_phase = 0
major_through_phase = 1


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

# bus_priority_lanes = {
#     0: ("2_3_0", "4_3_0"),  # TLS-1 (node 3)
#     1: ("5_6_0", "7_6_0"),  # TLS-2 (node 6)
#     2: ("20_17_0", "21_17_0"),  # TLS-3 (node 17)
#     3: ("22_18_0", "23_18_0"),  # TLS-4 (node 18)
#     4: ("24_19_0", "25_19_0"),  # TLS-5 (node 19)
# }

bus_signals_emit_lanes = {
    0: (
        "1_2_0",
        "5_4_0",
    ),  # TLS-1: 1000m (= 895+105) 72s upstream, 895m (=790+105) 64s downstream
    1: (
        "4_5_0",
        "20_7_0",
    ),  # TLS-2: 895m (=790+105) 64s upstream, 895m (=790+105) 64s downstream
    2: (
        "7_20_0",
        "22_21_0",
    ),  # TLS-3: 895m (=790+105) 64s upstream, 895m (=790+105) 64s downstream
    3: (
        "21_22_0",
        "24_23_0",
    ),  # TLS-4: 895m (=790+105) 64s upstream, 895m (=790+105) 64s downstream
    4: (
        "23_24_0",
        "8_25_0",
    ),  # TLS-5: 895m (=790+105) 64s upstream, 1000m (= 895+105) 72s downstream
}

# Need to make sure both AI and rule based agent dont go to P1 right after P1. They will need to pass through P2 earliest.

"""
Phase Green Time Configuration (seconds)
=========================================
| Phase | Description    | MIN_GREEN | MAX_GREEN |
|-------|----------------|-----------|-----------|
| P1    | Major Through  |     8     |    44     |
| P2    | Major Left     |     3     |    15     |
| P3    | Minor Through  |     5     |    24     |
| P4    | Minor Left     |     2     |    12     |

Fixed Transition Times:
- Leading Green: 1s (bicycle priority start)
- Yellow: 3s
- Red Clearance: 2s
"""

action_names = {0: "Continue", 1: "Skip2P1", 2: "Next"}

PRIORITY_ACTION_HOLD = "HOLD"
PRIORITY_ACTION_CYCLE = "CYCLE"
PRIORITY_ACTION_SKIP = "SKIP"

WARNING_TIME = 15
HOLD_THRESHOLD = 30
GAP_OUT_THRESHOLD = 3.0

# 5 TLS IDs for multi-agent network
TLS_IDS = ["3", "6", "17", "18", "19"]

# Number of agents (one per TLS)
NUM_AGENTS = len(TLS_IDS)

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

MAIN_GREEN_PHASES = {p1_main_green, p2_main_green, p3_main_green, p4_main_green}
YELLOW_PHASES = {p1_yellow, p2_yellow, p3_yellow, p4_yellow}
RED_PHASES = {p1_red, p2_red, p3_red, p4_red}
LEADING_GREEN_PHASES = {
    p1_leading_green,
    p2_leading_green,
    p3_leading_green,
    p4_leading_green,
}

main_controllable_phases = MAIN_GREEN_PHASES

phase_names = {
    p1_main_green: "P1",
    p2_main_green: "P2",
    p3_main_green: "P3",
    p4_main_green: "P4",
}

LEADING_GREEN_DURATION = 1
YELLOW_DURATION = 3
RED_DURATION = 2

auto_durations = {
    p1_leading_green: LEADING_GREEN_DURATION,
    p2_leading_green: LEADING_GREEN_DURATION,
    p3_leading_green: LEADING_GREEN_DURATION,
    p4_leading_green: LEADING_GREEN_DURATION,
    p1_yellow: YELLOW_DURATION,
    p2_yellow: YELLOW_DURATION,
    p3_yellow: YELLOW_DURATION,
    p4_yellow: YELLOW_DURATION,
    p1_red: RED_DURATION,
    p2_red: RED_DURATION,
    p3_red: RED_DURATION,
    p4_red: RED_DURATION,
}


def next_phase(index):
    return (index + 1) % num_phases


def is_main_green_phases(phase):
    return phase in MAIN_GREEN_PHASES
