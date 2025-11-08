================================================================================
EXPLAINABLE RL DATA CAPTURE - IMPLEMENTATION SUMMARY
================================================================================

Both scripts have been updated to capture comprehensive XAI data from testing.log.

================================================================================
SCRIPT 1: parse_testing_q_values.sh
================================================================================

FIXES APPLIED:
--------------
✅ Fixed "Unknown" phase display - Now tracks phases properly from log events
✅ Added phase duration tracking from PHASE CHANGE events
✅ Captures current phase from P1/P2/P3/P4 transitions

NEW FEATURES:
-------------
1. State-Action Pairs for Non-Continue Decisions (#1 Priority)
   - Captures decision context when agent selects Skip2P1 or Next
   - Records: phase, duration, bus wait time, blocked action count
   - Output: testing_decision_context.csv
   
2. Q-Value Ranking Changes (#4 Priority)
   - Detects when best action flips (e.g., Continue → Skip2P1)
   - Identifies decision boundaries in state space
   - Records: old best, new best, Q-values at transition, phase duration
   - Output: testing_q_ranking_changes.csv

3. Enhanced Q-Value Data
   - Added: best_action (highest Q-value)
   - Added: q_gap (selected Q - worst Q)
   - Shows phase as P1/P2/P3/P4 instead of "Unknown"
   - Shows actual phase duration in seconds

OUTPUT FILES:
-------------
1. testing_q_values.csv
   Columns: scenario, step, phase, duration, continue_q, skip2p1_q, next_q,
            selected_action, best_action, q_gap

2. testing_decision_context.csv (NEW!)
   Columns: scenario, step, phase, duration, action, context_type, context_value
   Example rows:
     Pr_0, 1000, P2, 3, Skip2P1, phase, P2
     Pr_0, 1000, P2, 3, Skip2P1, duration, 3
     Pr_0, 1000, P2, 3, Skip2P1, bus_wait, 12.5
     Pr_0, 1000, P2, 3, Skip2P1, blocked_count, 2

3. testing_q_ranking_changes.csv (NEW!)
   Columns: scenario, step, old_best, new_best, reason, phase_duration
   Example:
     Pr_0, 2700, Continue, Skip2P1, "Q-values shifted: Continue=0.32 Skip2P1=0.35 Next=0.21", 27

XAI VALUE:
----------
• Attention Mechanisms: Which features (phase, duration, bus wait) correlate with actions?
• Counterfactual Explanations: "At 27s phase duration, Skip2P1 becomes preferred"
• Decision Tree Extraction: State-action pairs ready for VIPER/TREPAN algorithms


================================================================================
SCRIPT 2: parse_testing_log.sh
================================================================================

NEW FEATURES:
-------------
2. Reward Breakdown by Scenario (#2 Priority)
   - Aggregates all reward events per scenario
   - Tracks: skip2p1_bonus, stability_bonus, next_bonus, bus_penalty,
            early_change_penalty, continue_spam_penalty
   - Shows: count, total value, average value
   - Output: testing_reward_breakdown.csv

3. Phase Transition Patterns (#3 Priority)
   - Captures all P1→P2, P2→P1, P1→P3, etc. transitions
   - Records frequency and average duration
   - Output: testing_phase_transitions.csv

5. Blocked Actions with Context (#5 Priority)
   - Records blocked exploitation actions with full context
   - Captures: phase, duration, attempted action, blocking reason
   - Output: testing_blocked_context.csv

6. Exploitation Decision Sequences (#6 Priority)
   - Chains consecutive exploitation decisions
   - Example: "P1→P2(36s) → P2→P1(3s) → P1→P2(33s)"
   - Shows temporal decision patterns
   - Output: testing_decision_sequences.csv

7. Exploration vs Exploitation Comparison (#7 Priority)
   - Counts exploitation vs exploration actions per scenario
   - Calculates percentage split
   - Output: testing_explore_vs_exploit.csv

8. Bus Assistance Events (#8 Priority)
   - Aggregates bus bonuses, penalties, excellent service
   - Records: count, average wait time, total bonus/penalty value
   - Output: testing_bus_events.csv

OUTPUT FILES:
-------------
1. testing_summary.md (ENHANCED!)
   - Original scenario summaries
   - PLUS integrated XAI analysis section per scenario:
     * Reward breakdown
     * Phase transition patterns
     * Exploration vs Exploitation split
     * Bus assistance summary

2. testing_reward_breakdown.csv (NEW!)
   Columns: scenario, reward_type, count, total_value, avg_value
   
3. testing_phase_transitions.csv (NEW!)
   Columns: scenario, from_phase, to_phase, action, count, avg_duration
   
4. testing_blocked_context.csv (NEW!)
   Columns: scenario, step, phase, duration, action, reason
   
5. testing_decision_sequences.csv (NEW!)
   Columns: scenario, sequence_num, decision_chain
   
6. testing_explore_vs_exploit.csv (NEW!)
   Columns: scenario, decision_type, total_actions, avg_reward, safety_violations
   
7. testing_bus_events.csv (NEW!)
   Columns: scenario, event_type, count, avg_wait, total_bonus_penalty

XAI VALUE:
----------
• Natural Language Generation: "Agent optimized [reward_type] in scenario [X]"
• Counterfactual Explanations: "If traffic was Bi_9 instead of Pr_0, agent would..."
• Policy Visualization: Phase transition patterns show learned strategies
• Trust Building: Blocked actions show safety constraints respected
• Human-AI Collaboration: Exploration vs exploitation shows learning vs execution


================================================================================
USAGE EXAMPLES
================================================================================

Run parse_testing_q_values.sh:
------------------------------
./scripts/drl/parse_testing_q_values.sh testing.log

Creates 3 CSV files with:
- Q-values with phase/duration context
- Decision context for non-Continue actions
- Q-value ranking changes (decision boundaries)


Run parse_testing_log.sh:
--------------------------
./scripts/drl/parse_testing_log.sh testing.log

Creates 7 files with:
- Enhanced summary with XAI analysis
- Reward breakdown
- Phase transitions
- Blocked actions
- Decision sequences
- Exploration vs exploitation
- Bus events


================================================================================
XAI PAPER APPLICATIONS
================================================================================

1. ATTENTION MECHANISMS
   Use: testing_decision_context.csv
   Analysis: Which features (phase, duration, bus_wait) most influence actions?
   Visualization: Heatmaps showing feature importance

2. COUNTERFACTUAL EXPLANATIONS
   Use: testing_q_ranking_changes.csv + testing_phase_transitions.csv
   Analysis: Minimal state changes that flip decisions
   Example: "If phase duration was 30s instead of 27s, agent would Continue"

3. DECISION TREE EXTRACTION
   Use: testing_decision_context.csv + testing_q_values.csv
   Analysis: Extract interpretable rules from state-action pairs
   Tool: VIPER, TREPAN algorithms

4. NATURAL LANGUAGE GENERATION
   Use: testing_reward_breakdown.csv + testing_bus_events.csv
   Example: "Agent prioritized bus service (12 bonuses) in Pr_0 scenario"
   
5. SALIENCY MAPS
   Use: testing_decision_context.csv
   Analysis: Which state dimensions correlate with Q-value changes?
   Visualization: Feature importance gradients

6. USER STUDY EXPLANATIONS
   Use: All CSV files + testing_summary.md
   Compare: No explanation vs Decision tree vs Natural language
   Metrics: Trust, usability, actionability


================================================================================
WHAT'S ALREADY CAPTURED VS WHAT NEEDS ANALYSIS
================================================================================

CAPTURED (Ready for XAI):
-------------------------
✅ State-action pairs for non-Continue decisions
✅ Q-value rankings and changes
✅ Reward breakdown by type and scenario
✅ Phase transition patterns
✅ Blocked actions with context
✅ Decision sequences
✅ Exploration vs exploitation split
✅ Bus assistance events
✅ Action distribution per scenario
✅ Safety violations per scenario

NEEDS POST-PROCESSING (For Paper):
-----------------------------------
□ Feature importance analysis (correlate context with actions)
□ Decision tree extraction (VIPER/TREPAN on state-action pairs)
□ Counterfactual generation (minimal state changes)
□ Natural language templates (fill from CSV data)
□ Attention visualizations (heatmaps)
□ User study design (compare explanation types)


================================================================================
NEXT STEPS FOR XAI PAPER
================================================================================

1. Run both scripts on testing.log
2. Load CSV files into Python/R for analysis
3. Correlation analysis: Which features predict which actions?
4. Decision tree extraction: VIPER algorithm on state-action pairs
5. Counterfactual generation: Find minimal state changes
6. Natural language templates: Fill from reward/bus/transition data
7. User study design: Test explanations with traffic engineers


================================================================================
FILE SIZES (Estimated for 30 scenarios x 10,000 steps)
================================================================================

testing_q_values.csv:              ~30,000 rows (1 per 100 steps x 30 scenarios)
testing_decision_context.csv:      ~5,000 rows (non-Continue actions only)
testing_q_ranking_changes.csv:     ~500 rows (ranking flips only)
testing_reward_breakdown.csv:      ~180 rows (6 types x 30 scenarios)
testing_phase_transitions.csv:     ~120 rows (4 transitions x 30 scenarios)
testing_blocked_context.csv:       ~2,000 rows (blocked actions)
testing_decision_sequences.csv:    ~300 rows (sequences per scenario)
testing_explore_vs_exploit.csv:    ~60 rows (2 types x 30 scenarios)
testing_bus_events.csv:            ~90 rows (3 types x 30 scenarios)

Total CSV data: ~38,000 rows across all files
All parseable, analyzable, and ready for XAI algorithms!


================================================================================
SUMMARY
================================================================================

Both scripts now capture ALL 10 suggested XAI data types:
✅ #1 State-Action Pairs (parse_testing_q_values.sh)
✅ #2 Reward Breakdown (parse_testing_log.sh)
✅ #3 Phase Transition Patterns (parse_testing_log.sh)
✅ #4 Q-Value Ranking Changes (parse_testing_q_values.sh)
✅ #5 Blocked Actions with Context (parse_testing_log.sh)
✅ #6 Exploitation Decision Sequences (parse_testing_log.sh)
✅ #7 Exploration vs Exploitation (parse_testing_log.sh)
✅ #8 Bus Assistance Events (parse_testing_log.sh)
✅ #9 Safety-Performance Tradeoff (already in original + enhanced)
✅ #10 Feature Importance Proxies (data captured, analysis in Python)

FIXED:
✅ "Unknown" phase display → Now shows P1/P2/P3/P4 correctly
✅ Missing phase duration → Now captured from log events
✅ Missing decision context → Now captured for all non-Continue actions

READY FOR:
✅ Explainable RL paper
✅ Attention mechanisms
✅ Counterfactual explanations
✅ Decision tree extraction
✅ Natural language generation
✅ User study with traffic engineers

All raw data exists in testing.log - scripts extract and structure it
for XAI analysis. No code changes needed to traffic control system!

================================================================================
