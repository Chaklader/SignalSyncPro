==================================================
DRL Single-Agent Explainability & Safety Analysis
==================================================

Model: models/training_20251103_163015/checkpoint_ep192.pth
Project Root: /Users/chaklader/PycharmProjects/SignalSyncPro

Starting analysis...


🔍 Auto-detected states file: results/test_states_20251115_202404.npz

================================================================================
  COMPREHENSIVE EXPLAINABILITY & SAFETY ANALYSIS
  Paper 2: Section 4 (Explainability) + Section 5 (Safety)
================================================================================

Model: models/training_20251103_163015/checkpoint_ep192.pth
Estimated runtime: ~25 minutes

Starting analysis...


================================================================================
  ANALYSIS 1/6: Saliency Maps (Section 4.4)
================================================================================

Using device: cpu
Model loaded from models/training_20251103_163015/checkpoint_ep192.pth
✅ Loaded model from: models/training_20251103_163015/checkpoint_ep192.pth
📊 State dim: 32, Action dim: 3

================================================================================
Processing: P1_Active_High_Vehicle_Queue (1/5)

================================================================================
SALIENCY ANALYSIS: P1_Active_High_Vehicle_Queue
================================================================================

🎯 Continue:
   Top 5 influential features:
   1. TLS6_Sim_Time: -1.2392
   2. TLS3_Sim_Time: -1.0013
   3. TLS3_Phase_P4: +0.5295
   4. TLS3_Bus_Wait: -0.4611
   5. TLS6_Bus_Wait: -0.3591

🎯 Skip2P1:
   Top 5 influential features:
   1. TLS6_Sim_Time: -1.2392
   2. TLS3_Sim_Time: -1.0013
   3. TLS3_Phase_P4: +0.5295
   4. TLS3_Bus_Wait: -0.4611
   5. TLS6_Bus_Wait: -0.3591

🎯 Next:
   Top 5 influential features:
   1. TLS6_Sim_Time: -1.2392
   2. TLS3_Sim_Time: -1.0013
   3. TLS3_Phase_P4: +0.5295
   4. TLS3_Bus_Wait: -0.4611
   5. TLS6_Bus_Wait: -0.3591
💾 Saved visualization to: images/2/saliency/saliency_000_P1_Active_High_Vehicle_Queue.png

================================================================================
Processing: P1_Active_Bus_Priority (2/5)

================================================================================
SALIENCY ANALYSIS: P1_Active_Bus_Priority
================================================================================

🎯 Continue:
   Top 5 influential features:
   1. TLS6_Phase_Duration: +1.3472
   2. TLS6_Sim_Time: -1.3019
   3. TLS3_Phase_Duration: +1.0728
   4. TLS3_Sim_Time: -1.0507
   5. TLS3_Phase_P4: +0.7140

🎯 Skip2P1:
   Top 5 influential features:
   1. TLS6_Phase_Duration: +1.3472
   2. TLS6_Sim_Time: -1.3019
   3. TLS3_Phase_Duration: +1.0728
   4. TLS3_Sim_Time: -1.0507
   5. TLS3_Phase_P4: +0.7140

🎯 Next:
   Top 5 influential features:
   1. TLS6_Phase_Duration: +1.3472
   2. TLS6_Sim_Time: -1.3019
   3. TLS3_Phase_Duration: +1.0728
   4. TLS3_Sim_Time: -1.0507
   5. TLS3_Phase_P4: +0.7140
💾 Saved visualization to: images/2/saliency/saliency_001_P1_Active_Bus_Priority.png

================================================================================
Processing: P3_Active_Mixed_Bicycle_Demand (3/5)

================================================================================
SALIENCY ANALYSIS: P3_Active_Mixed_Bicycle_Demand
================================================================================

🎯 Continue:
   Top 5 influential features:
   1. TLS3_Sim_Time: -0.9099
   2. TLS6_Phase_Duration: +0.5862
   3. TLS6_Sim_Time: -0.5708
   4. TLS3_Phase_P4: +0.4676
   5. TLS6_Bus_Wait: -0.4501

🎯 Skip2P1:
   Top 5 influential features:
   1. TLS3_Sim_Time: -0.9099
   2. TLS6_Phase_Duration: +0.5862
   3. TLS6_Sim_Time: -0.5708
   4. TLS3_Phase_P4: +0.4676
   5. TLS6_Bus_Wait: -0.4501

🎯 Next:
   Top 5 influential features:
   1. TLS3_Sim_Time: -0.9099
   2. TLS6_Phase_Duration: +0.5862
   3. TLS6_Sim_Time: -0.5708
   4. TLS3_Phase_P4: +0.4676
   5. TLS6_Bus_Wait: -0.4501
💾 Saved visualization to: images/2/saliency/saliency_002_P3_Active_Mixed_Bicycle_Demand.png

================================================================================
Processing: P4_Active_Long_Duration (4/5)

================================================================================
SALIENCY ANALYSIS: P4_Active_Long_Duration
================================================================================

🎯 Continue:
   Top 5 influential features:
   1. TLS3_Phase_Duration: +1.3923
   2. TLS6_Phase_Duration: +1.3624
   3. TLS6_Sim_Time: -0.9033
   4. TLS3_Sim_Time: -0.7249
   5. TLS3_Phase_P4: +0.6333

🎯 Skip2P1:
   Top 5 influential features:
   1. TLS3_Phase_Duration: +1.3923
   2. TLS6_Phase_Duration: +1.3624
   3. TLS6_Sim_Time: -0.9033
   4. TLS3_Sim_Time: -0.7249
   5. TLS3_Phase_P4: +0.6333

🎯 Next:
   Top 5 influential features:
   1. TLS3_Phase_Duration: +1.3923
   2. TLS6_Phase_Duration: +1.3624
   3. TLS6_Sim_Time: -0.9033
   4. TLS3_Sim_Time: -0.7249
   5. TLS3_Phase_P4: +0.6333
💾 Saved visualization to: images/2/saliency/saliency_003_P4_Active_Long_Duration.png

================================================================================
Processing: P1_Heavy_Congestion_All_Modes (5/5)

================================================================================
SALIENCY ANALYSIS: P1_Heavy_Congestion_All_Modes
================================================================================

🎯 Continue:
   Top 5 influential features:
   1. TLS6_Phase_Duration: +1.6456
   2. TLS3_Phase_Duration: +1.5265
   3. TLS3_Sim_Time: -1.3269
   4. TLS6_Sim_Time: -1.2519
   5. TLS3_Phase_P4: +0.7200

🎯 Skip2P1:
   Top 5 influential features:
   1. TLS6_Phase_Duration: +1.6456
   2. TLS3_Phase_Duration: +1.5265
   3. TLS3_Sim_Time: -1.3269
   4. TLS6_Sim_Time: -1.2519
   5. TLS3_Phase_P4: +0.7200

🎯 Next:
   Top 5 influential features:
   1. TLS6_Phase_Duration: +1.6456
   2. TLS3_Phase_Duration: +1.5265
   3. TLS3_Sim_Time: -1.3269
   4. TLS6_Sim_Time: -1.2519
   5. TLS3_Phase_P4: +0.7200
💾 Saved visualization to: images/2/saliency/saliency_004_P1_Heavy_Congestion_All_Modes.png

✅ Batch analysis complete! Results saved to: images/2/saliency
✅ Saliency analysis complete!

================================================================================
  ANALYSIS 2/6: Attention Patterns (Section 4.1)
================================================================================

Using device: cpu
Model loaded from models/training_20251103_163015/checkpoint_ep192.pth
✅ Loaded model from: models/training_20251103_163015/checkpoint_ep192.pth

================================================================================
Processing: P1_High_Vehicle_Queue (1/4)

================================================================================
ATTENTION ANALYSIS: P1_High_Vehicle_Queue
================================================================================

📊 Q-Values:
   Continue: 0.6431
🎯 Skip2P1: 0.8089
   Next: 0.4561

🔍 Attention Distribution (Selected Action: Skip2P1):
   TLS3_Phase_Encoding      : 11.72%
   TLS3_Timing              :  9.86%
   TLS3_Vehicle_Detectors   :  9.95%
   TLS3_Bicycle_Detectors   : 10.57%
   TLS3_Bus_Info            :  6.95%
   TLS6_Phase_Encoding      : 10.23%
   TLS6_Timing              : 11.82%
   TLS6_Vehicle_Detectors   : 11.12%
   TLS6_Bicycle_Detectors   : 11.11%
   TLS6_Bus_Info            :  6.65%
💾 Saved visualization to: images/2/attention/attention_000_P1_High_Vehicle_Queue.png

================================================================================
Processing: P1_Bus_Waiting (2/4)

================================================================================
ATTENTION ANALYSIS: P1_Bus_Waiting
================================================================================

📊 Q-Values:
   Continue: -0.2215
🎯 Skip2P1: -0.1748
   Next: -0.5995

🔍 Attention Distribution (Selected Action: Skip2P1):
   TLS3_Phase_Encoding      : 10.78%
   TLS3_Timing              : 11.06%
   TLS3_Vehicle_Detectors   :  9.75%
   TLS3_Bicycle_Detectors   : 10.37%
   TLS3_Bus_Info            :  7.35%
   TLS6_Phase_Encoding      :  9.46%
   TLS6_Timing              : 13.78%
   TLS6_Vehicle_Detectors   :  9.27%
   TLS6_Bicycle_Detectors   :  9.58%
   TLS6_Bus_Info            :  8.60%
💾 Saved visualization to: images/2/attention/attention_001_P1_Bus_Waiting.png

================================================================================
Processing: P1_Long_Duration_Mixed_Queue (3/4)

================================================================================
ATTENTION ANALYSIS: P1_Long_Duration_Mixed_Queue
================================================================================

📊 Q-Values:
🎯 Continue: 0.6856
   Skip2P1: 0.5675
   Next: 0.2832

🔍 Attention Distribution (Selected Action: Continue):
   TLS3_Phase_Encoding      : 11.27%
   TLS3_Timing              :  9.01%
   TLS3_Vehicle_Detectors   : 10.82%
   TLS3_Bicycle_Detectors   : 11.26%
   TLS3_Bus_Info            :  6.92%
   TLS6_Phase_Encoding      : 11.17%
   TLS6_Timing              :  9.03%
   TLS6_Vehicle_Detectors   : 12.01%
   TLS6_Bicycle_Detectors   : 10.97%
   TLS6_Bus_Info            :  7.55%
💾 Saved visualization to: images/2/attention/attention_002_P1_Long_Duration_Mixed_Queue.png

================================================================================
Processing: P3_High_Bicycle_Demand (4/4)

================================================================================
ATTENTION ANALYSIS: P3_High_Bicycle_Demand
================================================================================

📊 Q-Values:
🎯 Continue: -0.0019
   Skip2P1: -0.1023
   Next: -0.5744

🔍 Attention Distribution (Selected Action: Continue):
   TLS3_Phase_Encoding      : 11.83%
   TLS3_Timing              :  9.76%
   TLS3_Vehicle_Detectors   : 11.64%
   TLS3_Bicycle_Detectors   : 11.24%
   TLS3_Bus_Info            :  7.46%
   TLS6_Phase_Encoding      : 11.40%
   TLS6_Timing              :  6.69%
   TLS6_Vehicle_Detectors   : 11.12%
   TLS6_Bicycle_Detectors   : 10.97%
   TLS6_Bus_Info            :  7.88%
💾 Saved visualization to: images/2/attention/attention_003_P3_High_Bicycle_Demand.png

✅ Batch analysis complete! Results saved to: images/2/attention
✅ Attention analysis complete!

================================================================================
  ANALYSIS 3/6: Counterfactual Explanations (Section 4.2)
================================================================================

Using device: cpu
Model loaded from models/training_20251103_163015/checkpoint_ep192.pth
✅ Loaded model from: models/training_20251103_163015/checkpoint_ep192.pth

================================================================================
Processing: P1_Moderate_Queue (1/3)

   Generating: Skip2P1 → Continue
   ✓ Converged at iteration 17

================================================================================
COUNTERFACTUAL EXPLANATION
================================================================================

📊 Original Decision:
   Action: Skip2P1
   Q-values: [0.41521257 0.7850318  0.5343708 ]

🎯 Target Decision:
   Action: Continue

✨ Counterfactual Decision:
   Action: Continue
   Q-values: [0.5202397  0.49065903 0.13896504]

📏 Changes Required:
   Features changed: 17
   L2 distance: 0.4212
   Optimization iterations: 18

🔍 Feature Changes (|Δ| > 0.01):
   TLS3_Phase_P3            : 0.000 → 0.013 (Δ = +0.013)
   TLS3_Phase_Duration      : 0.700 → 0.582 (Δ = -0.118)
   TLS3_Vehicle_Det1        : 1.000 → 0.883 (Δ = -0.117)
   TLS3_Vehicle_Det2        : 0.000 → 0.082 (Δ = +0.082)
   TLS3_Vehicle_Det3        : 0.000 → 0.098 (Δ = +0.098)
   TLS3_Vehicle_Det4        : 0.000 → 0.111 (Δ = +0.111)
   TLS3_Bus_Present         : 0.000 → 0.088 (Δ = +0.088)
   TLS3_Sim_Time            : 0.000 → 0.120 (Δ = +0.120)
   TLS6_Phase_P2            : 0.000 → 0.079 (Δ = +0.079)
   TLS6_Phase_P3            : 0.000 → 0.117 (Δ = +0.117)
   TLS6_Phase_Duration      : 0.500 → 0.382 (Δ = -0.118)
   TLS6_Vehicle_Det1        : 0.000 → 0.117 (Δ = +0.117)
   TLS6_Vehicle_Det2        : 0.000 → 0.110 (Δ = +0.110)
   TLS6_Vehicle_Det3        : 0.000 → 0.027 (Δ = +0.027)
   TLS6_Bicycle_Det1        : 0.000 → 0.113 (Δ = +0.113)
   TLS6_Bicycle_Det4        : 0.000 → 0.107 (Δ = +0.107)
   TLS6_Sim_Time            : 0.000 → 0.119 (Δ = +0.119)
💾 Saved visualization to: images/2/counterfactuals/cf_000_P1_Moderate_Queue_to_Continue.png

   Generating: Skip2P1 → Next
   ✓ Converged at iteration 16

================================================================================
COUNTERFACTUAL EXPLANATION
================================================================================

📊 Original Decision:
   Action: Skip2P1
   Q-values: [0.41521257 0.7850318  0.5343708 ]

🎯 Target Decision:
   Action: Next

✨ Counterfactual Decision:
   Action: Next
   Q-values: [-0.256087    0.43197152  0.46567687]

📏 Changes Required:
   Features changed: 19
   L2 distance: 0.3431
   Optimization iterations: 17

🔍 Feature Changes (|Δ| > 0.01):
   TLS3_Phase_P1            : 1.000 → 0.920 (Δ = -0.080)
   TLS3_Phase_P2            : 0.000 → 0.077 (Δ = +0.077)
   TLS3_Phase_P4            : 0.000 → 0.080 (Δ = +0.080)
   TLS3_Phase_Duration      : 0.700 → 0.780 (Δ = +0.080)
   TLS3_Vehicle_Det4        : 0.000 → 0.079 (Δ = +0.079)
   TLS3_Bicycle_Det2        : 0.000 → 0.065 (Δ = +0.065)
   TLS3_Bicycle_Det3        : 0.000 → 0.078 (Δ = +0.078)
   TLS3_Bicycle_Det4        : 0.000 → 0.080 (Δ = +0.080)
   TLS3_Bus_Wait            : 0.000 → 0.080 (Δ = +0.080)
   TLS3_Sim_Time            : 0.000 → 0.080 (Δ = +0.080)
   TLS6_Phase_P1            : 1.000 → 0.920 (Δ = -0.080)
   TLS6_Phase_P4            : 0.000 → 0.080 (Δ = +0.080)
   TLS6_Phase_Duration      : 0.500 → 0.580 (Δ = +0.080)
   TLS6_Vehicle_Det1        : 0.000 → 0.080 (Δ = +0.080)
   TLS6_Vehicle_Det2        : 0.000 → 0.080 (Δ = +0.080)
   TLS6_Vehicle_Det3        : 0.000 → 0.075 (Δ = +0.075)
   TLS6_Vehicle_Det4        : 0.000 → 0.080 (Δ = +0.080)
   TLS6_Bus_Wait            : 0.000 → 0.080 (Δ = +0.080)
   TLS6_Sim_Time            : 0.000 → 0.080 (Δ = +0.080)
💾 Saved visualization to: images/2/counterfactuals/cf_000_P1_Moderate_Queue_to_Next.png

================================================================================
Processing: P1_Bus_Present (2/3)

   Generating: Continue → Skip2P1
   ✓ Converged at iteration 18

================================================================================
COUNTERFACTUAL EXPLANATION
================================================================================

📊 Original Decision:
   Action: Continue
   Q-values: [ 0.5638129   0.2403188  -0.30630067]

🎯 Target Decision:
   Action: Skip2P1

✨ Counterfactual Decision:
   Action: Skip2P1
   Q-values: [0.4429705  0.48121366 0.12508373]

📏 Changes Required:
   Features changed: 15
   L2 distance: 0.4506
   Optimization iterations: 19

🔍 Feature Changes (|Δ| > 0.01):
   TLS3_Phase_P1            : 1.000 → 0.871 (Δ = -0.129)
   TLS3_Phase_P2            : 0.000 → 0.104 (Δ = +0.104)
   TLS3_Phase_P4            : 0.000 → 0.129 (Δ = +0.129)
   TLS3_Phase_Duration      : 0.300 → 0.428 (Δ = +0.128)
   TLS3_Vehicle_Det4        : 0.000 → 0.117 (Δ = +0.117)
   TLS3_Bicycle_Det3        : 0.000 → 0.123 (Δ = +0.123)
   TLS3_Bus_Wait            : 0.600 → 0.726 (Δ = +0.126)
   TLS6_Phase_P1            : 1.000 → 0.871 (Δ = -0.129)
   TLS6_Phase_P2            : 0.000 → 0.012 (Δ = +0.012)
   TLS6_Phase_P4            : 0.000 → 0.129 (Δ = +0.129)
   TLS6_Phase_Duration      : 0.000 → 0.129 (Δ = +0.129)
   TLS6_Vehicle_Det1        : 0.000 → 0.080 (Δ = +0.080)
   TLS6_Vehicle_Det2        : 0.000 → 0.095 (Δ = +0.095)
   TLS6_Bus_Present         : 0.000 → 0.128 (Δ = +0.128)
   TLS6_Bus_Wait            : 0.000 → 0.126 (Δ = +0.126)
💾 Saved visualization to: images/2/counterfactuals/cf_001_P1_Bus_Present_to_Skip2P1.png

   Generating: Continue → Next
   ✓ Converged at iteration 28
❌ Failed to generate counterfactual

================================================================================
Processing: P1_Long_Duration (3/3)

   Generating: Continue → Skip2P1
   ✓ Converged at iteration 15

================================================================================
COUNTERFACTUAL EXPLANATION
================================================================================

📊 Original Decision:
   Action: Continue
   Q-values: [0.75434756 0.4715961  0.11655906]

🎯 Target Decision:
   Action: Skip2P1

✨ Counterfactual Decision:
   Action: Skip2P1
   Q-values: [0.5487462  0.61713547 0.39982235]

📏 Changes Required:
   Features changed: 17
   L2 distance: 0.3346
   Optimization iterations: 16

🔍 Feature Changes (|Δ| > 0.01):
   TLS3_Phase_P1            : 1.000 → 0.911 (Δ = -0.089)
   TLS3_Phase_P2            : 0.000 → 0.084 (Δ = +0.084)
   TLS3_Phase_P4            : 0.000 → 0.089 (Δ = +0.089)
   TLS3_Phase_Duration      : 0.730 → 0.819 (Δ = +0.089)
   TLS3_Vehicle_Det1        : 0.000 → 0.089 (Δ = +0.089)
   TLS3_Bicycle_Det1        : 0.000 → 0.088 (Δ = +0.088)
   TLS3_Bicycle_Det2        : 0.000 → 0.066 (Δ = +0.066)
   TLS6_Phase_P1            : 1.000 → 0.910 (Δ = -0.090)
   TLS6_Phase_P2            : 0.000 → 0.089 (Δ = +0.089)
   TLS6_Phase_P4            : 0.000 → 0.089 (Δ = +0.089)
   TLS6_Phase_Duration      : 0.000 → 0.089 (Δ = +0.089)
   TLS6_Vehicle_Det1        : 1.000 → 0.911 (Δ = -0.089)
   TLS6_Vehicle_Det3        : 0.000 → 0.075 (Δ = +0.075)
   TLS6_Vehicle_Det4        : 1.000 → 0.944 (Δ = -0.056)
   TLS6_Bicycle_Det2        : 0.000 → 0.022 (Δ = +0.022)
   TLS6_Bicycle_Det3        : 0.000 → 0.089 (Δ = +0.089)
   TLS6_Bicycle_Det4        : 0.000 → 0.062 (Δ = +0.062)
💾 Saved visualization to: images/2/counterfactuals/cf_002_P1_Long_Duration_to_Skip2P1.png

   Generating: Continue → Next
   ✓ Converged at iteration 21
❌ Failed to generate counterfactual

✅ Batch generation complete! Results saved to: images/2/counterfactuals
✅ Counterfactual generation complete!

   [Enhanced] Generating counterfactuals for rare transitions...

================================================================================
ENHANCED COUNTERFACTUAL GENERATION FOR RARE TRANSITIONS
================================================================================

   Total states: 300,000
   Action distribution:
      Continue: 242,281 (80.8%)
      Skip2P1: 6,857 (2.3%)
      Next: 50,862 (17.0%)

================================================================================
TRANSITION: Continue → Next
================================================================================
   Found 10 sample states

   Attempt 1/10 (Scenario: Pe_6):
   ✅ Success after 1 attempts, 2 iterations, distance: 0.229
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Continue_to_Next_1.png

   Attempt 2/10 (Scenario: Pr_6):
   ✅ Success after 1 attempts, 2 iterations, distance: 0.200
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Continue_to_Next_2.png

   Attempt 3/10 (Scenario: Pe_2):
   ✅ Success after 1 attempts, 5 iterations, distance: 0.859
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Continue_to_Next_3.png

   ✅ Success rate: 3/10

================================================================================
TRANSITION: Skip2P1 → Next
================================================================================
   Found 10 sample states

   Attempt 1/10 (Scenario: Pr_7):
   ✅ Success after 1 attempts, 2 iterations, distance: 0.206
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Skip2P1_to_Next_1.png

   Attempt 2/10 (Scenario: Pr_9):
   ✅ Success after 1 attempts, 2 iterations, distance: 0.212
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Skip2P1_to_Next_2.png

   Attempt 3/10 (Scenario: Pe_2):
   ✅ Success after 5 attempts, 2 iterations, distance: 0.531
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Skip2P1_to_Next_3.png

   ✅ Success rate: 3/10

================================================================================
TRANSITION: Next → Continue
================================================================================
   Found 10 sample states

   Attempt 1/10 (Scenario: Pe_9):
   ✅ Success after 1 attempts, 3 iterations, distance: 0.394
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Next_to_Continue_1.png

   Attempt 2/10 (Scenario: Pr_4):
   ✅ Success after 1 attempts, 2 iterations, distance: 0.218
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Next_to_Continue_2.png

   Attempt 3/10 (Scenario: Pe_5):
   ✅ Success after 1 attempts, 2 iterations, distance: 0.212
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Next_to_Continue_3.png

   ✅ Success rate: 3/10

================================================================================
TRANSITION: Next → Skip2P1
================================================================================
   Found 10 sample states

   Attempt 1/10 (Scenario: Pr_8):
   ✅ Success after 1 attempts, 4 iterations, distance: 0.406
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Next_to_Skip2P1_1.png

   Attempt 2/10 (Scenario: Pe_3):
   ✅ Success after 5 attempts, 8 iterations, distance: 0.925
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Next_to_Skip2P1_2.png

   Attempt 3/10 (Scenario: Pr_2):
   ✅ Success after 1 attempts, 8 iterations, distance: 0.905
   💾 Saved: images/2/counterfactuals_enhanced/cf_rare_Next_to_Skip2P1_3.png

   ✅ Success rate: 3/10

================================================================================
SUMMARY
================================================================================
   Total counterfactuals generated: 12
   Saved to: images/2/counterfactuals_enhanced

   Transition Success Summary:
      Continue → Next: 3 counterfactuals
      Skip2P1 → Next: 3 counterfactuals
      Next → Continue: 3 counterfactuals
      Next → Skip2P1: 3 counterfactuals

✅ Enhanced counterfactual generation complete!

================================================================================
  ANALYSIS 4/6: Decision Tree Extraction (Section 4.3)
================================================================================

Note: This analysis takes ~10 minutes
Using device: cpu
Model loaded from models/training_20251103_163015/checkpoint_ep192.pth
✅ Loaded DQN model from: models/training_20251103_163015/checkpoint_ep192.pth

[Phase 1/4] Collecting initial dataset...

📂 Loading REAL states from testing...
   File: results/test_states_20251115_202404.npz

✅ Real states loaded successfully!
   Total states in file: 300,000
   State shape: (300000, 32)
   Scenarios covered: 30

   Action distribution (from real policy):
   {'Continue': np.int64(242281), 'Skip2P1': np.int64(6857), 'Next': np.int64(50862)}
     Continue: 80.8%
     Skip2P1: 2.3%
     Next: 17.0%

[Phase 2/4] Running VIPER iterations...

================================================================================
VIPER Iteration 1/3
================================================================================

🌳 Training decision tree...
   Max depth: 10
   Min samples split: 50
   Min samples leaf: 20

✅ Tree trained!
   Train accuracy: 97.07%
   Test accuracy: 96.92%
   Tree depth: 10
   Number of leaves: 383

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.98      0.99      0.98     49683
     Skip2P1       0.84      0.82      0.83      1369
        Next       0.94      0.89      0.92      8948

    accuracy                           0.97     60000
   macro avg       0.92      0.90      0.91     60000
weighted avg       0.97      0.97      0.97     60000


🎲 Generating 2000 new samples using tree policy...
   Dataset size now: 302000

================================================================================
VIPER Iteration 2/3
================================================================================

🌳 Training decision tree...
   Max depth: 10
   Min samples split: 50
   Min samples leaf: 20

✅ Tree trained!
   Train accuracy: 97.09%
   Test accuracy: 94.75%
   Tree depth: 10
   Number of leaves: 390

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.96      0.99      0.97     48659
     Skip2P1       0.65      0.78      0.71      1307
        Next       0.94      0.79      0.86     10434

    accuracy                           0.95     60400
   macro avg       0.85      0.85      0.85     60400
weighted avg       0.95      0.95      0.95     60400


🎲 Generating 2000 new samples using tree policy...
   Dataset size now: 304000

================================================================================
VIPER Iteration 3/3
================================================================================

🌳 Training decision tree...
   Max depth: 10
   Min samples split: 50
   Min samples leaf: 20

✅ Tree trained!
   Train accuracy: 97.09%
   Test accuracy: 92.70%
   Tree depth: 10
   Number of leaves: 393

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.94      0.98      0.96     47623
     Skip2P1       0.53      0.75      0.63      1367
        Next       0.93      0.71      0.81     11810

    accuracy                           0.93     60800
   macro avg       0.80      0.82      0.80     60800
weighted avg       0.93      0.93      0.93     60800


🎲 Generating 2000 new samples using tree policy...
   Dataset size now: 306000

================================================================================
Final Tree Training
================================================================================

🌳 Training decision tree...
   Max depth: 8
   Min samples split: 50
   Min samples leaf: 20

✅ Tree trained!
   Train accuracy: 95.76%
   Test accuracy: 89.47%
   Tree depth: 8
   Number of leaves: 173

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.91      0.98      0.95     46671
     Skip2P1       0.38      0.63      0.47      1442
        Next       0.92      0.61      0.73     13087

    accuracy                           0.89     61200
   macro avg       0.74      0.74      0.72     61200
weighted avg       0.90      0.89      0.89     61200


[Phase 3/4] Extracting decision rules...

================================================================================
EXTRACTED DECISION RULES (Accuracy: 89.5%)
================================================================================

|--- TLS6_Phase_P1 <= 0.500
|   |--- TLS6_Phase_Duration <= 0.042
|   |   |--- TLS6_Phase_P4 <= 0.500
|   |   |   |--- TLS3_Bus_Wait <= 0.158
|   |   |   |   |--- TLS3_Vehicle_Det2 <= 0.500
|   |   |   |   |   |--- TLS6_Bus_Wait <= 0.279
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.109
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.025
|   |   |   |   |   |   |   |   |--- weights: [3396.000, 434.000, 0.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.025
|   |   |   |   |   |   |   |   |--- weights: [67.000, 1828.000, 800.000] class: 1
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.109
|   |   |   |   |   |   |   |--- TLS3_Phase_P2 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [59346.000, 360.000, 133.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Phase_P2 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [4785.000, 278.000, 1632.000] class: 0
|   |   |   |   |   |--- TLS6_Bus_Wait >  0.279
|   |   |   |   |   |   |--- TLS3_Phase_P3 <= 0.500
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.375
|   |   |   |   |   |   |   |   |--- weights: [36.000, 4.000, 61.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.375
|   |   |   |   |   |   |   |   |--- weights: [25.000, 0.000, 1346.000] class: 2
|   |   |   |   |   |   |--- TLS3_Phase_P3 >  0.500
|   |   |   |   |   |   |   |--- weights: [48.000, 0.000, 0.000] class: 0
|   |   |   |   |--- TLS3_Vehicle_Det2 >  0.500
|   |   |   |   |   |--- TLS3_Vehicle_Det3 <= 0.500
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.815
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [315.000, 0.000, 2.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [71.000, 1.000, 6.000] class: 0
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.815
|   |   |   |   |   |   |   |--- TLS6_Phase_P2 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [65.000, 0.000, 0.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Phase_P2 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [23.000, 0.000, 29.000] class: 2
|   |   |   |   |   |--- TLS3_Vehicle_Det3 >  0.500
|   |   |   |   |   |   |--- TLS6_Bicycle_Det3 <= 0.500
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [38.000, 0.000, 8.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [27.000, 0.000, 2030.000] class: 2
|   |   |   |   |   |   |--- TLS6_Bicycle_Det3 >  0.500
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det4 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [276.000, 0.000, 217.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det4 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [135.000, 0.000, 1042.000] class: 2
|   |   |   |--- TLS3_Bus_Wait >  0.158
|   |   |   |   |--- TLS3_Sim_Time <= 0.286
|   |   |   |   |   |--- TLS3_Bus_Wait <= 0.225
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.015
|   |   |   |   |   |   |   |--- weights: [0.000, 86.000, 0.000] class: 1
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.015
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.008
|   |   |   |   |   |   |   |   |--- weights: [17.000, 4.000, 0.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.008
|   |   |   |   |   |   |   |   |--- weights: [0.000, 44.000, 3.000] class: 1
|   |   |   |   |   |--- TLS3_Bus_Wait >  0.225
|   |   |   |   |   |   |--- weights: [20.000, 8.000, 7.000] class: 0
|   |   |   |   |--- TLS3_Sim_Time >  0.286
|   |   |   |   |   |--- TLS3_Phase_P3 <= 0.500
|   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.508
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.125
|   |   |   |   |   |   |   |   |--- weights: [118.000, 6.000, 111.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.125
|   |   |   |   |   |   |   |   |--- weights: [9.000, 7.000, 374.000] class: 2
|   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.508
|   |   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.380
|   |   |   |   |   |   |   |   |--- weights: [5.000, 0.000, 29.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Sim_Time >  0.380
|   |   |   |   |   |   |   |   |--- weights: [3.000, 0.000, 2240.000] class: 2
|   |   |   |   |   |--- TLS3_Phase_P3 >  0.500
|   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |--- weights: [96.000, 0.000, 0.000] class: 0
|   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.592
|   |   |   |   |   |   |   |   |--- weights: [8.000, 0.000, 13.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.592
|   |   |   |   |   |   |   |   |--- weights: [5.000, 0.000, 135.000] class: 2
|   |   |--- TLS6_Phase_P4 >  0.500
|   |   |   |--- weights: [0.000, 0.000, 4096.000] class: 2
|   |--- TLS6_Phase_Duration >  0.042
|   |   |--- TLS3_Phase_Duration <= 0.092
|   |   |   |--- TLS3_Phase_P3 <= 0.500
|   |   |   |   |--- TLS6_Sim_Time <= 0.240
|   |   |   |   |   |--- TLS6_Phase_P2 <= 0.500
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.035
|   |   |   |   |   |   |   |--- weights: [0.000, 338.000, 0.000] class: 1
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.035
|   |   |   |   |   |   |   |--- TLS3_Bus_Present <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [0.000, 9.000, 2163.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Bus_Present >  0.500
|   |   |   |   |   |   |   |   |--- weights: [0.000, 52.000, 1.000] class: 1
|   |   |   |   |   |--- TLS6_Phase_P2 >  0.500
|   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [110.000, 1024.000, 70.000] class: 1
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [104.000, 8.000, 24.000] class: 0
|   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.075
|   |   |   |   |   |   |   |   |--- weights: [105.000, 0.000, 2.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.075
|   |   |   |   |   |   |   |   |--- weights: [32.000, 0.000, 4.000] class: 0
|   |   |   |   |--- TLS6_Sim_Time >  0.240
|   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |--- TLS3_Phase_P2 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Bus_Present <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 10194.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Bus_Present >  0.500
|   |   |   |   |   |   |   |   |--- weights: [86.000, 66.000, 608.000] class: 2
|   |   |   |   |   |   |--- TLS3_Phase_P2 >  0.500
|   |   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.317
|   |   |   |   |   |   |   |   |--- weights: [210.000, 13.000, 255.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Sim_Time >  0.317
|   |   |   |   |   |   |   |   |--- weights: [240.000, 5.000, 2635.000] class: 2
|   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |--- TLS3_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.058
|   |   |   |   |   |   |   |   |--- weights: [95.000, 0.000, 13.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.058
|   |   |   |   |   |   |   |   |--- weights: [152.000, 0.000, 5.000] class: 0
|   |   |   |   |   |   |--- TLS3_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |--- weights: [10.000, 0.000, 17.000] class: 2
|   |   |   |--- TLS3_Phase_P3 >  0.500
|   |   |   |   |--- TLS3_Vehicle_Det3 <= 0.500
|   |   |   |   |   |--- TLS3_Bus_Wait <= 0.642
|   |   |   |   |   |   |--- weights: [3101.000, 0.000, 0.000] class: 0
|   |   |   |   |   |--- TLS3_Bus_Wait >  0.642
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.830
|   |   |   |   |   |   |   |--- weights: [14.000, 1.000, 8.000] class: 0
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.830
|   |   |   |   |   |   |   |--- weights: [53.000, 0.000, 0.000] class: 0
|   |   |   |   |--- TLS3_Vehicle_Det3 >  0.500
|   |   |   |   |   |--- TLS3_Vehicle_Det2 <= 0.500
|   |   |   |   |   |   |--- weights: [308.000, 0.000, 0.000] class: 0
|   |   |   |   |   |--- TLS3_Vehicle_Det2 >  0.500
|   |   |   |   |   |   |--- TLS3_Vehicle_Det1 <= 0.500
|   |   |   |   |   |   |   |--- weights: [60.000, 0.000, 0.000] class: 0
|   |   |   |   |   |   |--- TLS3_Vehicle_Det1 >  0.500
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.097
|   |   |   |   |   |   |   |   |--- weights: [8.000, 0.000, 12.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.097
|   |   |   |   |   |   |   |   |--- weights: [56.000, 0.000, 5706.000] class: 2
|   |   |--- TLS3_Phase_Duration >  0.092
|   |   |   |--- TLS3_Phase_Duration <= 0.292
|   |   |   |   |--- TLS6_Phase_P2 <= 0.500
|   |   |   |   |   |--- TLS6_Phase_Duration <= 0.275
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.571
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.242
|   |   |   |   |   |   |   |   |--- weights: [1372.000, 28.000, 18.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.242
|   |   |   |   |   |   |   |   |--- weights: [138.000, 72.000, 2.000] class: 0
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.571
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [9524.000, 38.000, 6.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [1160.000, 0.000, 64.000] class: 0
|   |   |   |   |   |--- TLS6_Phase_Duration >  0.275
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.704
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det4 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [47.000, 112.000, 2.000] class: 1
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det4 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [32.000, 12.000, 0.000] class: 0
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.704
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.675
|   |   |   |   |   |   |   |   |--- weights: [709.000, 17.000, 3.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.675
|   |   |   |   |   |   |   |   |--- weights: [10.000, 11.000, 1.000] class: 1
|   |   |   |   |--- TLS6_Phase_P2 >  0.500
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.126
|   |   |   |   |   |   |--- weights: [9.000, 16.000, 4.000] class: 1
|   |   |   |   |   |--- TLS6_Sim_Time >  0.126
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.433
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.353
|   |   |   |   |   |   |   |   |--- weights: [0.000, 1.000, 32.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.353
|   |   |   |   |   |   |   |   |--- weights: [4.000, 0.000, 16.000] class: 2
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.433
|   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 38.000] class: 2
|   |   |   |--- TLS3_Phase_Duration >  0.292
|   |   |   |   |--- TLS6_Phase_Duration <= 0.325
|   |   |   |   |   |--- TLS3_Sim_Time <= 0.814
|   |   |   |   |   |   |--- TLS6_Bicycle_Det4 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [63.000, 179.000, 0.000] class: 1
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [46.000, 1.000, 4.000] class: 0
|   |   |   |   |   |   |--- TLS6_Bicycle_Det4 >  0.500
|   |   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.610
|   |   |   |   |   |   |   |   |--- weights: [9.000, 15.000, 0.000] class: 1
|   |   |   |   |   |   |   |--- TLS6_Sim_Time >  0.610
|   |   |   |   |   |   |   |   |--- weights: [96.000, 13.000, 1.000] class: 0
|   |   |   |   |   |--- TLS3_Sim_Time >  0.814
|   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.308
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [403.000, 13.000, 0.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [65.000, 28.000, 1.000] class: 0
|   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.308
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.943
|   |   |   |   |   |   |   |   |--- weights: [176.000, 132.000, 2.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.943
|   |   |   |   |   |   |   |   |--- weights: [151.000, 5.000, 2.000] class: 0
|   |   |   |   |--- TLS6_Phase_Duration >  0.325
|   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |--- TLS3_Bicycle_Det4 <= 0.500
|   |   |   |   |   |   |   |--- TLS6_Bus_Present <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [53.000, 233.000, 3.000] class: 1
|   |   |   |   |   |   |   |--- TLS6_Bus_Present >  0.500
|   |   |   |   |   |   |   |   |--- weights: [39.000, 33.000, 1.000] class: 0
|   |   |   |   |   |   |--- TLS3_Bicycle_Det4 >  0.500
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [56.000, 24.000, 0.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [48.000, 68.000, 2.000] class: 1
|   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.856
|   |   |   |   |   |   |   |--- weights: [25.000, 17.000, 5.000] class: 0
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.856
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.358
|   |   |   |   |   |   |   |   |--- weights: [43.000, 2.000, 2.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.358
|   |   |   |   |   |   |   |   |--- weights: [12.000, 2.000, 7.000] class: 0
|--- TLS6_Phase_P1 >  0.500
|   |--- TLS6_Phase_Duration <= 0.558
|   |   |--- TLS6_Vehicle_Det3 <= 0.500
|   |   |   |--- TLS6_Phase_Duration <= 0.542
|   |   |   |   |--- TLS3_Bus_Wait <= 0.925
|   |   |   |   |   |--- TLS6_Phase_Duration <= 0.508
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.721
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.392
|   |   |   |   |   |   |   |   |--- weights: [50879.000, 0.000, 4.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.392
|   |   |   |   |   |   |   |   |--- weights: [9238.000, 0.000, 30.000] class: 0
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.721
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [7290.000, 0.000, 4.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [4536.000, 0.000, 116.000] class: 0
|   |   |   |   |   |--- TLS6_Phase_Duration >  0.508
|   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.925
|   |   |   |   |   |   |   |   |--- weights: [1797.000, 0.000, 15.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.925
|   |   |   |   |   |   |   |   |--- weights: [25.000, 0.000, 5.000] class: 0
|   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.653
|   |   |   |   |   |   |   |   |--- weights: [377.000, 0.000, 38.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.653
|   |   |   |   |   |   |   |   |--- weights: [28.000, 0.000, 30.000] class: 2
|   |   |   |   |--- TLS3_Bus_Wait >  0.925
|   |   |   |   |   |--- weights: [23.000, 0.000, 12.000] class: 0
|   |   |   |--- TLS6_Phase_Duration >  0.542
|   |   |   |   |--- TLS3_Bicycle_Det3 <= 0.500
|   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.500
|   |   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.869
|   |   |   |   |   |   |   |   |--- weights: [620.000, 0.000, 7.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Sim_Time >  0.869
|   |   |   |   |   |   |   |   |--- weights: [13.000, 0.000, 7.000] class: 0
|   |   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.500
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det2 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [60.000, 0.000, 29.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det2 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [75.000, 0.000, 3.000] class: 0
|   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.011
|   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 20.000] class: 2
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.011
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [77.000, 0.000, 50.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [66.000, 0.000, 2.000] class: 0
|   |   |   |   |--- TLS3_Bicycle_Det3 >  0.500
|   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.500
|   |   |   |   |   |   |--- TLS3_Bicycle_Det4 <= 0.500
|   |   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.136
|   |   |   |   |   |   |   |   |--- weights: [9.000, 0.000, 22.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Sim_Time >  0.136
|   |   |   |   |   |   |   |   |--- weights: [19.000, 0.000, 10.000] class: 0
|   |   |   |   |   |   |--- TLS3_Bicycle_Det4 >  0.500
|   |   |   |   |   |   |   |--- weights: [36.000, 0.000, 7.000] class: 0
|   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.500
|   |   |   |   |   |   |--- weights: [2.000, 0.000, 24.000] class: 2
|   |   |--- TLS6_Vehicle_Det3 >  0.500
|   |   |   |--- TLS3_Sim_Time <= 0.696
|   |   |   |   |--- TLS3_Vehicle_Det1 <= 0.500
|   |   |   |   |   |--- TLS6_Phase_Duration <= 0.525
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.475
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.681
|   |   |   |   |   |   |   |   |--- weights: [9430.000, 0.000, 5.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.681
|   |   |   |   |   |   |   |   |--- weights: [147.000, 0.000, 4.000] class: 0
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.475
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [2209.000, 0.000, 9.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [699.000, 0.000, 47.000] class: 0
|   |   |   |   |   |--- TLS6_Phase_Duration >  0.525
|   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det3 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [1027.000, 0.000, 20.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det3 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [59.000, 0.000, 40.000] class: 0
|   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [123.000, 0.000, 109.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [116.000, 0.000, 5.000] class: 0
|   |   |   |   |--- TLS3_Vehicle_Det1 >  0.500
|   |   |   |   |   |--- TLS6_Phase_Duration <= 0.525
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.482
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.475
|   |   |   |   |   |   |   |   |--- weights: [5807.000, 0.000, 142.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.475
|   |   |   |   |   |   |   |   |--- weights: [629.000, 0.000, 148.000] class: 0
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.482
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [1411.000, 0.000, 590.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [1748.000, 0.000, 107.000] class: 0
|   |   |   |   |   |--- TLS6_Phase_Duration >  0.525
|   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [74.000, 0.000, 121.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [3.000, 0.000, 53.000] class: 2
|   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [73.000, 0.000, 20.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [13.000, 0.000, 23.000] class: 2
|   |   |   |--- TLS3_Sim_Time >  0.696
|   |   |   |   |--- TLS3_Vehicle_Det2 <= 0.500
|   |   |   |   |   |--- TLS3_Bus_Wait <= 0.675
|   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [760.000, 0.000, 18.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [696.000, 0.000, 99.000] class: 0
|   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.375
|   |   |   |   |   |   |   |   |--- weights: [1379.000, 0.000, 4.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.375
|   |   |   |   |   |   |   |   |--- weights: [392.000, 0.000, 19.000] class: 0
|   |   |   |   |   |--- TLS3_Bus_Wait >  0.675
|   |   |   |   |   |   |--- TLS3_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.923
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 35.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.923
|   |   |   |   |   |   |   |   |--- weights: [6.000, 0.000, 26.000] class: 2
|   |   |   |   |   |   |--- TLS3_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |--- weights: [15.000, 0.000, 6.000] class: 0
|   |   |   |   |--- TLS3_Vehicle_Det2 >  0.500
|   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.500
|   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.442
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.292
|   |   |   |   |   |   |   |   |--- weights: [593.000, 0.000, 1.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.292
|   |   |   |   |   |   |   |   |--- weights: [231.000, 0.000, 20.000] class: 0
|   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.442
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [614.000, 0.000, 62.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [42.000, 0.000, 65.000] class: 2
|   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.500
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.075
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [504.000, 0.000, 494.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [1187.000, 0.000, 113.000] class: 0
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.075
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [113.000, 0.000, 954.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [724.000, 0.000, 908.000] class: 2
|   |--- TLS6_Phase_Duration >  0.558
|   |   |--- TLS3_Phase_Duration <= 0.592
|   |   |   |--- TLS6_Vehicle_Det4 <= 0.500
|   |   |   |   |--- TLS3_Bicycle_Det3 <= 0.500
|   |   |   |   |   |--- TLS3_Bicycle_Det2 <= 0.500
|   |   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.575
|   |   |   |   |   |   |   |   |--- weights: [918.000, 0.000, 53.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.575
|   |   |   |   |   |   |   |   |--- weights: [620.000, 0.000, 200.000] class: 0
|   |   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.500
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det3 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [133.000, 0.000, 55.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det3 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [32.000, 0.000, 70.000] class: 2
|   |   |   |   |   |--- TLS3_Bicycle_Det2 >  0.500
|   |   |   |   |   |   |--- TLS3_Bicycle_Det4 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det2 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [12.000, 0.000, 67.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det2 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [15.000, 0.000, 25.000] class: 2
|   |   |   |   |   |   |--- TLS3_Bicycle_Det4 >  0.500
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.118
|   |   |   |   |   |   |   |   |--- weights: [12.000, 0.000, 13.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.118
|   |   |   |   |   |   |   |   |--- weights: [32.000, 0.000, 9.000] class: 0
|   |   |   |   |--- TLS3_Bicycle_Det3 >  0.500
|   |   |   |   |   |--- TLS6_Bicycle_Det4 <= 0.500
|   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.575
|   |   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.355
|   |   |   |   |   |   |   |   |--- weights: [9.000, 0.000, 42.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Sim_Time >  0.355
|   |   |   |   |   |   |   |   |--- weights: [12.000, 0.000, 11.000] class: 0
|   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.575
|   |   |   |   |   |   |   |--- weights: [1.000, 0.000, 34.000] class: 2
|   |   |   |   |   |--- TLS6_Bicycle_Det4 >  0.500
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.341
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.135
|   |   |   |   |   |   |   |   |--- weights: [6.000, 0.000, 20.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.135
|   |   |   |   |   |   |   |   |--- weights: [18.000, 0.000, 16.000] class: 0
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.341
|   |   |   |   |   |   |   |--- weights: [25.000, 0.000, 5.000] class: 0
|   |   |   |--- TLS6_Vehicle_Det4 >  0.500
|   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.500
|   |   |   |   |   |--- TLS6_Bicycle_Det4 <= 0.500
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.024
|   |   |   |   |   |   |   |--- weights: [4.000, 0.000, 19.000] class: 2
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.024
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det2 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 79.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det2 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [1.000, 0.000, 60.000] class: 2
|   |   |   |   |   |--- TLS6_Bicycle_Det4 >  0.500
|   |   |   |   |   |   |--- TLS6_Vehicle_Det2 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.575
|   |   |   |   |   |   |   |   |--- weights: [10.000, 0.000, 19.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.575
|   |   |   |   |   |   |   |   |--- weights: [1.000, 0.000, 23.000] class: 2
|   |   |   |   |   |   |--- TLS6_Vehicle_Det2 >  0.500
|   |   |   |   |   |   |   |--- weights: [22.000, 0.000, 11.000] class: 0
|   |   |   |   |--- TLS6_Bicycle_Det1 >  0.500
|   |   |   |   |   |--- TLS6_Vehicle_Det3 <= 0.500
|   |   |   |   |   |   |--- TLS3_Vehicle_Det1 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.616
|   |   |   |   |   |   |   |   |--- weights: [69.000, 0.000, 2.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.616
|   |   |   |   |   |   |   |   |--- weights: [15.000, 0.000, 5.000] class: 0
|   |   |   |   |   |   |--- TLS3_Vehicle_Det1 >  0.500
|   |   |   |   |   |   |   |--- weights: [18.000, 0.000, 9.000] class: 0
|   |   |   |   |   |--- TLS6_Vehicle_Det3 >  0.500
|   |   |   |   |   |   |--- TLS3_Vehicle_Det2 <= 0.500
|   |   |   |   |   |   |   |--- weights: [36.000, 0.000, 10.000] class: 0
|   |   |   |   |   |   |--- TLS3_Vehicle_Det2 >  0.500
|   |   |   |   |   |   |   |--- weights: [2.000, 0.000, 21.000] class: 2
|   |   |--- TLS3_Phase_Duration >  0.592
|   |   |   |--- TLS3_Bicycle_Det4 <= 0.500
|   |   |   |   |--- TLS3_Phase_Duration <= 0.608
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.257
|   |   |   |   |   |   |--- TLS6_Vehicle_Det3 <= 0.500
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det2 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [2.000, 0.000, 104.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det2 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [19.000, 0.000, 22.000] class: 2
|   |   |   |   |   |   |--- TLS6_Vehicle_Det3 >  0.500
|   |   |   |   |   |   |   |--- weights: [21.000, 0.000, 20.000] class: 0
|   |   |   |   |   |--- TLS6_Sim_Time >  0.257
|   |   |   |   |   |   |--- TLS3_Vehicle_Det1 <= 0.500
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [129.000, 0.000, 105.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [5.000, 0.000, 16.000] class: 2
|   |   |   |   |   |   |--- TLS3_Vehicle_Det1 >  0.500
|   |   |   |   |   |   |   |--- weights: [6.000, 0.000, 36.000] class: 2
|   |   |   |   |--- TLS3_Phase_Duration >  0.608
|   |   |   |   |   |--- TLS6_Vehicle_Det3 <= 0.500
|   |   |   |   |   |   |--- TLS3_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 106.000] class: 2
|   |   |   |   |   |   |--- TLS3_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.572
|   |   |   |   |   |   |   |   |--- weights: [3.000, 0.000, 36.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.572
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 23.000] class: 2
|   |   |   |   |   |--- TLS6_Vehicle_Det3 >  0.500
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.283
|   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 23.000] class: 2
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.283
|   |   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.550
|   |   |   |   |   |   |   |   |--- weights: [24.000, 0.000, 35.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Sim_Time >  0.550
|   |   |   |   |   |   |   |   |--- weights: [2.000, 0.000, 18.000] class: 2
|   |   |   |--- TLS3_Bicycle_Det4 >  0.500
|   |   |   |   |--- TLS6_Phase_Duration <= 0.608
|   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.500
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.165
|   |   |   |   |   |   |   |--- weights: [23.000, 0.000, 23.000] class: 0
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.165
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [171.000, 0.000, 16.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [14.000, 0.000, 15.000] class: 2
|   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.500
|   |   |   |   |   |   |--- weights: [15.000, 0.000, 25.000] class: 2
|   |   |   |   |--- TLS6_Phase_Duration >  0.608
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.277
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.215
|   |   |   |   |   |   |   |--- weights: [3.000, 0.000, 31.000] class: 2
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.215
|   |   |   |   |   |   |   |--- weights: [5.000, 0.000, 15.000] class: 2
|   |   |   |   |   |--- TLS6_Sim_Time >  0.277
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.625
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det1 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [36.000, 0.000, 41.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det1 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [52.000, 0.000, 14.000] class: 0
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.625
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det2 <= 0.500
|   |   |   |   |   |   |   |   |--- weights: [8.000, 0.000, 45.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det2 >  0.500
|   |   |   |   |   |   |   |   |--- weights: [15.000, 0.000, 18.000] class: 2


[Phase 4/4] Creating visualizations...
💾 Saved tree visualization to: images/2/viper/decision_tree.png

📂 Loading REAL states from testing...
   File: results/test_states_20251115_202404.npz

✅ Real states loaded successfully!
   Total states in file: 300,000
   State shape: (300000, 32)
   Scenarios covered: 30
   Sampled 10,000 states for analysis

   Action distribution (from real policy):
   {'Continue': np.int64(8122), 'Skip2P1': np.int64(216), 'Next': np.int64(1662)}
     Continue: 81.2%
     Skip2P1: 2.2%
     Next: 16.6%
💾 Saved confusion matrix to: images/2/viper/confusion_matrix.png
💾 Saved tree to: images/2/viper/extracted_tree.pkl
✅ VIPER extraction complete!
   Tree accuracy: 89.5%
   Tree depth: 8
   Number of leaves: 173

================================================================================
  ANALYSIS 5/6: Safety Analysis (Section 5)
================================================================================


================================================================================
DATA SOURCES LOADED
================================================================================
✅ Test results:     30 scenarios (from results/drl_test_results_20251115_202404.csv)
✅ Blocking events:  563 records
✅ Q-value data:     300 records
✅ Decision chains:  30 scenarios
================================================================================

[Phase 1/5] Operational safety metrics...

================================================================================
OPERATIONAL SAFETY ANALYSIS
================================================================================

🚨 Safety Violations:
   Total across all scenarios: 0
   ✅ ZERO safety violations across all 30 scenarios!

⏱️  Maximum Waiting Times:
   Car         : Max = 52.08s (Pr_5), Mean = 42.14s
   Bicycle     : Max = 46.95s (Bi_9), Mean = 22.69s
   Pedestrian  : Max =  5.61s (Pr_0), Mean =  2.80s
   Bus         : Max = 14.74s (Pr_6), Mean =  4.77s

🚫 Blocking Events Analysis:
   Total blocking events: 4562
   Scenarios with blocks: 30
   Blocking by action:
      Next      : 4350 blocks
      Skip2P1   : 212 blocks

[Phase 2/5] Edge case identification...

================================================================================
EDGE CASE IDENTIFICATION
================================================================================

✅ Car: No edge cases detected

⚠️  Bicycle Waiting Time Edge Cases (>34.0s):
   Bi_6: 39.98s
   Bi_7: 39.32s
   Bi_8: 46.67s
   Bi_9: 46.95s

⚠️  Pedestrian Waiting Time Edge Cases (>4.2s):
   Pr_0: 5.61s
   Bi_1: 4.73s
   Bi_8: 5.06s
   Pe_6: 4.85s

⚠️  Bus Waiting Time Edge Cases (>7.2s):
   Pr_4: 8.76s
   Pr_5: 12.55s
   Pr_6: 14.74s
   Pr_7: 12.15s
   Pr_8: 11.85s
   Pr_9: 14.66s
   Bi_2: 7.36s

[Phase 3/5] Decision pattern analysis...

================================================================================
DECISION PATTERN ANALYSIS
================================================================================

📊 Performance by Scenario Type:

   Car Priority (Pr) Scenarios:
      Mean car wait:        39.64s
      Mean bicycle wait:    18.42s
      Mean pedestrian wait: 2.54s
      Mean bus wait:        8.30s

   Bicycle Priority (Bi) Scenarios:
      Mean car wait:        43.30s
      Mean bicycle wait:    28.43s
      Mean pedestrian wait: 2.63s
      Mean bus wait:        3.21s

   Pedestrian Priority (Pe) Scenarios:
      Mean car wait:        43.49s
      Mean bicycle wait:    21.23s
      Mean pedestrian wait: 3.25s
      Mean bus wait:        2.81s

🚌 Bus Priority Performance:
   Scenarios with good bus service (<10.0s): 25
   Scenarios with degraded bus service (≥10.0s): 5
   Degraded bus service scenarios:
      Pr_5: 12.55s
      Pr_6: 14.74s
      Pr_7: 12.15s
      Pr_8: 11.85s
      Pr_9: 14.66s

[Phase 4/5] Safe region characterization...

================================================================================
SAFE OPERATING REGION CHARACTERIZATION
================================================================================

📏 Car Waiting Time Distribution:
   50th percentile: 43.95s
   75th percentile: 47.31s
   90th percentile: 50.03s
   95th percentile: 50.64s

📏 Bicycle Waiting Time Distribution:
   50th percentile: 20.99s
   75th percentile: 23.44s
   90th percentile: 39.39s
   95th percentile: 43.66s

📏 Pedestrian Waiting Time Distribution:
   50th percentile: 2.67s
   75th percentile: 3.33s
   90th percentile: 4.74s
   95th percentile: 4.97s

📏 Bus Waiting Time Distribution:
   50th percentile: 2.33s
   75th percentile: 6.72s
   90th percentile: 12.19s
   95th percentile: 13.71s

✅ Recommended Safe Operating Thresholds:
   Car wait:        < 50s (90th percentile)
   Bicycle wait:    < 39s (90th percentile)
   Pedestrian wait: < 5s (90th percentile)
   Bus wait:        < 7s (75th percentile - priority mode)

[Phase 5/5] Generating visualizations and report...

💾 Saved safety summary to: images/2/safety/safety_summary.png
💾 Saved heatmap to: images/2/safety/waiting_time_heatmap.png

💾 Safety report saved to: images/2/safety/safety_report.txt
✅ Safety analysis complete!

================================================================================
  ANALYSIS 6/6: Bicycle Wait Time Spike Analysis
================================================================================


📂 Loading data...
   ✅ States: 300,000 samples (from results/test_states_20251115_202404.npz)
   ✅ Test results: 30 scenarios (from results/drl_test_results_20251115_202404.csv)
   ✅ Q-values: 300 records
   ✅ Blocking events: 563 records

[Phase 1/5] Analyzing action distribution...

================================================================================
ACTION DISTRIBUTION ANALYSIS
================================================================================

Good (Bi_0-5):
   Continue  :  49230 ( 82.0%)
   Skip2P1   :   1454 (  2.4%)
   Next      :   9316 ( 15.5%)

Bad (Bi_6-9):
   Continue  :  32959 ( 82.4%)
   Skip2P1   :    942 (  2.4%)
   Next      :   6099 ( 15.2%)

   💾 Saved: images/2/bicycle_analysis/action_distribution.png

[Phase 2/5] Analyzing phase durations...

================================================================================
PHASE DURATION ANALYSIS
================================================================================

Good (Bi_0-5):
   TLS3 Duration: 9.6s ± 9.8s (max: 39.0s)
   TLS6 Duration: 9.6s ± 9.8s (max: 39.0s)

Bad (Bi_6-9):
   TLS3 Duration: 10.3s ± 10.3s (max: 40.0s)
   TLS6 Duration: 10.3s ± 10.3s (max: 40.0s)

   💾 Saved: images/2/bicycle_analysis/phase_durations.png

[Phase 3/5] Analyzing detector patterns...

================================================================================
BICYCLE DETECTOR ANALYSIS
================================================================================

Good Scenarios:
   TLS3_Bike1: Activation 16.1%, Avg 0.161
   TLS3_Bike2: Activation 13.0%, Avg 0.130
   TLS3_Bike3: Activation 13.2%, Avg 0.132
   TLS3_Bike4: Activation 15.8%, Avg 0.158
   TLS6_Bike1: Activation 16.1%, Avg 0.161
   TLS6_Bike2: Activation 13.0%, Avg 0.130
   TLS6_Bike3: Activation 13.2%, Avg 0.132
   TLS6_Bike4: Activation 15.8%, Avg 0.158

Bad Scenarios:
   TLS3_Bike1: Activation 46.9%, Avg 0.469
   TLS3_Bike2: Activation 36.9%, Avg 0.369
   TLS3_Bike3: Activation 38.6%, Avg 0.386
   TLS3_Bike4: Activation 44.5%, Avg 0.444
   TLS6_Bike1: Activation 46.9%, Avg 0.469
   TLS6_Bike2: Activation 36.9%, Avg 0.369
   TLS6_Bike3: Activation 38.6%, Avg 0.386
   TLS6_Bike4: Activation 44.5%, Avg 0.444

   💾 Saved: images/2/bicycle_analysis/bicycle_detectors.png

[Phase 4/5] Analyzing Q-values...

================================================================================
Q-VALUE ANALYSIS
================================================================================

Good Scenarios:
   Continue Q: -0.358
   Skip2P1 Q:  -0.769
   Next Q:     -0.749
   Q-Gap:      0.614 ± 0.376

Bad Scenarios:
   Continue Q: -0.489
   Skip2P1 Q:  -0.839
   Next Q:     -0.818
   Q-Gap:      0.538 ± 0.274

   💾 Saved: images/2/bicycle_analysis/qvalue_analysis.png

[Phase 5/5] Analyzing blocking events...

================================================================================
BLOCKING EVENTS ANALYSIS
================================================================================

Good Scenarios:
   Total blocks: 642.0
   Blocks per scenario: 107.0
   Blocks by action:
      Next: 590.0
      Skip2P1: 52.0

Bad Scenarios:
   Total blocks: 347.0
   Blocks per scenario: 86.8
   Blocks by action:
      Next: 317.0
      Skip2P1: 30.0

   💾 Saved: images/2/bicycle_analysis/blocking_events.png

[Generating Summary Report...]

================================================================================
GENERATING SUMMARY REPORT
================================================================================
   💾 Saved report: images/2/bicycle_analysis/bicycle_spike_analysis_report.txt
✅ Bicycle spike analysis complete!

================================================================================
  ANALYSIS COMPLETE!
================================================================================

⏱️  Total runtime: 0m 13s

📊 Results saved to:
   - images/2/saliency/
   - images/2/attention/
   - images/2/counterfactuals/
   - images/2/counterfactuals_enhanced/
   - images/2/viper/
   - images/2/safety/
   - images/2/bicycle_analysis/

📝 Key files for Paper 2:
   Section 4.1: images/2/attention/*.png
   Section 4.2: images/2/counterfactuals/*.png, counterfactuals_enhanced/*.png
   Section 4.3: images/2/viper/decision_tree.png, decision_rules.txt
   Section 4.4: images/2/saliency/*.png
   Section 5:   images/2/safety/safety_report.txt, *.png
   Extended:    images/2/bicycle_analysis/bicycle_spike_analysis_report.txt, *.png

================================================================================

==================================================
✅ Analysis completed successfully!
==================================================
