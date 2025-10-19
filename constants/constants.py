# Signal timing constants
YELLOW_TIME = 3
ALLRED_TIME = 2
MIN_GREEN_TIME = 5

# Simulation constants
NUM_EPISODES = 100
SIMULATION_LIMIT = 3600  # Simulation duration in seconds (1 hour) - used by all controls

# Training constants
UPDATE_FREQUENCY = 4  # Update every N steps
TARGET_UPDATE_FREQUENCY = 500
MODEL_SAVE_FREQUENCY = 25  # Save model checkpoints every 25 episodes
LOG_SAVE_FREQUENCY = 1  # Save CSV logs after every episode

# Safety thresholds (Critical THW value)
SAFE_HEADWAY = 1.0  # Minimum time headway (seconds)
COLLISION_DISTANCE = 1.0  # Near-collision distance (meters)

# Traffic distribution ratios (used by route generation)
MINOR_TO_MAJOR_TRAFFIC_RATIO = 0.25
STRAIGHT_TRAFFIC_RATIO = 0.8
TURN_RATIO = 0.1

# possible emisssion classes
# --------------------------

# bus: HDV_12_12, passenger car: P_7_7 (used in simulation)
# bus: HDV_12_12, passenger car: P_14_8 (50%), P_14_9 (25 %), P_14_13 (25 %)

#  6-node1            11-node2               13 -node3            11-node4             7-node1
#  rrrrrr      rrrrrrr     rrrrrr         rrrrrrr   rrr rrr    rr rrrrr    rrrrrr         rrrrrrr

#  rrrrrr      GggGGrr     rrrrrr         rrrrrrr  rrr rrr     Gg gGGrr    rrrrrr         rrrrrrr    leading p1   rrrrrrGggGGrrrrrrrrrrrrrrrrrrrrrGggGGrrrrrrrrrrrrrrr
#  rrrrrr      GggGGrr     ggGGrr         rrrrrrr  rrr rrr     Gg gGGrr    ggGGrr         rrrrrrr    p1
#  rrrrrr      ryyyyrr     yyyyrr         rrrrrrr  rrr rrr     ry yyyrr    yyyyrr         rrrrrrr    change p1


#  rrrrrr      grrrrGG     rrrrrr         rrrrrrr  rrr rrr     gr rrrGG    rrrrrr         rrrrrrr    leading green p2
#  rrrrrr      grrrrGG     rrrrGG         rrrrrrr  rrr rrr     gr rrrGG    rrrrGG         rrrrrrr    p2
#  rrrrrr      rrrrryy     rrrryy         rrrrrrr  rrr rrr     rr rrryy    rrrryy         rrrrrrr    change p2


#  rrrrrr      rrrrrrr     rrrrrr         GggGGrr  rrr rrr     rr rrrrr    rrrrrr         GggGGrr    leading green p3
#  ggGGrr      rrrrrrr     rrrrrr         GggGGrr  ggG Grr     rr rrrrr    rrrrrr         GggGGrr    p3
#  yyyyrr      rrrrrrr     rrrrrr         ryyyyrr  yyy yrr     rr rrrrr    rrrrrr         ryyyyrr    change p3


#  rrrrrr      rrrrrrr     rrrrrr         grrrrGG  rrr rrr      rr rrrrr    rrrrrr         grrrrGG    leading green p4
#  rrrrGG      rrrrrrr     rrrrrr         grrrrGG  rrr rGG      rr rrrrr    rrrrrr         grrrrGG    p4
#  rrrryy      rrrrrrr     rrrrrr         rrrrryy  rrr ryy      rr rrrrr    rrrrrr         rrrrryy    change p4

#  rrrrrr      Grrrrrr     rrrrrr         Grrrrrr  rrr rrr      Gr rrrrr    rrrrrr         Grrrrrr    p5
