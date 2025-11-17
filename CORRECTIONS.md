I'll help you review Paper 1 for inconsistencies and analytical problems. Let me search for the relevant documents in
your project.##### Paper 1: Comprehensive Review and Analysis

###### Numerical Accuracy Verification

**Average Waiting Times (Section 9.2, Abstract, Performance Summary)**

The paper consistently cites the following average waiting times across all 30 scenarios:

- Cars: $43.3$s
- Bicycles: $22.9$s
- Pedestrians: $2.9$s
- Buses: $5.0$s

**Verification Against Table_Single_Agent.md (Table 2, Section D):** All values match the data table perfectly. The
comparison percentages are also correctly calculated:

- Cars vs Developed: $(43.3 - 36.5) / 36.5 = +18.6%$ ✓
- Bicycles vs Developed: $(22.9 - 48.1) / 48.1 = -52.4%$ ✓
- Pedestrians vs Developed: $(2.9 - 17.0) / 17.0 = -82.9%$ ✓
- Buses vs Developed: $(5.0 - 16.2) / 16.2 = -69.1%$ ✓

**Status:** ✅ No inconsistencies found.

---

###### Training Configuration Inconsistency

**CRITICAL ISSUE #1: Total Training Timesteps Mismatch**

**Paper Claim (Section 7.3, Section 9.1):**

- Training episodes: $200$
- Steps per episode: $3,600$
- **Total timesteps: $720,000$** (stated as $200 \times 3,600$)

**Paper Claim (Section 9.1 - Final Model Performance):**

- **"Total timesteps trained: $691,200$ ($192$ episodes $\times$ $3,600$ steps)"**

**Analysis:** There is a significant inconsistency. The paper claims Model 192 was selected for testing, which would
imply:

- $192 \times 3,600 = 691,200$ timesteps

However, the paper also states the training ran for 200 episodes, which would be:

- $200 \times 3,600 = 720,000$ timesteps

**Resolution Needed:** The paper needs to clarify:

1. Was the full training 200 episodes or 192 episodes?
2. If Model 192 was selected, what happened to episodes 193-200?
3. The $720,000$ total timestep claim conflicts with the $691,200$ for Model 192

**Recommendation:** Change Section 7.3 to state "**Training episodes: Up to 200 (Model 192 selected for testing)**" and
explain that while 200 episodes were completed, Model 192 was selected based on validation performance before the final
episodes.

---

###### Action Distribution Inconsistency

**CRITICAL ISSUE #2: Target vs Actual Action Distribution**

**Paper Claim (Abstract, Section 7.4, Research Contributions):**

- Target action distribution: $85%$ Continue, $2.5%$ Skip-to-P1, $12.5%$ Next

**Paper Claim (Paper 2, Section 3.2 Performance Summary - Testing Results):**

- **Actual action distribution during testing:** Continue $80.8%$, Skip2P1 $2.3%$, Next $17.0%$

**Analysis:** The actual distribution significantly deviates from the stated target:

- Continue: $80.8%$ vs target $85%$ (difference: $-4.2%$)
- Skip-to-P1: $2.3%$ vs target $2.5%$ (difference: $-0.2%$) ✓
- Next: $17.0%$ vs target $12.5%$ (difference: $+4.5%$)

**This is problematic because:**

1. Paper 1 repeatedly emphasizes that reward recalibration was done to achieve the $85%/2.5%/12.5%$ target
2. The actual distribution shows the agent uses "Next Phase" $36%$ more frequently than intended ($17%$ vs $12.5%$)
3. This suggests the reward recalibration did not fully achieve its stated objective

**Verification from Explainability_Result.md:**

```
Action distribution (from real policy):
{'Continue': 242281, 'Skip2P1': 6857, 'Next': 50862}
  Continue: 80.8%
  Skip2P1: 2.3%
  Next: 17.0%
```

This confirms the actual distribution differs from the target.

**Recommendation:** Paper 1 should either:

1. Acknowledge that the target distribution was not fully achieved and explain why
2. Discuss whether the $17%$ Next Phase usage represents improved policy discovery beyond the initial target
3. Remove or soften claims about "achieving target action distributions"

---

###### Reward Function Ambiguity

**ISSUE #3: Two-Phase Training Confusion**

**Paper Claim (Section 7.4, Abstract):** The paper describes "two-phase training" with:

- Phase 1: Episodes 1-50 (Exploration-dominant, $\epsilon: 1.0 \to 0.36$)
- Phase 2: Episodes 51-150 (Learning phase, $\epsilon: 0.36 \to 0.08$)
- Phase 3: Episodes 151-200 (Convergence phase, $\epsilon: 0.08 \to 0.05$)

**But the paper also states:** "Two-phase training methodology" with reward function recalibration after Episode 100

**Analysis:** This creates confusion:

1. The paper describes **three phases** based on exploration rate
2. But claims a "**two-phase** methodology" based on reward recalibration at Episode 100
3. These are overlapping but different phase definitions

**Resolution Needed:** The paper should clarify:

- "Three-phase convergence pattern" (based on $\epsilon$-decay)
- "Two-phase reward structure" (recalibration at Episode 100)
- These are separate concepts describing different aspects of training

**Recommendation:** Use consistent terminology. Either:

1. "Three-phase training convergence with mid-training reward recalibration"
2. Or clearly separate "convergence phases" from "training methodology phases"

---

###### Neural Network Architecture

**POTENTIAL ISSUE #4: Network Parameter Count**

**Paper Claim (Paper 2, Section 3.1):**

- Architecture: $256$-$256$-$128$ hidden layers
- **"approximately $107,523$ parameters"**

**Verification:** Let me calculate the actual parameter count:

- Input layer to Hidden 1: $(32 \times 256) + 256 = 8,192 + 256 = 8,448$
- Hidden 1 to Hidden 2: $(256 \times 256) + 256 = 65,536 + 256 = 65,792$
- Hidden 2 to Hidden 3: $(256 \times 128) + 128 = 32,768 + 128 = 32,896$
- Hidden 3 to Output: $(128 \times 3) + 3 = 384 + 3 = 387$

**Total:** $8,448 + 65,792 + 32,896 + 387 = 107,523$ ✓

**Status:** ✅ Calculation is correct.

---

###### Reward Function Mathematical Consistency

**ISSUE #5: Reward Component Weight Inconsistency**

**Paper Claim (Section 7.3 - Reward Component Weights Table):**

| Component      | Weight ($\alpha$) |
| -------------- | ----------------- |
| Waiting time   | 2.5               |
| Safety         | 2.0               |
| Next bonus     | 2.0               |
| Equity         | 0.5               |
| Stability      | 0.12              |
| Blocked action | 0.1               |
| Emissions      | 0.05              |

**Paper Claim (Section 6.1 - Reward Design Philosophy):** "**Next bonus** $+2.0$ to $+4.0$"

**Analysis:** There is an inconsistency. The table states next bonus weight is $2.0$, but the design philosophy section
mentions a range of $+2.0$ to $+4.0$. This suggests the next bonus reward is context-dependent, but this is not
explained clearly.

**Resolution Needed:** Clarify whether:

1. The next bonus is fixed at $2.0$ (as per table)
2. Or variable between $2.0$ and $4.0$ based on phase timing thresholds (as suggested in Section 6.1)

**Checking Section 6.3 for Phase Timing Rewards:** The paper needs to clearly specify the next bonus calculation formula
and when it varies.

---

###### Safety Violations Data

**ISSUE #6: Safety Violation Claims Lack Detail**

**Paper Claim (Multiple locations):**

- "**Zero safety violations** across 30 test scenarios"
- "Safety violations during training: $0$ (across all 200 episodes)"

**Analysis:** The paper never defines what constitutes a "safety violation." This is problematic because:

1. No operational definition of safety violation is provided
2. No methodology for detecting violations is explained
3. It's unclear if this refers to:
    - Collisions in SUMO?
    - Minimum green time violations?
    - Maximum waiting time thresholds?
    - All of the above?

**From Table_Single_Agent.md (Section E, Table 4):**

```
| Safety Metric               | Value | Status        |
| Total Safety Violations     | 0     | EXCELLENT     |
```

The data confirms zero violations, but still doesn't define the term.

**Recommendation:** Add a clear definition in the methodology section: "We define safety violations as: (1) collisions
detected by SUMO, (2) minimum green time violations (<10s), (3) pedestrian waiting times exceeding 60s, or (4) any
blocked action attempts that would violate phase transition constraints."

---

###### Performance Interpretation Issue

**ISSUE #7: Oversimplified Comparison Claims**

**Paper Claim (Abstract, Research Contributions):** "**$89.0%$ reduction** in bicycle waiting times (from $208.5$s to
$22.9$s) compared to Reference Control"

**Analysis:** While mathematically correct, this comparison is somewhat misleading because:

1. The Reference Control was designed for vehicular traffic only
2. It provides no bicycle priority whatsoever (hence the extreme $208.5$s wait time)
3. Comparing against a system with **no bicycle consideration** inflates the perceived improvement

**The more meaningful comparison** is against Developed Control:

- Bicycles: $52.4%$ improvement ($48.1$s to $22.9$s)
- This still represents significant improvement but is more realistic

**Recommendation:** While the Reference Control comparison is valid, the paper should acknowledge that Reference Control
represents a "worst-case baseline" with no multi-modal features, and emphasize the Developed Control comparison as the
primary achievement metric.

---

###### Training Convergence Claims

**ISSUE #8: Exploration Rate Arithmetic**

**Paper Claim (Section 9.1, Phase 1):** "Phase 1: Exploration-Dominant (Episodes 1-50, $\epsilon: 1.0 \to 0.36$)"

**Verification:** With $\epsilon$-decay formula:
$$\epsilon_t = \epsilon_{min} + (\epsilon_{max} - \epsilon_{min}) \times e^{-t/\tau}$$

Where:

- $\epsilon_{max} = 1.0$
- $\epsilon_{min} = 0.05$
- $\tau$ (decay rate) determines the slope

At episode $50$ (assuming $3,600$ steps per episode = $180,000$ total steps):

The stated value of $\epsilon = 0.36$ at episode 50 needs verification against the actual decay parameters used. **This
cannot be verified without knowing the exact $\tau$ value.**

**Recommendation:** Provide the $\epsilon$-decay formula parameters explicitly in the hyperparameter table.

---

###### Summary of Issues Found in Paper 1

| Issue # | Category       | Severity    | Description                                                           |
| ------- | -------------- | ----------- | --------------------------------------------------------------------- |
| 1       | Training       | **HIGH**    | Total timesteps mismatch: $720,000$ vs $691,200$                      |
| 2       | Results        | **HIGH**    | Action distribution: actual $80.8/2.3/17.0%$ vs target $85/2.5/12.5%$ |
| 3       | Methodology    | **MEDIUM**  | Conflicting "two-phase" vs "three-phase" training terminology         |
| 4       | Architecture   | ✅ VERIFIED | Network parameters correctly calculated                               |
| 5       | Reward         | **MEDIUM**  | Next bonus weight: fixed $2.0$ vs range $2.0$-$4.0$ inconsistency     |
| 6       | Safety         | **MEDIUM**  | "Safety violation" term undefined operationally                       |
| 7       | Interpretation | **LOW**     | Oversimplified Reference Control comparison claims                    |
| 8       | Training       | **LOW**     | $\epsilon$-decay parameters not fully specified                       |

---

---

---

---

##### Paper 2: Comprehensive Review and Analysis

###### Cross-Reference Consistency with Paper 1

**CRITICAL ISSUE #1: Inconsistent Performance Metrics Between Papers**

**Paper 2 Claim (Section 3.2 - Performance Summary):**

- Average Waiting Times: Cars $43.3$s | Bicycles $22.9$s | Pedestrians $2.9$s | Buses $5.0$s
- vs Developed Control: Cars $+18.6%$ | Bicycles $-52.4%$ | Pedestrians $-82.9%$ | Buses $-69.1%$
- Zero safety violations across 30 test scenarios ($108,000$s simulation time)
- **Action Distribution: Continue $80.8%$ | Skip2P1 $2.3%$ | Next $17.0%$**

**Verification Against Paper 1:** The waiting time metrics are consistent ✓

However, the action distribution already flagged in Paper 1 analysis remains problematic here.

**Status:** ⚠️ Paper 2 correctly reports testing results, but inherits Paper 1's action distribution issue.

---

###### Simulation Time Calculation Error

**CRITICAL ISSUE #2: Simulation Time Calculation**

**Paper 2 Claim (Section 3.2, Section 5.3.1):**

- "**108,000s simulation time**" ($30$ scenarios × $3,600$ seconds each)
- Also stated as "**108,000 hours** of simulated traffic" in Section 5.3.1

**Analysis:** This contains a severe unit error:

- $30 \text{ scenarios} \times 3,600\text{s} = 108,000\text{ seconds}$
- $108,000\text{ seconds} = 1,800\text{ minutes} = 30\text{ hours}$ (NOT $108,000$ hours)

**The correct statement should be:**

- "$30$ hours of simulated traffic" or "$108,000$ seconds"

**Location of Error:** Section 5.3.1 states: "Figure 5.1 presents the consolidated safety performance across all
transportation modes, derived from **108,000 hours** of simulated traffic (30 scenarios × 3,600 seconds each)."

**Recommendation:** Change to "$30$ hours ($108,000$ seconds) of simulated traffic"

---

###### VIPER Decision Tree Accuracy Inconsistency

**CRITICAL ISSUE #3: Conflicting VIPER Accuracy Claims**

**Paper 2 Claim (Section 4.3, Multiple Locations):**

1. Section 4.3.2: "VIPER achieved **90.53% test accuracy**"
2. Section 5.3.2: "**89.5% fidelity**"
3. Section 8.1: "**90.53% test accuracy**"
4. Abstract: No specific accuracy mentioned

**Verification from Explainability_Result.md:**

```
✅ VIPER extraction complete!
   Tree accuracy: 89.5%
   Tree depth: 8
   Number of leaves: 173
```

**Additional Data from Results:** The file shows multiple VIPER iterations with different accuracies:

- Iteration 1: $96.92%$ test accuracy, depth $10$, $383$ leaves
- Iteration 2: $94.70%$ test accuracy, depth $10$, $390$ leaves
- Iteration 3: $92.72%$ test accuracy, depth $10$, $393$ leaves
- **Final tree:** $89.5%$ accuracy, depth $8$, $173$ leaves

**Analysis:** The paper appears to cite an intermediate iteration accuracy ($90.53%$) rather than the final model
accuracy ($89.5%$). The final tree traded accuracy for interpretability (depth $10 \to 8$, leaves $393 \to 173$).

**Recommendation:** Use $89.5%$ consistently throughout the paper and explain that intermediate iterations achieved
higher accuracy but were too complex.

---

###### Decision Tree Structure Inconsistency

**ISSUE #4: Conflicting Tree Parameters**

**Paper 2 Claims:**

1. Section 4.3.2: "depth $8$, $115$ leaves"
2. Section 5.3.2: "$173$ leaf nodes"
3. Section 8.1: "depth $8$, $115$ leaves"
4. Table E.3 (from Table_Single_Agent.md): No tree structure data provided

**Verification from Explainability_Result.md:**

```
Tree depth: 8
Number of leaves: 173
```

**Analysis:** The paper inconsistently cites $115$ leaves in some sections but $173$ leaves in others. The actual result
is **$173$ leaves**.

**Recommendation:** Correct all instances to "$173$ leaves" throughout the paper.

---

###### Attention Analysis Numerical Claims

**ISSUE #5: Attention Weight Range Claims**

**Paper 2 Claim (Section 8.1):** "Attention analysis shows balanced feature consideration (**$6.3$-$17.3%$ attention
weights**)"

**Verification from Table E.1 (Table_Single_Agent.md):**

| Feature Group | Min Attention | Max Attention |
| ------------- | ------------- | ------------- |
| All features  | $6.65%$       | $13.78%$      |

**Analysis:** The paper claims max attention of $17.3%$, but the data table shows max of $13.78%$. The range should be
**$6.65%$-$13.78%$**, not $6.3%$-$17.3%$.

**Additional Check - Specific Claims:** The paper states: "phase duration emerging as the most consistently critical
feature across all methods (**$17.29%$ peak attention**)"

This $17.29%$ value does **not appear** in Table E.1. The highest attention weight in the table is $13.78%$ for TLS6
Timing in the P1_Bus_Waiting scenario.

**Recommendation:** Verify the actual maximum attention weight from the raw data and correct the paper accordingly.

---

###### Counterfactual Analysis Metrics

**ISSUE #6: Missing Detailed Counterfactual Data**

**Paper 2 Claim (Section 8.1):** "Counterfactual analysis identifies well-defined, stable decision boundaries with small
L2 distances (**$0.07$-$0.52$**) and fast convergence (**$3$-$22$ iterations**)"

**Problem:** These specific numerical values are cited in the conclusion but **do not appear anywhere earlier** in
Section 4.2 (Counterfactual Explanations) or in Table E.2.

**From Table E.2 (Table_Single_Agent.md):** The table shows "Minimal state perturbations required to flip agent
decisions" but **does not provide L2 distance or iteration count data**.

**Analysis:** The paper makes specific numerical claims in the conclusion that are not supported by data presented
earlier in the paper or in the tables.

**Recommendation:** Either:

1. Add detailed counterfactual metrics to Section 4.2 and Table E.2
2. Or remove the specific numerical claims from Section 8.1

---

###### Safety Violations Definition

**ISSUE #7: Undefined Safety Violation Term (Inherited from Paper 1)**

**Paper 2 Claim (Multiple locations):**

- "**Zero safety violations** across 30 test scenarios"
- Section 5.2 discusses "concerning behaviors" but never reports actual violations

**Problem:** Same issue as Paper 1 - no operational definition of what constitutes a "safety violation."

**From Table_Single_Agent.md (Section E, Table 4):**

```
| Safety Metric               | Value | Status        |
| Total Safety Violations     | 0     | EXCELLENT     |
```

The data confirms zero violations but doesn't define the measurement.

**Recommendation:** Add explicit definition in methodology section (same recommendation as Paper 1).

---

###### Bus Priority Attention Weight Discrepancy

**ISSUE #8: Bus Attention Claims vs Data**

**Paper 2 Claim (Section 8.1):** "Skip2P1 decisions prioritize bus waiting times (**up to $51%$ attention in bus
scenarios**)"

**Verification from Table E.1:** Looking at the "TLS3 Bus" and "TLS6 Bus" columns for Skip2P1 scenarios:

- P1_High_Vehicle_Queue (Skip2P1): TLS3 Bus $= 6.95%$, TLS6 Bus $= 6.65%$
- P1_Bus_Waiting (Skip2P1): TLS3 Bus $= 7.35%$, TLS6 Bus $= 8.60%$

**Analysis:** The table shows bus-related features receive $6.65%$-$8.60%$ attention, **not $51%$**. The $51%$ claim is
completely inconsistent with the data.

**Possible Explanation:** This might refer to a different analysis (e.g., relative importance within Skip2P1 decisions
only, not absolute attention weights). But if so, this needs clarification.

**Recommendation:** Either:

1. Verify whether $51%$ refers to conditional attention (given Skip2P1 action)
2. Or correct to the actual values from Table E.1 ($6.65%$-$8.60%$)
3. Or remove the claim entirely if unsupported

---

###### Blocking Events Data

**ISSUE #9: Blocking Events Count Discrepancy**

**Paper 2 Claim (Section 5.2):** No specific total blocking events mentioned in the safety analysis section.

**From Explainability_Result.md:**

```
Total blocking events: 4562
Scenarios with blocks: 30
Blocking by action:
   Next: 4350 blocks
   Skip2P1: 212 blocks
```

**From Table_Single_Agent.md (Section E, Table 4):**

```
| Total Blocking Events   | 4,562 | High |
```

**Status:** ✅ Data is consistent between sources, but Paper 2 should include this detailed blocking analysis in the
safety section.

---

###### Mathematical Notation Inconsistency

**ISSUE #10: Attention Mechanism Formula**

**Paper 2 Claim (Section 1.4):** "attention mechanism integration augments the DQN architecture to compute attention
weights $\alpha_i$ over state dimensions, revealing $\alpha_i = \frac{\exp(e_i)}{\sum_j \exp(e_j)}$"

**Problem:** The formula is presented but:

1. The paper never defines what $e_i$ represents
2. Section 4.1 mentions "gradient-based attribution (pseudo-attention)" but doesn't show how $e_i$ is calculated
3. The relationship between gradients and $e_i$ is not explained

**Recommendation:** Add explicit definition: "where $e_i = |\nabla_{s_i} Q(s,a)|$ represents the gradient magnitude of
Q-value with respect to state feature $i$"

---

###### Pedestrian Safety Edge Cases

**ISSUE #11: Edge Case Threshold Definition**

**Paper 2 Claim (Section 5.2, implicitly):** The paper discusses "concerning behaviors" including "excessive pedestrian
wait times in Pe_8-9"

**From Table_Single_Agent.md (Section E, Table 4):**

```
⚠️ Pedestrian Waiting Time Edge Cases (>4.2s):
   Pr_0: 5.61s
   Bi_1: 4.73s
   Bi_8: 5.06s
   Pe_6: 4.85s
```

**Analysis:** The table identifies $4$ pedestrian edge cases but **Pe_8 and Pe_9 are not among them**. The paper's
discussion of Pe_8-9 as problematic is not supported by the edge case data.

**Actual Pe_8 and Pe_9 waiting times** (from Table D.1):

- Pe_8: $4.01$s (below $4.2$s threshold)
- Pe_9: $4.19$s (just below $4.2$s threshold)

**Recommendation:** Verify whether Pe_8-9 are actually problematic or if the paper should reference the actual edge
cases (Pr_0, Bi_1, Bi_8, Pe_6).

---

###### VIPER Classification Report Inconsistency

**ISSUE #12: Continue Action Recall Claim**

**Paper 2 Claim (Section 5.3.2, Figure caption):** "Continue actions (Class 0) achieve **$98%$ recall**"

**Verification from Explainability_Result.md:** Looking at the final VIPER model:

```
Classification Report (Test Set):
              precision    recall  f1-score   support

    Continue       0.94      0.98      0.96     47586
```

**Status:** ✅ The $98%$ recall claim is correct.

---

###### Skip2P1 Classification Performance

**ISSUE #13: Skip2P1 Recall Claims**

**Paper 2 Claim (Section 5.3.2, Figure caption):** "rare Skip2P1 actions (Class 1) prove most challenging with only
**$62%$ recall**"

**Verification from Explainability_Result.md:** Final tree results show:

```
    Skip2P1       0.53      0.75      0.62      1370
```

**Analysis:** The data shows Skip2P1 recall is **$75%$**, not $62%$. The $62%$ is the **F1-score**, not recall.

**Recommendation:** Correct to "$75%$ recall (F1-score $62%$)"

---

###### Data Sample Size Claims

**ISSUE #14: Total States Analyzed**

**Paper 2 Claim (Section 4 - Data Collection):** "$32$ dimensions × $300$K samples = **$9.6$M data points**"

**Verification:** $32 \times 300,000 = 9,600,000$ ✓

**Status:** ✅ Calculation is correct.

---

###### Action Distribution in VIPER

**ISSUE #15: Sampled States Action Distribution**

**From Explainability_Result.md:**

```
Sampled 10,000 states for analysis

Action distribution (from real policy):
{'Continue': 8077, 'Skip2P1': 243, 'Next': 1680}
  Continue: 80.8%
  Skip2P1: 2.4%
  Next: 16.8%
```

**Paper 2 Claim (Section 3.2):** Action Distribution: Continue $80.8%$ | Skip2P1 **$2.3%$** | Next $17.0%$

**Analysis:** Minor discrepancy in the sampled subset:

- Full dataset: Skip2P1 $2.3%$, Next $17.0%$
- VIPER sample (10K): Skip2P1 $2.4%$, Next $16.8%$

This is acceptable sampling variation, but Paper 2 should acknowledge that VIPER analysis used a $10,000$-sample subset.

**Recommendation:** Clarify in Section 4.3 that "VIPER analysis was performed on a stratified $10,000$-sample subset..."

---

###### Summary of Issues Found in Paper 2

| Issue # | Category       | Severity     | Description                                                     |
| ------- | -------------- | ------------ | --------------------------------------------------------------- |
| 1       | Cross-Ref      | **MEDIUM**   | Inherits action distribution issue from Paper 1                 |
| 2       | Units          | **HIGH**     | "$108,000$ hours" should be "$30$ hours" - major unit error     |
| 3       | VIPER          | **HIGH**     | Accuracy claims inconsistent: $90.53%$ vs $89.5%$               |
| 4       | VIPER          | **HIGH**     | Tree leaves: $115$ vs $173$ - conflicting claims                |
| 5       | Attention      | **HIGH**     | Attention range $6.3$-$17.3%$ vs actual $6.65$-$13.78%$         |
| 6       | Counterfactual | **MEDIUM**   | L2 distance claims ($0.07$-$0.52$) not presented in Section 4.2 |
| 7       | Safety         | **MEDIUM**   | "Safety violation" term undefined (inherited from Paper 1)      |
| 8       | Attention      | **CRITICAL** | Bus attention "$51%$" vs actual $6.65$-$8.60%$ - major error    |
| 9       | Blocking       | ✅ VERIFIED  | Blocking events data consistent                                 |
| 10      | Math           | **LOW**      | Attention formula incomplete - missing $e_i$ definition         |
| 11      | Safety         | **MEDIUM**   | Pe_8-9 discussed as edge cases but data doesn't support this    |
| 12      | VIPER          | ✅ VERIFIED  | Continue recall $98%$ correct                                   |
| 13      | VIPER          | **MEDIUM**   | Skip2P1 recall $62%$ vs actual $75%$ (confused with F1-score)   |
| 14      | Data           | ✅ VERIFIED  | $9.6$M data points calculation correct                          |
| 15      | Sampling       | **LOW**      | Should clarify VIPER used $10$K sample subset                   |

---

**Critical Issues Requiring Immediate Attention:**

1. **Issue #2:** Simulation time unit error ($108,000$ hours vs $30$ hours)
2. **Issue #8:** Bus attention $51%$ claim is completely unsupported by data
3. **Issues #3, #4:** VIPER accuracy and tree structure inconsistencies
4. **Issue #5:** Attention weight range claims don't match data

These errors significantly impact the paper's credibility and must be corrected before publication.

---

