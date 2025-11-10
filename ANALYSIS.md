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
💾 Saved visualization to: images/2/saliency/saliency_000_P1_Active_High_Vehicle_Queue.png

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
💾 Saved visualization to: images/2/saliency/saliency_001_P2_Active_Bus_Priority.png

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
💾 Saved visualization to: images/2/attention/attention_000_P1_High_Vehicle_Queue.png

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
💾 Saved visualization to: images/2/attention/attention_001_P2_Bus_Priority.png

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
💾 Saved visualization to: images/2/counterfactuals/cf_001_P2_Bus_Present_to_Continue.png

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
💾 Saved visualization to: images/2/counterfactuals/cf_001_P2_Bus_Present_to_Next.png

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
💾 Saved visualization to: images/2/counterfactuals/cf_002_P1_Long_Duration_to_Skip2P1.png

   Generating: Continue → Next
   ✓ Converged at iteration 17
❌ Failed to generate counterfactual

✅ Batch generation complete! Results saved to: images/2/counterfactuals
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
   Action distribution: {'Continue': 1434, 'Skip2P1': 437, 'Next': 8129}

[Phase 2/4] Running VIPER iterations...

================================================================================
VIPER Iteration 1/3
================================================================================

🌳 Training decision tree...
   Max depth: 10
   Min samples split: 50
   Min samples leaf: 20

✅ Tree trained!
   Train accuracy: 93.53%
   Test accuracy: 91.75%
   Tree depth: 10
   Number of leaves: 94

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.85      0.84      0.85       296
     Skip2P1       0.34      0.19      0.25        73
        Next       0.94      0.96      0.95      1631

    accuracy                           0.92      2000
   macro avg       0.71      0.67      0.68      2000
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
   Train accuracy: 93.42%
   Test accuracy: 91.58%
   Tree depth: 10
   Number of leaves: 107

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.89      0.82      0.85       353
     Skip2P1       0.33      0.22      0.27        94
        Next       0.94      0.97      0.95      1953

    accuracy                           0.92      2400
   macro avg       0.72      0.67      0.69      2400
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
   Train accuracy: 93.68%
   Test accuracy: 91.39%
   Tree depth: 10
   Number of leaves: 123

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.84      0.85      0.85       414
     Skip2P1       0.39      0.26      0.31       113
        Next       0.94      0.96      0.95      2273

    accuracy                           0.91      2800
   macro avg       0.72      0.69      0.70      2800
weighted avg       0.91      0.91      0.91      2800


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
   Train accuracy: 93.92%
   Test accuracy: 90.53%
   Tree depth: 8
   Number of leaves: 115

📊 Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.83      0.84      0.84       513
     Skip2P1       0.45      0.29      0.35       139
        Next       0.94      0.95      0.94      2548

    accuracy                           0.91      3200
   macro avg       0.74      0.69      0.71      3200
weighted avg       0.90      0.91      0.90      3200


[Phase 3/4] Extracting decision rules...

================================================================================
EXTRACTED DECISION RULES (Accuracy: 90.5%)
================================================================================

|--- TLS6_Phase_P1 <= 0.500
|   |--- TLS3_Phase_P3 <= 0.500
|   |   |--- TLS6_Vehicle_Det1 <= 0.003
|   |   |   |--- weights: [1.000, 0.000, 19.000] class: 2
|   |   |--- TLS6_Vehicle_Det1 >  0.003
|   |   |   |--- weights: [0.000, 0.000, 6371.000] class: 2
|   |--- TLS3_Phase_P3 >  0.500
|   |   |--- TLS6_Phase_Duration <= 0.368
|   |   |   |--- TLS3_Phase_Duration <= 0.407
|   |   |   |   |--- TLS3_Bus_Wait <= 0.530
|   |   |   |   |   |--- TLS6_Phase_Duration <= 0.267
|   |   |   |   |   |   |--- TLS6_Vehicle_Det2 <= 0.554
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det2 <= 0.722
|   |   |   |   |   |   |   |   |--- weights: [84.000, 3.000, 2.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det2 >  0.722
|   |   |   |   |   |   |   |   |--- weights: [22.000, 0.000, 6.000] class: 0
|   |   |   |   |   |   |--- TLS6_Vehicle_Det2 >  0.554
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.669
|   |   |   |   |   |   |   |   |--- weights: [39.000, 4.000, 9.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.669
|   |   |   |   |   |   |   |   |--- weights: [6.000, 0.000, 14.000] class: 2
|   |   |   |   |   |--- TLS6_Phase_Duration >  0.267
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.146
|   |   |   |   |   |   |   |--- weights: [23.000, 1.000, 6.000] class: 0
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.146
|   |   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.442
|   |   |   |   |   |   |   |   |--- weights: [3.000, 11.000, 6.000] class: 1
|   |   |   |   |   |   |   |--- TLS6_Sim_Time >  0.442
|   |   |   |   |   |   |   |   |--- weights: [7.000, 2.000, 22.000] class: 2
|   |   |   |   |--- TLS3_Bus_Wait >  0.530
|   |   |   |   |   |--- TLS6_Bus_Wait <= 0.490
|   |   |   |   |   |   |--- TLS3_Vehicle_Det1 <= 0.526
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.160
|   |   |   |   |   |   |   |   |--- weights: [21.000, 0.000, 1.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.160
|   |   |   |   |   |   |   |   |--- weights: [19.000, 4.000, 12.000] class: 0
|   |   |   |   |   |   |--- TLS3_Vehicle_Det1 >  0.526
|   |   |   |   |   |   |   |--- weights: [13.000, 4.000, 27.000] class: 2
|   |   |   |   |   |--- TLS6_Bus_Wait >  0.490
|   |   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.249
|   |   |   |   |   |   |   |--- weights: [9.000, 4.000, 16.000] class: 2
|   |   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.249
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det2 <= 0.210
|   |   |   |   |   |   |   |   |--- weights: [8.000, 0.000, 18.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det2 >  0.210
|   |   |   |   |   |   |   |   |--- weights: [2.000, 3.000, 75.000] class: 2
|   |   |   |--- TLS3_Phase_Duration >  0.407
|   |   |   |   |--- TLS6_Bus_Present <= 0.788
|   |   |   |   |   |--- TLS3_Phase_Duration <= 0.558
|   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.447
|   |   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.509
|   |   |   |   |   |   |   |   |--- weights: [5.000, 20.000, 7.000] class: 1
|   |   |   |   |   |   |   |--- TLS6_Sim_Time >  0.509
|   |   |   |   |   |   |   |   |--- weights: [4.000, 3.000, 14.000] class: 2
|   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.447
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.184
|   |   |   |   |   |   |   |   |--- weights: [7.000, 2.000, 12.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.184
|   |   |   |   |   |   |   |   |--- weights: [0.000, 1.000, 32.000] class: 2
|   |   |   |   |   |--- TLS3_Phase_Duration >  0.558
|   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.423
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.285
|   |   |   |   |   |   |   |   |--- weights: [1.000, 19.000, 21.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.285
|   |   |   |   |   |   |   |   |--- weights: [2.000, 17.000, 122.000] class: 2
|   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.423
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det4 <= 0.890
|   |   |   |   |   |   |   |   |--- weights: [0.000, 2.000, 228.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det4 >  0.890
|   |   |   |   |   |   |   |   |--- weights: [0.000, 3.000, 17.000] class: 2
|   |   |   |   |--- TLS6_Bus_Present >  0.788
|   |   |   |   |   |--- TLS3_Sim_Time <= 0.242
|   |   |   |   |   |   |--- weights: [2.000, 26.000, 7.000] class: 1
|   |   |   |   |   |--- TLS3_Sim_Time >  0.242
|   |   |   |   |   |   |--- TLS3_Bicycle_Det3 <= 0.132
|   |   |   |   |   |   |   |--- weights: [0.000, 16.000, 9.000] class: 1
|   |   |   |   |   |   |--- TLS3_Bicycle_Det3 >  0.132
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.362
|   |   |   |   |   |   |   |   |--- weights: [4.000, 12.000, 18.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.362
|   |   |   |   |   |   |   |   |--- weights: [4.000, 6.000, 54.000] class: 2
|   |   |--- TLS6_Phase_Duration >  0.368
|   |   |   |--- TLS3_Phase_Duration <= 0.303
|   |   |   |   |--- TLS3_Bus_Wait <= 0.273
|   |   |   |   |   |--- TLS6_Bus_Wait <= 0.451
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.588
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.316
|   |   |   |   |   |   |   |   |--- weights: [0.000, 22.000, 0.000] class: 1
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.316
|   |   |   |   |   |   |   |   |--- weights: [5.000, 16.000, 10.000] class: 1
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.588
|   |   |   |   |   |   |   |--- weights: [3.000, 7.000, 16.000] class: 2
|   |   |   |   |   |--- TLS6_Bus_Wait >  0.451
|   |   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.259
|   |   |   |   |   |   |   |--- weights: [2.000, 12.000, 6.000] class: 1
|   |   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.259
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.264
|   |   |   |   |   |   |   |   |--- weights: [1.000, 7.000, 14.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.264
|   |   |   |   |   |   |   |   |--- weights: [1.000, 3.000, 50.000] class: 2
|   |   |   |   |--- TLS3_Bus_Wait >  0.273
|   |   |   |   |   |--- TLS6_Bus_Wait <= 0.548
|   |   |   |   |   |   |--- TLS3_Vehicle_Det4 <= 0.290
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det2 <= 0.238
|   |   |   |   |   |   |   |   |--- weights: [3.000, 13.000, 4.000] class: 1
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det2 >  0.238
|   |   |   |   |   |   |   |   |--- weights: [3.000, 11.000, 29.000] class: 2
|   |   |   |   |   |   |--- TLS3_Vehicle_Det4 >  0.290
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.118
|   |   |   |   |   |   |   |   |--- weights: [1.000, 8.000, 12.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.118
|   |   |   |   |   |   |   |   |--- weights: [8.000, 7.000, 113.000] class: 2
|   |   |   |   |   |--- TLS6_Bus_Wait >  0.548
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.461
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.225
|   |   |   |   |   |   |   |   |--- weights: [0.000, 8.000, 13.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.225
|   |   |   |   |   |   |   |   |--- weights: [0.000, 5.000, 65.000] class: 2
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.461
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.481
|   |   |   |   |   |   |   |   |--- weights: [1.000, 0.000, 19.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.481
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 92.000] class: 2
|   |   |   |--- TLS3_Phase_Duration >  0.303
|   |   |   |   |--- TLS6_Bus_Wait <= 0.052
|   |   |   |   |   |--- TLS6_Phase_Duration <= 0.619
|   |   |   |   |   |   |--- weights: [0.000, 12.000, 19.000] class: 2
|   |   |   |   |   |--- TLS6_Phase_Duration >  0.619
|   |   |   |   |   |   |--- weights: [0.000, 3.000, 45.000] class: 2
|   |   |   |   |--- TLS6_Bus_Wait >  0.052
|   |   |   |   |   |--- TLS6_Bus_Wait <= 0.341
|   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.160
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.691
|   |   |   |   |   |   |   |   |--- weights: [0.000, 12.000, 15.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.691
|   |   |   |   |   |   |   |   |--- weights: [0.000, 1.000, 25.000] class: 2
|   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.160
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.494
|   |   |   |   |   |   |   |   |--- weights: [0.000, 12.000, 88.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.494
|   |   |   |   |   |   |   |   |--- weights: [0.000, 3.000, 244.000] class: 2
|   |   |   |   |   |--- TLS6_Bus_Wait >  0.341
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.257
|   |   |   |   |   |   |   |--- TLS6_Bus_Present <= 0.583
|   |   |   |   |   |   |   |   |--- weights: [0.000, 1.000, 138.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Bus_Present >  0.583
|   |   |   |   |   |   |   |   |--- weights: [0.000, 8.000, 68.000] class: 2
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.257
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.143
|   |   |   |   |   |   |   |   |--- weights: [0.000, 3.000, 89.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.143
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 608.000] class: 2
|--- TLS6_Phase_P1 >  0.500
|   |--- TLS6_Phase_Duration <= 0.523
|   |   |--- TLS3_Phase_Duration <= 0.710
|   |   |   |--- TLS3_Phase_Duration <= 0.560
|   |   |   |   |--- TLS6_Phase_Duration <= 0.470
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.818
|   |   |   |   |   |   |--- TLS3_Vehicle_Det3 <= 0.971
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.907
|   |   |   |   |   |   |   |   |--- weights: [612.000, 0.000, 2.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.907
|   |   |   |   |   |   |   |   |--- weights: [46.000, 0.000, 3.000] class: 0
|   |   |   |   |   |   |--- TLS3_Vehicle_Det3 >  0.971
|   |   |   |   |   |   |   |--- weights: [17.000, 0.000, 3.000] class: 0
|   |   |   |   |   |--- TLS6_Sim_Time >  0.818
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.335
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det3 <= 0.787
|   |   |   |   |   |   |   |   |--- weights: [64.000, 0.000, 0.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det3 >  0.787
|   |   |   |   |   |   |   |   |--- weights: [19.000, 0.000, 1.000] class: 0
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.335
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.293
|   |   |   |   |   |   |   |   |--- weights: [37.000, 0.000, 2.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.293
|   |   |   |   |   |   |   |   |--- weights: [15.000, 0.000, 10.000] class: 0
|   |   |   |   |--- TLS6_Phase_Duration >  0.470
|   |   |   |   |   |--- TLS3_Phase_Duration <= 0.432
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.280
|   |   |   |   |   |   |   |--- weights: [43.000, 0.000, 0.000] class: 0
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.280
|   |   |   |   |   |   |   |--- weights: [24.000, 1.000, 4.000] class: 0
|   |   |   |   |   |--- TLS3_Phase_Duration >  0.432
|   |   |   |   |   |   |--- weights: [10.000, 7.000, 6.000] class: 0
|   |   |   |--- TLS3_Phase_Duration >  0.560
|   |   |   |   |--- TLS6_Phase_Duration <= 0.294
|   |   |   |   |   |--- TLS6_Bus_Wait <= 0.775
|   |   |   |   |   |   |--- TLS3_Bus_Present <= 0.785
|   |   |   |   |   |   |   |--- weights: [81.000, 0.000, 0.000] class: 0
|   |   |   |   |   |   |--- TLS3_Bus_Present >  0.785
|   |   |   |   |   |   |   |--- weights: [18.000, 0.000, 2.000] class: 0
|   |   |   |   |   |--- TLS6_Bus_Wait >  0.775
|   |   |   |   |   |   |--- weights: [23.000, 0.000, 7.000] class: 0
|   |   |   |   |--- TLS6_Phase_Duration >  0.294
|   |   |   |   |   |--- TLS6_Bus_Present <= 0.243
|   |   |   |   |   |   |--- weights: [3.000, 0.000, 23.000] class: 2
|   |   |   |   |   |--- TLS6_Bus_Present >  0.243
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.222
|   |   |   |   |   |   |   |--- weights: [7.000, 14.000, 6.000] class: 1
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.222
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.575
|   |   |   |   |   |   |   |   |--- weights: [27.000, 1.000, 11.000] class: 0
|   |   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.575
|   |   |   |   |   |   |   |   |--- weights: [8.000, 2.000, 19.000] class: 2
|   |   |--- TLS3_Phase_Duration >  0.710
|   |   |   |--- TLS6_Phase_Duration <= 0.245
|   |   |   |   |--- TLS3_Phase_Duration <= 0.923
|   |   |   |   |   |--- TLS6_Vehicle_Det4 <= 0.835
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.795
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.755
|   |   |   |   |   |   |   |   |--- weights: [79.000, 1.000, 5.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.755
|   |   |   |   |   |   |   |   |--- weights: [12.000, 3.000, 7.000] class: 0
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.795
|   |   |   |   |   |   |   |--- weights: [12.000, 0.000, 10.000] class: 0
|   |   |   |   |   |--- TLS6_Vehicle_Det4 >  0.835
|   |   |   |   |   |   |--- weights: [8.000, 3.000, 11.000] class: 2
|   |   |   |   |--- TLS3_Phase_Duration >  0.923
|   |   |   |   |   |--- TLS6_Phase_Duration <= 0.150
|   |   |   |   |   |   |--- weights: [17.000, 5.000, 12.000] class: 0
|   |   |   |   |   |--- TLS6_Phase_Duration >  0.150
|   |   |   |   |   |   |--- weights: [1.000, 2.000, 18.000] class: 2
|   |   |   |--- TLS6_Phase_Duration >  0.245
|   |   |   |   |--- TLS3_Sim_Time <= 0.199
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.455
|   |   |   |   |   |   |--- weights: [0.000, 19.000, 11.000] class: 1
|   |   |   |   |   |--- TLS6_Sim_Time >  0.455
|   |   |   |   |   |   |--- weights: [4.000, 2.000, 22.000] class: 2
|   |   |   |   |--- TLS3_Sim_Time >  0.199
|   |   |   |   |   |--- TLS3_Bicycle_Det4 <= 0.756
|   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.286
|   |   |   |   |   |   |   |--- weights: [6.000, 1.000, 15.000] class: 2
|   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.286
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.234
|   |   |   |   |   |   |   |   |--- weights: [2.000, 1.000, 22.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.234
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 106.000] class: 2
|   |   |   |   |   |--- TLS3_Bicycle_Det4 >  0.756
|   |   |   |   |   |   |--- weights: [0.000, 10.000, 32.000] class: 2
|   |--- TLS6_Phase_Duration >  0.523
|   |   |--- TLS3_Phase_Duration <= 0.299
|   |   |   |--- TLS6_Phase_Duration <= 0.732
|   |   |   |   |--- TLS3_Bus_Wait <= 0.703
|   |   |   |   |   |--- TLS3_Bicycle_Det1 <= 0.174
|   |   |   |   |   |   |--- weights: [18.000, 2.000, 3.000] class: 0
|   |   |   |   |   |--- TLS3_Bicycle_Det1 >  0.174
|   |   |   |   |   |   |--- TLS3_Bicycle_Det2 <= 0.307
|   |   |   |   |   |   |   |--- weights: [32.000, 0.000, 3.000] class: 0
|   |   |   |   |   |   |--- TLS3_Bicycle_Det2 >  0.307
|   |   |   |   |   |   |   |--- weights: [68.000, 0.000, 0.000] class: 0
|   |   |   |   |--- TLS3_Bus_Wait >  0.703
|   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.689
|   |   |   |   |   |   |--- weights: [27.000, 1.000, 3.000] class: 0
|   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.689
|   |   |   |   |   |   |--- weights: [10.000, 0.000, 10.000] class: 0
|   |   |   |--- TLS6_Phase_Duration >  0.732
|   |   |   |   |--- TLS3_Phase_Duration <= 0.101
|   |   |   |   |   |--- TLS6_Phase_Duration <= 0.917
|   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.578
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 <= 0.442
|   |   |   |   |   |   |   |   |--- weights: [16.000, 0.000, 4.000] class: 0
|   |   |   |   |   |   |   |--- TLS6_Bicycle_Det1 >  0.442
|   |   |   |   |   |   |   |   |--- weights: [30.000, 0.000, 0.000] class: 0
|   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.578
|   |   |   |   |   |   |   |--- weights: [14.000, 3.000, 10.000] class: 0
|   |   |   |   |   |--- TLS6_Phase_Duration >  0.917
|   |   |   |   |   |   |--- weights: [11.000, 1.000, 20.000] class: 2
|   |   |   |   |--- TLS3_Phase_Duration >  0.101
|   |   |   |   |   |--- TLS3_Sim_Time <= 0.440
|   |   |   |   |   |   |--- TLS6_Sim_Time <= 0.414
|   |   |   |   |   |   |   |--- weights: [3.000, 22.000, 6.000] class: 1
|   |   |   |   |   |   |--- TLS6_Sim_Time >  0.414
|   |   |   |   |   |   |   |--- weights: [18.000, 0.000, 15.000] class: 0
|   |   |   |   |   |--- TLS3_Sim_Time >  0.440
|   |   |   |   |   |   |--- TLS3_Bus_Wait <= 0.382
|   |   |   |   |   |   |   |--- weights: [13.000, 0.000, 11.000] class: 0
|   |   |   |   |   |   |--- TLS3_Bus_Wait >  0.382
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det2 <= 0.532
|   |   |   |   |   |   |   |   |--- weights: [0.000, 1.000, 40.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Vehicle_Det2 >  0.532
|   |   |   |   |   |   |   |   |--- weights: [7.000, 3.000, 20.000] class: 2
|   |   |--- TLS3_Phase_Duration >  0.299
|   |   |   |--- TLS3_Phase_Duration <= 0.475
|   |   |   |   |--- TLS6_Phase_Duration <= 0.611
|   |   |   |   |   |--- TLS6_Bicycle_Det2 <= 0.435
|   |   |   |   |   |   |--- weights: [25.000, 0.000, 3.000] class: 0
|   |   |   |   |   |--- TLS6_Bicycle_Det2 >  0.435
|   |   |   |   |   |   |--- weights: [11.000, 4.000, 7.000] class: 0
|   |   |   |   |--- TLS6_Phase_Duration >  0.611
|   |   |   |   |   |--- TLS6_Sim_Time <= 0.425
|   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.395
|   |   |   |   |   |   |   |--- weights: [0.000, 27.000, 11.000] class: 1
|   |   |   |   |   |   |--- TLS3_Sim_Time >  0.395
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.769
|   |   |   |   |   |   |   |   |--- weights: [7.000, 5.000, 12.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.769
|   |   |   |   |   |   |   |   |--- weights: [0.000, 3.000, 33.000] class: 2
|   |   |   |   |   |--- TLS6_Sim_Time >  0.425
|   |   |   |   |   |   |--- TLS6_Phase_Duration <= 0.704
|   |   |   |   |   |   |   |--- weights: [9.000, 2.000, 22.000] class: 2
|   |   |   |   |   |   |--- TLS6_Phase_Duration >  0.704
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.200
|   |   |   |   |   |   |   |   |--- weights: [1.000, 4.000, 22.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.200
|   |   |   |   |   |   |   |   |--- weights: [0.000, 1.000, 70.000] class: 2
|   |   |   |--- TLS3_Phase_Duration >  0.475
|   |   |   |   |--- TLS6_Sim_Time <= 0.461
|   |   |   |   |   |--- TLS3_Sim_Time <= 0.323
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.705
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.630
|   |   |   |   |   |   |   |   |--- weights: [0.000, 25.000, 9.000] class: 1
|   |   |   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.630
|   |   |   |   |   |   |   |   |--- weights: [2.000, 5.000, 18.000] class: 2
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.705
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.309
|   |   |   |   |   |   |   |   |--- weights: [0.000, 10.000, 16.000] class: 2
|   |   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.309
|   |   |   |   |   |   |   |   |--- weights: [0.000, 2.000, 49.000] class: 2
|   |   |   |   |   |--- TLS3_Sim_Time >  0.323
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.569
|   |   |   |   |   |   |   |--- weights: [3.000, 6.000, 35.000] class: 2
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.569
|   |   |   |   |   |   |   |--- TLS3_Sim_Time <= 0.486
|   |   |   |   |   |   |   |   |--- weights: [0.000, 4.000, 43.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Sim_Time >  0.486
|   |   |   |   |   |   |   |   |--- weights: [1.000, 0.000, 159.000] class: 2
|   |   |   |   |--- TLS6_Sim_Time >  0.461
|   |   |   |   |   |--- TLS6_Vehicle_Det1 <= 0.156
|   |   |   |   |   |   |--- TLS6_Bus_Wait <= 0.217
|   |   |   |   |   |   |   |--- weights: [3.000, 3.000, 16.000] class: 2
|   |   |   |   |   |   |--- TLS6_Bus_Wait >  0.217
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det2 <= 0.668
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 40.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Bicycle_Det2 >  0.668
|   |   |   |   |   |   |   |   |--- weights: [0.000, 1.000, 19.000] class: 2
|   |   |   |   |   |--- TLS6_Vehicle_Det1 >  0.156
|   |   |   |   |   |   |--- TLS3_Phase_Duration <= 0.562
|   |   |   |   |   |   |   |--- TLS3_Bus_Present <= 0.704
|   |   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 46.000] class: 2
|   |   |   |   |   |   |   |--- TLS3_Bus_Present >  0.704
|   |   |   |   |   |   |   |   |--- weights: [3.000, 0.000, 17.000] class: 2
|   |   |   |   |   |   |--- TLS3_Phase_Duration >  0.562
|   |   |   |   |   |   |   |--- weights: [0.000, 0.000, 326.000] class: 2


[Phase 4/4] Creating visualizations...
💾 Saved tree visualization to: images/2/viper/decision_tree.png

🎲 Collecting 1000 samples from DQN policy...

✅ Dataset collected!
   Action distribution: {'Continue': 136, 'Skip2P1': 31, 'Next': 833}
💾 Saved confusion matrix to: images/2/viper/confusion_matrix.png
💾 Saved tree to: images/2/viper/extracted_tree.pkl
✅ VIPER extraction complete!
   Tree accuracy: 90.5%
   Tree depth: 8
   Number of leaves: 115

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

💾 Saved safety summary to: images/2/safety/safety_summary.png
💾 Saved heatmap to: images/2/safety/waiting_time_heatmap.png

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

💾 Safety report saved to: images/2/safety/safety_report.txt
✅ Safety analysis complete!

================================================================================
  ANALYSIS COMPLETE!
================================================================================

⏱️  Total runtime: 0m 15s

📊 Results saved to:
   - images/2/saliency/
   - images/2/attention/
   - images/2/counterfactuals/
   - images/2/viper/
   - images/2/safety/

📝 Key files for Paper 2:
   Section 4.1: images/2/attention/*.png
   Section 4.2: images/2/counterfactuals/*.png
   Section 4.3: images/2/viper/decision_tree.png, decision_rules.txt
   Section 4.4: images/2/saliency/*.png
   Section 5:   images/2/safety/safety_report.txt, *.png

================================================================================

==================================================
✅ Analysis completed successfully!
==================================================
