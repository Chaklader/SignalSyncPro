================================================================================
SCENARIO 1 - Pr_0
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_0
  Cars: 100/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_0:
  Total actions: 10000
  Continue (0): 8908 (89.1%)
  Skip to P1 (1): 313 (3.1%)
  Next Phase (2): 779 (7.8%)

✓ Results for Pr_0 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 15112
  Phase changes executed: 1628
  Actions blocked (MIN_GREEN_TIME): 176
  Phase change rate: 10.8%
  Block rate: 1.2%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 305 events, Total: 6.10, Avg: 0.020
  next_bonus: 2 events, Total: 6.73, Avg: 3.364
  skip2p1_bonus: 1 events, Total: 0.30, Avg: 0.300
  stability_bonus: 33 events, Total: 5.58, Avg: 0.169

PHASE TRANSITION PATTERNS:
  P3 → P1: 105 times, Avg duration: 17.1s
  P2 → P1: 46 times, Avg duration: 3.0s
  P2 → P3: 105 times, Avg duration: 3.1s
  P1 → P2: 151 times, Avg duration: 35.0s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 4.0s, Total value: 0.15

===================

================================================================================
SCENARIO 2 - Pr_1
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_1
  Cars: 200/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_1:
  Total actions: 10000
  Continue (0): 8856 (88.6%)
  Skip to P1 (1): 271 (2.7%)
  Next Phase (2): 873 (8.7%)

✓ Results for Pr_1 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14872
  Phase changes executed: 1708
  Actions blocked (MIN_GREEN_TIME): 298
  Phase change rate: 11.5%
  Block rate: 2.0%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 290 events, Total: 6.10, Avg: 0.021
  early_change_penalty: 2 events, Total: 0.61, Avg: 0.303
  next_bonus: 1 events, Total: 3.36, Avg: 3.364
  skip2p1_bonus: 3 events, Total: 0.70, Avg: 0.233
  stability_bonus: 33 events, Total: 5.80, Avg: 0.176
  bus_penalty: 2 events, Total: 0.48, Avg: 0.240

PHASE TRANSITION PATTERNS:
  P3 → P1: 95 times, Avg duration: 17.7s
  P3 → P4: 13 times, Avg duration: 5.5s
  P2 → P1: 45 times, Avg duration: 3.1s
  P2 → P3: 108 times, Avg duration: 3.2s
  P4 → P1: 13 times, Avg duration: 2.0s
  P1 → P2: 153 times, Avg duration: 33.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 3 - Pr_2
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_2
  Cars: 300/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_2:
  Total actions: 10000
  Continue (0): 8676 (86.8%)
  Skip to P1 (1): 278 (2.8%)
  Next Phase (2): 1046 (10.5%)

✓ Results for Pr_2 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14558
  Phase changes executed: 1810
  Actions blocked (MIN_GREEN_TIME): 482
  Phase change rate: 12.4%
  Block rate: 3.3%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 267 events, Total: 5.37, Avg: 0.020
  early_change_penalty: 1 events, Total: 0.46, Avg: 0.458
  next_bonus: 2 events, Total: 6.73, Avg: 3.364
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 25 events, Total: 4.26, Avg: 0.170

PHASE TRANSITION PATTERNS:
  P3 → P1: 73 times, Avg duration: 18.0s
  P3 → P4: 32 times, Avg duration: 5.9s
  P2 → P1: 50 times, Avg duration: 3.0s
  P2 → P3: 107 times, Avg duration: 3.1s
  P4 → P1: 33 times, Avg duration: 2.0s
  P1 → P2: 157 times, Avg duration: 33.1s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 4 - Pr_3
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_3
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_3:
  Total actions: 10000
  Continue (0): 8550 (85.5%)
  Skip to P1 (1): 253 (2.5%)
  Next Phase (2): 1197 (12.0%)

✓ Results for Pr_3 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14176
  Phase changes executed: 1940
  Actions blocked (MIN_GREEN_TIME): 618
  Phase change rate: 13.7%
  Block rate: 4.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 267 events, Total: 6.37, Avg: 0.024
  early_change_penalty: 2 events, Total: 0.50, Avg: 0.250
  next_bonus: 4 events, Total: 14.09, Avg: 3.523
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 21 events, Total: 3.65, Avg: 0.174
  bus_penalty: 1 events, Total: 0.33, Avg: 0.330

PHASE TRANSITION PATTERNS:
  P3 → P1: 70 times, Avg duration: 18.6s
  P3 → P4: 45 times, Avg duration: 7.2s
  P2 → P1: 47 times, Avg duration: 3.1s
  P2 → P3: 115 times, Avg duration: 3.3s
  P4 → P1: 45 times, Avg duration: 2.0s
  P1 → P2: 163 times, Avg duration: 29.7s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 1.0s, Total value: 0.15

===================

================================================================================
SCENARIO 5 - Pr_4
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_4
  Cars: 500/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_4:
  Total actions: 10000
  Continue (0): 7285 (72.9%)
  Skip to P1 (1): 191 (1.9%)
  Next Phase (2): 2524 (25.2%)

✓ Results for Pr_4 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 12580
  Phase changes executed: 2472
  Actions blocked (MIN_GREEN_TIME): 1676
  Phase change rate: 19.7%
  Block rate: 13.3%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 157 events, Total: 2.87, Avg: 0.018
  early_change_penalty: 9 events, Total: 2.18, Avg: 0.242
  next_bonus: 1 events, Total: 3.36, Avg: 3.364
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 34 events, Total: 5.88, Avg: 0.173
  bus_penalty: 17 events, Total: 6.88, Avg: 0.405

PHASE TRANSITION PATTERNS:
  P3 → P1: 34 times, Avg duration: 17.2s
  P3 → P4: 107 times, Avg duration: 5.9s
  P2 → P1: 44 times, Avg duration: 3.1s
  P2 → P3: 141 times, Avg duration: 3.3s
  P4 → P1: 107 times, Avg duration: 2.0s
  P1 → P2: 185 times, Avg duration: 23.0s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 2 events, Avg wait: 2.0s, Total value: 0.30

===================

================================================================================
SCENARIO 6 - Pr_5
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_5
  Cars: 600/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_5:
  Total actions: 10000
  Continue (0): 6913 (69.1%)
  Skip to P1 (1): 168 (1.7%)
  Next Phase (2): 2919 (29.2%)

✓ Results for Pr_5 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 11520
  Phase changes executed: 2826
  Actions blocked (MIN_GREEN_TIME): 2166
  Phase change rate: 24.5%
  Block rate: 18.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 84 events, Total: 1.14, Avg: 0.014
  early_change_penalty: 13 events, Total: 3.44, Avg: 0.265
  next_bonus: 4 events, Total: 13.37, Avg: 3.341
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 19 events, Total: 3.18, Avg: 0.167
  bus_penalty: 9 events, Total: 3.58, Avg: 0.398

PHASE TRANSITION PATTERNS:
  P3 → P4: 153 times, Avg duration: 5.0s
  P2 → P1: 47 times, Avg duration: 3.1s
  P2 → P3: 153 times, Avg duration: 3.3s
  P4 → P1: 153 times, Avg duration: 2.0s
  P1 → P2: 201 times, Avg duration: 20.1s

===================

================================================================================
SCENARIO 7 - Pr_6
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_6
  Cars: 700/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_6:
  Total actions: 10000
  Continue (0): 6851 (68.5%)
  Skip to P1 (1): 170 (1.7%)
  Next Phase (2): 2979 (29.8%)

✓ Results for Pr_6 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 11428
  Phase changes executed: 2856
  Actions blocked (MIN_GREEN_TIME): 2284
  Phase change rate: 25.0%
  Block rate: 20.0%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 79 events, Total: 0.79, Avg: 0.010
  early_change_penalty: 8 events, Total: 2.08, Avg: 0.260
  next_bonus: 6 events, Total: 21.18, Avg: 3.530
  skip2p1_bonus: 2 events, Total: 0.40, Avg: 0.200
  stability_bonus: 23 events, Total: 3.79, Avg: 0.165
  bus_penalty: 16 events, Total: 5.57, Avg: 0.348

PHASE TRANSITION PATTERNS:
  P3 → P4: 157 times, Avg duration: 5.0s
  P2 → P1: 43 times, Avg duration: 3.3s
  P2 → P3: 157 times, Avg duration: 3.3s
  P4 → P1: 157 times, Avg duration: 2.0s
  P1 → P2: 200 times, Avg duration: 19.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 8 - Pr_7
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_7
  Cars: 800/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_7:
  Total actions: 10000
  Continue (0): 6957 (69.6%)
  Skip to P1 (1): 147 (1.5%)
  Next Phase (2): 2896 (29.0%)

✓ Results for Pr_7 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 11260
  Phase changes executed: 2912
  Actions blocked (MIN_GREEN_TIME): 2308
  Phase change rate: 25.9%
  Block rate: 20.5%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 69 events, Total: 0.79, Avg: 0.011
  early_change_penalty: 13 events, Total: 3.57, Avg: 0.274
  next_bonus: 4 events, Total: 15.36, Avg: 3.841
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 21 events, Total: 3.52, Avg: 0.168
  bus_penalty: 10 events, Total: 3.96, Avg: 0.396

PHASE TRANSITION PATTERNS:
  P3 → P4: 163 times, Avg duration: 5.0s
  P2 → P1: 37 times, Avg duration: 3.4s
  P2 → P3: 164 times, Avg duration: 3.5s
  P4 → P1: 163 times, Avg duration: 2.0s
  P1 → P2: 201 times, Avg duration: 18.9s

===================

================================================================================
SCENARIO 9 - Pr_8
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_8
  Cars: 900/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_8:
  Total actions: 10000
  Continue (0): 6763 (67.6%)
  Skip to P1 (1): 139 (1.4%)
  Next Phase (2): 3098 (31.0%)

✓ Results for Pr_8 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 11104
  Phase changes executed: 2966
  Actions blocked (MIN_GREEN_TIME): 2406
  Phase change rate: 26.7%
  Block rate: 21.7%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 62 events, Total: 0.62, Avg: 0.010
  early_change_penalty: 12 events, Total: 3.17, Avg: 0.264
  next_bonus: 6 events, Total: 21.18, Avg: 3.530
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 14 events, Total: 2.42, Avg: 0.173
  bus_penalty: 11 events, Total: 4.11, Avg: 0.374

PHASE TRANSITION PATTERNS:
  P3 → P1: 1 times, Avg duration: 13.0s
  P3 → P4: 168 times, Avg duration: 5.0s
  P2 → P1: 33 times, Avg duration: 3.4s
  P2 → P3: 169 times, Avg duration: 3.5s
  P4 → P1: 168 times, Avg duration: 2.0s
  P1 → P2: 203 times, Avg duration: 18.0s

===================

================================================================================
SCENARIO 10 - Pr_9
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_9
  Cars: 1000/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_9:
  Total actions: 10000
  Continue (0): 6701 (67.0%)
  Skip to P1 (1): 156 (1.6%)
  Next Phase (2): 3143 (31.4%)

✓ Results for Pr_9 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 11140
  Phase changes executed: 2954
  Actions blocked (MIN_GREEN_TIME): 2388
  Phase change rate: 26.5%
  Block rate: 21.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 64 events, Total: 0.64, Avg: 0.010
  early_change_penalty: 15 events, Total: 4.25, Avg: 0.284
  next_bonus: 4 events, Total: 14.09, Avg: 3.523
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 10 events, Total: 1.62, Avg: 0.162
  bus_penalty: 18 events, Total: 6.04, Avg: 0.336

PHASE TRANSITION PATTERNS:
  P3 → P4: 165 times, Avg duration: 5.0s
  P2 → P1: 39 times, Avg duration: 3.3s
  P2 → P3: 165 times, Avg duration: 3.4s
  P4 → P1: 165 times, Avg duration: 2.0s
  P1 → P2: 205 times, Avg duration: 18.2s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 11 - Bi_0
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_0
  Cars: 400/hr
  Bicycles: 100/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_0:
  Total actions: 10000
  Continue (0): 8352 (83.5%)
  Skip to P1 (1): 249 (2.5%)
  Next Phase (2): 1399 (14.0%)

✓ Results for Bi_0 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13888
  Phase changes executed: 2036
  Actions blocked (MIN_GREEN_TIME): 880
  Phase change rate: 14.7%
  Block rate: 6.3%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 234 events, Total: 4.94, Avg: 0.021
  early_change_penalty: 4 events, Total: 1.14, Avg: 0.286
  skip2p1_bonus: 4 events, Total: 0.90, Avg: 0.225
  stability_bonus: 38 events, Total: 6.46, Avg: 0.170

PHASE TRANSITION PATTERNS:
  P3 → P1: 60 times, Avg duration: 19.1s
  P3 → P4: 61 times, Avg duration: 5.7s
  P2 → P1: 42 times, Avg duration: 3.1s
  P2 → P3: 121 times, Avg duration: 3.4s
  P4 → P1: 61 times, Avg duration: 2.0s
  P1 → P2: 164 times, Avg duration: 29.2s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 12 - Bi_1
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_1
  Cars: 400/hr
  Bicycles: 200/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_1:
  Total actions: 10000
  Continue (0): 8115 (81.2%)
  Skip to P1 (1): 203 (2.0%)
  Next Phase (2): 1682 (16.8%)

✓ Results for Bi_1 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13494
  Phase changes executed: 2168
  Actions blocked (MIN_GREEN_TIME): 1238
  Phase change rate: 16.1%
  Block rate: 9.2%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 202 events, Total: 4.22, Avg: 0.021
  early_change_penalty: 9 events, Total: 1.87, Avg: 0.208
  next_bonus: 4 events, Total: 13.18, Avg: 3.296
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 30 events, Total: 5.04, Avg: 0.168
  bus_penalty: 2 events, Total: 0.38, Avg: 0.190

PHASE TRANSITION PATTERNS:
  P3 → P1: 32 times, Avg duration: 19.8s
  P3 → P4: 92 times, Avg duration: 5.7s
  P2 → P1: 39 times, Avg duration: 3.2s
  P2 → P3: 124 times, Avg duration: 3.4s
  P4 → P1: 92 times, Avg duration: 2.0s
  P1 → P2: 163 times, Avg duration: 29.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 2 events, Avg wait: 2.0s, Total value: 0.30

===================

================================================================================
SCENARIO 13 - Bi_2
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_2
  Cars: 400/hr
  Bicycles: 300/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_2:
  Total actions: 10000
  Continue (0): 8098 (81.0%)
  Skip to P1 (1): 215 (2.1%)
  Next Phase (2): 1687 (16.9%)

✓ Results for Bi_2 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13516
  Phase changes executed: 2160
  Actions blocked (MIN_GREEN_TIME): 1186
  Phase change rate: 16.0%
  Block rate: 8.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 208 events, Total: 4.48, Avg: 0.022
  early_change_penalty: 7 events, Total: 1.67, Avg: 0.238
  next_bonus: 5 events, Total: 16.55, Avg: 3.309
  skip2p1_bonus: 2 events, Total: 0.50, Avg: 0.250
  stability_bonus: 25 events, Total: 4.31, Avg: 0.172
  bus_penalty: 4 events, Total: 1.28, Avg: 0.320

PHASE TRANSITION PATTERNS:
  P3 → P1: 46 times, Avg duration: 19.0s
  P3 → P4: 79 times, Avg duration: 5.1s
  P2 → P1: 42 times, Avg duration: 3.2s
  P2 → P3: 126 times, Avg duration: 3.3s
  P4 → P1: 79 times, Avg duration: 2.0s
  P1 → P2: 168 times, Avg duration: 28.4s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 2.0s, Total value: 0.15

===================

================================================================================
SCENARIO 14 - Bi_3
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_3
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_3:
  Total actions: 10000
  Continue (0): 8311 (83.1%)
  Skip to P1 (1): 228 (2.3%)
  Next Phase (2): 1461 (14.6%)

✓ Results for Bi_3 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13736
  Phase changes executed: 2084
  Actions blocked (MIN_GREEN_TIME): 906
  Phase change rate: 15.2%
  Block rate: 6.6%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 218 events, Total: 5.13, Avg: 0.024
  early_change_penalty: 2 events, Total: 0.63, Avg: 0.315
  next_bonus: 1 events, Total: 3.27, Avg: 3.273
  skip2p1_bonus: 1 events, Total: 0.30, Avg: 0.300
  stability_bonus: 28 events, Total: 4.76, Avg: 0.170
  bus_penalty: 4 events, Total: 0.91, Avg: 0.227

PHASE TRANSITION PATTERNS:
  P3 → P1: 43 times, Avg duration: 19.0s
  P3 → P4: 73 times, Avg duration: 6.0s
  P2 → P1: 48 times, Avg duration: 3.1s
  P2 → P3: 117 times, Avg duration: 3.2s
  P4 → P1: 74 times, Avg duration: 2.0s
  P1 → P2: 166 times, Avg duration: 29.6s

===================

================================================================================
SCENARIO 15 - Bi_4
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_4
  Cars: 400/hr
  Bicycles: 500/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_4:
  Total actions: 10000
  Continue (0): 8005 (80.0%)
  Skip to P1 (1): 216 (2.2%)
  Next Phase (2): 1779 (17.8%)

✓ Results for Bi_4 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13276
  Phase changes executed: 2240
  Actions blocked (MIN_GREEN_TIME): 1208
  Phase change rate: 16.9%
  Block rate: 9.1%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 189 events, Total: 3.74, Avg: 0.020
  early_change_penalty: 1 events, Total: 0.21, Avg: 0.214
  next_bonus: 3 events, Total: 10.73, Avg: 3.576
  skip2p1_bonus: 1 events, Total: 0.30, Avg: 0.300
  stability_bonus: 33 events, Total: 5.56, Avg: 0.169
  bus_penalty: 4 events, Total: 1.31, Avg: 0.327

PHASE TRANSITION PATTERNS:
  P3 → P1: 36 times, Avg duration: 19.7s
  P3 → P4: 92 times, Avg duration: 5.1s
  P2 → P1: 41 times, Avg duration: 3.2s
  P2 → P3: 129 times, Avg duration: 3.2s
  P4 → P1: 92 times, Avg duration: 2.0s
  P1 → P2: 170 times, Avg duration: 27.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 16 - Bi_5
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_5
  Cars: 400/hr
  Bicycles: 600/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_5:
  Total actions: 10000
  Continue (0): 8579 (85.8%)
  Skip to P1 (1): 240 (2.4%)
  Next Phase (2): 1181 (11.8%)

✓ Results for Bi_5 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14212
  Phase changes executed: 1928
  Actions blocked (MIN_GREEN_TIME): 620
  Phase change rate: 13.6%
  Block rate: 4.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 250 events, Total: 5.60, Avg: 0.022
  early_change_penalty: 2 events, Total: 0.50, Avg: 0.250
  next_bonus: 5 events, Total: 18.64, Avg: 3.727
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 39 events, Total: 6.72, Avg: 0.172

PHASE TRANSITION PATTERNS:
  P3 → P1: 58 times, Avg duration: 18.9s
  P3 → P4: 56 times, Avg duration: 6.1s
  P2 → P1: 42 times, Avg duration: 3.1s
  P2 → P3: 114 times, Avg duration: 3.3s
  P4 → P1: 56 times, Avg duration: 2.0s
  P1 → P2: 156 times, Avg duration: 32.2s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 3 events, Avg wait: 0.7s, Total value: 0.45

===================

================================================================================
SCENARIO 17 - Bi_6
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_6
  Cars: 400/hr
  Bicycles: 700/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_6:
  Total actions: 10000
  Continue (0): 8257 (82.6%)
  Skip to P1 (1): 205 (2.1%)
  Next Phase (2): 1538 (15.4%)

✓ Results for Bi_6 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13710
  Phase changes executed: 2090
  Actions blocked (MIN_GREEN_TIME): 1032
  Phase change rate: 15.2%
  Block rate: 7.5%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 188 events, Total: 3.93, Avg: 0.021
  early_change_penalty: 4 events, Total: 1.16, Avg: 0.291
  next_bonus: 3 events, Total: 10.00, Avg: 3.334
  skip2p1_bonus: 3 events, Total: 0.70, Avg: 0.233
  stability_bonus: 40 events, Total: 6.87, Avg: 0.172
  bus_penalty: 2 events, Total: 0.52, Avg: 0.260

PHASE TRANSITION PATTERNS:
  P3 → P1: 20 times, Avg duration: 20.0s
  P3 → P4: 90 times, Avg duration: 5.2s
  P2 → P1: 47 times, Avg duration: 3.1s
  P2 → P3: 113 times, Avg duration: 3.2s
  P4 → P1: 92 times, Avg duration: 2.0s
  P1 → P2: 160 times, Avg duration: 32.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 2 events, Avg wait: 2.0s, Total value: 0.30

===================

================================================================================
SCENARIO 18 - Bi_7
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_7
  Cars: 400/hr
  Bicycles: 800/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_7:
  Total actions: 10000
  Continue (0): 8320 (83.2%)
  Skip to P1 (1): 257 (2.6%)
  Next Phase (2): 1423 (14.2%)

✓ Results for Bi_7 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13958
  Phase changes executed: 2010
  Actions blocked (MIN_GREEN_TIME): 940
  Phase change rate: 14.4%
  Block rate: 6.7%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 236 events, Total: 5.36, Avg: 0.023
  early_change_penalty: 4 events, Total: 1.08, Avg: 0.271
  next_bonus: 4 events, Total: 14.00, Avg: 3.500
  skip2p1_bonus: 3 events, Total: 0.70, Avg: 0.233
  stability_bonus: 35 events, Total: 5.93, Avg: 0.169
  bus_penalty: 1 events, Total: 0.25, Avg: 0.250

PHASE TRANSITION PATTERNS:
  P3 → P1: 45 times, Avg duration: 19.8s
  P3 → P4: 69 times, Avg duration: 5.3s
  P2 → P1: 44 times, Avg duration: 3.1s
  P2 → P3: 115 times, Avg duration: 3.2s
  P4 → P1: 70 times, Avg duration: 2.0s
  P1 → P2: 159 times, Avg duration: 31.7s

===================

================================================================================
SCENARIO 19 - Bi_8
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_8
  Cars: 400/hr
  Bicycles: 900/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_8:
  Total actions: 10000
  Continue (0): 8295 (83.0%)
  Skip to P1 (1): 227 (2.3%)
  Next Phase (2): 1478 (14.8%)

✓ Results for Bi_8 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13914
  Phase changes executed: 2018
  Actions blocked (MIN_GREEN_TIME): 1022
  Phase change rate: 14.5%
  Block rate: 7.3%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 223 events, Total: 5.03, Avg: 0.023
  early_change_penalty: 6 events, Total: 1.34, Avg: 0.224
  skip2p1_bonus: 3 events, Total: 0.80, Avg: 0.267
  stability_bonus: 32 events, Total: 5.42, Avg: 0.169
  bus_penalty: 1 events, Total: 0.28, Avg: 0.280

PHASE TRANSITION PATTERNS:
  P3 → P1: 26 times, Avg duration: 20.6s
  P3 → P4: 81 times, Avg duration: 5.9s
  P2 → P1: 44 times, Avg duration: 3.1s
  P2 → P3: 111 times, Avg duration: 3.3s
  P4 → P1: 85 times, Avg duration: 2.0s
  P1 → P2: 156 times, Avg duration: 33.3s

===================

================================================================================
SCENARIO 20 - Bi_9
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_9
  Cars: 400/hr
  Bicycles: 1000/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_9:
  Total actions: 10000
  Continue (0): 8314 (83.1%)
  Skip to P1 (1): 255 (2.5%)
  Next Phase (2): 1431 (14.3%)

✓ Results for Bi_9 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14102
  Phase changes executed: 1962
  Actions blocked (MIN_GREEN_TIME): 1094
  Phase change rate: 13.9%
  Block rate: 7.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 246 events, Total: 6.16, Avg: 0.025
  early_change_penalty: 5 events, Total: 1.48, Avg: 0.296
  next_bonus: 3 events, Total: 10.64, Avg: 3.546
  skip2p1_bonus: 3 events, Total: 0.80, Avg: 0.267
  stability_bonus: 37 events, Total: 6.36, Avg: 0.172

PHASE TRANSITION PATTERNS:
  P3 → P1: 41 times, Avg duration: 20.5s
  P3 → P4: 68 times, Avg duration: 6.5s
  P2 → P1: 45 times, Avg duration: 3.1s
  P2 → P3: 111 times, Avg duration: 3.1s
  P4 → P1: 69 times, Avg duration: 2.0s
  P1 → P2: 156 times, Avg duration: 32.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 2.0s, Total value: 0.15

===================

================================================================================
SCENARIO 21 - Pe_0
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_0
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 100/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_0:
  Total actions: 10000
  Continue (0): 8247 (82.5%)
  Skip to P1 (1): 229 (2.3%)
  Next Phase (2): 1524 (15.2%)

✓ Results for Pe_0 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13718
  Phase changes executed: 2090
  Actions blocked (MIN_GREEN_TIME): 938
  Phase change rate: 15.2%
  Block rate: 6.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 224 events, Total: 4.84, Avg: 0.022
  early_change_penalty: 6 events, Total: 1.78, Avg: 0.297
  next_bonus: 3 events, Total: 11.18, Avg: 3.727
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 40 events, Total: 6.68, Avg: 0.167
  bus_penalty: 2 events, Total: 0.67, Avg: 0.333

PHASE TRANSITION PATTERNS:
  P3 → P1: 52 times, Avg duration: 18.9s
  P3 → P4: 72 times, Avg duration: 5.4s
  P2 → P1: 38 times, Avg duration: 3.0s
  P2 → P3: 125 times, Avg duration: 3.3s
  P4 → P1: 72 times, Avg duration: 2.0s
  P1 → P2: 163 times, Avg duration: 29.4s

===================

================================================================================
SCENARIO 22 - Pe_1
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_1
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 200/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_1:
  Total actions: 10000
  Continue (0): 8378 (83.8%)
  Skip to P1 (1): 237 (2.4%)
  Next Phase (2): 1385 (13.9%)

✓ Results for Pe_1 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13924
  Phase changes executed: 2024
  Actions blocked (MIN_GREEN_TIME): 858
  Phase change rate: 14.5%
  Block rate: 6.2%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 246 events, Total: 5.26, Avg: 0.021
  early_change_penalty: 4 events, Total: 0.96, Avg: 0.241
  skip2p1_bonus: 1 events, Total: 0.30, Avg: 0.300
  stability_bonus: 33 events, Total: 5.62, Avg: 0.170
  bus_penalty: 1 events, Total: 0.53, Avg: 0.530

PHASE TRANSITION PATTERNS:
  P3 → P1: 62 times, Avg duration: 18.5s
  P3 → P4: 58 times, Avg duration: 6.3s
  P2 → P1: 43 times, Avg duration: 3.0s
  P2 → P3: 121 times, Avg duration: 3.3s
  P4 → P1: 58 times, Avg duration: 2.0s
  P1 → P2: 164 times, Avg duration: 29.2s

===================

================================================================================
SCENARIO 23 - Pe_2
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_2
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 300/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_2:
  Total actions: 10000
  Continue (0): 8580 (85.8%)
  Skip to P1 (1): 243 (2.4%)
  Next Phase (2): 1177 (11.8%)

✓ Results for Pe_2 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14258
  Phase changes executed: 1912
  Actions blocked (MIN_GREEN_TIME): 564
  Phase change rate: 13.4%
  Block rate: 4.0%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 261 events, Total: 6.01, Avg: 0.023
  early_change_penalty: 1 events, Total: 0.21, Avg: 0.214
  next_bonus: 5 events, Total: 17.36, Avg: 3.473
  skip2p1_bonus: 1 events, Total: 0.30, Avg: 0.300
  stability_bonus: 50 events, Total: 8.73, Avg: 0.175
  bus_penalty: 3 events, Total: 0.61, Avg: 0.203

PHASE TRANSITION PATTERNS:
  P3 → P1: 69 times, Avg duration: 18.7s
  P3 → P4: 45 times, Avg duration: 6.4s
  P2 → P1: 44 times, Avg duration: 3.2s
  P2 → P3: 115 times, Avg duration: 3.3s
  P4 → P1: 46 times, Avg duration: 2.0s
  P1 → P2: 159 times, Avg duration: 30.9s

===================

================================================================================
SCENARIO 24 - Pe_3
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_3
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_3:
  Total actions: 10000
  Continue (0): 8395 (84.0%)
  Skip to P1 (1): 223 (2.2%)
  Next Phase (2): 1382 (13.8%)

✓ Results for Pe_3 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13910
  Phase changes executed: 2026
  Actions blocked (MIN_GREEN_TIME): 808
  Phase change rate: 14.6%
  Block rate: 5.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 233 events, Total: 5.08, Avg: 0.022
  early_change_penalty: 2 events, Total: 0.61, Avg: 0.303
  next_bonus: 1 events, Total: 3.36, Avg: 3.364
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 45 events, Total: 7.64, Avg: 0.170
  bus_penalty: 2 events, Total: 0.36, Avg: 0.180

PHASE TRANSITION PATTERNS:
  P3 → P1: 47 times, Avg duration: 19.1s
  P3 → P4: 68 times, Avg duration: 5.8s
  P2 → P1: 44 times, Avg duration: 3.2s
  P2 → P3: 117 times, Avg duration: 3.2s
  P4 → P1: 69 times, Avg duration: 2.0s
  P1 → P2: 161 times, Avg duration: 30.9s

===================

================================================================================
SCENARIO 25 - Pe_4
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_4
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 500/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_4:
  Total actions: 10000
  Continue (0): 8089 (80.9%)
  Skip to P1 (1): 191 (1.9%)
  Next Phase (2): 1720 (17.2%)

✓ Results for Pe_4 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13284
  Phase changes executed: 2238
  Actions blocked (MIN_GREEN_TIME): 1250
  Phase change rate: 16.8%
  Block rate: 9.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 156 events, Total: 2.61, Avg: 0.017
  early_change_penalty: 7 events, Total: 2.19, Avg: 0.313
  next_bonus: 4 events, Total: 13.46, Avg: 3.364
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 29 events, Total: 4.98, Avg: 0.172
  bus_penalty: 2 events, Total: 0.36, Avg: 0.180

PHASE TRANSITION PATTERNS:
  P3 → P1: 7 times, Avg duration: 20.9s
  P3 → P4: 112 times, Avg duration: 5.3s
  P2 → P1: 45 times, Avg duration: 3.2s
  P2 → P3: 119 times, Avg duration: 3.2s
  P4 → P1: 112 times, Avg duration: 2.0s
  P1 → P2: 165 times, Avg duration: 31.2s

===================

================================================================================
SCENARIO 26 - Pe_5
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_5
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 600/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_5:
  Total actions: 10000
  Continue (0): 8276 (82.8%)
  Skip to P1 (1): 225 (2.2%)
  Next Phase (2): 1499 (15.0%)

✓ Results for Pe_5 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13630
  Phase changes executed: 2114
  Actions blocked (MIN_GREEN_TIME): 936
  Phase change rate: 15.5%
  Block rate: 6.9%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 195 events, Total: 4.05, Avg: 0.021
  early_change_penalty: 1 events, Total: 0.38, Avg: 0.375
  next_bonus: 2 events, Total: 6.46, Avg: 3.228
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 25 events, Total: 4.32, Avg: 0.173
  bus_penalty: 1 events, Total: 0.21, Avg: 0.210

PHASE TRANSITION PATTERNS:
  P3 → P1: 26 times, Avg duration: 19.7s
  P3 → P4: 88 times, Avg duration: 5.4s
  P2 → P1: 44 times, Avg duration: 3.1s
  P2 → P3: 117 times, Avg duration: 3.3s
  P4 → P1: 91 times, Avg duration: 2.0s
  P1 → P2: 161 times, Avg duration: 31.4s

===================

================================================================================
SCENARIO 27 - Pe_6
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_6
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 700/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_6:
  Total actions: 10000
  Continue (0): 8304 (83.0%)
  Skip to P1 (1): 237 (2.4%)
  Next Phase (2): 1459 (14.6%)

✓ Results for Pe_6 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13744
  Phase changes executed: 2084
  Actions blocked (MIN_GREEN_TIME): 898
  Phase change rate: 15.2%
  Block rate: 6.5%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 212 events, Total: 4.37, Avg: 0.021
  early_change_penalty: 4 events, Total: 0.91, Avg: 0.227
  next_bonus: 2 events, Total: 7.27, Avg: 3.636
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 42 events, Total: 7.06, Avg: 0.168

PHASE TRANSITION PATTERNS:
  P3 → P1: 42 times, Avg duration: 19.4s
  P3 → P4: 75 times, Avg duration: 5.7s
  P2 → P1: 47 times, Avg duration: 3.1s
  P2 → P3: 117 times, Avg duration: 3.3s
  P4 → P1: 75 times, Avg duration: 2.0s
  P1 → P2: 165 times, Avg duration: 30.0s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 4.0s, Total value: 0.15

===================

================================================================================
SCENARIO 28 - Pe_7
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_7
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 800/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_7:
  Total actions: 10000
  Continue (0): 8310 (83.1%)
  Skip to P1 (1): 226 (2.3%)
  Next Phase (2): 1464 (14.6%)

✓ Results for Pe_7 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13732
  Phase changes executed: 2088
  Actions blocked (MIN_GREEN_TIME): 900
  Phase change rate: 15.2%
  Block rate: 6.6%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 218 events, Total: 4.73, Avg: 0.022
  early_change_penalty: 5 events, Total: 1.46, Avg: 0.293
  next_bonus: 3 events, Total: 10.00, Avg: 3.334
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 30 events, Total: 5.36, Avg: 0.179
  bus_penalty: 2 events, Total: 0.60, Avg: 0.302

PHASE TRANSITION PATTERNS:
  P3 → P1: 47 times, Avg duration: 19.3s
  P3 → P4: 73 times, Avg duration: 5.6s
  P2 → P1: 44 times, Avg duration: 3.1s
  P2 → P3: 120 times, Avg duration: 3.3s
  P4 → P1: 73 times, Avg duration: 2.0s
  P1 → P2: 165 times, Avg duration: 29.5s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 5 events, Avg wait: 2.2s, Total value: 0.75

===================

================================================================================
SCENARIO 29 - Pe_8
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_8
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 900/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_8:
  Total actions: 10000
  Continue (0): 8306 (83.1%)
  Skip to P1 (1): 209 (2.1%)
  Next Phase (2): 1485 (14.8%)

✓ Results for Pe_8 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13802
  Phase changes executed: 2062
  Actions blocked (MIN_GREEN_TIME): 846
  Phase change rate: 14.9%
  Block rate: 6.1%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 221 events, Total: 5.01, Avg: 0.023
  early_change_penalty: 4 events, Total: 1.04, Avg: 0.259
  next_bonus: 3 events, Total: 10.73, Avg: 3.576
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 24 events, Total: 4.08, Avg: 0.170
  bus_penalty: 7 events, Total: 1.86, Avg: 0.266

PHASE TRANSITION PATTERNS:
  P3 → P1: 52 times, Avg duration: 18.7s
  P3 → P4: 66 times, Avg duration: 5.8s
  P2 → P1: 45 times, Avg duration: 3.0s
  P2 → P3: 120 times, Avg duration: 3.3s
  P4 → P1: 67 times, Avg duration: 2.0s
  P1 → P2: 165 times, Avg duration: 29.4s

===================

================================================================================
SCENARIO 30 - Pe_9
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_9
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 1000/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_9:
  Total actions: 10000
  Continue (0): 7962 (79.6%)
  Skip to P1 (1): 219 (2.2%)
  Next Phase (2): 1819 (18.2%)

✓ Results for Pe_9 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13262
  Phase changes executed: 2242
  Actions blocked (MIN_GREEN_TIME): 1162
  Phase change rate: 16.9%
  Block rate: 8.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 194 events, Total: 4.09, Avg: 0.021
  early_change_penalty: 8 events, Total: 1.89, Avg: 0.236
  next_bonus: 7 events, Total: 24.09, Avg: 3.442
  skip2p1_bonus: 3 events, Total: 0.70, Avg: 0.233
  stability_bonus: 28 events, Total: 4.81, Avg: 0.172
  bus_penalty: 6 events, Total: 2.29, Avg: 0.381

PHASE TRANSITION PATTERNS:
  P3 → P1: 45 times, Avg duration: 18.7s
  P3 → P4: 83 times, Avg duration: 5.6s
  P2 → P1: 45 times, Avg duration: 3.2s
  P2 → P3: 129 times, Avg duration: 3.3s
  P4 → P1: 84 times, Avg duration: 2.0s
  P1 → P2: 174 times, Avg duration: 26.2s

===================

================================================================================
SCENARIO 1 - Pr_0
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_0
  Cars: 100/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_0:
  Total actions: 10000
  Continue (0): 8908 (89.1%)
  Skip to P1 (1): 313 (3.1%)
  Next Phase (2): 779 (7.8%)

✓ Results for Pr_0 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 15112
  Phase changes executed: 1628
  Actions blocked (MIN_GREEN_TIME): 176
  Phase change rate: 10.8%
  Block rate: 1.2%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 305 events, Total: 6.10, Avg: 0.020
  next_bonus: 2 events, Total: 6.73, Avg: 3.364
  skip2p1_bonus: 1 events, Total: 0.30, Avg: 0.300
  stability_bonus: 33 events, Total: 5.58, Avg: 0.169

PHASE TRANSITION PATTERNS:
  P3 → P1: 105 times, Avg duration: 17.1s
  P2 → P1: 46 times, Avg duration: 3.0s
  P2 → P3: 105 times, Avg duration: 3.1s
  P1 → P2: 151 times, Avg duration: 35.0s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 4.0s, Total value: 0.15

===================

================================================================================
SCENARIO 2 - Pr_1
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_1
  Cars: 200/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_1:
  Total actions: 10000
  Continue (0): 8856 (88.6%)
  Skip to P1 (1): 271 (2.7%)
  Next Phase (2): 873 (8.7%)

✓ Results for Pr_1 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14872
  Phase changes executed: 1708
  Actions blocked (MIN_GREEN_TIME): 298
  Phase change rate: 11.5%
  Block rate: 2.0%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 290 events, Total: 6.10, Avg: 0.021
  early_change_penalty: 2 events, Total: 0.61, Avg: 0.303
  next_bonus: 1 events, Total: 3.36, Avg: 3.364
  skip2p1_bonus: 3 events, Total: 0.70, Avg: 0.233
  stability_bonus: 33 events, Total: 5.80, Avg: 0.176
  bus_penalty: 2 events, Total: 0.48, Avg: 0.240

PHASE TRANSITION PATTERNS:
  P3 → P1: 95 times, Avg duration: 17.7s
  P3 → P4: 13 times, Avg duration: 5.5s
  P2 → P1: 45 times, Avg duration: 3.1s
  P2 → P3: 108 times, Avg duration: 3.2s
  P4 → P1: 13 times, Avg duration: 2.0s
  P1 → P2: 153 times, Avg duration: 33.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 3 - Pr_2
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_2
  Cars: 300/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_2:
  Total actions: 10000
  Continue (0): 8676 (86.8%)
  Skip to P1 (1): 278 (2.8%)
  Next Phase (2): 1046 (10.5%)

✓ Results for Pr_2 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14558
  Phase changes executed: 1810
  Actions blocked (MIN_GREEN_TIME): 482
  Phase change rate: 12.4%
  Block rate: 3.3%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 267 events, Total: 5.37, Avg: 0.020
  early_change_penalty: 1 events, Total: 0.46, Avg: 0.458
  next_bonus: 2 events, Total: 6.73, Avg: 3.364
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 25 events, Total: 4.26, Avg: 0.170

PHASE TRANSITION PATTERNS:
  P3 → P1: 73 times, Avg duration: 18.0s
  P3 → P4: 32 times, Avg duration: 5.9s
  P2 → P1: 50 times, Avg duration: 3.0s
  P2 → P3: 107 times, Avg duration: 3.1s
  P4 → P1: 33 times, Avg duration: 2.0s
  P1 → P2: 157 times, Avg duration: 33.1s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 4 - Pr_3
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_3
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_3:
  Total actions: 10000
  Continue (0): 8550 (85.5%)
  Skip to P1 (1): 253 (2.5%)
  Next Phase (2): 1197 (12.0%)

✓ Results for Pr_3 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14176
  Phase changes executed: 1940
  Actions blocked (MIN_GREEN_TIME): 618
  Phase change rate: 13.7%
  Block rate: 4.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 267 events, Total: 6.37, Avg: 0.024
  early_change_penalty: 2 events, Total: 0.50, Avg: 0.250
  next_bonus: 4 events, Total: 14.09, Avg: 3.523
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 21 events, Total: 3.65, Avg: 0.174
  bus_penalty: 1 events, Total: 0.33, Avg: 0.330

PHASE TRANSITION PATTERNS:
  P3 → P1: 70 times, Avg duration: 18.6s
  P3 → P4: 45 times, Avg duration: 7.2s
  P2 → P1: 47 times, Avg duration: 3.1s
  P2 → P3: 115 times, Avg duration: 3.3s
  P4 → P1: 45 times, Avg duration: 2.0s
  P1 → P2: 163 times, Avg duration: 29.7s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 1.0s, Total value: 0.15

===================

================================================================================
SCENARIO 5 - Pr_4
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_4
  Cars: 500/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_4:
  Total actions: 10000
  Continue (0): 7285 (72.9%)
  Skip to P1 (1): 191 (1.9%)
  Next Phase (2): 2524 (25.2%)

✓ Results for Pr_4 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 12580
  Phase changes executed: 2472
  Actions blocked (MIN_GREEN_TIME): 1676
  Phase change rate: 19.7%
  Block rate: 13.3%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 157 events, Total: 2.87, Avg: 0.018
  early_change_penalty: 9 events, Total: 2.18, Avg: 0.242
  next_bonus: 1 events, Total: 3.36, Avg: 3.364
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 34 events, Total: 5.88, Avg: 0.173
  bus_penalty: 17 events, Total: 6.88, Avg: 0.405

PHASE TRANSITION PATTERNS:
  P3 → P1: 34 times, Avg duration: 17.2s
  P3 → P4: 107 times, Avg duration: 5.9s
  P2 → P1: 44 times, Avg duration: 3.1s
  P2 → P3: 141 times, Avg duration: 3.3s
  P4 → P1: 107 times, Avg duration: 2.0s
  P1 → P2: 185 times, Avg duration: 23.0s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 2 events, Avg wait: 2.0s, Total value: 0.30

===================

================================================================================
SCENARIO 6 - Pr_5
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_5
  Cars: 600/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_5:
  Total actions: 10000
  Continue (0): 6913 (69.1%)
  Skip to P1 (1): 168 (1.7%)
  Next Phase (2): 2919 (29.2%)

✓ Results for Pr_5 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 11520
  Phase changes executed: 2826
  Actions blocked (MIN_GREEN_TIME): 2166
  Phase change rate: 24.5%
  Block rate: 18.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 84 events, Total: 1.14, Avg: 0.014
  early_change_penalty: 13 events, Total: 3.44, Avg: 0.265
  next_bonus: 4 events, Total: 13.37, Avg: 3.341
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 19 events, Total: 3.18, Avg: 0.167
  bus_penalty: 9 events, Total: 3.58, Avg: 0.398

PHASE TRANSITION PATTERNS:
  P3 → P4: 153 times, Avg duration: 5.0s
  P2 → P1: 47 times, Avg duration: 3.1s
  P2 → P3: 153 times, Avg duration: 3.3s
  P4 → P1: 153 times, Avg duration: 2.0s
  P1 → P2: 201 times, Avg duration: 20.1s

===================

================================================================================
SCENARIO 7 - Pr_6
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_6
  Cars: 700/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_6:
  Total actions: 10000
  Continue (0): 6851 (68.5%)
  Skip to P1 (1): 170 (1.7%)
  Next Phase (2): 2979 (29.8%)

✓ Results for Pr_6 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 11428
  Phase changes executed: 2856
  Actions blocked (MIN_GREEN_TIME): 2284
  Phase change rate: 25.0%
  Block rate: 20.0%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 79 events, Total: 0.79, Avg: 0.010
  early_change_penalty: 8 events, Total: 2.08, Avg: 0.260
  next_bonus: 6 events, Total: 21.18, Avg: 3.530
  skip2p1_bonus: 2 events, Total: 0.40, Avg: 0.200
  stability_bonus: 23 events, Total: 3.79, Avg: 0.165
  bus_penalty: 16 events, Total: 5.57, Avg: 0.348

PHASE TRANSITION PATTERNS:
  P3 → P4: 157 times, Avg duration: 5.0s
  P2 → P1: 43 times, Avg duration: 3.3s
  P2 → P3: 157 times, Avg duration: 3.3s
  P4 → P1: 157 times, Avg duration: 2.0s
  P1 → P2: 200 times, Avg duration: 19.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 8 - Pr_7
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_7
  Cars: 800/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_7:
  Total actions: 10000
  Continue (0): 6957 (69.6%)
  Skip to P1 (1): 147 (1.5%)
  Next Phase (2): 2896 (29.0%)

✓ Results for Pr_7 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 11260
  Phase changes executed: 2912
  Actions blocked (MIN_GREEN_TIME): 2308
  Phase change rate: 25.9%
  Block rate: 20.5%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 69 events, Total: 0.79, Avg: 0.011
  early_change_penalty: 13 events, Total: 3.57, Avg: 0.274
  next_bonus: 4 events, Total: 15.36, Avg: 3.841
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 21 events, Total: 3.52, Avg: 0.168
  bus_penalty: 10 events, Total: 3.96, Avg: 0.396

PHASE TRANSITION PATTERNS:
  P3 → P4: 163 times, Avg duration: 5.0s
  P2 → P1: 37 times, Avg duration: 3.4s
  P2 → P3: 164 times, Avg duration: 3.5s
  P4 → P1: 163 times, Avg duration: 2.0s
  P1 → P2: 201 times, Avg duration: 18.9s

===================

================================================================================
SCENARIO 9 - Pr_8
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_8
  Cars: 900/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_8:
  Total actions: 10000
  Continue (0): 6763 (67.6%)
  Skip to P1 (1): 139 (1.4%)
  Next Phase (2): 3098 (31.0%)

✓ Results for Pr_8 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 11104
  Phase changes executed: 2966
  Actions blocked (MIN_GREEN_TIME): 2406
  Phase change rate: 26.7%
  Block rate: 21.7%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 62 events, Total: 0.62, Avg: 0.010
  early_change_penalty: 12 events, Total: 3.17, Avg: 0.264
  next_bonus: 6 events, Total: 21.18, Avg: 3.530
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 14 events, Total: 2.42, Avg: 0.173
  bus_penalty: 11 events, Total: 4.11, Avg: 0.374

PHASE TRANSITION PATTERNS:
  P3 → P1: 1 times, Avg duration: 13.0s
  P3 → P4: 168 times, Avg duration: 5.0s
  P2 → P1: 33 times, Avg duration: 3.4s
  P2 → P3: 169 times, Avg duration: 3.5s
  P4 → P1: 168 times, Avg duration: 2.0s
  P1 → P2: 203 times, Avg duration: 18.0s

===================

================================================================================
SCENARIO 10 - Pr_9
================================================================================

TRAFFIC CONFIG:
Scenario: Pr_9
  Cars: 1000/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pr_9:
  Total actions: 10000
  Continue (0): 6701 (67.0%)
  Skip to P1 (1): 156 (1.6%)
  Next Phase (2): 3143 (31.4%)

✓ Results for Pr_9 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 11140
  Phase changes executed: 2954
  Actions blocked (MIN_GREEN_TIME): 2388
  Phase change rate: 26.5%
  Block rate: 21.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 64 events, Total: 0.64, Avg: 0.010
  early_change_penalty: 15 events, Total: 4.25, Avg: 0.284
  next_bonus: 4 events, Total: 14.09, Avg: 3.523
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 10 events, Total: 1.62, Avg: 0.162
  bus_penalty: 18 events, Total: 6.04, Avg: 0.336

PHASE TRANSITION PATTERNS:
  P3 → P4: 165 times, Avg duration: 5.0s
  P2 → P1: 39 times, Avg duration: 3.3s
  P2 → P3: 165 times, Avg duration: 3.4s
  P4 → P1: 165 times, Avg duration: 2.0s
  P1 → P2: 205 times, Avg duration: 18.2s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 11 - Bi_0
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_0
  Cars: 400/hr
  Bicycles: 100/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_0:
  Total actions: 10000
  Continue (0): 8352 (83.5%)
  Skip to P1 (1): 249 (2.5%)
  Next Phase (2): 1399 (14.0%)

✓ Results for Bi_0 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13888
  Phase changes executed: 2036
  Actions blocked (MIN_GREEN_TIME): 880
  Phase change rate: 14.7%
  Block rate: 6.3%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 234 events, Total: 4.94, Avg: 0.021
  early_change_penalty: 4 events, Total: 1.14, Avg: 0.286
  skip2p1_bonus: 4 events, Total: 0.90, Avg: 0.225
  stability_bonus: 38 events, Total: 6.46, Avg: 0.170

PHASE TRANSITION PATTERNS:
  P3 → P1: 60 times, Avg duration: 19.1s
  P3 → P4: 61 times, Avg duration: 5.7s
  P2 → P1: 42 times, Avg duration: 3.1s
  P2 → P3: 121 times, Avg duration: 3.4s
  P4 → P1: 61 times, Avg duration: 2.0s
  P1 → P2: 164 times, Avg duration: 29.2s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 12 - Bi_1
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_1
  Cars: 400/hr
  Bicycles: 200/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_1:
  Total actions: 10000
  Continue (0): 8115 (81.2%)
  Skip to P1 (1): 203 (2.0%)
  Next Phase (2): 1682 (16.8%)

✓ Results for Bi_1 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13494
  Phase changes executed: 2168
  Actions blocked (MIN_GREEN_TIME): 1238
  Phase change rate: 16.1%
  Block rate: 9.2%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 202 events, Total: 4.22, Avg: 0.021
  early_change_penalty: 9 events, Total: 1.87, Avg: 0.208
  next_bonus: 4 events, Total: 13.18, Avg: 3.296
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 30 events, Total: 5.04, Avg: 0.168
  bus_penalty: 2 events, Total: 0.38, Avg: 0.190

PHASE TRANSITION PATTERNS:
  P3 → P1: 32 times, Avg duration: 19.8s
  P3 → P4: 92 times, Avg duration: 5.7s
  P2 → P1: 39 times, Avg duration: 3.2s
  P2 → P3: 124 times, Avg duration: 3.4s
  P4 → P1: 92 times, Avg duration: 2.0s
  P1 → P2: 163 times, Avg duration: 29.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 2 events, Avg wait: 2.0s, Total value: 0.30

===================

================================================================================
SCENARIO 13 - Bi_2
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_2
  Cars: 400/hr
  Bicycles: 300/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_2:
  Total actions: 10000
  Continue (0): 8098 (81.0%)
  Skip to P1 (1): 215 (2.1%)
  Next Phase (2): 1687 (16.9%)

✓ Results for Bi_2 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13516
  Phase changes executed: 2160
  Actions blocked (MIN_GREEN_TIME): 1186
  Phase change rate: 16.0%
  Block rate: 8.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 208 events, Total: 4.48, Avg: 0.022
  early_change_penalty: 7 events, Total: 1.67, Avg: 0.238
  next_bonus: 5 events, Total: 16.55, Avg: 3.309
  skip2p1_bonus: 2 events, Total: 0.50, Avg: 0.250
  stability_bonus: 25 events, Total: 4.31, Avg: 0.172
  bus_penalty: 4 events, Total: 1.28, Avg: 0.320

PHASE TRANSITION PATTERNS:
  P3 → P1: 46 times, Avg duration: 19.0s
  P3 → P4: 79 times, Avg duration: 5.1s
  P2 → P1: 42 times, Avg duration: 3.2s
  P2 → P3: 126 times, Avg duration: 3.3s
  P4 → P1: 79 times, Avg duration: 2.0s
  P1 → P2: 168 times, Avg duration: 28.4s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 2.0s, Total value: 0.15

===================

================================================================================
SCENARIO 14 - Bi_3
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_3
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_3:
  Total actions: 10000
  Continue (0): 8311 (83.1%)
  Skip to P1 (1): 228 (2.3%)
  Next Phase (2): 1461 (14.6%)

✓ Results for Bi_3 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13736
  Phase changes executed: 2084
  Actions blocked (MIN_GREEN_TIME): 906
  Phase change rate: 15.2%
  Block rate: 6.6%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 218 events, Total: 5.13, Avg: 0.024
  early_change_penalty: 2 events, Total: 0.63, Avg: 0.315
  next_bonus: 1 events, Total: 3.27, Avg: 3.273
  skip2p1_bonus: 1 events, Total: 0.30, Avg: 0.300
  stability_bonus: 28 events, Total: 4.76, Avg: 0.170
  bus_penalty: 4 events, Total: 0.91, Avg: 0.227

PHASE TRANSITION PATTERNS:
  P3 → P1: 43 times, Avg duration: 19.0s
  P3 → P4: 73 times, Avg duration: 6.0s
  P2 → P1: 48 times, Avg duration: 3.1s
  P2 → P3: 117 times, Avg duration: 3.2s
  P4 → P1: 74 times, Avg duration: 2.0s
  P1 → P2: 166 times, Avg duration: 29.6s

===================

================================================================================
SCENARIO 15 - Bi_4
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_4
  Cars: 400/hr
  Bicycles: 500/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_4:
  Total actions: 10000
  Continue (0): 8005 (80.0%)
  Skip to P1 (1): 216 (2.2%)
  Next Phase (2): 1779 (17.8%)

✓ Results for Bi_4 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13276
  Phase changes executed: 2240
  Actions blocked (MIN_GREEN_TIME): 1208
  Phase change rate: 16.9%
  Block rate: 9.1%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 189 events, Total: 3.74, Avg: 0.020
  early_change_penalty: 1 events, Total: 0.21, Avg: 0.214
  next_bonus: 3 events, Total: 10.73, Avg: 3.576
  skip2p1_bonus: 1 events, Total: 0.30, Avg: 0.300
  stability_bonus: 33 events, Total: 5.56, Avg: 0.169
  bus_penalty: 4 events, Total: 1.31, Avg: 0.327

PHASE TRANSITION PATTERNS:
  P3 → P1: 36 times, Avg duration: 19.7s
  P3 → P4: 92 times, Avg duration: 5.1s
  P2 → P1: 41 times, Avg duration: 3.2s
  P2 → P3: 129 times, Avg duration: 3.2s
  P4 → P1: 92 times, Avg duration: 2.0s
  P1 → P2: 170 times, Avg duration: 27.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 0.0s, Total value: 0.15

===================

================================================================================
SCENARIO 16 - Bi_5
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_5
  Cars: 400/hr
  Bicycles: 600/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_5:
  Total actions: 10000
  Continue (0): 8579 (85.8%)
  Skip to P1 (1): 240 (2.4%)
  Next Phase (2): 1181 (11.8%)

✓ Results for Bi_5 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14212
  Phase changes executed: 1928
  Actions blocked (MIN_GREEN_TIME): 620
  Phase change rate: 13.6%
  Block rate: 4.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 250 events, Total: 5.60, Avg: 0.022
  early_change_penalty: 2 events, Total: 0.50, Avg: 0.250
  next_bonus: 5 events, Total: 18.64, Avg: 3.727
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 39 events, Total: 6.72, Avg: 0.172

PHASE TRANSITION PATTERNS:
  P3 → P1: 58 times, Avg duration: 18.9s
  P3 → P4: 56 times, Avg duration: 6.1s
  P2 → P1: 42 times, Avg duration: 3.1s
  P2 → P3: 114 times, Avg duration: 3.3s
  P4 → P1: 56 times, Avg duration: 2.0s
  P1 → P2: 156 times, Avg duration: 32.2s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 3 events, Avg wait: 0.7s, Total value: 0.45

===================

================================================================================
SCENARIO 17 - Bi_6
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_6
  Cars: 400/hr
  Bicycles: 700/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_6:
  Total actions: 10000
  Continue (0): 8257 (82.6%)
  Skip to P1 (1): 205 (2.1%)
  Next Phase (2): 1538 (15.4%)

✓ Results for Bi_6 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13710
  Phase changes executed: 2090
  Actions blocked (MIN_GREEN_TIME): 1032
  Phase change rate: 15.2%
  Block rate: 7.5%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 188 events, Total: 3.93, Avg: 0.021
  early_change_penalty: 4 events, Total: 1.16, Avg: 0.291
  next_bonus: 3 events, Total: 10.00, Avg: 3.334
  skip2p1_bonus: 3 events, Total: 0.70, Avg: 0.233
  stability_bonus: 40 events, Total: 6.87, Avg: 0.172
  bus_penalty: 2 events, Total: 0.52, Avg: 0.260

PHASE TRANSITION PATTERNS:
  P3 → P1: 20 times, Avg duration: 20.0s
  P3 → P4: 90 times, Avg duration: 5.2s
  P2 → P1: 47 times, Avg duration: 3.1s
  P2 → P3: 113 times, Avg duration: 3.2s
  P4 → P1: 92 times, Avg duration: 2.0s
  P1 → P2: 160 times, Avg duration: 32.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 2 events, Avg wait: 2.0s, Total value: 0.30

===================

================================================================================
SCENARIO 18 - Bi_7
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_7
  Cars: 400/hr
  Bicycles: 800/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_7:
  Total actions: 10000
  Continue (0): 8320 (83.2%)
  Skip to P1 (1): 257 (2.6%)
  Next Phase (2): 1423 (14.2%)

✓ Results for Bi_7 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13958
  Phase changes executed: 2010
  Actions blocked (MIN_GREEN_TIME): 940
  Phase change rate: 14.4%
  Block rate: 6.7%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 236 events, Total: 5.36, Avg: 0.023
  early_change_penalty: 4 events, Total: 1.08, Avg: 0.271
  next_bonus: 4 events, Total: 14.00, Avg: 3.500
  skip2p1_bonus: 3 events, Total: 0.70, Avg: 0.233
  stability_bonus: 35 events, Total: 5.93, Avg: 0.169
  bus_penalty: 1 events, Total: 0.25, Avg: 0.250

PHASE TRANSITION PATTERNS:
  P3 → P1: 45 times, Avg duration: 19.8s
  P3 → P4: 69 times, Avg duration: 5.3s
  P2 → P1: 44 times, Avg duration: 3.1s
  P2 → P3: 115 times, Avg duration: 3.2s
  P4 → P1: 70 times, Avg duration: 2.0s
  P1 → P2: 159 times, Avg duration: 31.7s

===================

================================================================================
SCENARIO 19 - Bi_8
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_8
  Cars: 400/hr
  Bicycles: 900/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_8:
  Total actions: 10000
  Continue (0): 8295 (83.0%)
  Skip to P1 (1): 227 (2.3%)
  Next Phase (2): 1478 (14.8%)

✓ Results for Bi_8 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13914
  Phase changes executed: 2018
  Actions blocked (MIN_GREEN_TIME): 1022
  Phase change rate: 14.5%
  Block rate: 7.3%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 223 events, Total: 5.03, Avg: 0.023
  early_change_penalty: 6 events, Total: 1.34, Avg: 0.224
  skip2p1_bonus: 3 events, Total: 0.80, Avg: 0.267
  stability_bonus: 32 events, Total: 5.42, Avg: 0.169
  bus_penalty: 1 events, Total: 0.28, Avg: 0.280

PHASE TRANSITION PATTERNS:
  P3 → P1: 26 times, Avg duration: 20.6s
  P3 → P4: 81 times, Avg duration: 5.9s
  P2 → P1: 44 times, Avg duration: 3.1s
  P2 → P3: 111 times, Avg duration: 3.3s
  P4 → P1: 85 times, Avg duration: 2.0s
  P1 → P2: 156 times, Avg duration: 33.3s

===================

================================================================================
SCENARIO 20 - Bi_9
================================================================================

TRAFFIC CONFIG:
Scenario: Bi_9
  Cars: 400/hr
  Bicycles: 1000/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Bi_9:
  Total actions: 10000
  Continue (0): 8314 (83.1%)
  Skip to P1 (1): 255 (2.5%)
  Next Phase (2): 1431 (14.3%)

✓ Results for Bi_9 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14102
  Phase changes executed: 1962
  Actions blocked (MIN_GREEN_TIME): 1094
  Phase change rate: 13.9%
  Block rate: 7.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 246 events, Total: 6.16, Avg: 0.025
  early_change_penalty: 5 events, Total: 1.48, Avg: 0.296
  next_bonus: 3 events, Total: 10.64, Avg: 3.546
  skip2p1_bonus: 3 events, Total: 0.80, Avg: 0.267
  stability_bonus: 37 events, Total: 6.36, Avg: 0.172

PHASE TRANSITION PATTERNS:
  P3 → P1: 41 times, Avg duration: 20.5s
  P3 → P4: 68 times, Avg duration: 6.5s
  P2 → P1: 45 times, Avg duration: 3.1s
  P2 → P3: 111 times, Avg duration: 3.1s
  P4 → P1: 69 times, Avg duration: 2.0s
  P1 → P2: 156 times, Avg duration: 32.8s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 2.0s, Total value: 0.15

===================

================================================================================
SCENARIO 21 - Pe_0
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_0
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 100/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_0:
  Total actions: 10000
  Continue (0): 8247 (82.5%)
  Skip to P1 (1): 229 (2.3%)
  Next Phase (2): 1524 (15.2%)

✓ Results for Pe_0 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13718
  Phase changes executed: 2090
  Actions blocked (MIN_GREEN_TIME): 938
  Phase change rate: 15.2%
  Block rate: 6.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 224 events, Total: 4.84, Avg: 0.022
  early_change_penalty: 6 events, Total: 1.78, Avg: 0.297
  next_bonus: 3 events, Total: 11.18, Avg: 3.727
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 40 events, Total: 6.68, Avg: 0.167
  bus_penalty: 2 events, Total: 0.67, Avg: 0.333

PHASE TRANSITION PATTERNS:
  P3 → P1: 52 times, Avg duration: 18.9s
  P3 → P4: 72 times, Avg duration: 5.4s
  P2 → P1: 38 times, Avg duration: 3.0s
  P2 → P3: 125 times, Avg duration: 3.3s
  P4 → P1: 72 times, Avg duration: 2.0s
  P1 → P2: 163 times, Avg duration: 29.4s

===================

================================================================================
SCENARIO 22 - Pe_1
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_1
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 200/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_1:
  Total actions: 10000
  Continue (0): 8378 (83.8%)
  Skip to P1 (1): 237 (2.4%)
  Next Phase (2): 1385 (13.9%)

✓ Results for Pe_1 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13924
  Phase changes executed: 2024
  Actions blocked (MIN_GREEN_TIME): 858
  Phase change rate: 14.5%
  Block rate: 6.2%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 246 events, Total: 5.26, Avg: 0.021
  early_change_penalty: 4 events, Total: 0.96, Avg: 0.241
  skip2p1_bonus: 1 events, Total: 0.30, Avg: 0.300
  stability_bonus: 33 events, Total: 5.62, Avg: 0.170
  bus_penalty: 1 events, Total: 0.53, Avg: 0.530

PHASE TRANSITION PATTERNS:
  P3 → P1: 62 times, Avg duration: 18.5s
  P3 → P4: 58 times, Avg duration: 6.3s
  P2 → P1: 43 times, Avg duration: 3.0s
  P2 → P3: 121 times, Avg duration: 3.3s
  P4 → P1: 58 times, Avg duration: 2.0s
  P1 → P2: 164 times, Avg duration: 29.2s

===================

================================================================================
SCENARIO 23 - Pe_2
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_2
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 300/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_2:
  Total actions: 10000
  Continue (0): 8580 (85.8%)
  Skip to P1 (1): 243 (2.4%)
  Next Phase (2): 1177 (11.8%)

✓ Results for Pe_2 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 14258
  Phase changes executed: 1912
  Actions blocked (MIN_GREEN_TIME): 564
  Phase change rate: 13.4%
  Block rate: 4.0%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 261 events, Total: 6.01, Avg: 0.023
  early_change_penalty: 1 events, Total: 0.21, Avg: 0.214
  next_bonus: 5 events, Total: 17.36, Avg: 3.473
  skip2p1_bonus: 1 events, Total: 0.30, Avg: 0.300
  stability_bonus: 50 events, Total: 8.73, Avg: 0.175
  bus_penalty: 3 events, Total: 0.61, Avg: 0.203

PHASE TRANSITION PATTERNS:
  P3 → P1: 69 times, Avg duration: 18.7s
  P3 → P4: 45 times, Avg duration: 6.4s
  P2 → P1: 44 times, Avg duration: 3.2s
  P2 → P3: 115 times, Avg duration: 3.3s
  P4 → P1: 46 times, Avg duration: 2.0s
  P1 → P2: 159 times, Avg duration: 30.9s

===================

================================================================================
SCENARIO 24 - Pe_3
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_3
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 400/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_3:
  Total actions: 10000
  Continue (0): 8395 (84.0%)
  Skip to P1 (1): 223 (2.2%)
  Next Phase (2): 1382 (13.8%)

✓ Results for Pe_3 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13910
  Phase changes executed: 2026
  Actions blocked (MIN_GREEN_TIME): 808
  Phase change rate: 14.6%
  Block rate: 5.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 233 events, Total: 5.08, Avg: 0.022
  early_change_penalty: 2 events, Total: 0.61, Avg: 0.303
  next_bonus: 1 events, Total: 3.36, Avg: 3.364
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 45 events, Total: 7.64, Avg: 0.170
  bus_penalty: 2 events, Total: 0.36, Avg: 0.180

PHASE TRANSITION PATTERNS:
  P3 → P1: 47 times, Avg duration: 19.1s
  P3 → P4: 68 times, Avg duration: 5.8s
  P2 → P1: 44 times, Avg duration: 3.2s
  P2 → P3: 117 times, Avg duration: 3.2s
  P4 → P1: 69 times, Avg duration: 2.0s
  P1 → P2: 161 times, Avg duration: 30.9s

===================

================================================================================
SCENARIO 25 - Pe_4
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_4
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 500/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_4:
  Total actions: 10000
  Continue (0): 8089 (80.9%)
  Skip to P1 (1): 191 (1.9%)
  Next Phase (2): 1720 (17.2%)

✓ Results for Pe_4 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13284
  Phase changes executed: 2238
  Actions blocked (MIN_GREEN_TIME): 1250
  Phase change rate: 16.8%
  Block rate: 9.4%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 156 events, Total: 2.61, Avg: 0.017
  early_change_penalty: 7 events, Total: 2.19, Avg: 0.313
  next_bonus: 4 events, Total: 13.46, Avg: 3.364
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 29 events, Total: 4.98, Avg: 0.172
  bus_penalty: 2 events, Total: 0.36, Avg: 0.180

PHASE TRANSITION PATTERNS:
  P3 → P1: 7 times, Avg duration: 20.9s
  P3 → P4: 112 times, Avg duration: 5.3s
  P2 → P1: 45 times, Avg duration: 3.2s
  P2 → P3: 119 times, Avg duration: 3.2s
  P4 → P1: 112 times, Avg duration: 2.0s
  P1 → P2: 165 times, Avg duration: 31.2s

===================

================================================================================
SCENARIO 26 - Pe_5
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_5
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 600/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_5:
  Total actions: 10000
  Continue (0): 8276 (82.8%)
  Skip to P1 (1): 225 (2.2%)
  Next Phase (2): 1499 (15.0%)

✓ Results for Pe_5 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13630
  Phase changes executed: 2114
  Actions blocked (MIN_GREEN_TIME): 936
  Phase change rate: 15.5%
  Block rate: 6.9%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 195 events, Total: 4.05, Avg: 0.021
  early_change_penalty: 1 events, Total: 0.38, Avg: 0.375
  next_bonus: 2 events, Total: 6.46, Avg: 3.228
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 25 events, Total: 4.32, Avg: 0.173
  bus_penalty: 1 events, Total: 0.21, Avg: 0.210

PHASE TRANSITION PATTERNS:
  P3 → P1: 26 times, Avg duration: 19.7s
  P3 → P4: 88 times, Avg duration: 5.4s
  P2 → P1: 44 times, Avg duration: 3.1s
  P2 → P3: 117 times, Avg duration: 3.3s
  P4 → P1: 91 times, Avg duration: 2.0s
  P1 → P2: 161 times, Avg duration: 31.4s

===================

================================================================================
SCENARIO 27 - Pe_6
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_6
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 700/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_6:
  Total actions: 10000
  Continue (0): 8304 (83.0%)
  Skip to P1 (1): 237 (2.4%)
  Next Phase (2): 1459 (14.6%)

✓ Results for Pe_6 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13744
  Phase changes executed: 2084
  Actions blocked (MIN_GREEN_TIME): 898
  Phase change rate: 15.2%
  Block rate: 6.5%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 212 events, Total: 4.37, Avg: 0.021
  early_change_penalty: 4 events, Total: 0.91, Avg: 0.227
  next_bonus: 2 events, Total: 7.27, Avg: 3.636
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 42 events, Total: 7.06, Avg: 0.168

PHASE TRANSITION PATTERNS:
  P3 → P1: 42 times, Avg duration: 19.4s
  P3 → P4: 75 times, Avg duration: 5.7s
  P2 → P1: 47 times, Avg duration: 3.1s
  P2 → P3: 117 times, Avg duration: 3.3s
  P4 → P1: 75 times, Avg duration: 2.0s
  P1 → P2: 165 times, Avg duration: 30.0s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 4.0s, Total value: 0.15

===================

================================================================================
SCENARIO 28 - Pe_7
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_7
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 800/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_7:
  Total actions: 10000
  Continue (0): 8310 (83.1%)
  Skip to P1 (1): 226 (2.3%)
  Next Phase (2): 1464 (14.6%)

✓ Results for Pe_7 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13732
  Phase changes executed: 2088
  Actions blocked (MIN_GREEN_TIME): 900
  Phase change rate: 15.2%
  Block rate: 6.6%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 218 events, Total: 4.73, Avg: 0.022
  early_change_penalty: 5 events, Total: 1.46, Avg: 0.293
  next_bonus: 3 events, Total: 10.00, Avg: 3.334
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 30 events, Total: 5.36, Avg: 0.179
  bus_penalty: 2 events, Total: 0.60, Avg: 0.302

PHASE TRANSITION PATTERNS:
  P3 → P1: 47 times, Avg duration: 19.3s
  P3 → P4: 73 times, Avg duration: 5.6s
  P2 → P1: 44 times, Avg duration: 3.1s
  P2 → P3: 120 times, Avg duration: 3.3s
  P4 → P1: 73 times, Avg duration: 2.0s
  P1 → P2: 165 times, Avg duration: 29.5s

BUS ASSISTANCE SUMMARY:
  bus_excellent: 5 events, Avg wait: 2.2s, Total value: 0.75

===================

================================================================================
SCENARIO 29 - Pe_8
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_8
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 900/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_8:
  Total actions: 10000
  Continue (0): 8306 (83.1%)
  Skip to P1 (1): 209 (2.1%)
  Next Phase (2): 1485 (14.8%)

✓ Results for Pe_8 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13802
  Phase changes executed: 2062
  Actions blocked (MIN_GREEN_TIME): 846
  Phase change rate: 14.9%
  Block rate: 6.1%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 221 events, Total: 5.01, Avg: 0.023
  early_change_penalty: 4 events, Total: 1.04, Avg: 0.259
  next_bonus: 3 events, Total: 10.73, Avg: 3.576
  skip2p1_bonus: 1 events, Total: 0.20, Avg: 0.200
  stability_bonus: 24 events, Total: 4.08, Avg: 0.170
  bus_penalty: 7 events, Total: 1.86, Avg: 0.266

PHASE TRANSITION PATTERNS:
  P3 → P1: 52 times, Avg duration: 18.7s
  P3 → P4: 66 times, Avg duration: 5.8s
  P2 → P1: 45 times, Avg duration: 3.0s
  P2 → P3: 120 times, Avg duration: 3.3s
  P4 → P1: 67 times, Avg duration: 2.0s
  P1 → P2: 165 times, Avg duration: 29.4s

===================

================================================================================
SCENARIO 30 - Pe_9
================================================================================

TRAFFIC CONFIG:
Scenario: Pe_9
  Cars: 400/hr
  Bicycles: 400/hr
  Pedestrians: 1000/hr
  Buses: every_15min/hr

[ACTION SUMMARY] Pe_9:
  Total actions: 10000
  Continue (0): 7962 (79.6%)
  Skip to P1 (1): 219 (2.2%)
  Next Phase (2): 1819 (18.2%)

✓ Results for Pe_9 saved to: results/drl_test_results_20251104_114708.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 13262
  Phase changes executed: 2242
  Actions blocked (MIN_GREEN_TIME): 1162
  Phase change rate: 16.9%
  Block rate: 8.8%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     0
  Violation Rate:              0.00% of steps
================================================================================

=== XAI ANALYSIS ===

REWARD BREAKDOWN:
  continue_spam_penalty: 194 events, Total: 4.09, Avg: 0.021
  early_change_penalty: 8 events, Total: 1.89, Avg: 0.236
  next_bonus: 7 events, Total: 24.09, Avg: 3.442
  skip2p1_bonus: 3 events, Total: 0.70, Avg: 0.233
  stability_bonus: 28 events, Total: 4.81, Avg: 0.172
  bus_penalty: 6 events, Total: 2.29, Avg: 0.381

PHASE TRANSITION PATTERNS:
  P3 → P1: 45 times, Avg duration: 18.7s
  P3 → P4: 83 times, Avg duration: 5.6s
  P2 → P1: 45 times, Avg duration: 3.2s
  P2 → P3: 129 times, Avg duration: 3.3s
  P4 → P1: 84 times, Avg duration: 2.0s
  P1 → P2: 174 times, Avg duration: 26.2s

===================

