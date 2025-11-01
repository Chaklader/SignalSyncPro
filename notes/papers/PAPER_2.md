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

#### **Expected Contributions:**

NOVELTY: ✓✓✓ First comprehensive XAI study for RL traffic control ✓✓ User study with domain experts (traffic engineers)
✓✓ Comparison of multiple explainability methods ✓ Practical deployment insights

EXPECTED RESULTS:

- Attention: Reveals queue length is primary factor (75% weight) ✓
- Decision tree: 92% policy fidelity, 12 rules ✓✓
- Natural language: 85% engineer trust (vs 40% black-box) ✓✓✓
- Counterfactuals: Identify edge cases for improvement ✓

PUBLICATION TARGET:

- CHI (Human-Computer Interaction) - 60% chance
- IUI (Intelligent User Interfaces) - 75% chance ✓✓
- IEEE TITS - 90% chance ✓✓✓
- XAI Workshop (NeurIPS/ICML) - 95% chance ✓✓✓

TIME ESTIMATE: 3-4 months (uses existing model!) DIFFICULTY: Medium ✓✓ IMPACT: Very High ✓✓✓ (enables adoption)

---
