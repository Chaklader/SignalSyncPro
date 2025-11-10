==================================================
DRL Single-Agent Explainability & Safety Analysis
==================================================

Model: models/training_20251103_163015/checkpoint_ep192.pth
Project Root: /Users/chaklader/PycharmProjects/SignalSyncPro

Starting analysis...


================================================================================
  COMPREHENSIVE EXPLAINABILITY & SAFETY ANALYSIS
  Paper 2: Section 4 (Explainability) + Section 5 (Safety)
================================================================================

Model: models/training_20251103_163015/checkpoint_ep192.pth
Estimated runtime: ~20 minutes

Starting analysis...


================================================================================
  ANALYSIS 1/5: Saliency Maps (Section 4.4)
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
💾 Saved visualization to: results/saliency/saliency_000_P1_Active_High_Vehicle_Queue.png

================================================================================
Processing: P2_Active_Bus_Priority (2/5)

================================================================================
SALIENCY ANALYSIS: P2_Active_Bus_Priority
================================================================================

🎯 Continue:
   Top 5 influential features:
   1. TLS6_Sim_Time: -1.4102
   2. TLS6_Phase_Duration: +1.1022
   3. TLS3_Sim_Time: -1.0678
   4. TLS6_Bus_Wait: -0.8965
   5. TLS3_Phase_Duration: +0.8962

🎯 Skip2P1:
   Top 5 influential features:
   1. TLS6_Sim_Time: -1.4102
   2. TLS6_Phase_Duration: +1.1022
   3. TLS3_Sim_Time: -1.0678
   4. TLS6_Bus_Wait: -0.8965
   5. TLS3_Phase_Duration: +0.8962

🎯 Next:
   Top 5 influential features:
   1. TLS6_Sim_Time: -1.4102
   2. TLS6_Phase_Duration: +1.1022
   3. TLS3_Sim_Time: -1.0678
   4. TLS6_Bus_Wait: -0.8965
   5. TLS3_Phase_Duration: +0.8962
💾 Saved visualization to: results/saliency/saliency_001_P2_Active_Bus_Priority.png

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
💾 Saved visualization to: results/saliency/saliency_002_P3_Active_Mixed_Bicycle_Demand.png

================================================================================
Processing: P4_Active_Long_Duration (4/5)

================================================================================
SALIENCY ANALYSIS: P4_Active_Long_Duration
================================================================================

🎯 Continue:
   Top 5 influential features:
   1. TLS3_Phase_P4: +0.5285
   2. TLS3_Sim_Time: -0.5064
   3. TLS6_Sim_Time: -0.4860
   4. TLS6_Phase_P3: -0.3950
   5. TLS3_Phase_Duration: +0.3681

🎯 Skip2P1:
   Top 5 influential features:
   1. TLS3_Phase_P4: +0.5285
   2. TLS3_Sim_Time: -0.5064
   3. TLS6_Sim_Time: -0.4860
   4. TLS6_Phase_P3: -0.3950
   5. TLS3_Phase_Duration: +0.3681

🎯 Next:
   Top 5 influential features:
   1. TLS3_Phase_P4: +0.5285
   2. TLS3_Sim_Time: -0.5064
   3. TLS6_Sim_Time: -0.4860
   4. TLS6_Phase_P3: -0.3950
   5. TLS3_Phase_Duration: +0.3681
💾 Saved visualization to: results/saliency/saliency_003_P4_Active_Long_Duration.png

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
💾 Saved visualization to: results/saliency/saliency_004_P1_Heavy_Congestion_All_Modes.png

✅ Batch analysis complete! Results saved to: results/saliency
✅ Saliency analysis complete!

================================================================================
  ANALYSIS 2/5: Attention Patterns (Section 4.1)
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
💾 Saved visualization to: results/attention/attention_000_P1_High_Vehicle_Queue.png

================================================================================
Processing: P2_Bus_Priority (2/4)

================================================================================
ATTENTION ANALYSIS: P2_Bus_Priority
================================================================================

📊 Q-Values:
   Continue: -1.2909
   Skip2P1: -0.7766
🎯 Next: -0.5932

🔍 Attention Distribution (Selected Action: Next):
   TLS3_Phase_Encoding      : 10.25%
   TLS3_Timing              : 11.49%
   TLS3_Vehicle_Detectors   :  9.14%
   TLS3_Bicycle_Detectors   :  9.42%
   TLS3_Bus_Info            :  6.28%
   TLS6_Phase_Encoding      : 10.79%
   TLS6_Timing              : 17.29%
   TLS6_Vehicle_Detectors   :  8.68%
   TLS6_Bicycle_Detectors   :  8.81%
   TLS6_Bus_Info            :  7.86%
💾 Saved visualization to: results/attention/attention_001_P2_Bus_Priority.png

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
💾 Saved visualization to: results/attention/attention_002_P1_Long_Duration_Mixed_Queue.png

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
💾 Saved visualization to: results/attention/attention_003_P3_High_Bicycle_Demand.png

✅ Batch analysis complete! Results saved to: results/attention
✅ Attention analysis complete!

================================================================================
  ANALYSIS 3/5: Counterfactual Explanations (Section 4.2)
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
💾 Saved visualization to: results/counterfactuals/cf_000_P1_Moderate_Queue_to_Continue.png

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
💾 Saved visualization to: results/counterfactuals/cf_000_P1_Moderate_Queue_to_Next.png

================================================================================
Processing: P2_Bus_Present (2/3)

   Generating: Skip2P1 → Continue
   ✓ Converged at iteration 21

================================================================================
COUNTERFACTUAL EXPLANATION
================================================================================

📊 Original Decision:
   Action: Skip2P1
   Q-values: [-0.46391618 -0.06714318 -0.07344471]

🎯 Target Decision:
   Action: Continue

✨ Counterfactual Decision:
   Action: Continue
   Q-values: [-0.03355091 -0.06452232 -0.28716344]

📏 Changes Required:
   Features changed: 19
   L2 distance: 0.5162
   Optimization iterations: 22

🔍 Feature Changes (|Δ| > 0.01):
   TLS3_Phase_P1            : 0.000 → 0.136 (Δ = +0.136)
   TLS3_Phase_P3            : 0.000 → 0.137 (Δ = +0.137)
   TLS3_Phase_Duration      : 0.300 → 0.162 (Δ = -0.138)
   TLS3_Vehicle_Det3        : 0.000 → 0.126 (Δ = +0.126)
   TLS3_Vehicle_Det4        : 0.000 → 0.098 (Δ = +0.098)
   TLS3_Bicycle_Det2        : 0.000 → 0.052 (Δ = +0.052)
   TLS3_Bicycle_Det3        : 0.000 → 0.079 (Δ = +0.079)
   TLS3_Bus_Wait            : 0.600 → 0.480 (Δ = -0.120)
   TLS3_Sim_Time            : 0.000 → 0.015 (Δ = +0.015)
   TLS6_Phase_P1            : 0.000 → 0.137 (Δ = +0.137)
   TLS6_Phase_P2            : 1.000 → 0.872 (Δ = -0.128)
   TLS6_Phase_P3            : 0.000 → 0.138 (Δ = +0.138)
   TLS6_Vehicle_Det1        : 0.000 → 0.127 (Δ = +0.127)
   TLS6_Vehicle_Det2        : 0.000 → 0.134 (Δ = +0.134)
   TLS6_Vehicle_Det3        : 0.000 → 0.027 (Δ = +0.027)
   TLS6_Vehicle_Det4        : 0.000 → 0.135 (Δ = +0.135)
   TLS6_Bicycle_Det2        : 0.000 → 0.126 (Δ = +0.126)
   TLS6_Bicycle_Det4        : 0.000 → 0.137 (Δ = +0.137)
   TLS6_Sim_Time            : 0.000 → 0.139 (Δ = +0.139)
💾 Saved visualization to: results/counterfactuals/cf_001_P2_Bus_Present_to_Continue.png

   Generating: Skip2P1 → Next
   ✓ Converged at iteration 2

================================================================================
COUNTERFACTUAL EXPLANATION
================================================================================

📊 Original Decision:
   Action: Skip2P1
   Q-values: [-0.46391618 -0.06714318 -0.07344471]

🎯 Target Decision:
   Action: Next

✨ Counterfactual Decision:
   Action: Next
   Q-values: [-0.60985863 -0.15774071 -0.09732461]

📏 Changes Required:
   Features changed: 20
   L2 distance: 0.0733
   Optimization iterations: 3

🔍 Feature Changes (|Δ| > 0.01):
   TLS3_Phase_P2            : 1.000 → 0.983 (Δ = -0.017)
   TLS3_Phase_P4            : 0.000 → 0.017 (Δ = +0.017)
   TLS3_Phase_Duration      : 0.300 → 0.317 (Δ = +0.017)
   TLS3_Vehicle_Det1        : 0.000 → 0.016 (Δ = +0.016)
   TLS3_Vehicle_Det4        : 0.000 → 0.016 (Δ = +0.016)
   TLS3_Bicycle_Det1        : 0.000 → 0.016 (Δ = +0.016)
   TLS3_Bicycle_Det2        : 0.000 → 0.017 (Δ = +0.017)
   TLS3_Bicycle_Det3        : 0.000 → 0.017 (Δ = +0.017)
   TLS3_Bicycle_Det4        : 0.000 → 0.017 (Δ = +0.017)
   TLS3_Bus_Present         : 1.000 → 0.984 (Δ = -0.016)
   TLS3_Bus_Wait            : 0.600 → 0.617 (Δ = +0.017)
   TLS3_Sim_Time            : 0.000 → 0.017 (Δ = +0.017)
   TLS6_Phase_P4            : 0.000 → 0.017 (Δ = +0.017)
   TLS6_Phase_Duration      : 0.000 → 0.017 (Δ = +0.017)
   TLS6_Vehicle_Det2        : 0.000 → 0.016 (Δ = +0.016)
   TLS6_Vehicle_Det3        : 0.000 → 0.016 (Δ = +0.016)
   TLS6_Vehicle_Det4        : 0.000 → 0.017 (Δ = +0.017)
   TLS6_Bicycle_Det3        : 0.000 → 0.015 (Δ = +0.015)
   TLS6_Bus_Wait            : 0.000 → 0.017 (Δ = +0.017)
   TLS6_Sim_Time            : 0.000 → 0.017 (Δ = +0.017)
💾 Saved visualization to: results/counterfactuals/cf_001_P2_Bus_Present_to_Next.png

================================================================================
Processing: P1_Long_Duration (3/3)

   Generating: Continue → Skip2P1
   ✓ Converged at iteration 9

================================================================================
COUNTERFACTUAL EXPLANATION
================================================================================

📊 Original Decision:
   Action: Continue
   Q-values: [0.746863   0.54130954 0.20565295]

🎯 Target Decision:
   Action: Skip2P1

✨ Counterfactual Decision:
   Action: Skip2P1
   Q-values: [0.55451536 0.62224996 0.39900124]

📏 Changes Required:
   Features changed: 17
   L2 distance: 0.2318
   Optimization iterations: 10

🔍 Feature Changes (|Δ| > 0.01):
   TLS3_Phase_P1            : 1.000 → 0.941 (Δ = -0.059)
   TLS3_Phase_P2            : 0.000 → 0.058 (Δ = +0.058)
   TLS3_Phase_P4            : 0.000 → 0.059 (Δ = +0.059)
   TLS3_Phase_Duration      : 0.850 → 0.909 (Δ = +0.059)
   TLS3_Vehicle_Det1        : 0.000 → 0.027 (Δ = +0.027)
   TLS3_Vehicle_Det2        : 1.000 → 0.943 (Δ = -0.057)
   TLS3_Vehicle_Det3        : 1.000 → 0.942 (Δ = -0.058)
   TLS3_Bicycle_Det1        : 0.000 → 0.058 (Δ = +0.058)
   TLS3_Bicycle_Det3        : 0.000 → 0.054 (Δ = +0.054)
   TLS6_Phase_P1            : 1.000 → 0.941 (Δ = -0.059)
   TLS6_Phase_P2            : 0.000 → 0.058 (Δ = +0.058)
   TLS6_Phase_P4            : 0.000 → 0.059 (Δ = +0.059)
   TLS6_Phase_Duration      : 0.000 → 0.059 (Δ = +0.059)
   TLS6_Vehicle_Det1        : 1.000 → 0.942 (Δ = -0.058)
   TLS6_Bicycle_Det2        : 0.000 → 0.057 (Δ = +0.057)
   TLS6_Bicycle_Det3        : 0.000 → 0.054 (Δ = +0.054)
   TLS6_Bus_Present         : 0.000 → 0.057 (Δ = +0.057)
💾 Saved visualization to: results/counterfactuals/cf_002_P1_Long_Duration_to_Skip2P1.png

   Generating: Continue → Next
   ✓ Converged at iteration 17
❌ Failed to generate counterfactual

✅ Batch generation complete! Results saved to: results/counterfactuals
✅ Counterfactual generation complete!

================================================================================
  ANALYSIS 4/5: Decision Tree Extraction (Section 4.3)
================================================================================

Note: This analysis takes ~10 minutes
Using device: cpu
Model loaded from models/training_20251103_163015/checkpoint_ep192.pth
✅ Loaded DQN model from: models/training_20251103_163015/checkpoint_ep192.pth

[Phase 1/4] Collecting initial dataset...

🎲 Collecting 10000 samples from DQN policy...
   Collected 2000/10000 samples...
   Collected 4000/10000 samples...
   Collected 6000/10000 samples...
   Collected 8000/10000 samples...
   Collected 10000/10000 samples...

✅ Dataset collected!
   Action distribution: {'Continue': 1479, 'Skip2P1': 397, 'Next': 8124}

[Phase 2/4] Running VIPER iterations...

================================================================================
VIPER Iteration 1/3
================================================================================

🌳 Training decision tree...
   Max depth: 10
   Min samples split: 50
   Min samples leaf: 20

✅ Tree trained!
   Train accuracy: 93.55%
   Test accuracy: 91.75%
   Tree depth: 10
   Number of leaves: 87

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.84      0.85      0.84       303
     Skip2P1       0.51      0.35      0.41        86
        Next       0.95      0.96      0.95      1611

    accuracy                           0.92      2000
   macro avg       0.76      0.72      0.74      2000
weighted avg       0.91      0.92      0.91      2000


🎲 Generating 2000 new samples using tree policy...
   Dataset size now: 12000

================================================================================
VIPER Iteration 2/3
================================================================================

🌳 Training decision tree...
   Max depth: 10
   Min samples split: 50
   Min samples leaf: 20

✅ Tree trained!
   Train accuracy: 93.53%
   Test accuracy: 91.50%
   Tree depth: 9
   Number of leaves: 97

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.84      0.84      0.84       363
     Skip2P1       0.47      0.27      0.34       100
        Next       0.94      0.96      0.95      1937

    accuracy                           0.92      2400
   macro avg       0.75      0.69      0.71      2400
weighted avg       0.91      0.92      0.91      2400


🎲 Generating 2000 new samples using tree policy...
   Dataset size now: 14000

================================================================================
VIPER Iteration 3/3
================================================================================

🌳 Training decision tree...
   Max depth: 10
   Min samples split: 50
   Min samples leaf: 20

✅ Tree trained!
   Train accuracy: 93.80%
   Test accuracy: 91.79%
   Tree depth: 10
   Number of leaves: 109

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.85      0.84      0.85       406
     Skip2P1       0.44      0.23      0.30       116
        Next       0.94      0.97      0.95      2278

    accuracy                           0.92      2800
   macro avg       0.74      0.68      0.70      2800
weighted avg       0.91      0.92      0.91      2800


🎲 Generating 2000 new samples using tree policy...
   Dataset size now: 16000

================================================================================
Final Tree Training
================================================================================

🌳 Training decision tree...
   Max depth: 8
   Min samples split: 50
   Min samples leaf: 20

✅ Tree trained!
   Train accuracy: 93.81%
   Test accuracy: 91.00%
   Tree depth: 8
   Number of leaves: 105

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.83      0.86      0.84       502
     Skip2P1       0.39      0.20      0.27       132
        Next       0.94      0.96      0.95      2566

    accuracy                           0.91      3200
   macro avg       0.72      0.67      0.69      3200
weighted avg       0.90      0.91      0.90      3200


[Phase 3/4] Extracting decision rules...

================================================================================
EXTRACTED DECISION RULES (Accuracy: 91.0%)
================================================================================

|--- TLS6_Phase_P1 <= 0.500
|   |--- TLS3_Phase_P3 <= 0.500
|   |   |--- weights: [0.000, 0.000, 6378.000] class: 2
|   |--- TLS3_Phase_P3 >  0.500
|   |   |--- TLS6_Phase_Duration <= 0.289
|   |   |   |--- TLS3_Phase_Duration <= 0.389
|   |   |   |   |--- TLS3_Bus_Wait <= 0.766
|   |   |   |   |   |--- TLS6_Bus_Wait <= 0.602
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.233
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det3 <= 0.756
|   |   |   |   |   |   |   |   |--- weights: [76.000, 1.000, 3.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det3 >  0.756
|   |   |   |   |   |   |   |   |--- weights: [15.000, 1.000, 4.000] class: 0
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.233
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det3 <= 0.483
|   |   |   |   |   |   |   |   |--- weights: [12.000, 9.000, 10.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det3 >  0.483
|   |   |   |   |   |   |   |   |--- weights: [29.000, 1.000, 2.000] class: 0
|   |   |   |   |   |--- TLS6_Bus_Wait >  0.602
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.117
|   |   |   |   |   |   |   |--- weights: [30.000, 0.000, 6.000] class: 0
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.117
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.397
|   |   |   |   |   |   |   |   |--- weights: [23.000, 4.000, 17.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.397
|   |   |   |   |   |   |   |   |--- weights: [6.000, 1.000, 36.000] class: 2
|   |   |   |   |--- TLS3_Bus_Wait >  0.766
|   |   |   |   |   |--- TLS6_Bus_Wait <= 0.239
|   |   |   |   |   |   |--- weights: [21.000, 0.000, 7.000] class: 0
|   |   |   |   |   |--- TLS6_Bus_Wait >  0.239
|   |   |   |   |   |   |--- TLS6_Bus_Present <= 0.591
|   |   |   |   |   |   |   |--- weights: [2.000, 1.000, 43.000] class: 2
|   |   |   |   |   |   |--- TLS6_Bus_Present >  0.591
|   |   |   |   |   |   |   |--- weights: [10.000, 2.000, 23.000] class: 2
|   |   |   |--- TLS3_Phase_Duration >  0.389
|   |   |   |   |--- TLS6_Bus_Wait <= 0.325
|   |   |   |   |   |--- TLS3_Phase_Duration <= 0.567
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.418
|   |   |   |   |   |   |   |--- weights: [5.000, 22.000, 5.000] class: 1
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.418
|   |   |   |   |   |   |   |--- weights: [14.000, 5.000, 14.000] class: 0
|   |   |   |   |   |--- TLS3_Phase_Duration >  0.567
|   |   |   |   |   |   |--- TLS6_Bus_Present <= 0.825
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.310
|   |   |   |   |   |   |   |   |--- weights: [0.000, 10.000, 18.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.310
|   |   |   |   |   |   |   |   |--- weights: [1.000, 2.000, 55.000] class: 2
|   |   |   |   |   |   |--- TLS6_Bus_Present >  0.825
|   |   |   |   |   |   |   |--- weights: [2.000, 16.000, 5.000] class: 1
|   |   |   |   |--- TLS6_Bus_Wait >  0.325
|   |   |   |   |   |--- TLS3_Bus_Wait <= 0.388
|   |   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.175
|   |   |   |   |   |   |   |--- weights: [5.000, 11.000, 7.000] class: 1
|   |   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.175
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det3 <= 0.174
|   |   |   |   |   |   |   |   |--- weights: [1.000, 9.000, 13.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det3 >  0.174
|   |   |   |   |   |   |   |   |--- weights: [5.000, 6.000, 82.000] class: 2
|   |   |   |   |   |--- TLS3_Bus_Wait >  0.388
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.161
|   |   |   |   |   |   |   |--- weights: [1.000, 7.000, 25.000] class: 2
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.161
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.110
|   |   |   |   |   |   |   |   |--- weights: [1.000, 3.000, 18.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.110
|   |   |   |   |   |   |   |   |--- weights: [1.000, 4.000, 185.000] class: 2
|   |   |--- TLS6_Phase_Duration >  0.289
|   |   |   |--- TLS3_Phase_Duration <= 0.399
|   |   |   |   |--- TLS3_Sim_Time <= 0.318
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.624
|   |   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.204
|   |   |   |   |   |   |   |--- weights: [3.000, 31.000, 8.000] class: 1
|   |   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.204
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.771
|   |   |   |   |   |   |   |   |--- weights: [5.000, 40.000, 39.000] class: 1
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.771
|   |   |   |   |   |   |   |   |--- weights: [0.000, 5.000, 38.000] class: 2
|   |   |   |   |   |--- TLS6_Sim_Time >  0.624
|   |   |   |   |   |   |--- TLS3_Bicycle_Det3 <= 0.287
|   |   |   |   |   |   |   |--- weights: [2.000, 9.000, 13.000] class: 2
|   |   |   |   |   |   |--- TLS3_Bicycle_Det3 >  0.287
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det3 <= 0.587
|   |   |   |   |   |   |   |   |--- weights: [1.000, 0.000, 46.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det3 >  0.587
|   |   |   |   |   |   |   |   |--- weights: [4.000, 3.000, 15.000] class: 2
|   |   |   |   |--- TLS3_Sim_Time >  0.318
|   |   |   |   |   |--- TLS3_Bus_Wait <= 0.298
|   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.452
|   |   |   |   |   |   |   |--- weights: [18.000, 7.000, 9.000] class: 0
|   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.452
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.252
|   |   |   |   |   |   |   |   |--- weights: [3.000, 18.000, 19.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.252
|   |   |   |   |   |   |   |   |--- weights: [7.000, 9.000, 97.000] class: 2
|   |   |   |   |   |--- TLS3_Bus_Wait >  0.298
|   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.386
|   |   |   |   |   |   |   |--- weights: [7.000, 5.000, 34.000] class: 2
|   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.386
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det1 <= 0.138
|   |   |   |   |   |   |   |   |--- weights: [3.000, 7.000, 34.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det1 >  0.138
|   |   |   |   |   |   |   |   |--- weights: [0.000, 12.000, 303.000] class: 2
|   |   |   |--- TLS3_Phase_Duration >  0.399
|   |   |   |   |--- TLS6_Phase_Duration <= 0.508
|   |   |   |   |   |--- TLS3_Phase_Duration <= 0.611
|   |   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.138
|   |   |   |   |   |   |   |--- weights: [0.000, 14.000, 8.000] class: 1
|   |   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.138
|   |   |   |   |   |   |   |--- TLS3_Bus_Present <= 0.695
|   |   |   |   |   |   |   |   |--- weights: [0.000, 4.000, 83.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Bus_Present >  0.695
|   |   |   |   |   |   |   |   |--- weights: [0.000, 13.000, 22.000] class: 2
|   |   |   |   |   |--- TLS3_Phase_Duration >  0.611
|   |   |   |   |   |   |--- TLS6_Bus_Present <= 0.911
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.860
|   |   |   |   |   |   |   |   |--- weights: [0.000, 2.000, 241.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.860
|   |   |   |   |   |   |   |   |--- weights: [0.000, 3.000, 26.000] class: 2
|   |   |   |   |   |   |--- TLS6_Bus_Present >  0.911
|   |   |   |   |   |   |   |--- weights: [0.000, 5.000, 29.000] class: 2
|   |   |   |   |--- TLS6_Phase_Duration >  0.508
|   |   |   |   |   |--- TLS6_Bus_Present <= 0.981
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.110
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.741
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 61.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.741
|   |   |   |   |   |   |   |   |--- weights: [0.000, 4.000, 21.000] class: 2
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.110
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det3 <= 0.073
|   |   |   |   |   |   |   |   |--- weights: [0.000, 2.000, 66.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det3 >  0.073
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 777.000] class: 2
|   |   |   |   |   |--- TLS6_Bus_Present >  0.981
|   |   |   |   |   |   |--- weights: [0.000, 3.000, 17.000] class: 2
|--- TLS6_Phase_P1 >  0.500
|   |--- TLS6_Phase_Duration <= 0.426
|   |   |--- TLS3_Phase_Duration <= 0.681
|   |   |   |--- TLS3_Phase_Duration <= 0.614
|   |   |   |   |--- TLS3_Sim_Time <= 0.948
|   |   |   |   |   |--- TLS3_Phase_Duration <= 0.476
|   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.411
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.902
|   |   |   |   |   |   |   |   |--- weights: [544.000, 0.000, 0.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.902
|   |   |   |   |   |   |   |   |--- weights: [59.000, 0.000, 2.000] class: 0
|   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.411
|   |   |   |   |   |   |   |--- weights: [18.000, 1.000, 1.000] class: 0
|   |   |   |   |   |--- TLS3_Phase_Duration >  0.476
|   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.801
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.723
|   |   |   |   |   |   |   |   |--- weights: [122.000, 1.000, 0.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.723
|   |   |   |   |   |   |   |   |--- weights: [35.000, 0.000, 4.000] class: 0
|   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.801
|   |   |   |   |   |   |   |--- weights: [29.000, 0.000, 8.000] class: 0
|   |   |   |   |--- TLS3_Sim_Time >  0.948
|   |   |   |   |   |--- weights: [34.000, 0.000, 9.000] class: 0
|   |   |   |--- TLS3_Phase_Duration >  0.614
|   |   |   |   |--- TLS6_Phase_Duration <= 0.320
|   |   |   |   |   |--- TLS3_Sim_Time <= 0.651
|   |   |   |   |   |   |--- TLS3_Bicycle_Det4 <= 0.484
|   |   |   |   |   |   |   |--- weights: [19.000, 1.000, 0.000] class: 0
|   |   |   |   |   |   |--- TLS3_Bicycle_Det4 >  0.484
|   |   |   |   |   |   |   |--- weights: [30.000, 0.000, 0.000] class: 0
|   |   |   |   |   |--- TLS3_Sim_Time >  0.651
|   |   |   |   |   |   |--- weights: [17.000, 0.000, 6.000] class: 0
|   |   |   |   |--- TLS6_Phase_Duration >  0.320
|   |   |   |   |   |--- weights: [7.000, 2.000, 11.000] class: 2
|   |   |--- TLS3_Phase_Duration >  0.681
|   |   |   |--- TLS6_Phase_Duration <= 0.208
|   |   |   |   |--- TLS6_Bus_Wait <= 0.697
|   |   |   |   |   |--- TLS3_Phase_Duration <= 0.904
|   |   |   |   |   |   |--- TLS6_Bicycle_Det2 <= 0.400
|   |   |   |   |   |   |   |--- weights: [27.000, 0.000, 7.000] class: 0
|   |   |   |   |   |   |--- TLS6_Bicycle_Det2 >  0.400
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.394
|   |   |   |   |   |   |   |   |--- weights: [19.000, 0.000, 1.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.394
|   |   |   |   |   |   |   |   |--- weights: [46.000, 0.000, 0.000] class: 0
|   |   |   |   |   |--- TLS3_Phase_Duration >  0.904
|   |   |   |   |   |   |--- weights: [26.000, 6.000, 15.000] class: 0
|   |   |   |   |--- TLS6_Bus_Wait >  0.697
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.363
|   |   |   |   |   |   |--- weights: [12.000, 7.000, 3.000] class: 0
|   |   |   |   |   |--- TLS6_Sim_Time >  0.363
|   |   |   |   |   |   |--- weights: [7.000, 0.000, 27.000] class: 2
|   |   |   |--- TLS6_Phase_Duration >  0.208
|   |   |   |   |--- TLS6_Sim_Time <= 0.501
|   |   |   |   |   |--- TLS3_Sim_Time <= 0.395
|   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.518
|   |   |   |   |   |   |   |--- weights: [4.000, 23.000, 1.000] class: 1
|   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.518
|   |   |   |   |   |   |   |--- weights: [3.000, 10.000, 14.000] class: 2
|   |   |   |   |   |--- TLS3_Sim_Time >  0.395
|   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.441
|   |   |   |   |   |   |   |--- weights: [12.000, 3.000, 13.000] class: 2
|   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.441
|   |   |   |   |   |   |   |--- weights: [2.000, 1.000, 24.000] class: 2
|   |   |   |   |--- TLS6_Sim_Time >  0.501
|   |   |   |   |   |--- TLS6_Bus_Wait <= 0.406
|   |   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.516
|   |   |   |   |   |   |   |--- weights: [17.000, 0.000, 12.000] class: 0
|   |   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.516
|   |   |   |   |   |   |   |--- weights: [5.000, 0.000, 24.000] class: 2
|   |   |   |   |   |--- TLS6_Bus_Wait >  0.406
|   |   |   |   |   |   |--- TLS3_Bicycle_Det3 <= 0.251
|   |   |   |   |   |   |   |--- weights: [6.000, 0.000, 14.000] class: 2
|   |   |   |   |   |   |--- TLS3_Bicycle_Det3 >  0.251
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.661
|   |   |   |   |   |   |   |   |--- weights: [1.000, 0.000, 19.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.661
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 30.000] class: 2
|   |--- TLS6_Phase_Duration >  0.426
|   |   |--- TLS3_Phase_Duration <= 0.428
|   |   |   |--- TLS6_Phase_Duration <= 0.795
|   |   |   |   |--- TLS6_Phase_Duration <= 0.682
|   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.646
|   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.896
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.897
|   |   |   |   |   |   |   |   |--- weights: [198.000, 1.000, 2.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.897
|   |   |   |   |   |   |   |   |--- weights: [18.000, 0.000, 3.000] class: 0
|   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.896
|   |   |   |   |   |   |   |--- weights: [16.000, 0.000, 4.000] class: 0
|   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.646
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.235
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det4 <= 0.408
|   |   |   |   |   |   |   |   |--- weights: [19.000, 0.000, 5.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det4 >  0.408
|   |   |   |   |   |   |   |   |--- weights: [37.000, 0.000, 0.000] class: 0
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.235
|   |   |   |   |   |   |   |--- weights: [23.000, 3.000, 18.000] class: 0
|   |   |   |   |--- TLS6_Phase_Duration >  0.682
|   |   |   |   |   |--- TLS3_Phase_Duration <= 0.291
|   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.813
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.698
|   |   |   |   |   |   |   |   |--- weights: [49.000, 3.000, 1.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.698
|   |   |   |   |   |   |   |   |--- weights: [16.000, 0.000, 8.000] class: 0
|   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.813
|   |   |   |   |   |   |   |--- weights: [8.000, 2.000, 12.000] class: 2
|   |   |   |   |   |--- TLS3_Phase_Duration >  0.291
|   |   |   |   |   |   |--- weights: [7.000, 11.000, 23.000] class: 2
|   |   |   |--- TLS6_Phase_Duration >  0.795
|   |   |   |   |--- TLS3_Phase_Duration <= 0.212
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.265
|   |   |   |   |   |   |--- weights: [5.000, 17.000, 21.000] class: 2
|   |   |   |   |   |--- TLS6_Sim_Time >  0.265
|   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.884
|   |   |   |   |   |   |   |--- weights: [27.000, 1.000, 7.000] class: 0
|   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.884
|   |   |   |   |   |   |   |--- weights: [14.000, 1.000, 30.000] class: 2
|   |   |   |   |--- TLS3_Phase_Duration >  0.212
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.321
|   |   |   |   |   |   |--- weights: [1.000, 17.000, 30.000] class: 2
|   |   |   |   |   |--- TLS6_Sim_Time >  0.321
|   |   |   |   |   |   |--- TLS3_Bicycle_Det1 <= 0.683
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.324
|   |   |   |   |   |   |   |   |--- weights: [1.000, 0.000, 19.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.324
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 51.000] class: 2
|   |   |   |   |   |   |--- TLS3_Bicycle_Det1 >  0.683
|   |   |   |   |   |   |   |--- weights: [2.000, 4.000, 18.000] class: 2
|   |   |--- TLS3_Phase_Duration >  0.428
|   |   |   |--- TLS6_Phase_Duration <= 0.679
|   |   |   |   |--- TLS3_Phase_Duration <= 0.686
|   |   |   |   |   |--- TLS3_Sim_Time <= 0.374
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.364
|   |   |   |   |   |   |   |--- weights: [3.000, 23.000, 3.000] class: 1
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.364
|   |   |   |   |   |   |   |--- weights: [16.000, 5.000, 25.000] class: 2
|   |   |   |   |   |--- TLS3_Sim_Time >  0.374
|   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.330
|   |   |   |   |   |   |   |--- weights: [18.000, 3.000, 20.000] class: 2
|   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.330
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.363
|   |   |   |   |   |   |   |   |--- weights: [7.000, 3.000, 23.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.363
|   |   |   |   |   |   |   |   |--- weights: [1.000, 0.000, 55.000] class: 2
|   |   |   |   |--- TLS3_Phase_Duration >  0.686
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.333
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.292
|   |   |   |   |   |   |   |--- weights: [0.000, 15.000, 8.000] class: 1
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.292
|   |   |   |   |   |   |   |--- TLS3_Bus_Present <= 0.674
|   |   |   |   |   |   |   |   |--- weights: [1.000, 0.000, 34.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Bus_Present >  0.674
|   |   |   |   |   |   |   |   |--- weights: [0.000, 7.000, 16.000] class: 2
|   |   |   |   |   |--- TLS6_Sim_Time >  0.333
|   |   |   |   |   |   |--- TLS6_Bicycle_Det4 <= 0.825
|   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 152.000] class: 2
|   |   |   |   |   |   |--- TLS6_Bicycle_Det4 >  0.825
|   |   |   |   |   |   |   |--- weights: [1.000, 4.000, 33.000] class: 2
|   |   |   |--- TLS6_Phase_Duration >  0.679
|   |   |   |   |--- TLS3_Phase_Duration <= 0.539
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.227
|   |   |   |   |   |   |--- weights: [0.000, 9.000, 14.000] class: 2
|   |   |   |   |   |--- TLS6_Sim_Time >  0.227
|   |   |   |   |   |   |--- TLS6_Vehicle_Det2 <= 0.296
|   |   |   |   |   |   |   |--- weights: [0.000, 5.000, 15.000] class: 2
|   |   |   |   |   |   |--- TLS6_Vehicle_Det2 >  0.296
|   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 60.000] class: 2
|   |   |   |   |--- TLS3_Phase_Duration >  0.539
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.045
|   |   |   |   |   |   |--- weights: [0.000, 3.000, 17.000] class: 2
|   |   |   |   |   |--- TLS6_Sim_Time >  0.045
|   |   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.183
|   |   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.294
|   |   |   |   |   |   |   |   |--- weights: [0.000, 4.000, 19.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Sim_Time >  0.294
|   |   |   |   |   |   |   |   |--- weights: [1.000, 0.000, 55.000] class: 2
|   |   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.183
|   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 382.000] class: 2


[Phase 4/4] Creating visualizations...
💾 Saved tree visualization to: results/viper/decision_tree.png

🎲 Collecting 1000 samples from DQN policy...

✅ Dataset collected!
   Action distribution: {'Continue': 150, 'Skip2P1': 39, 'Next': 811}
💾 Saved confusion matrix to: results/viper/confusion_matrix.png
💾 Saved tree to: results/viper/extracted_tree.pkl
✅ VIPER extraction complete!
   Tree accuracy: 91.0%
   Tree depth: 8
   Number of leaves: 105

================================================================================
  ANALYSIS 5/5: Safety Analysis (Section 5)
================================================================================

✅ Loaded test results for 23 scenarios
✅ Loaded 25 blocking event records
[Phase 1/5] Operational safety metrics...

================================================================================
OPERATIONAL SAFETY ANALYSIS
================================================================================

🚨 Safety Violations:
   Total across all scenarios: 0
   ✅ ZERO safety violations across all 30 scenarios!

⏱️  Maximum Waiting Times:
   Car         : Max = 51.07s (Pr_4), Mean = 41.88s
   Bicycle     : Max = 45.33s (Bi_8), Mean = 22.90s
   Pedestrian  : Max =  5.72s (Pr_2), Mean =  2.87s
   Bus         : Max = 14.54s (Pr_8), Mean =  5.01s

🚫 Blocking Events Analysis:
   Total blocking events: 65
   Scenarios with blocks: 3
   Blocking by action:
      Next      : 45 blocks
      Skip2P1   : 20 blocks

[Phase 2/5] Edge case identification...

================================================================================
EDGE CASE IDENTIFICATION
================================================================================

✅ Car: No edge cases detected

⚠️  Bicycle Waiting Time Edge Cases (>34.4s):
   Bi_6: 43.05s
   Bi_7: 39.49s
   Bi_8: 45.33s
   Bi_9: 42.40s

⚠️  Pedestrian Waiting Time Edge Cases (>4.3s):
   Pr_0: 4.79s
   Pr_2: 5.72s
   Pr_5: 4.86s
   Bi_3: 5.21s
   Bi_6: 5.21s

⚠️  Bus Waiting Time Edge Cases (>7.5s):
   Pr_4: 12.08s
   Pr_5: 10.30s
   Pr_6: 12.79s
   Pr_7: 10.87s
   Pr_8: 14.54s
   Pr_9: 13.47s

[Phase 3/5] Decision pattern analysis...

================================================================================
DECISION PATTERN ANALYSIS
================================================================================

📊 Performance by Scenario Type:

   Car Priority (Pr) Scenarios:
      Mean car wait:        40.18s
      Mean bicycle wait:    18.20s
      Mean pedestrian wait: 3.02s
      Mean bus wait:        8.20s

   Bicycle Priority (Bi) Scenarios:
      Mean car wait:        44.37s
      Mean bicycle wait:    28.69s
      Mean pedestrian wait: 3.01s
      Mean bus wait:        2.45s

   Pedestrian Priority (Pe) Scenarios:
      Mean car wait:        39.26s
      Mean bicycle wait:    19.29s
      Mean pedestrian wait: 1.91s
      Mean bus wait:        2.92s

🚌 Bus Priority Performance:
   Scenarios with good bus service (<10.0s): 17
   Scenarios with degraded bus service (≥10.0s): 6
   Degraded bus service scenarios:
      Pr_4: 12.08s
      Pr_5: 10.30s
      Pr_6: 12.79s
      Pr_7: 10.87s
      Pr_8: 14.54s
      Pr_9: 13.47s

[Phase 4/5] Safe region characterization...

================================================================================
SAFE OPERATING REGION CHARACTERIZATION
================================================================================

📏 Car Waiting Time Distribution:
   50th percentile: 44.81s
   75th percentile: 46.22s
   90th percentile: 49.38s
   95th percentile: 50.69s

📏 Bicycle Waiting Time Distribution:
   50th percentile: 20.34s
   75th percentile: 27.00s
   90th percentile: 41.82s
   95th percentile: 42.98s

📏 Pedestrian Waiting Time Distribution:
   50th percentile: 2.29s
   75th percentile: 3.52s
   90th percentile: 5.14s
   95th percentile: 5.21s

📏 Bus Waiting Time Distribution:
   50th percentile: 2.67s
   75th percentile: 7.09s
   90th percentile: 12.65s
   95th percentile: 13.40s

✅ Recommended Safe Operating Thresholds:
   Car wait:        < 49s (90th percentile)
   Bicycle wait:    < 42s (90th percentile)
   Pedestrian wait: < 5s (90th percentile)
   Bus wait:        < 7s (75th percentile - priority mode)

[Phase 5/5] Generating visualizations and report...

💾 Saved safety summary to: results/safety/safety_summary.png
💾 Saved heatmap to: results/safety/waiting_time_heatmap.png

================================================================================
OPERATIONAL SAFETY ANALYSIS
================================================================================

🚨 Safety Violations:
   Total across all scenarios: 0
   ✅ ZERO safety violations across all 30 scenarios!

⏱️  Maximum Waiting Times:
   Car         : Max = 51.07s (Pr_4), Mean = 41.88s
   Bicycle     : Max = 45.33s (Bi_8), Mean = 22.90s
   Pedestrian  : Max =  5.72s (Pr_2), Mean =  2.87s
   Bus         : Max = 14.54s (Pr_8), Mean =  5.01s

🚫 Blocking Events Analysis:
   Total blocking events: 65
   Scenarios with blocks: 3
   Blocking by action:
      Next      : 45 blocks
      Skip2P1   : 20 blocks

================================================================================
EDGE CASE IDENTIFICATION
================================================================================

✅ Car: No edge cases detected

⚠️  Bicycle Waiting Time Edge Cases (>34.4s):
   Bi_6: 43.05s
   Bi_7: 39.49s
   Bi_8: 45.33s
   Bi_9: 42.40s

⚠️  Pedestrian Waiting Time Edge Cases (>4.3s):
   Pr_0: 4.79s
   Pr_2: 5.72s
   Pr_5: 4.86s
   Bi_3: 5.21s
   Bi_6: 5.21s

⚠️  Bus Waiting Time Edge Cases (>7.5s):
   Pr_4: 12.08s
   Pr_5: 10.30s
   Pr_6: 12.79s
   Pr_7: 10.87s
   Pr_8: 14.54s
   Pr_9: 13.47s

================================================================================
DECISION PATTERN ANALYSIS
================================================================================

📊 Performance by Scenario Type:

   Car Priority (Pr) Scenarios:
      Mean car wait:        40.18s
      Mean bicycle wait:    18.20s
      Mean pedestrian wait: 3.02s
      Mean bus wait:        8.20s

   Bicycle Priority (Bi) Scenarios:
      Mean car wait:        44.37s
      Mean bicycle wait:    28.69s
      Mean pedestrian wait: 3.01s
      Mean bus wait:        2.45s

   Pedestrian Priority (Pe) Scenarios:
      Mean car wait:        39.26s
      Mean bicycle wait:    19.29s
      Mean pedestrian wait: 1.91s
      Mean bus wait:        2.92s

🚌 Bus Priority Performance:
   Scenarios with good bus service (<10.0s): 17
   Scenarios with degraded bus service (≥10.0s): 6
   Degraded bus service scenarios:
      Pr_4: 12.08s
      Pr_5: 10.30s
      Pr_6: 12.79s
      Pr_7: 10.87s
      Pr_8: 14.54s
      Pr_9: 13.47s

================================================================================
SAFE OPERATING REGION CHARACTERIZATION
================================================================================

📏 Car Waiting Time Distribution:
   50th percentile: 44.81s
   75th percentile: 46.22s
   90th percentile: 49.38s
   95th percentile: 50.69s

📏 Bicycle Waiting Time Distribution:
   50th percentile: 20.34s
   75th percentile: 27.00s
   90th percentile: 41.82s
   95th percentile: 42.98s

📏 Pedestrian Waiting Time Distribution:
   50th percentile: 2.29s
   75th percentile: 3.52s
   90th percentile: 5.14s
   95th percentile: 5.21s

📏 Bus Waiting Time Distribution:
   50th percentile: 2.67s
   75th percentile: 7.09s
   90th percentile: 12.65s
   95th percentile: 13.40s

✅ Recommended Safe Operating Thresholds:
   Car wait:        < 49s (90th percentile)
   Bicycle wait:    < 42s (90th percentile)
   Pedestrian wait: < 5s (90th percentile)
   Bus wait:        < 7s (75th percentile - priority mode)

💾 Safety report saved to: results/safety/safety_report.txt
✅ Safety analysis complete!

================================================================================
  ANALYSIS COMPLETE!
================================================================================

⏱️  Total runtime: 0m 15s

📊 Results saved to:
   - results/saliency/
   - results/attention/
   - results/counterfactuals/
   - results/viper/
   - results/safety/

📝 Key files for Paper 2:
   Section 4.1: results/attention/*.png
   Section 4.2: results/counterfactuals/*.png
   Section 4.3: results/viper/decision_tree.png, decision_rules.txt
   Section 4.4: results/saliency/*.png
   Section 5:   results/safety/safety_report.txt, *.png

================================================================================

==================================================
✅ Analysis completed successfully!
==================================================
