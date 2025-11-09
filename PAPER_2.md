# Explainable Deep Reinforcement Learning for Safe Adaptive Traffic Signal Control: Interpretability and Safety Verification

## Abstract

While deep reinforcement learning (DRL) demonstrates promising performance in adaptive traffic signal control, the
black-box nature of neural network policies raises critical questions about decision transparency and operational
safety. This paper presents a simulation-based framework for explaining and analyzing the safety of DRL agent decisions
in multi-modal traffic signal control. Building upon a trained DQN-PER model evaluated across 30 diverse traffic
scenarios, we apply multiple interpretability techniques to understand how the agent makes decisions: attention
mechanisms reveal which state features (queue lengths, phase durations, pedestrian demand) influence action selection;
counterfactual analysis identifies decision boundaries through "what-if" scenarios; and policy distillation extracts
human-readable decision rules from the neural network. We systematically analyze agent behavior across critical safety
scenarios including high pedestrian demand, public transport priority, and extreme traffic conditions using SUMO
simulation. Our analysis reveals both the decision-making logic of the trained agent and identifies specific conditions
where the agent's actions align with or deviate from safe traffic control principles. The explainability framework
provides interpretable insights into neural network decisions, while the simulation-based safety analysis characterizes
agent behavior boundaries. This work demonstrates how explainability techniques can be applied to understand DRL traffic
controllers and establish a foundation for future real-world safety validation.

**Keywords:** Explainable AI, Deep Reinforcement Learning, Traffic Signal Control, Interpretability, Attention
Mechanisms, Counterfactual Explanations, Policy Distillation, Behavioral Analysis

---

## 1. Introduction

### 1.1 The Black-Box Problem in DRL Traffic Control

- DRL demonstrates superior performance in simulation (reference PAPER_1)
- Critical question: How does the agent actually make decisions?
- Black-box neural networks provide no insight into decision logic
- Need for transparency to understand agent behavior
- Foundation for future real-world deployment requires interpretability

### 1.2 Problem Statement

- **Interpretability Challenge:** Why did the agent choose action A instead of B in state S?
- **Behavioral Analysis:** What state features drive decision-making?
- **Safety Characterization:** Under what conditions does the agent make safe vs unsafe decisions?
- **Decision Boundaries:** When does the agent switch between actions?

### 1.3 Research Questions

1. What state features does the trained DRL agent prioritize when making decisions?
2. Can we extract interpretable rules that approximate the neural network policy?
3. How does the agent behave in critical safety scenarios (high pedestrian demand, emergency situations)?
4. What are the decision boundaries that cause action switching?

### 1.4 Contributions

- **Explainability Framework:** Multi-technique analysis suite applied to trained DRL model
    - Attention-based feature attribution
    - Counterfactual decision boundary analysis
    - Decision tree policy extraction
- **Safety Analysis Protocol:** Simulation-based evaluation of agent behavior in critical scenarios
- **Decision Characterization:** Systematic analysis of how agent responds to traffic conditions
- **Interpretable Insights:** Human-readable explanations of agent decision logic

### 1.5 Paper Organization

Section 2 reviews XAI literature. Section 3 summarizes the base DRL model. Section 4 presents explainability
methodologies. Section 5 describes simulation-based safety analysis. Section 6 shows results from applying these methods
to the trained agent across 30 test scenarios. Section 7 discusses findings and limitations. Section 8 concludes.

---

## 2. Related Work

### 2.1 Explainable AI (XAI)

- Post-hoc explanation methods (LIME, SHAP, attention)
- Counterfactual explanations
- Rule extraction from neural networks (TREPAN, VIPER)
- User studies on XAI effectiveness

### 2.2 XAI for Autonomous Systems

- Self-driving car explanation systems
- Robot action justification
- Medical diagnosis interpretability
- Safety-critical AI transparency requirements

### 2.3 Safety Verification for RL

- Formal verification of neural network policies
- Safe RL with constraints
- Worst-case scenario testing
- Robustness certification

### 2.4 Trust in AI Systems

- Human factors in AI deployment
- Explainability vs performance trade-offs
- Domain expert evaluation studies
- Regulatory frameworks for AI safety

---

## 3. Base DRL Model (From Paper #1)

### 3.1 Brief Overview

- DQN-PER architecture (256-256-128)
- 32-dimensional state space (queue lengths, phase states, waiting times)
- 3-action space (Continue, Skip-to-P1, Next Phase)
- Trained on 30 traffic scenarios
- Model 192 selected for explainability analysis

### 3.2 Performance Summary

- [Reference key metrics from PAPER_1]
- Demonstrates strong performance but lacks interpretability
- Motivation for explainability layer

---

## 4. Explainability Methodologies

### 4.1 Attention-Based State Attribution

#### 4.1.1 Attention Layer Addition

- Augment DQN with attention mechanism
- Attention weights over 32 state dimensions
- Visualization: Which features drive decisions?

#### 4.1.2 Interpretation Protocol

- Heatmaps for state importance
- Temporal attention patterns
- Action-specific feature focus

#### 4.1.3 Example Explanations

- "Agent prioritizes queue length on approach lane (attention weight: 0.42)"
- "Pedestrian waiting time receives high attention before ped phase activation"

### 4.2 Counterfactual Explanation Generation

#### 4.2.1 Methodology

- Minimal state perturbations that flip decision
- "If queue was X cars instead of Y, action would have been Z"
- Actionable insights for operators

#### 4.2.2 Counterfactual Search Algorithm

- Gradient-based perturbation
- Constraint satisfaction (realistic states only)
- Multiple counterfactual generation

#### 4.2.3 Example Counterfactuals

- "If car queue was 5 instead of 10, would have extended green by 5s"
- "If bus wasn't present, would not have activated Skip-to-P1"

### 4.3 Decision Tree Policy Extraction

#### 4.3.1 VIPER Algorithm Application

- Distill DQN policy into interpretable decision tree
- Iterative dataset aggregation
- Tree pruning for simplicity

#### 4.3.2 Tree Structure and Rules

- Maximum depth: 8 levels
- ~90% fidelity to original DQN policy
- Human-readable if-then rules

#### 4.3.3 Example Rule

```
IF queue_major > 15 AND phase_duration > 30 AND no_pedestrian_demand
  THEN Continue (confidence: 94%)
ELSE IF queue_minor > 8 AND phase == P1
  THEN Next (confidence: 87%)
```

### 4.4 Saliency Maps and Gradient-Based Attribution

#### 4.4.1 Gradient Computation

- ∂Q(s,a)/∂s for each state dimension
- Identifies sensitivity of Q-values to state changes

#### 4.4.2 Visualization Methods

- Per-action saliency maps
- Temporal saliency evolution
- Critical state dimension identification

### 4.5 Natural Language Explanation Generation

#### 4.5.1 Template-Based System

- Action templates: "Extended green because {reason}"
- Reason extraction from attention + saliency
- Context-aware explanation selection

#### 4.5.2 Example Generated Explanations

- "Maintained current phase due to high vehicle queue (18 cars) on major approach"
- "Activated Skip-to-P1 to prioritize bus on main corridor (wait time: 23s)"
- "Switched to pedestrian phase as 8 pedestrians waiting exceeded threshold"

---

## 5. Simulation-Based Safety Analysis

### 5.1 Critical Scenario Design

#### 5.1.1 Pedestrian Safety Scenarios

- High pedestrian demand scenarios (Pe_7 to Pe_9: 800-1000 peds/hr)
- Analyzing agent's pedestrian phase activation patterns
- Measuring pedestrian waiting times
- Comparing against safe thresholds (e.g., max wait < 90s)

#### 5.1.2 High-Volume Traffic Scenarios

- Extreme car volumes (Pr_7 to Pr_9: 800-1000 cars/hr)
- Extreme bicycle volumes (Bi_7 to Bi_9: 800-1000 bikes/hr)
- Agent behavior under congestion
- Queue buildup and clearance patterns

#### 5.1.3 Mixed Demand Scenarios

- Competing modal priorities (high cars + high peds)
- Bus arrival timing analysis
- Multi-modal conflict resolution
- Action selection under competing demands

### 5.2 Safety Metrics from Simulation

#### 5.2.1 Operational Safety Indicators

- **Phase Duration Compliance:** % of phase changes respecting MIN_GREEN_TIME
- **Maximum Waiting Time:** Longest wait experienced by any mode
- **Pedestrian Service:** % of high-demand periods where ped phase activated
- **Action Blocking:** % of attempted actions blocked by safety constraints
- **Emergency Response:** Agent behavior when bus approaches

#### 5.2.2 Behavioral Analysis Methods

- Replay 30 test scenarios from Tables/1_Single_Agent.md
- Log all state-action pairs
- Identify potential safety violations
- Compare agent decisions to safety rules

### 5.3 Decision Pattern Analysis

#### 5.3.1 Action Selection Under Critical Conditions

- What does agent do when queue > 20 vehicles?
- How does agent respond to pedestrian demand > 6 people?
- When does agent activate Skip-to-P1 for bus priority?
- Phase switching patterns under congestion

#### 5.3.2 Edge Case Identification

- Scenarios where agent makes questionable decisions
- States where action choice seems suboptimal
- Conditions leading to blocked actions
- Instances of very long waiting times

### 5.4 Safety Boundary Characterization

#### 5.4.1 Safe Operating Region

- Traffic volume ranges where agent performs well
- Modal balance conditions for reliable operation
- State space regions with consistent safe decisions

#### 5.4.2 Concerning Behaviors

- Conditions where agent ignores high pedestrian demand
- Situations with excessive phase duration
- Cases of modal starvation (one mode waiting too long)
- Action sequences that could indicate unsafe logic

---

## 6. Results: Understanding Agent Decision-Making

### 6.1 Attention-Based Feature Analysis

#### 6.1.1 State Feature Importance

- Analysis of attention weights across 30 test scenarios
- Which state dimensions receive highest attention during each action?
- Consistency of attention patterns across similar traffic states
- Temporal evolution of attention during episode progression

#### 6.1.2 Action-Specific Attention Patterns

- **Continue Action:** Attention focused on current phase queue lengths
- **Skip-to-P1 Action:** Attention focused on bus waiting times and Phase 1 demand
- **Next Phase Action:** Attention focused on alternative phase queues and duration
- Visualization of attention heatmaps for representative scenarios

### 6.2 Counterfactual Analysis Results

#### 6.2.1 Decision Boundary Identification

- "If queue was X instead of Y, action would change from A to B"
- Minimal perturbations required to flip action decisions
- Sensitivity analysis: which state changes most affect decisions?
- State space regions with stable vs unstable action preferences

#### 6.2.2 Critical Thresholds Discovered

- Queue length thresholds triggering action switches
- Phase duration tipping points for phase changes
- Pedestrian demand levels affecting action selection
- Bus waiting time thresholds for Skip-to-P1 activation

### 6.3 Decision Tree Policy Extraction

#### 6.3.1 Extracted Rule Structure

- Tree depth: X levels
- Number of decision nodes: Y
- Fidelity to original DQN policy: Z% agreement
- Top-level rules capturing majority of decisions

#### 6.3.2 Example Interpretable Rules

```
[Actual rules extracted from trained model to be added]
```

#### 6.3.3 Rule Analysis

- Which rules fire most frequently?
- Conditions that lead to each action
- Comparison with domain expert heuristics

### 6.4 Safety Analysis Across Test Scenarios

#### 6.4.1 Pedestrian Safety Performance

- Pe_7, Pe_8, Pe_9 analysis (800-1000 pedestrians/hr)
- Pedestrian phase activation frequency
- Maximum pedestrian waiting times observed
- Comparison against safety threshold (e.g., 90s max wait)

#### 6.4.2 High-Volume Scenario Behavior

- Agent performance in Pr_9 (1000 cars/hr) and Bi_9 (1000 bikes/hr)
- Queue management effectiveness
- Phase cycling patterns under congestion
- Identification of any modal starvation

#### 6.4.3 Action Distribution in Critical States

- What actions does agent select under high demand?
- Frequency of Skip-to-P1 when bus present
- Continue vs Next Phase decisions under congestion
- Blocked action rates in different scenarios

#### 6.4.4 Potential Safety Concerns Identified

- Scenarios with longer-than-expected waiting times
- Cases where pedestrian demand might be underserved
- Situations with very high action blocking rates
- Edge cases requiring further investigation

---

## 7. Discussion

### 7.1 Insights from Explainability Analysis

#### 7.1.1 What We Learned About Agent Decision-Making

- Attention analysis reveals which state features drive decisions
- Counterfactual analysis identifies decision boundaries and thresholds
- Decision tree extraction provides interpretable approximation of policy
- Multi-method approach gives complementary perspectives on agent logic

#### 7.1.2 Understanding Agent Behavior Patterns

- Agent's decision logic can be characterized through explainability techniques
- State feature priorities vary by action type
- Decision boundaries are identifiable through systematic analysis
- Some decisions align with traffic engineering intuition, others require deeper investigation

### 7.2 Safety Analysis Findings

#### 7.2.1 Behavioral Characterization

- Agent behavior analyzed across 30 diverse traffic scenarios
- Critical scenarios reveal strengths and potential weaknesses
- Action selection patterns under high demand identified
- Edge cases requiring further investigation documented

#### 7.2.2 Simulation-Based Safety Assessment

- Operational metrics (waiting times, phase durations) measurable
- Agent behavior in pedestrian safety scenarios characterized
- High-volume traffic handling patterns understood
- Potential safety concerns identified for future work

### 7.3 Limitations

#### 7.3.1 Explainability Method Limitations

- Post-hoc explanations may not reflect true neural network computation
- Attention weights show correlation, not causation
- Decision tree fidelity involves approximation error
- Counterfactuals limited to feasible state perturbations

#### 7.3.2 Analysis Scope Limitations

- Analysis based on simulation only, not real-world data
- Limited to 30 test scenarios defined in study
- State space coverage incomplete (infinite possible states)
- No real traffic engineer validation of explanations
- No actual deployment testing

#### 7.3.3 Safety Analysis Limitations

- Simulation may not capture all real-world edge cases
- Safety assessment qualitative, not formal verification
- Sensor failure modes not tested
- Weather and lighting conditions not modeled
- No testing with actual vulnerable road users

### 7.4 Future Work

#### 7.4.1 Expanding Explainability Analysis

- Apply methods to additional trained models
- Compare explanation consistency across training runs
- Develop interactive explanation interfaces
- Validate explanations with domain experts

#### 7.4.2 Enhancing Safety Analysis

- Expand test scenarios to cover more edge cases
- Introduce perturbations and sensor noise
- Test with different traffic demand patterns
- Analyze failure modes systematically
- Compare with traditional controllers on safety metrics

#### 7.4.3 Toward Real-World Validation

- Conduct user studies with traffic engineers
- Establish formal safety verification protocols
- Pilot testing in controlled environments
- Integration with traffic management systems
- Real-world deployment with safety monitoring

---

## 8. Conclusion

### 8.1 Summary

This work demonstrates how explainability techniques can be applied to understand DRL-based traffic signal controllers
trained for multi-modal traffic management. We applied multiple interpretation methods—attention mechanisms,
counterfactual analysis, and decision tree extraction—to a trained DQN-PER agent evaluated across 30 traffic scenarios.
The explainability framework reveals which state features influence agent decisions, identifies decision boundaries
through counterfactual analysis, and extracts interpretable rules approximating the neural network policy.
Simulation-based safety analysis characterizes agent behavior in critical scenarios including high pedestrian demand,
extreme traffic volumes, and competing modal priorities. This analysis identifies both strengths (effective queue
management, modal balance) and areas requiring further investigation (edge case behaviors, action blocking patterns).
The work provides a methodological foundation for analyzing DRL traffic controllers and establishes a starting point for
future real-world validation studies.

### 8.2 Contributions to the Field

- Demonstrates application of XAI techniques to traffic signal control domain
- Provides multi-method framework for understanding DRL agent decision logic
- Characterizes agent behavior across diverse traffic scenarios through simulation
- Identifies the importance of explainability for understanding learned control policies
- Establishes methodology for simulation-based safety analysis of DRL controllers

### 8.3 Path Forward

While this work demonstrates explainability techniques in simulation, significant additional work is needed before
real-world deployment: validation with traffic engineering experts, formal safety verification, testing with actual
sensor data, pilot deployments with monitoring, and integration with existing traffic management infrastructure. The
methods presented here provide tools for understanding what DRL agents learn, which is an essential step toward building
deployable systems.

---

## References

[To be added - include PAPER_1 as primary reference]

---

## Appendices

### Appendix A: Attention Mechanism Architecture

[Technical specifications of attention layer added to DQN] [Mathematical formulation of attention weights]
[Implementation details]

### Appendix B: Counterfactual Generation Algorithm

[Gradient-based perturbation method] [Constraint satisfaction for realistic states] [Search procedure for minimal
perturbations]

### Appendix C: Decision Tree Extraction Implementation

[VIPER/TREPAN algorithm details] [Hyperparameters for tree extraction] [Fidelity measurement methodology]

### Appendix D: Test Scenario Specifications

[30 traffic scenarios from Tables/1_Single_Agent.md] [Traffic volume ranges: Pr_0-9, Bi_0-9, Pe_0-9] [Constant:
15-minute bus frequency]

### Appendix E: Explainability Method Comparison

[Strengths and weaknesses of each technique] [Computational costs] [Complementary insights provided]

### Appendix F: Sample State-Action Logs

[Representative state vectors with agent decisions] [Explanation outputs for each method] [Critical scenario
state-action sequences]

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
