Parsing training log: training.log
========================================

================================================================================
EPISODE 1
================================================================================
TRAFFIC CONFIG:
Episode 1 - Generating routes (initial):
  Cars: 400
  Bicycles: 200
  Pedestrians: 400
  Buses: every_15min

[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1308
  Actions blocked (MIN_GREEN_TIME): 3524
  Phase change rate: 18.2%
  Block rate: 48.9%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    2
  Total Distance Violations:   0
  Total Red Light Violations:  859
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     861
  Violation Rate:              23.92% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 1 Complete:
  Reward: -0.5281 | Loss: 0.1929 | Steps: 3600 | Epsilon: 0.980
  Avg Wait: 4.36s | Sync Rate: 40.08%
  Car: 18.33s | Bike: 5.53s | Bus: 0.58s
  Reward Components (avg per step):
    Waiting:    -0.4686
    Flow:       +0.4636
    Sync:       +0.0601
    CO2:        -0.0088
    Equity:     -0.0159
    Safety:     -0.2392  (861 violations, 23.9% of steps)
    Pedestrian: -0.2709  (0 ignored, 0.0% of steps)
    TOTAL:      -0.5281
================================================================================

================================================================================
EPISODE 2
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1304
  Actions blocked (MIN_GREEN_TIME): 3682
  Phase change rate: 18.1%
  Block rate: 51.1%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    3
  Total Distance Violations:   0
  Total Red Light Violations:  864
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     867
  Violation Rate:              24.08% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 2 Complete:
  Reward: -4.9419 | Loss: 0.6420 | Steps: 3600 | Epsilon: 0.960
  Avg Wait: 29.51s | Sync Rate: 41.67%
  Car: 49.10s | Bike: 31.36s | Bus: 1.43s
  Reward Components (avg per step):
    Waiting:    -4.6771
    Flow:       +0.2541
    Sync:       +0.0625
    CO2:        -0.0074
    Equity:     -0.0080
    Safety:     -0.2408  (867 violations, 24.1% of steps)
    Pedestrian: -0.2942  (0 ignored, 0.0% of steps)
    TOTAL:      -4.9419
================================================================================

================================================================================
EPISODE 3
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1298
  Actions blocked (MIN_GREEN_TIME): 3578
  Phase change rate: 18.0%
  Block rate: 49.7%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    4
  Total Distance Violations:   0
  Total Red Light Violations:  850
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     854
  Violation Rate:              23.72% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 3 Complete:
  Reward: -4.5352 | Loss: 1.0317 | Steps: 3600 | Epsilon: 0.941
  Avg Wait: 25.20s | Sync Rate: 42.81%
  Car: 50.23s | Bike: 28.09s | Bus: 2.89s
  Reward Components (avg per step):
    Waiting:    -4.3164
    Flow:       +0.2900
    Sync:       +0.0642
    CO2:        -0.0082
    Equity:     -0.0101
    Safety:     -0.2372  (854 violations, 23.7% of steps)
    Pedestrian: -0.2769  (0 ignored, 0.0% of steps)
    TOTAL:      -4.5352
================================================================================

================================================================================
EPISODE 4
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1290
  Actions blocked (MIN_GREEN_TIME): 3394
  Phase change rate: 17.9%
  Block rate: 47.1%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    2
  Total Distance Violations:   0
  Total Red Light Violations:  838
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     840
  Violation Rate:              23.33% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 4 Complete:
  Reward: -2.9099 | Loss: 0.9462 | Steps: 3600 | Epsilon: 0.922
  Avg Wait: 18.24s | Sync Rate: 41.28%
  Car: 41.52s | Bike: 22.91s | Bus: 3.92s
  Reward Components (avg per step):
    Waiting:    -2.7574
    Flow:       +0.3480
    Sync:       +0.0619
    CO2:        -0.0078
    Equity:     -0.0102
    Safety:     -0.2333  (840 violations, 23.3% of steps)
    Pedestrian: -0.2644  (0 ignored, 0.0% of steps)
    TOTAL:      -2.9099
================================================================================

================================================================================
EPISODE 5
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1286
  Actions blocked (MIN_GREEN_TIME): 3304
  Phase change rate: 17.9%
  Block rate: 45.9%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    1
  Total Distance Violations:   0
  Total Red Light Violations:  638
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     639
  Violation Rate:              17.75% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 5 Complete:
  Reward: -0.4024 | Loss: 0.7778 | Steps: 3600 | Epsilon: 0.904
  Avg Wait: 2.91s | Sync Rate: 40.06%
  Car: 25.55s | Bike: 6.13s | Bus: 0.69s
  Reward Components (avg per step):
    Waiting:    -0.4109
    Flow:       +0.4757
    Sync:       +0.0601
    CO2:        -0.0045
    Equity:     -0.0180
    Safety:     -0.1775  (639 violations, 17.8% of steps)
    Pedestrian: -0.2820  (0 ignored, 0.0% of steps)
    TOTAL:      -0.4024
================================================================================

================================================================================
EPISODE 6
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1302
  Actions blocked (MIN_GREEN_TIME): 3512
  Phase change rate: 18.1%
  Block rate: 48.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    10
  Total Distance Violations:   0
  Total Red Light Violations:  845
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     855
  Violation Rate:              23.75% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 6 Complete:
  Reward: -2.4813 | Loss: 0.7481 | Steps: 3600 | Epsilon: 0.886
  Avg Wait: 15.57s | Sync Rate: 40.58%
  Car: 37.77s | Bike: 26.61s | Bus: 1.50s
  Reward Components (avg per step):
    Waiting:    -2.3426
    Flow:       +0.3703
    Sync:       +0.0609
    CO2:        -0.0056
    Equity:     -0.0061
    Safety:     -0.2375  (855 violations, 23.8% of steps)
    Pedestrian: -0.2724  (0 ignored, 0.0% of steps)
    TOTAL:      -2.4813
================================================================================

================================================================================
EPISODE 7
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1288
  Actions blocked (MIN_GREEN_TIME): 3444
  Phase change rate: 17.9%
  Block rate: 47.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    6
  Total Distance Violations:   0
  Total Red Light Violations:  910
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     916
  Violation Rate:              25.44% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 7 Complete:
  Reward: -5.8767 | Loss: 0.7736 | Steps: 3600 | Epsilon: 0.868
  Avg Wait: 35.68s | Sync Rate: 42.81%
  Car: 51.87s | Bike: 31.29s | Bus: 1.32s
  Reward Components (avg per step):
    Waiting:    -5.5814
    Flow:       +0.2027
    Sync:       +0.0642
    CO2:        -0.0118
    Equity:     -0.0083
    Safety:     -0.2544  (916 violations, 25.4% of steps)
    Pedestrian: -0.2709  (0 ignored, 0.0% of steps)
    TOTAL:      -5.8767
================================================================================

================================================================================
EPISODE 8
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1276
  Actions blocked (MIN_GREEN_TIME): 3268
  Phase change rate: 17.7%
  Block rate: 45.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    2
  Total Distance Violations:   0
  Total Red Light Violations:  802
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     804
  Violation Rate:              22.33% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 8 Complete:
  Reward: -2.3485 | Loss: 0.8068 | Steps: 3600 | Epsilon: 0.851
  Avg Wait: 17.64s | Sync Rate: 41.72%
  Car: 28.48s | Bike: 28.85s | Bus: 0.78s
  Reward Components (avg per step):
    Waiting:    -2.2122
    Flow:       +0.3530
    Sync:       +0.0626
    CO2:        -0.0055
    Equity:     -0.0038
    Safety:     -0.2233  (804 violations, 22.3% of steps)
    Pedestrian: -0.2749  (0 ignored, 0.0% of steps)
    TOTAL:      -2.3485
================================================================================

================================================================================
EPISODE 9
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1282
  Actions blocked (MIN_GREEN_TIME): 3154
  Phase change rate: 17.8%
  Block rate: 43.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    8
  Total Distance Violations:   0
  Total Red Light Violations:  843
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     851
  Violation Rate:              23.64% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 9 Complete:
  Reward: -2.5952 | Loss: 0.7472 | Steps: 3600 | Epsilon: 0.834
  Avg Wait: 17.01s | Sync Rate: 39.78%
  Car: 30.40s | Bike: 31.84s | Bus: 1.54s
  Reward Components (avg per step):
    Waiting:    -2.4574
    Flow:       +0.3582
    Sync:       +0.0597
    CO2:        -0.0032
    Equity:     -0.0047
    Safety:     -0.2364  (851 violations, 23.6% of steps)
    Pedestrian: -0.2682  (0 ignored, 0.0% of steps)
    TOTAL:      -2.5952
================================================================================

================================================================================
EPISODE 10
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1266
  Actions blocked (MIN_GREEN_TIME): 3292
  Phase change rate: 17.6%
  Block rate: 45.7%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    7
  Total Distance Violations:   0
  Total Red Light Violations:  976
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     983
  Violation Rate:              27.31% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 10 Complete:
  Reward: -3.9735 | Loss: 0.6987 | Steps: 3600 | Epsilon: 0.817
  Avg Wait: 25.30s | Sync Rate: 43.39%
  Car: 46.53s | Bike: 14.89s | Bus: 1.13s
  Reward Components (avg per step):
    Waiting:    -3.7170
    Flow:       +0.2892
    Sync:       +0.0651
    CO2:        -0.0120
    Equity:     -0.0160
    Safety:     -0.2731  (983 violations, 27.3% of steps)
    Pedestrian: -0.2651  (0 ignored, 0.0% of steps)
    TOTAL:      -3.9735
================================================================================

================================================================================
EPISODE 11
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1236
  Actions blocked (MIN_GREEN_TIME): 3062
  Phase change rate: 17.2%
  Block rate: 42.5%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    4
  Total Distance Violations:   0
  Total Red Light Violations:  719
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     723
  Violation Rate:              20.08% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 11 Complete:
  Reward: -3.0900 | Loss: 0.6619 | Steps: 3600 | Epsilon: 0.801
  Avg Wait: 16.73s | Sync Rate: 43.19%
  Car: 39.43s | Bike: 33.51s | Bus: 0.85s
  Reward Components (avg per step):
    Waiting:    -2.9873
    Flow:       +0.3606
    Sync:       +0.0648
    CO2:        -0.0028
    Equity:     -0.0038
    Safety:     -0.2008  (723 violations, 20.1% of steps)
    Pedestrian: -0.2793  (0 ignored, 0.0% of steps)
    TOTAL:      -3.0900
================================================================================

================================================================================
EPISODE 12
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1270
  Actions blocked (MIN_GREEN_TIME): 3210
  Phase change rate: 17.6%
  Block rate: 44.6%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    4
  Total Distance Violations:   0
  Total Red Light Violations:  895
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     899
  Violation Rate:              24.97% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 12 Complete:
  Reward: -0.6274 | Loss: 0.6398 | Steps: 3600 | Epsilon: 0.785
  Avg Wait: 4.92s | Sync Rate: 42.28%
  Car: 24.20s | Bike: 10.92s | Bus: 2.99s
  Reward Components (avg per step):
    Waiting:    -0.5695
    Flow:       +0.4590
    Sync:       +0.0634
    CO2:        -0.0052
    Equity:     -0.0119
    Safety:     -0.2497  (899 violations, 25.0% of steps)
    Pedestrian: -0.2700  (0 ignored, 0.0% of steps)
    TOTAL:      -0.6274
================================================================================

================================================================================
EPISODE 13
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1268
  Actions blocked (MIN_GREEN_TIME): 3268
  Phase change rate: 17.6%
  Block rate: 45.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    6
  Total Distance Violations:   0
  Total Red Light Violations:  902
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     908
  Violation Rate:              25.22% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 13 Complete:
  Reward: -0.8129 | Loss: 0.6543 | Steps: 3600 | Epsilon: 0.769
  Avg Wait: 5.16s | Sync Rate: 42.94%
  Car: 32.29s | Bike: 10.11s | Bus: 0.57s
  Reward Components (avg per step):
    Waiting:    -0.7798
    Flow:       +0.4570
    Sync:       +0.0644
    CO2:        -0.0046
    Equity:     -0.0159
    Safety:     -0.2522  (908 violations, 25.2% of steps)
    Pedestrian: -0.2371  (0 ignored, 0.0% of steps)
    TOTAL:      -0.8129
================================================================================

================================================================================
EPISODE 14
================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 1280
  Actions blocked (MIN_GREEN_TIME): 3310
  Phase change rate: 17.8%
  Block rate: 46.0%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    5
  Total Distance Violations:   0
  Total Red Light Violations:  865
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     870
  Violation Rate:              24.17% of steps
================================================================================

Interrupt signal received, trying to exit gracefully.

================================================================================
Episode 14 Complete:
  Reward: -0.4179 | Loss: 0.6312 | Steps: 3600 | Epsilon: 0.754
  Avg Wait: 3.21s | Sync Rate: 45.11%
  Car: 24.09s | Bike: 6.36s | Bus: 0.83s
  Reward Components (avg per step):
    Waiting:    -0.4135
    Flow:       +0.4732
    Sync:       +0.0677
    CO2:        -0.0045
    Equity:     -0.0171
    Safety:     -0.2417  (870 violations, 24.2% of steps)
    Pedestrian: -0.2369  (0 ignored, 0.0% of steps)
    TOTAL:      -0.4179
================================================================================


========================================
Parsing complete!
