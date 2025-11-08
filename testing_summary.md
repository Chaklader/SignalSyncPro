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

EXPLORATION VS EXPLOITATION:
  Exploitation: 407 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 4.0s, Total value: 0.15

===================

================================================================================
SCENARIO 2 - Pr_0
================================================================================

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
  continue_spam_penalty: 595 events, Total: 12.20, Avg: 0.021
  early_change_penalty: 2 events, Total: 0.61, Avg: 0.303
  next_bonus: 3 events, Total: 10.09, Avg: 3.364
  skip2p1_bonus: 4 events, Total: 1.00, Avg: 0.250
  stability_bonus: 66 events, Total: 11.38, Avg: 0.172
  bus_penalty: 2 events, Total: 0.48, Avg: 0.240

PHASE TRANSITION PATTERNS:
  P3 → P1: 200 times, Avg duration: 17.4s
  P3 → P4: 13 times, Avg duration: 5.5s
  P2 → P1: 91 times, Avg duration: 3.0s
  P2 → P3: 213 times, Avg duration: 3.2s
  P4 → P1: 13 times, Avg duration: 2.0s
  P1 → P2: 304 times, Avg duration: 34.4s

EXPLORATION VS EXPLOITATION:
  Exploitation: 834 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 2 events, Avg wait: 2.0s, Total value: 0.30

===================

================================================================================
SCENARIO 3 - Pr_0
================================================================================

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
  continue_spam_penalty: 862 events, Total: 17.57, Avg: 0.020
  early_change_penalty: 3 events, Total: 1.06, Avg: 0.355
  next_bonus: 5 events, Total: 16.82, Avg: 3.364
  skip2p1_bonus: 5 events, Total: 1.20, Avg: 0.240
  stability_bonus: 91 events, Total: 15.64, Avg: 0.172
  bus_penalty: 2 events, Total: 0.48, Avg: 0.240

PHASE TRANSITION PATTERNS:
  P3 → P1: 273 times, Avg duration: 17.5s
  P3 → P4: 45 times, Avg duration: 5.8s
  P2 → P1: 141 times, Avg duration: 3.0s
  P2 → P3: 320 times, Avg duration: 3.1s
  P4 → P1: 46 times, Avg duration: 2.0s
  P1 → P2: 461 times, Avg duration: 33.9s

EXPLORATION VS EXPLOITATION:
  Exploitation: 1286 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 3 events, Avg wait: 1.3s, Total value: 0.45

===================

================================================================================
SCENARIO 4 - Pr_0
================================================================================

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
  continue_spam_penalty: 1129 events, Total: 23.94, Avg: 0.021
  early_change_penalty: 5 events, Total: 1.56, Avg: 0.313
  next_bonus: 9 events, Total: 30.91, Avg: 3.435
  skip2p1_bonus: 6 events, Total: 1.40, Avg: 0.233
  stability_bonus: 112 events, Total: 19.29, Avg: 0.172
  bus_penalty: 3 events, Total: 0.81, Avg: 0.270

PHASE TRANSITION PATTERNS:
  P3 → P1: 343 times, Avg duration: 17.8s
  P3 → P4: 90 times, Avg duration: 6.5s
  P2 → P1: 188 times, Avg duration: 3.1s
  P2 → P3: 435 times, Avg duration: 3.2s
  P4 → P1: 91 times, Avg duration: 2.0s
  P1 → P2: 624 times, Avg duration: 32.8s

EXPLORATION VS EXPLOITATION:
  Exploitation: 1771 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 4 events, Avg wait: 1.2s, Total value: 0.60

===================

================================================================================
SCENARIO 5 - Pr_0
================================================================================

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
  continue_spam_penalty: 1286 events, Total: 26.81, Avg: 0.021
  early_change_penalty: 14 events, Total: 3.75, Avg: 0.268
  next_bonus: 10 events, Total: 34.28, Avg: 3.428
  skip2p1_bonus: 7 events, Total: 1.60, Avg: 0.229
  stability_bonus: 146 events, Total: 25.17, Avg: 0.172
  bus_penalty: 20 events, Total: 7.69, Avg: 0.384

PHASE TRANSITION PATTERNS:
  P3 → P1: 377 times, Avg duration: 17.7s
  P3 → P4: 197 times, Avg duration: 6.1s
  P2 → P1: 232 times, Avg duration: 3.1s
  P2 → P3: 576 times, Avg duration: 3.2s
  P4 → P1: 198 times, Avg duration: 2.0s
  P1 → P2: 809 times, Avg duration: 30.6s

EXPLORATION VS EXPLOITATION:
  Exploitation: 2389 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 6 events, Avg wait: 1.5s, Total value: 0.90

===================

================================================================================
SCENARIO 6 - Pr_0
================================================================================

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
  continue_spam_penalty: 1370 events, Total: 27.95, Avg: 0.020
  early_change_penalty: 27 events, Total: 7.19, Avg: 0.266
  next_bonus: 14 events, Total: 47.64, Avg: 3.403
  skip2p1_bonus: 8 events, Total: 1.80, Avg: 0.225
  stability_bonus: 165 events, Total: 28.35, Avg: 0.172
  bus_penalty: 29 events, Total: 11.27, Avg: 0.389

PHASE TRANSITION PATTERNS:
  P3 → P1: 377 times, Avg duration: 17.7s
  P3 → P4: 350 times, Avg duration: 5.6s
  P2 → P1: 279 times, Avg duration: 3.1s
  P2 → P3: 729 times, Avg duration: 3.2s
  P4 → P1: 351 times, Avg duration: 2.0s
  P1 → P2: 1010 times, Avg duration: 28.5s

EXPLORATION VS EXPLOITATION:
  Exploitation: 3096 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 6 events, Avg wait: 1.5s, Total value: 0.90

===================

================================================================================
SCENARIO 7 - Pr_0
================================================================================

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
  continue_spam_penalty: 1449 events, Total: 28.74, Avg: 0.020
  early_change_penalty: 35 events, Total: 9.27, Avg: 0.265
  next_bonus: 20 events, Total: 68.82, Avg: 3.441
  skip2p1_bonus: 10 events, Total: 2.20, Avg: 0.220
  stability_bonus: 188 events, Total: 32.14, Avg: 0.171
  bus_penalty: 45 events, Total: 16.84, Avg: 0.374

PHASE TRANSITION PATTERNS:
  P3 → P1: 377 times, Avg duration: 17.7s
  P3 → P4: 507 times, Avg duration: 5.4s
  P2 → P1: 322 times, Avg duration: 3.1s
  P2 → P3: 886 times, Avg duration: 3.2s
  P4 → P1: 508 times, Avg duration: 2.0s
  P1 → P2: 1210 times, Avg duration: 27.1s

EXPLORATION VS EXPLOITATION:
  Exploitation: 3810 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 7 events, Avg wait: 1.3s, Total value: 1.05

===================

================================================================================
SCENARIO 8 - Pr_0
================================================================================

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
  continue_spam_penalty: 1518 events, Total: 29.53, Avg: 0.019
  early_change_penalty: 48 events, Total: 12.84, Avg: 0.267
  next_bonus: 24 events, Total: 84.19, Avg: 3.508
  skip2p1_bonus: 11 events, Total: 2.40, Avg: 0.218
  stability_bonus: 209 events, Total: 35.66, Avg: 0.171
  bus_penalty: 55 events, Total: 20.80, Avg: 0.378

PHASE TRANSITION PATTERNS:
  P3 → P1: 377 times, Avg duration: 17.7s
  P3 → P4: 670 times, Avg duration: 5.3s
  P2 → P1: 359 times, Avg duration: 3.1s
  P2 → P3: 1050 times, Avg duration: 3.3s
  P4 → P1: 671 times, Avg duration: 2.0s
  P1 → P2: 1411 times, Avg duration: 25.9s

EXPLORATION VS EXPLOITATION:
  Exploitation: 4538 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 7 events, Avg wait: 1.3s, Total value: 1.05

===================

================================================================================
SCENARIO 9 - Pr_0
================================================================================

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
  continue_spam_penalty: 1580 events, Total: 30.15, Avg: 0.019
  early_change_penalty: 60 events, Total: 16.01, Avg: 0.267
  next_bonus: 30 events, Total: 105.37, Avg: 3.512
  skip2p1_bonus: 12 events, Total: 2.60, Avg: 0.217
  stability_bonus: 223 events, Total: 38.09, Avg: 0.171
  bus_penalty: 66 events, Total: 24.91, Avg: 0.377

PHASE TRANSITION PATTERNS:
  P3 → P1: 378 times, Avg duration: 17.7s
  P3 → P4: 838 times, Avg duration: 5.3s
  P2 → P1: 392 times, Avg duration: 3.2s
  P2 → P3: 1219 times, Avg duration: 3.3s
  P4 → P1: 839 times, Avg duration: 2.0s
  P1 → P2: 1614 times, Avg duration: 24.9s

EXPLORATION VS EXPLOITATION:
  Exploitation: 5280 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 7 events, Avg wait: 1.3s, Total value: 1.05

===================

================================================================================
SCENARIO 10 - Pr_0
================================================================================

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
  continue_spam_penalty: 1644 events, Total: 30.79, Avg: 0.019
  early_change_penalty: 75 events, Total: 20.26, Avg: 0.270
  next_bonus: 34 events, Total: 119.46, Avg: 3.514
  skip2p1_bonus: 13 events, Total: 2.80, Avg: 0.215
  stability_bonus: 233 events, Total: 39.71, Avg: 0.170
  bus_penalty: 84 events, Total: 30.95, Avg: 0.368

PHASE TRANSITION PATTERNS:
  P3 → P1: 378 times, Avg duration: 17.7s
  P3 → P4: 1003 times, Avg duration: 5.2s
  P2 → P1: 431 times, Avg duration: 3.2s
  P2 → P3: 1384 times, Avg duration: 3.3s
  P4 → P1: 1004 times, Avg duration: 2.0s
  P1 → P2: 1819 times, Avg duration: 24.1s

EXPLORATION VS EXPLOITATION:
  Exploitation: 6019 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 8 events, Avg wait: 1.1s, Total value: 1.20

===================

================================================================================
SCENARIO 11 - Pr_0
================================================================================

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
  continue_spam_penalty: 1878 events, Total: 35.73, Avg: 0.019
  early_change_penalty: 79 events, Total: 21.41, Avg: 0.271
  next_bonus: 34 events, Total: 119.46, Avg: 3.514
  skip2p1_bonus: 17 events, Total: 3.70, Avg: 0.218
  stability_bonus: 271 events, Total: 46.17, Avg: 0.170
  bus_penalty: 84 events, Total: 30.95, Avg: 0.368

PHASE TRANSITION PATTERNS:
  P3 → P1: 438 times, Avg duration: 17.9s
  P3 → P4: 1064 times, Avg duration: 5.2s
  P2 → P1: 473 times, Avg duration: 3.2s
  P2 → P3: 1505 times, Avg duration: 3.3s
  P4 → P1: 1065 times, Avg duration: 2.0s
  P1 → P2: 1983 times, Avg duration: 24.6s

EXPLORATION VS EXPLOITATION:
  Exploitation: 6528 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 9 events, Avg wait: 1.0s, Total value: 1.35

===================

================================================================================
SCENARIO 12 - Pr_0
================================================================================

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
  continue_spam_penalty: 2080 events, Total: 39.95, Avg: 0.019
  early_change_penalty: 88 events, Total: 23.28, Avg: 0.265
  next_bonus: 38 events, Total: 132.65, Avg: 3.491
  skip2p1_bonus: 18 events, Total: 3.90, Avg: 0.217
  stability_bonus: 301 events, Total: 51.21, Avg: 0.170
  bus_penalty: 86 events, Total: 31.33, Avg: 0.364

PHASE TRANSITION PATTERNS:
  P3 → P1: 470 times, Avg duration: 18.0s
  P3 → P4: 1156 times, Avg duration: 5.3s
  P2 → P1: 512 times, Avg duration: 3.2s
  P2 → P3: 1629 times, Avg duration: 3.3s
  P4 → P1: 1157 times, Avg duration: 2.0s
  P1 → P2: 2146 times, Avg duration: 25.0s

EXPLORATION VS EXPLOITATION:
  Exploitation: 7070 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 11 events, Avg wait: 1.2s, Total value: 1.65

===================

================================================================================
SCENARIO 13 - Pr_0
================================================================================

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
  continue_spam_penalty: 2288 events, Total: 44.43, Avg: 0.019
  early_change_penalty: 95 events, Total: 24.94, Avg: 0.263
  next_bonus: 43 events, Total: 149.19, Avg: 3.470
  skip2p1_bonus: 20 events, Total: 4.40, Avg: 0.220
  stability_bonus: 326 events, Total: 55.52, Avg: 0.170
  bus_penalty: 90 events, Total: 32.61, Avg: 0.362

PHASE TRANSITION PATTERNS:
  P3 → P1: 516 times, Avg duration: 18.1s
  P3 → P4: 1235 times, Avg duration: 5.3s
  P2 → P1: 554 times, Avg duration: 3.2s
  P2 → P3: 1755 times, Avg duration: 3.3s
  P4 → P1: 1236 times, Avg duration: 2.0s
  P1 → P2: 2314 times, Avg duration: 25.2s

EXPLORATION VS EXPLOITATION:
  Exploitation: 7610 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 12 events, Avg wait: 1.2s, Total value: 1.80

===================

================================================================================
SCENARIO 14 - Pr_0
================================================================================

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
  continue_spam_penalty: 2506 events, Total: 49.56, Avg: 0.020
  early_change_penalty: 97 events, Total: 25.57, Avg: 0.264
  next_bonus: 44 events, Total: 152.47, Avg: 3.465
  skip2p1_bonus: 21 events, Total: 4.70, Avg: 0.224
  stability_bonus: 354 events, Total: 60.28, Avg: 0.170
  bus_penalty: 94 events, Total: 33.52, Avg: 0.357

PHASE TRANSITION PATTERNS:
  P3 → P1: 559 times, Avg duration: 18.2s
  P3 → P4: 1308 times, Avg duration: 5.3s
  P2 → P1: 602 times, Avg duration: 3.2s
  P2 → P3: 1872 times, Avg duration: 3.3s
  P4 → P1: 1310 times, Avg duration: 2.0s
  P1 → P2: 2480 times, Avg duration: 25.5s

EXPLORATION VS EXPLOITATION:
  Exploitation: 8131 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 12 events, Avg wait: 1.2s, Total value: 1.80

===================

================================================================================
SCENARIO 15 - Pr_0
================================================================================

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
  continue_spam_penalty: 2695 events, Total: 53.30, Avg: 0.020
  early_change_penalty: 98 events, Total: 25.78, Avg: 0.263
  next_bonus: 47 events, Total: 163.19, Avg: 3.472
  skip2p1_bonus: 22 events, Total: 5.00, Avg: 0.227
  stability_bonus: 387 events, Total: 65.84, Avg: 0.170
  bus_penalty: 98 events, Total: 34.83, Avg: 0.355

PHASE TRANSITION PATTERNS:
  P3 → P1: 595 times, Avg duration: 18.3s
  P3 → P4: 1400 times, Avg duration: 5.3s
  P2 → P1: 643 times, Avg duration: 3.2s
  P2 → P3: 2001 times, Avg duration: 3.3s
  P4 → P1: 1402 times, Avg duration: 2.0s
  P1 → P2: 2650 times, Avg duration: 25.7s

EXPLORATION VS EXPLOITATION:
  Exploitation: 8691 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 13 events, Avg wait: 1.2s, Total value: 1.95

===================

================================================================================
SCENARIO 16 - Pr_0
================================================================================

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
  continue_spam_penalty: 2945 events, Total: 58.90, Avg: 0.020
  early_change_penalty: 100 events, Total: 26.28, Avg: 0.263
  next_bonus: 52 events, Total: 181.83, Avg: 3.497
  skip2p1_bonus: 23 events, Total: 5.20, Avg: 0.226
  stability_bonus: 426 events, Total: 72.56, Avg: 0.170
  bus_penalty: 98 events, Total: 34.83, Avg: 0.355

PHASE TRANSITION PATTERNS:
  P3 → P1: 653 times, Avg duration: 18.3s
  P3 → P4: 1456 times, Avg duration: 5.3s
  P2 → P1: 685 times, Avg duration: 3.2s
  P2 → P3: 2115 times, Avg duration: 3.3s
  P4 → P1: 1458 times, Avg duration: 2.0s
  P1 → P2: 2806 times, Avg duration: 26.0s

EXPLORATION VS EXPLOITATION:
  Exploitation: 9173 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 16 events, Avg wait: 1.1s, Total value: 2.40

===================

================================================================================
SCENARIO 17 - Pr_0
================================================================================

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
  continue_spam_penalty: 3133 events, Total: 62.83, Avg: 0.020
  early_change_penalty: 104 events, Total: 27.45, Avg: 0.264
  next_bonus: 55 events, Total: 191.83, Avg: 3.488
  skip2p1_bonus: 26 events, Total: 5.90, Avg: 0.227
  stability_bonus: 466 events, Total: 79.44, Avg: 0.170
  bus_penalty: 100 events, Total: 35.35, Avg: 0.354

PHASE TRANSITION PATTERNS:
  P3 → P1: 673 times, Avg duration: 18.4s
  P3 → P4: 1546 times, Avg duration: 5.3s
  P2 → P1: 732 times, Avg duration: 3.2s
  P2 → P3: 2228 times, Avg duration: 3.3s
  P4 → P1: 1550 times, Avg duration: 2.0s
  P1 → P2: 2966 times, Avg duration: 26.4s

EXPLORATION VS EXPLOITATION:
  Exploitation: 9695 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 18 events, Avg wait: 1.2s, Total value: 2.70

===================

================================================================================
SCENARIO 18 - Pr_0
================================================================================

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
  continue_spam_penalty: 3369 events, Total: 68.19, Avg: 0.020
  early_change_penalty: 108 events, Total: 28.53, Avg: 0.264
  next_bonus: 59 events, Total: 205.83, Avg: 3.489
  skip2p1_bonus: 29 events, Total: 6.60, Avg: 0.228
  stability_bonus: 501 events, Total: 85.37, Avg: 0.170
  bus_penalty: 101 events, Total: 35.60, Avg: 0.352

PHASE TRANSITION PATTERNS:
  P3 → P1: 718 times, Avg duration: 18.5s
  P3 → P4: 1615 times, Avg duration: 5.3s
  P2 → P1: 776 times, Avg duration: 3.2s
  P2 → P3: 2343 times, Avg duration: 3.3s
  P4 → P1: 1620 times, Avg duration: 2.0s
  P1 → P2: 3125 times, Avg duration: 26.7s

EXPLORATION VS EXPLOITATION:
  Exploitation: 10197 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 18 events, Avg wait: 1.2s, Total value: 2.70

===================

================================================================================
SCENARIO 19 - Pr_0
================================================================================

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
  continue_spam_penalty: 3592 events, Total: 73.22, Avg: 0.020
  early_change_penalty: 114 events, Total: 29.87, Avg: 0.262
  next_bonus: 59 events, Total: 205.83, Avg: 3.489
  skip2p1_bonus: 32 events, Total: 7.40, Avg: 0.231
  stability_bonus: 533 events, Total: 90.79, Avg: 0.170
  bus_penalty: 102 events, Total: 35.88, Avg: 0.352

PHASE TRANSITION PATTERNS:
  P3 → P1: 744 times, Avg duration: 18.5s
  P3 → P4: 1696 times, Avg duration: 5.3s
  P2 → P1: 820 times, Avg duration: 3.2s
  P2 → P3: 2454 times, Avg duration: 3.3s
  P4 → P1: 1705 times, Avg duration: 2.0s
  P1 → P2: 3281 times, Avg duration: 27.0s

EXPLORATION VS EXPLOITATION:
  Exploitation: 10700 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 18 events, Avg wait: 1.2s, Total value: 2.70

===================

================================================================================
SCENARIO 20 - Pr_0
================================================================================

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
  continue_spam_penalty: 3838 events, Total: 79.38, Avg: 0.021
  early_change_penalty: 119 events, Total: 31.35, Avg: 0.263
  next_bonus: 62 events, Total: 216.47, Avg: 3.491
  skip2p1_bonus: 35 events, Total: 8.20, Avg: 0.234
  stability_bonus: 570 events, Total: 97.16, Avg: 0.170
  bus_penalty: 102 events, Total: 35.88, Avg: 0.352

PHASE TRANSITION PATTERNS:
  P3 → P1: 785 times, Avg duration: 18.6s
  P3 → P4: 1764 times, Avg duration: 5.4s
  P2 → P1: 865 times, Avg duration: 3.1s
  P2 → P3: 2565 times, Avg duration: 3.3s
  P4 → P1: 1774 times, Avg duration: 2.0s
  P1 → P2: 3437 times, Avg duration: 27.2s

EXPLORATION VS EXPLOITATION:
  Exploitation: 11190 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 21 - Pr_0
================================================================================

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
  continue_spam_penalty: 4062 events, Total: 84.22, Avg: 0.021
  early_change_penalty: 125 events, Total: 33.13, Avg: 0.265
  next_bonus: 65 events, Total: 227.65, Avg: 3.502
  skip2p1_bonus: 36 events, Total: 8.40, Avg: 0.233
  stability_bonus: 610 events, Total: 103.83, Avg: 0.170
  bus_penalty: 104 events, Total: 36.55, Avg: 0.351

PHASE TRANSITION PATTERNS:
  P3 → P1: 837 times, Avg duration: 18.7s
  P3 → P4: 1836 times, Avg duration: 5.4s
  P2 → P1: 903 times, Avg duration: 3.1s
  P2 → P3: 2690 times, Avg duration: 3.3s
  P4 → P1: 1846 times, Avg duration: 2.0s
  P1 → P2: 3600 times, Avg duration: 27.3s

EXPLORATION VS EXPLOITATION:
  Exploitation: 11712 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 22 - Pr_0
================================================================================

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
  continue_spam_penalty: 4308 events, Total: 89.48, Avg: 0.021
  early_change_penalty: 129 events, Total: 34.10, Avg: 0.264
  next_bonus: 65 events, Total: 227.65, Avg: 3.502
  skip2p1_bonus: 37 events, Total: 8.70, Avg: 0.235
  stability_bonus: 643 events, Total: 109.46, Avg: 0.170
  bus_penalty: 105 events, Total: 37.08, Avg: 0.353

PHASE TRANSITION PATTERNS:
  P3 → P1: 899 times, Avg duration: 18.6s
  P3 → P4: 1894 times, Avg duration: 5.4s
  P2 → P1: 946 times, Avg duration: 3.1s
  P2 → P3: 2811 times, Avg duration: 3.3s
  P4 → P1: 1904 times, Avg duration: 2.0s
  P1 → P2: 3764 times, Avg duration: 27.4s

EXPLORATION VS EXPLOITATION:
  Exploitation: 12218 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 23 - Pr_0
================================================================================

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
  continue_spam_penalty: 4569 events, Total: 95.49, Avg: 0.021
  early_change_penalty: 130 events, Total: 34.31, Avg: 0.264
  next_bonus: 70 events, Total: 245.02, Avg: 3.500
  skip2p1_bonus: 38 events, Total: 9.00, Avg: 0.237
  stability_bonus: 693 events, Total: 118.18, Avg: 0.171
  bus_penalty: 108 events, Total: 37.69, Avg: 0.349

PHASE TRANSITION PATTERNS:
  P3 → P1: 968 times, Avg duration: 18.7s
  P3 → P4: 1939 times, Avg duration: 5.4s
  P2 → P1: 990 times, Avg duration: 3.1s
  P2 → P3: 2926 times, Avg duration: 3.3s
  P4 → P1: 1950 times, Avg duration: 2.0s
  P1 → P2: 3923 times, Avg duration: 27.6s

EXPLORATION VS EXPLOITATION:
  Exploitation: 12696 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 24 - Pr_0
================================================================================

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
  continue_spam_penalty: 4802 events, Total: 100.57, Avg: 0.021
  early_change_penalty: 132 events, Total: 34.92, Avg: 0.265
  next_bonus: 71 events, Total: 248.38, Avg: 3.498
  skip2p1_bonus: 39 events, Total: 9.20, Avg: 0.236
  stability_bonus: 738 events, Total: 125.83, Avg: 0.171
  bus_penalty: 110 events, Total: 38.05, Avg: 0.346

PHASE TRANSITION PATTERNS:
  P3 → P1: 1015 times, Avg duration: 18.7s
  P3 → P4: 2007 times, Avg duration: 5.5s
  P2 → P1: 1034 times, Avg duration: 3.1s
  P2 → P3: 3043 times, Avg duration: 3.3s
  P4 → P1: 2019 times, Avg duration: 2.0s
  P1 → P2: 4084 times, Avg duration: 27.7s

EXPLORATION VS EXPLOITATION:
  Exploitation: 13202 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 25 - Pr_0
================================================================================

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
  continue_spam_penalty: 4958 events, Total: 103.18, Avg: 0.021
  early_change_penalty: 139 events, Total: 37.11, Avg: 0.267
  next_bonus: 75 events, Total: 261.84, Avg: 3.491
  skip2p1_bonus: 40 events, Total: 9.40, Avg: 0.235
  stability_bonus: 767 events, Total: 130.81, Avg: 0.171
  bus_penalty: 112 events, Total: 38.41, Avg: 0.343

PHASE TRANSITION PATTERNS:
  P3 → P1: 1022 times, Avg duration: 18.7s
  P3 → P4: 2119 times, Avg duration: 5.4s
  P2 → P1: 1079 times, Avg duration: 3.1s
  P2 → P3: 3162 times, Avg duration: 3.3s
  P4 → P1: 2131 times, Avg duration: 2.0s
  P1 → P2: 4249 times, Avg duration: 27.8s

EXPLORATION VS EXPLOITATION:
  Exploitation: 13762 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 26 - Pr_0
================================================================================

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
  continue_spam_penalty: 5153 events, Total: 107.23, Avg: 0.021
  early_change_penalty: 140 events, Total: 37.49, Avg: 0.268
  next_bonus: 77 events, Total: 268.29, Avg: 3.484
  skip2p1_bonus: 41 events, Total: 9.60, Avg: 0.234
  stability_bonus: 792 events, Total: 135.13, Avg: 0.171
  bus_penalty: 113 events, Total: 38.62, Avg: 0.342

PHASE TRANSITION PATTERNS:
  P3 → P1: 1048 times, Avg duration: 18.7s
  P3 → P4: 2207 times, Avg duration: 5.4s
  P2 → P1: 1123 times, Avg duration: 3.1s
  P2 → P3: 3279 times, Avg duration: 3.3s
  P4 → P1: 2222 times, Avg duration: 2.0s
  P1 → P2: 4410 times, Avg duration: 28.0s

EXPLORATION VS EXPLOITATION:
  Exploitation: 14289 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 27 - Pr_0
================================================================================

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
  continue_spam_penalty: 5365 events, Total: 111.60, Avg: 0.021
  early_change_penalty: 144 events, Total: 38.39, Avg: 0.267
  next_bonus: 79 events, Total: 275.57, Avg: 3.488
  skip2p1_bonus: 42 events, Total: 9.80, Avg: 0.233
  stability_bonus: 834 events, Total: 142.19, Avg: 0.170
  bus_penalty: 113 events, Total: 38.62, Avg: 0.342

PHASE TRANSITION PATTERNS:
  P3 → P1: 1090 times, Avg duration: 18.7s
  P3 → P4: 2282 times, Avg duration: 5.5s
  P2 → P1: 1170 times, Avg duration: 3.1s
  P2 → P3: 3396 times, Avg duration: 3.3s
  P4 → P1: 2297 times, Avg duration: 2.0s
  P1 → P2: 4575 times, Avg duration: 28.0s

EXPLORATION VS EXPLOITATION:
  Exploitation: 14810 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 20 events, Avg wait: 1.4s, Total value: 3.00

===================

================================================================================
SCENARIO 28 - Pr_0
================================================================================

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
  continue_spam_penalty: 5583 events, Total: 116.33, Avg: 0.021
  early_change_penalty: 149 events, Total: 39.86, Avg: 0.268
  next_bonus: 82 events, Total: 285.57, Avg: 3.483
  skip2p1_bonus: 43 events, Total: 10.00, Avg: 0.233
  stability_bonus: 864 events, Total: 147.55, Avg: 0.171
  bus_penalty: 115 events, Total: 39.22, Avg: 0.341

PHASE TRANSITION PATTERNS:
  P3 → P1: 1137 times, Avg duration: 18.8s
  P3 → P4: 2355 times, Avg duration: 5.5s
  P2 → P1: 1214 times, Avg duration: 3.1s
  P2 → P3: 3516 times, Avg duration: 3.3s
  P4 → P1: 2370 times, Avg duration: 2.0s
  P1 → P2: 4740 times, Avg duration: 28.1s

EXPLORATION VS EXPLOITATION:
  Exploitation: 15332 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 25 events, Avg wait: 1.5s, Total value: 3.75

===================

================================================================================
SCENARIO 29 - Pr_0
================================================================================

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
  continue_spam_penalty: 5804 events, Total: 121.34, Avg: 0.021
  early_change_penalty: 153 events, Total: 40.89, Avg: 0.267
  next_bonus: 85 events, Total: 296.29, Avg: 3.486
  skip2p1_bonus: 44 events, Total: 10.20, Avg: 0.232
  stability_bonus: 888 events, Total: 151.63, Avg: 0.171
  bus_penalty: 122 events, Total: 41.08, Avg: 0.337

PHASE TRANSITION PATTERNS:
  P3 → P1: 1189 times, Avg duration: 18.8s
  P3 → P4: 2421 times, Avg duration: 5.5s
  P2 → P1: 1259 times, Avg duration: 3.1s
  P2 → P3: 3636 times, Avg duration: 3.3s
  P4 → P1: 2437 times, Avg duration: 2.0s
  P1 → P2: 4905 times, Avg duration: 28.1s

EXPLORATION VS EXPLOITATION:
  Exploitation: 15847 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 25 events, Avg wait: 1.5s, Total value: 3.75

===================

================================================================================
SCENARIO 30 - Pr_0
================================================================================

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
  continue_spam_penalty: 5998 events, Total: 125.43, Avg: 0.021
  early_change_penalty: 161 events, Total: 42.79, Avg: 0.266
  next_bonus: 92 events, Total: 320.39, Avg: 3.482
  skip2p1_bonus: 47 events, Total: 10.90, Avg: 0.232
  stability_bonus: 916 events, Total: 156.45, Avg: 0.171
  bus_penalty: 128 events, Total: 43.37, Avg: 0.339

PHASE TRANSITION PATTERNS:
  P3 → P1: 1234 times, Avg duration: 18.8s
  P3 → P4: 2504 times, Avg duration: 5.5s
  P2 → P1: 1304 times, Avg duration: 3.1s
  P2 → P3: 3765 times, Avg duration: 3.3s
  P4 → P1: 2521 times, Avg duration: 2.0s
  P1 → P2: 5079 times, Avg duration: 28.1s

EXPLORATION VS EXPLOITATION:
  Exploitation: 16407 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 25 events, Avg wait: 1.5s, Total value: 3.75

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

EXPLORATION VS EXPLOITATION:
  Exploitation: 407 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 1 events, Avg wait: 4.0s, Total value: 0.15

===================

================================================================================
SCENARIO 2 - Pr_0
================================================================================

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
  continue_spam_penalty: 595 events, Total: 12.20, Avg: 0.021
  early_change_penalty: 2 events, Total: 0.61, Avg: 0.303
  next_bonus: 3 events, Total: 10.09, Avg: 3.364
  skip2p1_bonus: 4 events, Total: 1.00, Avg: 0.250
  stability_bonus: 66 events, Total: 11.38, Avg: 0.172
  bus_penalty: 2 events, Total: 0.48, Avg: 0.240

PHASE TRANSITION PATTERNS:
  P3 → P1: 200 times, Avg duration: 17.4s
  P3 → P4: 13 times, Avg duration: 5.5s
  P2 → P1: 91 times, Avg duration: 3.0s
  P2 → P3: 213 times, Avg duration: 3.2s
  P4 → P1: 13 times, Avg duration: 2.0s
  P1 → P2: 304 times, Avg duration: 34.4s

EXPLORATION VS EXPLOITATION:
  Exploitation: 834 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 2 events, Avg wait: 2.0s, Total value: 0.30

===================

================================================================================
SCENARIO 3 - Pr_0
================================================================================

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
  continue_spam_penalty: 862 events, Total: 17.57, Avg: 0.020
  early_change_penalty: 3 events, Total: 1.06, Avg: 0.355
  next_bonus: 5 events, Total: 16.82, Avg: 3.364
  skip2p1_bonus: 5 events, Total: 1.20, Avg: 0.240
  stability_bonus: 91 events, Total: 15.64, Avg: 0.172
  bus_penalty: 2 events, Total: 0.48, Avg: 0.240

PHASE TRANSITION PATTERNS:
  P3 → P1: 273 times, Avg duration: 17.5s
  P3 → P4: 45 times, Avg duration: 5.8s
  P2 → P1: 141 times, Avg duration: 3.0s
  P2 → P3: 320 times, Avg duration: 3.1s
  P4 → P1: 46 times, Avg duration: 2.0s
  P1 → P2: 461 times, Avg duration: 33.9s

EXPLORATION VS EXPLOITATION:
  Exploitation: 1286 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 3 events, Avg wait: 1.3s, Total value: 0.45

===================

================================================================================
SCENARIO 4 - Pr_0
================================================================================

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
  continue_spam_penalty: 1129 events, Total: 23.94, Avg: 0.021
  early_change_penalty: 5 events, Total: 1.56, Avg: 0.313
  next_bonus: 9 events, Total: 30.91, Avg: 3.435
  skip2p1_bonus: 6 events, Total: 1.40, Avg: 0.233
  stability_bonus: 112 events, Total: 19.29, Avg: 0.172
  bus_penalty: 3 events, Total: 0.81, Avg: 0.270

PHASE TRANSITION PATTERNS:
  P3 → P1: 343 times, Avg duration: 17.8s
  P3 → P4: 90 times, Avg duration: 6.5s
  P2 → P1: 188 times, Avg duration: 3.1s
  P2 → P3: 435 times, Avg duration: 3.2s
  P4 → P1: 91 times, Avg duration: 2.0s
  P1 → P2: 624 times, Avg duration: 32.8s

EXPLORATION VS EXPLOITATION:
  Exploitation: 1771 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 4 events, Avg wait: 1.2s, Total value: 0.60

===================

================================================================================
SCENARIO 5 - Pr_0
================================================================================

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
  continue_spam_penalty: 1286 events, Total: 26.81, Avg: 0.021
  early_change_penalty: 14 events, Total: 3.75, Avg: 0.268
  next_bonus: 10 events, Total: 34.28, Avg: 3.428
  skip2p1_bonus: 7 events, Total: 1.60, Avg: 0.229
  stability_bonus: 146 events, Total: 25.17, Avg: 0.172
  bus_penalty: 20 events, Total: 7.69, Avg: 0.384

PHASE TRANSITION PATTERNS:
  P3 → P1: 377 times, Avg duration: 17.7s
  P3 → P4: 197 times, Avg duration: 6.1s
  P2 → P1: 232 times, Avg duration: 3.1s
  P2 → P3: 576 times, Avg duration: 3.2s
  P4 → P1: 198 times, Avg duration: 2.0s
  P1 → P2: 809 times, Avg duration: 30.6s

EXPLORATION VS EXPLOITATION:
  Exploitation: 2389 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 6 events, Avg wait: 1.5s, Total value: 0.90

===================

================================================================================
SCENARIO 6 - Pr_0
================================================================================

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
  continue_spam_penalty: 1370 events, Total: 27.95, Avg: 0.020
  early_change_penalty: 27 events, Total: 7.19, Avg: 0.266
  next_bonus: 14 events, Total: 47.64, Avg: 3.403
  skip2p1_bonus: 8 events, Total: 1.80, Avg: 0.225
  stability_bonus: 165 events, Total: 28.35, Avg: 0.172
  bus_penalty: 29 events, Total: 11.27, Avg: 0.389

PHASE TRANSITION PATTERNS:
  P3 → P1: 377 times, Avg duration: 17.7s
  P3 → P4: 350 times, Avg duration: 5.6s
  P2 → P1: 279 times, Avg duration: 3.1s
  P2 → P3: 729 times, Avg duration: 3.2s
  P4 → P1: 351 times, Avg duration: 2.0s
  P1 → P2: 1010 times, Avg duration: 28.5s

EXPLORATION VS EXPLOITATION:
  Exploitation: 3096 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 6 events, Avg wait: 1.5s, Total value: 0.90

===================

================================================================================
SCENARIO 7 - Pr_0
================================================================================

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
  continue_spam_penalty: 1449 events, Total: 28.74, Avg: 0.020
  early_change_penalty: 35 events, Total: 9.27, Avg: 0.265
  next_bonus: 20 events, Total: 68.82, Avg: 3.441
  skip2p1_bonus: 10 events, Total: 2.20, Avg: 0.220
  stability_bonus: 188 events, Total: 32.14, Avg: 0.171
  bus_penalty: 45 events, Total: 16.84, Avg: 0.374

PHASE TRANSITION PATTERNS:
  P3 → P1: 377 times, Avg duration: 17.7s
  P3 → P4: 507 times, Avg duration: 5.4s
  P2 → P1: 322 times, Avg duration: 3.1s
  P2 → P3: 886 times, Avg duration: 3.2s
  P4 → P1: 508 times, Avg duration: 2.0s
  P1 → P2: 1210 times, Avg duration: 27.1s

EXPLORATION VS EXPLOITATION:
  Exploitation: 3810 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 7 events, Avg wait: 1.3s, Total value: 1.05

===================

================================================================================
SCENARIO 8 - Pr_0
================================================================================

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
  continue_spam_penalty: 1518 events, Total: 29.53, Avg: 0.019
  early_change_penalty: 48 events, Total: 12.84, Avg: 0.267
  next_bonus: 24 events, Total: 84.19, Avg: 3.508
  skip2p1_bonus: 11 events, Total: 2.40, Avg: 0.218
  stability_bonus: 209 events, Total: 35.66, Avg: 0.171
  bus_penalty: 55 events, Total: 20.80, Avg: 0.378

PHASE TRANSITION PATTERNS:
  P3 → P1: 377 times, Avg duration: 17.7s
  P3 → P4: 670 times, Avg duration: 5.3s
  P2 → P1: 359 times, Avg duration: 3.1s
  P2 → P3: 1050 times, Avg duration: 3.3s
  P4 → P1: 671 times, Avg duration: 2.0s
  P1 → P2: 1411 times, Avg duration: 25.9s

EXPLORATION VS EXPLOITATION:
  Exploitation: 4538 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 7 events, Avg wait: 1.3s, Total value: 1.05

===================

================================================================================
SCENARIO 9 - Pr_0
================================================================================

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
  continue_spam_penalty: 1580 events, Total: 30.15, Avg: 0.019
  early_change_penalty: 60 events, Total: 16.01, Avg: 0.267
  next_bonus: 30 events, Total: 105.37, Avg: 3.512
  skip2p1_bonus: 12 events, Total: 2.60, Avg: 0.217
  stability_bonus: 223 events, Total: 38.09, Avg: 0.171
  bus_penalty: 66 events, Total: 24.91, Avg: 0.377

PHASE TRANSITION PATTERNS:
  P3 → P1: 378 times, Avg duration: 17.7s
  P3 → P4: 838 times, Avg duration: 5.3s
  P2 → P1: 392 times, Avg duration: 3.2s
  P2 → P3: 1219 times, Avg duration: 3.3s
  P4 → P1: 839 times, Avg duration: 2.0s
  P1 → P2: 1614 times, Avg duration: 24.9s

EXPLORATION VS EXPLOITATION:
  Exploitation: 5280 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 7 events, Avg wait: 1.3s, Total value: 1.05

===================

================================================================================
SCENARIO 10 - Pr_0
================================================================================

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
  continue_spam_penalty: 1644 events, Total: 30.79, Avg: 0.019
  early_change_penalty: 75 events, Total: 20.26, Avg: 0.270
  next_bonus: 34 events, Total: 119.46, Avg: 3.514
  skip2p1_bonus: 13 events, Total: 2.80, Avg: 0.215
  stability_bonus: 233 events, Total: 39.71, Avg: 0.170
  bus_penalty: 84 events, Total: 30.95, Avg: 0.368

PHASE TRANSITION PATTERNS:
  P3 → P1: 378 times, Avg duration: 17.7s
  P3 → P4: 1003 times, Avg duration: 5.2s
  P2 → P1: 431 times, Avg duration: 3.2s
  P2 → P3: 1384 times, Avg duration: 3.3s
  P4 → P1: 1004 times, Avg duration: 2.0s
  P1 → P2: 1819 times, Avg duration: 24.1s

EXPLORATION VS EXPLOITATION:
  Exploitation: 6019 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 8 events, Avg wait: 1.1s, Total value: 1.20

===================

================================================================================
SCENARIO 11 - Pr_0
================================================================================

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
  continue_spam_penalty: 1878 events, Total: 35.73, Avg: 0.019
  early_change_penalty: 79 events, Total: 21.41, Avg: 0.271
  next_bonus: 34 events, Total: 119.46, Avg: 3.514
  skip2p1_bonus: 17 events, Total: 3.70, Avg: 0.218
  stability_bonus: 271 events, Total: 46.17, Avg: 0.170
  bus_penalty: 84 events, Total: 30.95, Avg: 0.368

PHASE TRANSITION PATTERNS:
  P3 → P1: 438 times, Avg duration: 17.9s
  P3 → P4: 1064 times, Avg duration: 5.2s
  P2 → P1: 473 times, Avg duration: 3.2s
  P2 → P3: 1505 times, Avg duration: 3.3s
  P4 → P1: 1065 times, Avg duration: 2.0s
  P1 → P2: 1983 times, Avg duration: 24.6s

EXPLORATION VS EXPLOITATION:
  Exploitation: 6528 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 9 events, Avg wait: 1.0s, Total value: 1.35

===================

================================================================================
SCENARIO 12 - Pr_0
================================================================================

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
  continue_spam_penalty: 2080 events, Total: 39.95, Avg: 0.019
  early_change_penalty: 88 events, Total: 23.28, Avg: 0.265
  next_bonus: 38 events, Total: 132.65, Avg: 3.491
  skip2p1_bonus: 18 events, Total: 3.90, Avg: 0.217
  stability_bonus: 301 events, Total: 51.21, Avg: 0.170
  bus_penalty: 86 events, Total: 31.33, Avg: 0.364

PHASE TRANSITION PATTERNS:
  P3 → P1: 470 times, Avg duration: 18.0s
  P3 → P4: 1156 times, Avg duration: 5.3s
  P2 → P1: 512 times, Avg duration: 3.2s
  P2 → P3: 1629 times, Avg duration: 3.3s
  P4 → P1: 1157 times, Avg duration: 2.0s
  P1 → P2: 2146 times, Avg duration: 25.0s

EXPLORATION VS EXPLOITATION:
  Exploitation: 7070 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 11 events, Avg wait: 1.2s, Total value: 1.65

===================

================================================================================
SCENARIO 13 - Pr_0
================================================================================

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
  continue_spam_penalty: 2288 events, Total: 44.43, Avg: 0.019
  early_change_penalty: 95 events, Total: 24.94, Avg: 0.263
  next_bonus: 43 events, Total: 149.19, Avg: 3.470
  skip2p1_bonus: 20 events, Total: 4.40, Avg: 0.220
  stability_bonus: 326 events, Total: 55.52, Avg: 0.170
  bus_penalty: 90 events, Total: 32.61, Avg: 0.362

PHASE TRANSITION PATTERNS:
  P3 → P1: 516 times, Avg duration: 18.1s
  P3 → P4: 1235 times, Avg duration: 5.3s
  P2 → P1: 554 times, Avg duration: 3.2s
  P2 → P3: 1755 times, Avg duration: 3.3s
  P4 → P1: 1236 times, Avg duration: 2.0s
  P1 → P2: 2314 times, Avg duration: 25.2s

EXPLORATION VS EXPLOITATION:
  Exploitation: 7610 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 12 events, Avg wait: 1.2s, Total value: 1.80

===================

================================================================================
SCENARIO 14 - Pr_0
================================================================================

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
  continue_spam_penalty: 2506 events, Total: 49.56, Avg: 0.020
  early_change_penalty: 97 events, Total: 25.57, Avg: 0.264
  next_bonus: 44 events, Total: 152.47, Avg: 3.465
  skip2p1_bonus: 21 events, Total: 4.70, Avg: 0.224
  stability_bonus: 354 events, Total: 60.28, Avg: 0.170
  bus_penalty: 94 events, Total: 33.52, Avg: 0.357

PHASE TRANSITION PATTERNS:
  P3 → P1: 559 times, Avg duration: 18.2s
  P3 → P4: 1308 times, Avg duration: 5.3s
  P2 → P1: 602 times, Avg duration: 3.2s
  P2 → P3: 1872 times, Avg duration: 3.3s
  P4 → P1: 1310 times, Avg duration: 2.0s
  P1 → P2: 2480 times, Avg duration: 25.5s

EXPLORATION VS EXPLOITATION:
  Exploitation: 8131 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 12 events, Avg wait: 1.2s, Total value: 1.80

===================

================================================================================
SCENARIO 15 - Pr_0
================================================================================

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
  continue_spam_penalty: 2695 events, Total: 53.30, Avg: 0.020
  early_change_penalty: 98 events, Total: 25.78, Avg: 0.263
  next_bonus: 47 events, Total: 163.19, Avg: 3.472
  skip2p1_bonus: 22 events, Total: 5.00, Avg: 0.227
  stability_bonus: 387 events, Total: 65.84, Avg: 0.170
  bus_penalty: 98 events, Total: 34.83, Avg: 0.355

PHASE TRANSITION PATTERNS:
  P3 → P1: 595 times, Avg duration: 18.3s
  P3 → P4: 1400 times, Avg duration: 5.3s
  P2 → P1: 643 times, Avg duration: 3.2s
  P2 → P3: 2001 times, Avg duration: 3.3s
  P4 → P1: 1402 times, Avg duration: 2.0s
  P1 → P2: 2650 times, Avg duration: 25.7s

EXPLORATION VS EXPLOITATION:
  Exploitation: 8691 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 13 events, Avg wait: 1.2s, Total value: 1.95

===================

================================================================================
SCENARIO 16 - Pr_0
================================================================================

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
  continue_spam_penalty: 2945 events, Total: 58.90, Avg: 0.020
  early_change_penalty: 100 events, Total: 26.28, Avg: 0.263
  next_bonus: 52 events, Total: 181.83, Avg: 3.497
  skip2p1_bonus: 23 events, Total: 5.20, Avg: 0.226
  stability_bonus: 426 events, Total: 72.56, Avg: 0.170
  bus_penalty: 98 events, Total: 34.83, Avg: 0.355

PHASE TRANSITION PATTERNS:
  P3 → P1: 653 times, Avg duration: 18.3s
  P3 → P4: 1456 times, Avg duration: 5.3s
  P2 → P1: 685 times, Avg duration: 3.2s
  P2 → P3: 2115 times, Avg duration: 3.3s
  P4 → P1: 1458 times, Avg duration: 2.0s
  P1 → P2: 2806 times, Avg duration: 26.0s

EXPLORATION VS EXPLOITATION:
  Exploitation: 9173 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 16 events, Avg wait: 1.1s, Total value: 2.40

===================

================================================================================
SCENARIO 17 - Pr_0
================================================================================

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
  continue_spam_penalty: 3133 events, Total: 62.83, Avg: 0.020
  early_change_penalty: 104 events, Total: 27.45, Avg: 0.264
  next_bonus: 55 events, Total: 191.83, Avg: 3.488
  skip2p1_bonus: 26 events, Total: 5.90, Avg: 0.227
  stability_bonus: 466 events, Total: 79.44, Avg: 0.170
  bus_penalty: 100 events, Total: 35.35, Avg: 0.354

PHASE TRANSITION PATTERNS:
  P3 → P1: 673 times, Avg duration: 18.4s
  P3 → P4: 1546 times, Avg duration: 5.3s
  P2 → P1: 732 times, Avg duration: 3.2s
  P2 → P3: 2228 times, Avg duration: 3.3s
  P4 → P1: 1550 times, Avg duration: 2.0s
  P1 → P2: 2966 times, Avg duration: 26.4s

EXPLORATION VS EXPLOITATION:
  Exploitation: 9695 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 18 events, Avg wait: 1.2s, Total value: 2.70

===================

================================================================================
SCENARIO 18 - Pr_0
================================================================================

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
  continue_spam_penalty: 3369 events, Total: 68.19, Avg: 0.020
  early_change_penalty: 108 events, Total: 28.53, Avg: 0.264
  next_bonus: 59 events, Total: 205.83, Avg: 3.489
  skip2p1_bonus: 29 events, Total: 6.60, Avg: 0.228
  stability_bonus: 501 events, Total: 85.37, Avg: 0.170
  bus_penalty: 101 events, Total: 35.60, Avg: 0.352

PHASE TRANSITION PATTERNS:
  P3 → P1: 718 times, Avg duration: 18.5s
  P3 → P4: 1615 times, Avg duration: 5.3s
  P2 → P1: 776 times, Avg duration: 3.2s
  P2 → P3: 2343 times, Avg duration: 3.3s
  P4 → P1: 1620 times, Avg duration: 2.0s
  P1 → P2: 3125 times, Avg duration: 26.7s

EXPLORATION VS EXPLOITATION:
  Exploitation: 10197 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 18 events, Avg wait: 1.2s, Total value: 2.70

===================

================================================================================
SCENARIO 19 - Pr_0
================================================================================

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
  continue_spam_penalty: 3592 events, Total: 73.22, Avg: 0.020
  early_change_penalty: 114 events, Total: 29.87, Avg: 0.262
  next_bonus: 59 events, Total: 205.83, Avg: 3.489
  skip2p1_bonus: 32 events, Total: 7.40, Avg: 0.231
  stability_bonus: 533 events, Total: 90.79, Avg: 0.170
  bus_penalty: 102 events, Total: 35.88, Avg: 0.352

PHASE TRANSITION PATTERNS:
  P3 → P1: 744 times, Avg duration: 18.5s
  P3 → P4: 1696 times, Avg duration: 5.3s
  P2 → P1: 820 times, Avg duration: 3.2s
  P2 → P3: 2454 times, Avg duration: 3.3s
  P4 → P1: 1705 times, Avg duration: 2.0s
  P1 → P2: 3281 times, Avg duration: 27.0s

EXPLORATION VS EXPLOITATION:
  Exploitation: 10700 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 18 events, Avg wait: 1.2s, Total value: 2.70

===================

================================================================================
SCENARIO 20 - Pr_0
================================================================================

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
  continue_spam_penalty: 3838 events, Total: 79.38, Avg: 0.021
  early_change_penalty: 119 events, Total: 31.35, Avg: 0.263
  next_bonus: 62 events, Total: 216.47, Avg: 3.491
  skip2p1_bonus: 35 events, Total: 8.20, Avg: 0.234
  stability_bonus: 570 events, Total: 97.16, Avg: 0.170
  bus_penalty: 102 events, Total: 35.88, Avg: 0.352

PHASE TRANSITION PATTERNS:
  P3 → P1: 785 times, Avg duration: 18.6s
  P3 → P4: 1764 times, Avg duration: 5.4s
  P2 → P1: 865 times, Avg duration: 3.1s
  P2 → P3: 2565 times, Avg duration: 3.3s
  P4 → P1: 1774 times, Avg duration: 2.0s
  P1 → P2: 3437 times, Avg duration: 27.2s

EXPLORATION VS EXPLOITATION:
  Exploitation: 11190 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 21 - Pr_0
================================================================================

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
  continue_spam_penalty: 4062 events, Total: 84.22, Avg: 0.021
  early_change_penalty: 125 events, Total: 33.13, Avg: 0.265
  next_bonus: 65 events, Total: 227.65, Avg: 3.502
  skip2p1_bonus: 36 events, Total: 8.40, Avg: 0.233
  stability_bonus: 610 events, Total: 103.83, Avg: 0.170
  bus_penalty: 104 events, Total: 36.55, Avg: 0.351

PHASE TRANSITION PATTERNS:
  P3 → P1: 837 times, Avg duration: 18.7s
  P3 → P4: 1836 times, Avg duration: 5.4s
  P2 → P1: 903 times, Avg duration: 3.1s
  P2 → P3: 2690 times, Avg duration: 3.3s
  P4 → P1: 1846 times, Avg duration: 2.0s
  P1 → P2: 3600 times, Avg duration: 27.3s

EXPLORATION VS EXPLOITATION:
  Exploitation: 11712 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 22 - Pr_0
================================================================================

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
  continue_spam_penalty: 4308 events, Total: 89.48, Avg: 0.021
  early_change_penalty: 129 events, Total: 34.10, Avg: 0.264
  next_bonus: 65 events, Total: 227.65, Avg: 3.502
  skip2p1_bonus: 37 events, Total: 8.70, Avg: 0.235
  stability_bonus: 643 events, Total: 109.46, Avg: 0.170
  bus_penalty: 105 events, Total: 37.08, Avg: 0.353

PHASE TRANSITION PATTERNS:
  P3 → P1: 899 times, Avg duration: 18.6s
  P3 → P4: 1894 times, Avg duration: 5.4s
  P2 → P1: 946 times, Avg duration: 3.1s
  P2 → P3: 2811 times, Avg duration: 3.3s
  P4 → P1: 1904 times, Avg duration: 2.0s
  P1 → P2: 3764 times, Avg duration: 27.4s

EXPLORATION VS EXPLOITATION:
  Exploitation: 12218 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 23 - Pr_0
================================================================================

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
  continue_spam_penalty: 4569 events, Total: 95.49, Avg: 0.021
  early_change_penalty: 130 events, Total: 34.31, Avg: 0.264
  next_bonus: 70 events, Total: 245.02, Avg: 3.500
  skip2p1_bonus: 38 events, Total: 9.00, Avg: 0.237
  stability_bonus: 693 events, Total: 118.18, Avg: 0.171
  bus_penalty: 108 events, Total: 37.69, Avg: 0.349

PHASE TRANSITION PATTERNS:
  P3 → P1: 968 times, Avg duration: 18.7s
  P3 → P4: 1939 times, Avg duration: 5.4s
  P2 → P1: 990 times, Avg duration: 3.1s
  P2 → P3: 2926 times, Avg duration: 3.3s
  P4 → P1: 1950 times, Avg duration: 2.0s
  P1 → P2: 3923 times, Avg duration: 27.6s

EXPLORATION VS EXPLOITATION:
  Exploitation: 12696 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 24 - Pr_0
================================================================================

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
  continue_spam_penalty: 4802 events, Total: 100.57, Avg: 0.021
  early_change_penalty: 132 events, Total: 34.92, Avg: 0.265
  next_bonus: 71 events, Total: 248.38, Avg: 3.498
  skip2p1_bonus: 39 events, Total: 9.20, Avg: 0.236
  stability_bonus: 738 events, Total: 125.83, Avg: 0.171
  bus_penalty: 110 events, Total: 38.05, Avg: 0.346

PHASE TRANSITION PATTERNS:
  P3 → P1: 1015 times, Avg duration: 18.7s
  P3 → P4: 2007 times, Avg duration: 5.5s
  P2 → P1: 1034 times, Avg duration: 3.1s
  P2 → P3: 3043 times, Avg duration: 3.3s
  P4 → P1: 2019 times, Avg duration: 2.0s
  P1 → P2: 4084 times, Avg duration: 27.7s

EXPLORATION VS EXPLOITATION:
  Exploitation: 13202 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 25 - Pr_0
================================================================================

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
  continue_spam_penalty: 4958 events, Total: 103.18, Avg: 0.021
  early_change_penalty: 139 events, Total: 37.11, Avg: 0.267
  next_bonus: 75 events, Total: 261.84, Avg: 3.491
  skip2p1_bonus: 40 events, Total: 9.40, Avg: 0.235
  stability_bonus: 767 events, Total: 130.81, Avg: 0.171
  bus_penalty: 112 events, Total: 38.41, Avg: 0.343

PHASE TRANSITION PATTERNS:
  P3 → P1: 1022 times, Avg duration: 18.7s
  P3 → P4: 2119 times, Avg duration: 5.4s
  P2 → P1: 1079 times, Avg duration: 3.1s
  P2 → P3: 3162 times, Avg duration: 3.3s
  P4 → P1: 2131 times, Avg duration: 2.0s
  P1 → P2: 4249 times, Avg duration: 27.8s

EXPLORATION VS EXPLOITATION:
  Exploitation: 13762 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 26 - Pr_0
================================================================================

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
  continue_spam_penalty: 5153 events, Total: 107.23, Avg: 0.021
  early_change_penalty: 140 events, Total: 37.49, Avg: 0.268
  next_bonus: 77 events, Total: 268.29, Avg: 3.484
  skip2p1_bonus: 41 events, Total: 9.60, Avg: 0.234
  stability_bonus: 792 events, Total: 135.13, Avg: 0.171
  bus_penalty: 113 events, Total: 38.62, Avg: 0.342

PHASE TRANSITION PATTERNS:
  P3 → P1: 1048 times, Avg duration: 18.7s
  P3 → P4: 2207 times, Avg duration: 5.4s
  P2 → P1: 1123 times, Avg duration: 3.1s
  P2 → P3: 3279 times, Avg duration: 3.3s
  P4 → P1: 2222 times, Avg duration: 2.0s
  P1 → P2: 4410 times, Avg duration: 28.0s

EXPLORATION VS EXPLOITATION:
  Exploitation: 14289 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 19 events, Avg wait: 1.2s, Total value: 2.85

===================

================================================================================
SCENARIO 27 - Pr_0
================================================================================

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
  continue_spam_penalty: 5365 events, Total: 111.60, Avg: 0.021
  early_change_penalty: 144 events, Total: 38.39, Avg: 0.267
  next_bonus: 79 events, Total: 275.57, Avg: 3.488
  skip2p1_bonus: 42 events, Total: 9.80, Avg: 0.233
  stability_bonus: 834 events, Total: 142.19, Avg: 0.170
  bus_penalty: 113 events, Total: 38.62, Avg: 0.342

PHASE TRANSITION PATTERNS:
  P3 → P1: 1090 times, Avg duration: 18.7s
  P3 → P4: 2282 times, Avg duration: 5.5s
  P2 → P1: 1170 times, Avg duration: 3.1s
  P2 → P3: 3396 times, Avg duration: 3.3s
  P4 → P1: 2297 times, Avg duration: 2.0s
  P1 → P2: 4575 times, Avg duration: 28.0s

EXPLORATION VS EXPLOITATION:
  Exploitation: 14810 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 20 events, Avg wait: 1.4s, Total value: 3.00

===================

================================================================================
SCENARIO 28 - Pr_0
================================================================================

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
  continue_spam_penalty: 5583 events, Total: 116.33, Avg: 0.021
  early_change_penalty: 149 events, Total: 39.86, Avg: 0.268
  next_bonus: 82 events, Total: 285.57, Avg: 3.483
  skip2p1_bonus: 43 events, Total: 10.00, Avg: 0.233
  stability_bonus: 864 events, Total: 147.55, Avg: 0.171
  bus_penalty: 115 events, Total: 39.22, Avg: 0.341

PHASE TRANSITION PATTERNS:
  P3 → P1: 1137 times, Avg duration: 18.8s
  P3 → P4: 2355 times, Avg duration: 5.5s
  P2 → P1: 1214 times, Avg duration: 3.1s
  P2 → P3: 3516 times, Avg duration: 3.3s
  P4 → P1: 2370 times, Avg duration: 2.0s
  P1 → P2: 4740 times, Avg duration: 28.1s

EXPLORATION VS EXPLOITATION:
  Exploitation: 15332 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 25 events, Avg wait: 1.5s, Total value: 3.75

===================

================================================================================
SCENARIO 29 - Pr_0
================================================================================

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
  continue_spam_penalty: 5804 events, Total: 121.34, Avg: 0.021
  early_change_penalty: 153 events, Total: 40.89, Avg: 0.267
  next_bonus: 85 events, Total: 296.29, Avg: 3.486
  skip2p1_bonus: 44 events, Total: 10.20, Avg: 0.232
  stability_bonus: 888 events, Total: 151.63, Avg: 0.171
  bus_penalty: 122 events, Total: 41.08, Avg: 0.337

PHASE TRANSITION PATTERNS:
  P3 → P1: 1189 times, Avg duration: 18.8s
  P3 → P4: 2421 times, Avg duration: 5.5s
  P2 → P1: 1259 times, Avg duration: 3.1s
  P2 → P3: 3636 times, Avg duration: 3.3s
  P4 → P1: 2437 times, Avg duration: 2.0s
  P1 → P2: 4905 times, Avg duration: 28.1s

EXPLORATION VS EXPLOITATION:
  Exploitation: 15847 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 25 events, Avg wait: 1.5s, Total value: 3.75

===================

================================================================================
SCENARIO 30 - Pr_0
================================================================================

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
  continue_spam_penalty: 5998 events, Total: 125.43, Avg: 0.021
  early_change_penalty: 161 events, Total: 42.79, Avg: 0.266
  next_bonus: 92 events, Total: 320.39, Avg: 3.482
  skip2p1_bonus: 47 events, Total: 10.90, Avg: 0.232
  stability_bonus: 916 events, Total: 156.45, Avg: 0.171
  bus_penalty: 128 events, Total: 43.37, Avg: 0.339

PHASE TRANSITION PATTERNS:
  P3 → P1: 1234 times, Avg duration: 18.8s
  P3 → P4: 2504 times, Avg duration: 5.5s
  P2 → P1: 1304 times, Avg duration: 3.1s
  P2 → P3: 3765 times, Avg duration: 3.3s
  P4 → P1: 2521 times, Avg duration: 2.0s
  P1 → P2: 5079 times, Avg duration: 28.1s

EXPLORATION VS EXPLOITATION:
  Exploitation: 16407 actions (100.0%)
  Exploration: 0 actions (0.0%)

BUS ASSISTANCE SUMMARY:
  bus_excellent: 25 events, Avg wait: 1.5s, Total value: 3.75

===================

