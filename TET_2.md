Extracting Q-values and decision context from: testing.log
==========================================


==========================================
Extraction complete!
Total Q-values extracted: 3000

Output files:
  1. testing_q_values.csv - All Q-values with phase and duration
  2. testing_decision_context.csv - State context for non-Continue decisions
  3. testing_q_ranking_changes.csv - Q-value ranking changes (decision boundaries)

CSV columns (Q-values):
  - scenario, step, phase, duration, continue_q, skip2p1_q, next_q
  - selected_action, best_action (highest Q), q_gap (selected - worst)

Decision contexts captured: 1798 (for non-Continue actions)
Q-ranking changes detected: 971 (action preference flips)

==========================================
Q-VALUE RANKING CHANGES (First 10)
==========================================

scenario  step  old_best  new_best  reason                                                       phase_duration
Pr_0      100   Continue  Skip2P1   "Q-values shifted: Continue=0.26 Skip2P1=0.32 Next=0.26"     3
Pr_0      200   Skip2P1   Continue  "Q-values shifted: Continue=0.37 Skip2P1=0.32 Next=0.24"     3
Pr_0      300   Continue  Skip2P1   "Q-values shifted: Continue=0.32 Skip2P1=0.34 Next=0.31"     3
Pr_0      400   Skip2P1   Next      "Q-values shifted: Continue=0.26 Skip2P1=0.35 Next=0.35"     3
Pr_0      500   Next      Continue  "Q-values shifted: Continue=0.26 Skip2P1=0.19 Next=0.14"     3
Pr_0      2400  Continue  Next      "Q-values shifted: Continue=-0.19 Skip2P1=-0.25 Next=-0.11"  37
Pr_0      2500  Next      Continue  "Q-values shifted: Continue=-0.10 Skip2P1=-0.41 Next=-0.37"  12
Pr_0      2900  Continue  Skip2P1   "Q-values shifted: Continue=0.14 Skip2P1=0.31 Next=0.01"     17
Pr_0      3000  Skip2P1   Continue  "Q-values shifted: Continue=0.22 Skip2P1=-0.01 Next=-0.45"   4
Pr_0      3300  Continue  Next      "Q-values shifted: Continue=-0.28 Skip2P1=-0.43 Next=-0.25"  14

==========================================
DECISION CONTEXT EXAMPLES (First 10)
==========================================

scenario  step  phase  duration  action   context_type   context_value
Pr_0      100   P1     3         Skip2P1  phase          P1
Pr_0      100   P1     3         Skip2P1  duration       3
Pr_0      100   P1     3         Skip2P1  blocked_count  3
Pr_0      300   P1     3         Skip2P1  phase          P1
Pr_0      300   P1     3         Skip2P1  duration       3
Pr_0      300   P1     3         Skip2P1  blocked_count  4
Pr_0      400   P1     3         Next     phase          P1
Pr_0      400   P1     3         Next     duration       3
Pr_0      400   P1     3         Next     blocked_count  4
Pr_0      2400  P2     37        Next     phase          P2

==========================================
Analysis complete! Use these files for:
  • Attention mechanisms (which features matter?)
  • Counterfactual explanations (decision boundaries)
  • State-action pattern analysis
==========================================

