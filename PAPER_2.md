# Explainable RL for Traffic Control

#### **Core Idea:**

REUSES: Your trained model completely! ✓✓✓

PROBLEM: "Why did the agent choose this action?" Traffic engineers don't trust black-box RL

INNOVATION: Make RL decisions interpretable: - Attention mechanisms (what state features matter?) - Counterfactual
explanations (what if traffic was different?) - Decision trees extracted from RL policy - Natural language explanations

WHY VALUABLE: ✓✓✓ Deployment blocker: Engineers won't adopt black boxes ✓✓ XAI (Explainable AI) is critical research
area ✓✓ Bridge RL research ↔ traffic practice ✓ Enables human-AI collaboration

#### **Methodology:**

EXPLAINABILITY TECHNIQUES:

1. ATTENTION-AUGMENTED DQN

    - Add attention layer to your DQN
    - Visualize which state features matter
    - "Agent focuses on queue length at approaching intersection"

2. COUNTERFACTUAL EXPLANATIONS

    - "If queue was 5 cars instead of 10, would have extended green"
    - Generate minimal state changes that flip decision
    - Actionable insights for engineers

3. DECISION TREE EXTRACTION

    - Use VIPER, TREPAN algorithms
    - Distill RL policy into interpretable tree
    - 90% accuracy, human-readable rules

4. SALIENCY MAPS

    - Gradient-based attribution
    - Which state dimensions most influence Q-values?
    - Heatmaps for visualization

5. NATURAL LANGUAGE GENERATION
    - Templates: "Extended green because {reason}"
    - Reasons: high queue, pedestrian waiting, sync opportunity
    - Automatically generate explanations

USER STUDY:

- Traffic engineers evaluate explanations
- Trust, usability, actionability metrics
- Compare: No explanation vs Decision tree vs Natural language

---

##### Complete List of Reward Events Found:

- Check please

1. **[EARLY CHANGE]** - Phase changed too early penalty
2. **[SKIP2P1 BONUS]** - Skip helped bus bonus
3. **[SKIP2P1 EFFECTIVE]** - Effective skip action bonus
4. **[CONTINUE UNDERUSED via Q-values]** - Continue underused bonus
5. **[ACTION 2 OVERUSED]** - Next action overused penalty
6. **[STABILITY BONUS]** - Phase duration stability bonus
7. **[CONTINUE SPAM]** - Consecutive Continue penalty
8. **[NEXT BONUS]** - Next action after min duration bonus
9. **[BLOCKED - BUS WAIT]** - Blocked action with bus waiting penalty
10. **[BUS PENALTY]** - Bus waiting too long penalty
11. **[BUS EXCELLENT]** - Very short bus wait bonus
12. **[MAX_GREEN FORCED]** - Max green time enforcement


---
---

Given the complexity and variability of the XAI data, I recommend **separate supplementary tables** rather than cramming everything into one massive table. Here's a well-organized approach:

---

## **Approach 1: Separate XAI Tables (Recommended)**

### **Table 1: Traffic Configuration & Action Distribution**

| Scenario | Cars (veh/hr) | Bicycles (veh/hr) | Pedestrians (veh/hr) | Buses | Total Actions | Continue | Skip to P1 | Next |
|---|---|---|---|---|---|---|---|---|
| Pr_0 | 100 | 400 | 400 | every_15min | 10000 | 8908 (89.1%) | 313 (3.1%) | 779 (7.8%) |
| Pr_1 | 200 | 400 | 400 | every_15min | 10000 | 8856 (88.6%) | 271 (2.7%) | 873 (8.7%) |

### **Table 2: Phase Change & Safety Metrics**

| Scenario | Actions Attempted | Phase Changes | Actions Blocked | Phase Change Rate | Block Rate | Total Safety Violations | Violation Rate |
|---|---|---|---|---|---|---|---|
| Pr_0 | 15112 | 1628 | 176 | 10.8% | 1.2% | 0 | 0.00% |
| Pr_1 | 14872 | 1708 | 298 | 11.5% | 2.0% | 0 | 0.00% |

### **Table 3: Reward Breakdown (Events & Total Values)**

| Scenario | Continue Spam Penalty | Next Bonus | Skip2P1 Bonus | Stability Bonus | Early Change Penalty | Bus Penalty |
|---|---|---|---|---|---|---|
| Pr_0 | 305 events (6.10) | 2 events (6.73) | 1 event (0.30) | 33 events (5.58) | - | - |
| Pr_1 | 290 events (6.10) | 1 event (3.36) | 3 events (0.70) | 33 events (5.80) | 2 events (0.61) | 2 events (0.48) |

**Note:** Values in parentheses show total reward contribution.

### **Table 4: Phase Transition Patterns**

| Scenario | P1→P2 (times, avg duration) | P2→P1 (times, avg duration) | P2→P3 (times, avg duration) | P3→P1 (times, avg duration) | P3→P4 (times, avg duration) | P4→P1 (times, avg duration) |
|---|---|---|---|---|---|---|
| Pr_0 | 151 (35.0s) | 46 (3.0s) | 105 (3.1s) | 105 (17.1s) | - | - |
| Pr_1 | 153 (33.8s) | 45 (3.1s) | 108 (3.2s) | 95 (17.7s) | 13 (5.5s) | 13 (2.0s) |

### **Table 5: Bus Assistance Summary**

| Scenario | Bus Excellent Events | Avg Wait (s) | Total Value |
|---|---|---|---|
| Pr_0 | 1 | 4.0 | 0.15 |
| Pr_1 | 1 | 0.0 | 0.15 |

---

