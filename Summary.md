Parsing testing log: testing.log
========================================

================================================================================
SCENARIO 1
================================================================================
TRAFFIC CONFIG:
Scenario: Pr_0
  Cars: 100
  Bicycles: 400
  Pedestrians: 400
  Buses: every_15min

[PEDESTRIAN DEBUG] Step 3600:
  Total pedestrians: 864
  Stopped pedestrians: 233
  Avg waiting time: 33.94s

[SAFETY SUMMARY] Step 3600:
  Headway violations: 0 (FAST vehicles only: speed > 8.0 m/s)
  Distance violations: 0 (MOVING only: speed > 1.0 m/s)
  Red light violations: 0
  Episode totals - Headway: 0, Distance: 0, Red light: 129


[ACTION SUMMARY] Pr_0:
  Total actions: 3600
  Continue (0): 3173 (88.1%)
  Skip to P1 (1): 427 (11.9%)
  Next Phase (2): 0 (0.0%)
  Pedestrian (3): 0 (0.0%)

✓ Results for Pr_0 saved to: results/drl_test_results_20251020_070713.csv

================================================================================
[EPISODE SUMMARY] Phase Change Statistics:
  Total actions attempted: 7200
  Phase changes executed: 0
  Actions blocked (MIN_GREEN_TIME): 0
  Phase change rate: 0.0%
  Block rate: 0.0%
================================================================================


================================================================================
[FINAL SAFETY SUMMARY] Episode Complete
================================================================================
  Total Headway Violations:    0
  Total Distance Violations:   0
  Total Red Light Violations:  129
  ────────────────────────────────────────────────────────────────────────────
  TOTAL SAFETY VIOLATIONS:     129
  Violation Rate:              3.58% of steps
================================================================================


========================================
Parsing complete!
