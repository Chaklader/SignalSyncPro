Parsing training log: training.log
========================================

================================================================================
EPISODE 1
================================================================================
TRAFFIC CONFIG:
Episode 1 - Generating routes (initial):
  Cars: 347
  Bicycles: 564
  Pedestrians: 304
  Buses: every_15min

[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1320
  Actions blocked (MIN_GREEN_TIME): 3588
  Phase change rate: 18.3%
  Block rate: 49.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    1
  Total Distance Violations:   0
  Total Red Light Violations:  795
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     796
  Violation Rate:              22.11% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 1 Complete:
  Reward: -2.0202 | Loss: 0.5583 | Steps: 3600 | Epsilon: 0.980
  Avg Wait: 16.01s | Sync Rate: 38.83%
  Car: 26.14s | Bike: 26.16s | Bus: 0.46s
  Reward Components (avg per step):
    Waiting:    -1.8793
    Flow:       +0.3666
    Sync:       +0.0583
    CO2:        -0.0067
    Equity:     -0.0046
    Safety:     -0.2211  (796 violations, 22.1% of steps)
    Pedestrian: -0.2838  (0 ignored, 0.0% of steps)
    TOTAL:      -2.0202
================================================================================

================================================================================
EPISODE 2
================================================================================
TRAFFIC CONFIG:
Episode 2 - Generating routes:
  Cars: 782/hr
  Bicycles: 890/hr
  Pedestrians: 538/hr
  Buses: every_15min

[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1314
  Actions blocked (MIN_GREEN_TIME): 3556
  Phase change rate: 18.2%
  Block rate: 49.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    6
  Total Distance Violations:   0
  Total Red Light Violations:  830
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     836
  Violation Rate:              23.22% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 2 Complete:
  Reward: -3.5730 | Loss: 0.4485 | Steps: 3600 | Epsilon: 0.960
  Avg Wait: 23.06s | Sync Rate: 40.31%
  Car: 43.28s | Bike: 28.09s | Bus: 3.86s
  Reward Components (avg per step):
    Waiting:    -3.3609
    Flow:       +0.3078
    Sync:       +0.0605
    CO2:        -0.0071
    Equity:     -0.0079
    Safety:     -0.2322  (836 violations, 23.2% of steps)
    Pedestrian: -0.2842  (0 ignored, 0.0% of steps)
    TOTAL:      -3.5730
================================================================================

================================================================================
EPISODE 3
================================================================================
TRAFFIC CONFIG:
Episode 3 - Generating routes:
  Cars: 867/hr
  Bicycles: 111/hr
  Pedestrians: 840/hr
  Buses: every_15min

[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1284
  Actions blocked (MIN_GREEN_TIME): 3412
  Phase change rate: 17.8%
  Block rate: 47.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    2
  Total Distance Violations:   0
  Total Red Light Violations:  753
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     755
  Violation Rate:              20.97% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 3 Complete:
  Reward: -2.8688 | Loss: 0.5303 | Steps: 3600 | Epsilon: 0.941
  Avg Wait: 18.29s | Sync Rate: 41.67%
  Car: 45.20s | Bike: 5.39s | Bus: 4.61s
  Reward Components (avg per step):
    Waiting:    -2.7184
    Flow:       +0.3476
    Sync:       +0.0625
    CO2:        -0.0092
    Equity:     -0.0232
    Safety:     -0.2097  (755 violations, 21.0% of steps)
    Pedestrian: -0.2718  (0 ignored, 0.0% of steps)
    TOTAL:      -2.8688
================================================================================

================================================================================
EPISODE 4
================================================================================
TRAFFIC CONFIG:
Episode 4 - Generating routes:
  Cars: 690/hr
  Bicycles: 450/hr
  Pedestrians: 353/hr
  Buses: every_15min

[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1290
  Actions blocked (MIN_GREEN_TIME): 3520
  Phase change rate: 17.9%
  Block rate: 48.9%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    3
  Total Distance Violations:   0
  Total Red Light Violations:  976
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     979
  Violation Rate:              27.19% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 4 Complete:
  Reward: -3.5976 | Loss: 0.4094 | Steps: 3600 | Epsilon: 0.922
  Avg Wait: 23.52s | Sync Rate: 43.67%
  Car: 46.01s | Bike: 21.46s | Bus: 1.52s
  Reward Components (avg per step):
    Waiting:    -3.3681
    Flow:       +0.3040
    Sync:       +0.0655
    CO2:        -0.0111
    Equity:     -0.0115
    Safety:     -0.2719  (979 violations, 27.2% of steps)
    Pedestrian: -0.2562  (0 ignored, 0.0% of steps)
    TOTAL:      -3.5976
================================================================================


========================================
Parsing complete!
