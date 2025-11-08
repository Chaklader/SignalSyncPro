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
