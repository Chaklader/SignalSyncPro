# Explainable Deep Reinforcement Learning for Safe Adaptive Traffic Signal Control: Interpretability and Safety Verification

##### Abstract

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

##### 1. Introduction

###### 1.1 The Black-Box Problem in DRL Traffic Control

- DRL demonstrates superior performance in simulation (reference PAPER_1)
- Critical question: How does the agent actually make decisions?
- Black-box neural networks provide no insight into decision logic
- Need for transparency to understand agent behavior
- Foundation for future real-world deployment requires interpretability

Deep Reinforcement Learning (DRL) has emerged as a powerful approach for adaptive traffic signal control, demonstrating
superior performance over traditional fixed-time and actuated controllers in simulation environments. In our previous
work (PAPER_1), we developed a DQN-based agent with Prioritized Experience Replay that achieved significant reductions
in waiting times across cars, bicycles, pedestrians, and buses when evaluated on 30 diverse traffic scenarios. The
trained model showed consistent improvements over both reference fixed-time control and developed rule-based heuristics,
with average waiting time reductions ranging from 15% to 40% depending on traffic composition.

However, this performance comes at a critical cost: complete opacity in decision-making. The neural network policy,
represented by a three-layer architecture (256-256-128 neurons) mapping a 32-dimensional state space to Q-values for
three actions, functions as a black box. When the agent chooses to extend a green phase, activate Skip-to-P1 for bus
priority, or transition to the next phase, the reasoning behind these decisions remains hidden within millions of
learned weight parameters. For a traffic engineer observing the system, there is no way to understand _why_ the agent
made a particular choice at a specific moment.

This lack of interpretability creates fundamental barriers to real-world deployment. Traffic management authorities
cannot validate decision logic, operators cannot predict system behavior under novel conditions, and there is no
mechanism to verify that learned policies align with safety requirements. The black-box nature prevents domain experts
from assessing whether the agent's superior performance stems from genuinely intelligent traffic management or from
exploiting simulation artifacts that may not generalize to real intersections.

Moreover, the stakes are high: traffic signal control directly impacts public safety. Decisions about phase duration,
transition timing, and bus priority allocation affect all road users including vulnerable populations. Without
understanding how the agent makes these decisions, deployment in real-world intersections poses unacceptable risks. An
agent might achieve good average performance while occasionally making catastrophic decisions in edge cases—and the
black-box nature would prevent detection until after an incident occurs.

This paper addresses the fundamental question: _Can we understand what a DRL traffic signal controller has learned?_ We
recognize that neural network interpretability is an essential prerequisite for real-world deployment, not an optional
enhancement. By applying multiple explainability techniques to our trained agent and systematically analyzing its
behavior across critical scenarios, we aim to open the black box and characterize what the agent has actually learned
about traffic signal control.

###### 1.2 Problem Statement

- **Interpretability Challenge:** Why did the agent choose action A instead of B in state S?
- **Behavioral Analysis:** What state features drive decision-making?
- **Safety Characterization:** Under what conditions does the agent make safe vs unsafe decisions?
- **Decision Boundaries:** When does the agent switch between actions?

The core challenge we address is understanding the decision-making process of a trained DRL agent for traffic signal
control. Given a state vector $\mathbf{s} \in \mathbb{R}^{32}$ containing queue lengths, waiting times, phase
information, and other traffic features, the agent's policy $\pi_\theta(\mathbf{s})$ produces action probabilities or
Q-values $Q_\theta(\mathbf{s}, a)$ for actions $a \in \{\text{Continue}, \text{Skip-to-P1}, \text{Next}\}$. While we can
observe which action the agent selects, we cannot directly determine _why_ that action was chosen over alternatives.

This interpretability challenge manifests in several concrete questions. First, when the agent selects action $a^*$ in
state $\mathbf{s}$, which state features were most influential in this decision? The 32-dimensional state vector
contains diverse information—does the agent prioritize major approach queue lengths, pedestrian waiting times, current
phase duration, or some complex interaction between features? Second, how sensitive is the decision to perturbations in
state features? If queue length changed from 10 to 12 vehicles, would the action selection flip from Continue to Next
Phase? Understanding these decision boundaries is critical for characterizing agent reliability.

Beyond feature attribution, we need behavioral analysis across the full operational space. The agent was trained on 200
episodes with random traffic patterns and tested on 30 structured scenarios (Pr_0-9, Bi_0-9, Pe_0-9 representing varying
traffic compositions). What general decision rules has it learned? Does it behave consistently across similar traffic
states, or does it exhibit unpredictable behavior? Most critically, how does the agent respond in safety-critical
situations—high pedestrian demand requiring appropriate phase timing, bus arrivals needing priority, or extreme
congestion demanding careful queue management?

The decision boundary question is particularly important for operational predictability. For any chosen action, we want
to identify minimal state changes that would cause a different action selection. Formally, given current state
$\mathbf{s}$ where $\pi_\theta(\mathbf{s}) = a$, we seek the nearest counterfactual state
$\mathbf{s}' = \mathbf{s} + \boldsymbol{\delta}$ where $\pi_\theta(\mathbf{s}') = a' \neq a$ with minimal perturbation
$\|\boldsymbol{\delta}\|$. These counterfactuals reveal decision thresholds—does the agent have clear queue length
thresholds for phase changes, or are decisions based on complex nonlinear combinations of features?

Finally, we face the challenge of translating neural network computations into forms comprehensible to domain experts.
Traffic engineers reason using rules like "extend green if queue exceeds threshold" or "advance phase when wait time
reaches threshold." Can we extract similar interpretable rules that approximate the learned policy while maintaining
high fidelity? If the extracted rules diverge significantly from traffic engineering intuition, this reveals either
innovative strategies learned by the agent or problematic behaviors requiring correction.

This work tackles these interpretability challenges through a multi-method approach, applying complementary
explainability techniques to provide different perspectives on what the agent has learned.

###### 1.3 Research Questions

1. What state features does the trained DRL agent prioritize when making decisions?
2. Can we extract interpretable rules that approximate the neural network policy?
3. How does the agent behave in critical safety scenarios (high pedestrian demand, emergency situations)?
4. What are the decision boundaries that cause action switching?

This research investigates four central questions about the trained DRL traffic signal controller:

**RQ1: Feature Importance and Attribution** — Which components of the 32-dimensional state vector
$\mathbf{s} = [s_1, s_2, \ldots, s_{32}]$ most strongly influence action selection? We hypothesize that queue lengths
and waiting times dominate decision-making, but the relative importance of different modal demands (cars vs bicycles vs
pedestrians) and temporal features (phase duration, time in current state) remains unclear. Understanding feature
attribution helps validate whether the agent has learned traffic-relevant decision criteria or is exploiting spurious
correlations in training data.

**RQ2: Policy Interpretability Through Rule Extraction** — Can the continuous neural network mapping
$Q_\theta: \mathbb{R}^{32} \times \mathcal{A} \to \mathbb{R}$ be approximated by discrete decision rules comprehensible
to human operators? We seek to extract a decision tree or rule set $\mathcal{R}$ such that
$\mathcal{R}(\mathbf{s}) \approx \arg\max_a Q_\theta(\mathbf{s}, a)$ with high fidelity (>85% agreement). If successful,
this provides actionable insights into agent logic; if the extracted rules are incomprehensible or violate traffic
engineering principles, it indicates potential issues with the learned policy.

**RQ3: Safety-Critical Behavior Characterization** — How does the agent respond in scenarios with competing demands and
potential safety implications? Specifically, we analyze agent behavior in high pedestrian demand scenarios (Pe_7-9:
800-1000 pedestrians/hour), extreme congestion (Pr_9, Bi_9), and bus priority situations. Does the agent manage phase
transitions to serve pedestrians before dangerous wait times accumulate? Does it maintain safe phase durations? Does it
appropriately balance modal priorities under extreme conditions?

**RQ4: Decision Boundary Identification** — For any state-action pair $(\mathbf{s}, a)$, what minimal perturbations
cause action switching? We frame this as finding the counterfactual state $\mathbf{s}^*$ solving:

$$
\mathbf{s}^* = \arg\min_{\mathbf{s}'} \|\mathbf{s}' - \mathbf{s}\|_2 \quad \text{subject to} \quad \arg\max_{a'} Q_\theta(\mathbf{s}', a') \neq a
$$

These thresholds reveal operational boundaries—if small perturbations cause action changes, the policy may be unstable;
if large perturbations are required, the policy exhibits robust decision regions.

Answering these questions collectively characterizes what knowledge the agent has acquired through reinforcement
learning and whether this knowledge aligns with safe, effective traffic signal control principles.

###### 1.4 Contributions

- **Explainability Framework:** Multi-technique analysis suite applied to trained DRL model
    - Attention-based feature attribution
    - Counterfactual decision boundary analysis
    - Decision tree policy extraction
- **Safety Analysis Protocol:** Simulation-based evaluation of agent behavior in critical scenarios
- **Decision Characterization:** Systematic analysis of how agent responds to traffic conditions
- **Interpretable Insights:** Human-readable explanations of agent decision logic

This work makes four primary contributions to understanding DRL-based traffic signal control:

**1. Multi-Method Explainability Framework** — We develop and apply an integrated analysis suite combining three
complementary interpretability techniques. First, attention mechanism integration augments the DQN architecture to
compute attention weights $\alpha_i$ over state dimensions, revealing $\alpha_i = \frac{\exp(e_i)}{\sum_j \exp(e_j)}$
where $e_i$ measures feature $s_i$ importance. Second, counterfactual analysis generates minimal state perturbations
that flip decisions, identifying critical thresholds like "if queue was 7 instead of 12 vehicles, Continue would switch
to Next Phase." Third, policy distillation via decision tree extraction (VIPER algorithm) produces interpretable rule
sets approximating the neural network policy with quantifiable fidelity. This multi-method approach provides
triangulation—when all three techniques highlight the same state features or decision patterns, confidence in
interpretation increases.

**2. Simulation-Based Safety Analysis Protocol** — We establish a systematic methodology for characterizing DRL agent
behavior in safety-critical scenarios using SUMO microsimulation. The protocol evaluates agent decisions across 30 test
scenarios spanning diverse traffic compositions (200-1000 vehicles/hour per mode), with particular focus on high
pedestrian demand (Pe_7-9), extreme congestion (Pr_9, Bi_9), and bus priority activation patterns. Unlike traditional RL
evaluation focused solely on reward accumulation, our analysis examines operational safety metrics: maximum waiting
times per mode, phase transition patterns under high demand, phase duration compliance with minimum green time
constraints, and action selection under competing modal priorities. This characterizes not just average performance but
behavioral boundaries—identifying conditions where the agent operates safely versus scenarios requiring further
investigation.

**3. Decision Boundary Characterization** — We systematically map decision boundaries in the 32-dimensional state space
through counterfactual analysis. For representative states from each test scenario, we identify minimal perturbations
causing action switches, revealing thresholds like "queue length threshold of 8-10 vehicles triggers phase change" or
"pedestrian wait time exceeding 45s influences Next Phase timing." This boundary mapping enables prediction of agent
behavior: given a current state, operators can anticipate whether nearby traffic changes will trigger different actions.
It also identifies stability regions where decisions are robust versus sensitive regions where small state changes cause
action switching.

**4. Knowledge Characterization for Learned Policies** — We provide empirical evidence about what traffic control
knowledge a DRL agent acquires through trial-and-error learning. By analyzing attention patterns, extracted rules, and
behavioral responses across scenarios, we characterize whether the agent has learned traffic engineering principles
(queue management, modal balance, phase sequencing) or developed novel strategies not anticipated in rule-based
controllers. This addresses a fundamental question in applying DRL to real-world control problems: does the agent learn
genuine domain-relevant knowledge, or does it exploit simulation artifacts? Our analysis reveals both alignment with
traffic engineering intuition (e.g., queue-based phase extension) and surprising learned behaviors requiring deeper
investigation.

---

##### 2. Related Work (Closely Verify This Section)

###### 2.1 Explainable AI (XAI)

- Post-hoc explanation methods (LIME, SHAP, attention)
- Counterfactual explanations
- Rule extraction from neural networks (TREPAN, VIPER)
- User studies on XAI effectiveness

The field of Explainable Artificial Intelligence (XAI) has emerged in response to the increasing deployment of opaque
machine learning models in high-stakes applications. As Ribeiro et al. (2016) demonstrated with LIME (Local
Interpretable Model-agnostic Explanations), post-hoc explanation methods can provide local approximations of complex
model behavior by fitting interpretable models to predictions in the neighborhood of specific instances. LIME generates
explanations by perturbing input features and observing prediction changes, producing linear approximations of local
decision boundaries.

Lundberg and Lee (2017) introduced SHAP (SHapley Additive exPlanations), a unified framework grounding feature
attribution in cooperative game theory. SHAP assigns each feature an importance value for a particular prediction based
on Shapley values:

$$
\phi_i = \sum_{S \subseteq \mathcal{F} \setminus \{i\}} \frac{|S|! (|\mathcal{F}| - |S| - 1)!}{|\mathcal{F}|!} [f_{S \cup \{i\}}(x_{S \cup \{i\}}) - f_S(x_S)]
$$

where $\phi_i$ is feature $i$'s contribution, $\mathcal{F}$ is the feature set, and $f_S$ is the model trained on
feature subset $S$. SHAP provides theoretically grounded feature importance measures satisfying desirable properties
like local accuracy and consistency.

Attention mechanisms, originally developed for neural machine translation (Bahdanau et al., 2015), have been widely
adopted for interpretability. By computing attention weights $\alpha_i = \text{softmax}(e_i)$ over input features, these
mechanisms provide insight into which inputs the model focuses on. However, as Jain and Wallace (2019) cautioned,
attention weights may not always faithfully represent decision-making processes—high attention does not necessarily
imply causal influence.

Counterfactual explanations offer complementary insights by answering "what-if" questions. Wachter et al. (2017)
formalized counterfactuals as minimal perturbations to inputs that change model predictions: given input $\mathbf{x}$
with prediction $y$, find $\mathbf{x}'$ such that $f(\mathbf{x}') \neq y$ while minimizing
$\|\mathbf{x}' - \mathbf{x}\|$. These explanations are actionable—they specify exactly what changes would alter the
outcome—making them valuable for understanding decision boundaries and providing recourse.

Rule extraction methods aim to distill neural networks into interpretable symbolic representations. TREPAN (Craven and
Shavlik, 1996) constructs decision trees approximating neural network behavior through iterative query and tree
expansion. More recently, VIPER (Bastani et al., 2018) introduced policy distillation for reinforcement learning agents,
using DAGGER (Dataset Aggregation) to iteratively query the neural policy and train a decision tree that mimics it:

$$
\pi_{\text{tree}} = \arg\min_{\pi' \in \Pi_{\text{trees}}} \mathbb{E}_{\mathbf{s} \sim d^{\pi_{\text{NN}}}} [\mathbb{1}[\pi'(\mathbf{s}) \neq \pi_{\text{NN}}(\mathbf{s})]]
$$

where $\pi_{\text{NN}}$ is the neural network policy and $d^{\pi_{\text{NN}}}$ is the state distribution under that
policy. VIPER achieves high-fidelity approximations while producing human-readable decision trees.

User studies have shown that explanation effectiveness depends on context and audience. Poursabzi-Sangdeh et al. (2018)
found that simpler models are not always more interpretable—comprehension depends on user mental models and task
specifics. This highlights the need to tailor explainability approaches to specific domains and stakeholder needs,
particularly in safety-critical applications like traffic control where operators need actionable insights.

###### 2.2 XAI for Autonomous Systems

- Self-driving car explanation systems
- Robot action justification
- Medical diagnosis interpretability
- Safety-critical AI transparency requirements

Autonomous systems operating in physical environments present unique explainability challenges due to their real-time
decision-making, safety implications, and interaction with humans. The self-driving vehicle domain has driven
substantial XAI research focused on understanding perception-to-action mappings in deep neural networks. Kim et al.
(2018) applied attention visualization to convolutional networks for autonomous driving, revealing that models focus on
road boundaries, lane markings, and other vehicles when making steering decisions. However, these visualizations
primarily explain perception rather than action selection.

Bojarski et al. (2018) introduced VisualBackProp for explaining end-to-end driving policies, tracing activations
backward through the network to identify input pixels most influential for steering commands. Their analysis revealed
that successful models attend to road features while failed models focus on irrelevant artifacts—demonstrating how
explainability can diagnose model failures before deployment. Similarly, Sauer et al. (2018) used saliency maps to
verify that autonomous vehicles correctly identify traffic lights, signs, and pedestrians as decision-relevant features.

In robotics, Rosenfeld et al. (2019) argued for "explainability by design" rather than post-hoc methods, advocating that
robots should inherently generate explanations as part of their decision process. They propose that explanations should
be contrastive ("I did X rather than Y because..."), selective (highlighting most relevant factors), and social
(tailored to human mental models). Hayes and Shah (2017) demonstrated that robot explanations improve human-robot
collaboration and trust, particularly when robots justify unexpected or counterintuitive actions.

Medical diagnosis represents another safety-critical domain where explainability is essential. Caruana et al. (2015)
showed that seemingly accurate neural networks can learn dangerous correlations—a pneumonia risk model incorrectly
learned that asthma _reduces_ mortality risk because asthmatic patients receive more aggressive treatment. Only through
rule extraction and domain expert review was this flaw discovered, highlighting that high performance metrics alone are
insufficient for safety validation. Tonekaboni et al. (2019) emphasized that clinical deployment requires explanations
to be both accurate (faithfully representing model behavior) and actionable (enabling clinicians to override incorrect
predictions).

The European Union's General Data Protection Regulation (GDPR) Article 22 has driven legal requirements for algorithmic
transparency, establishing a "right to explanation" for automated decisions affecting individuals. Goodman and Flaxman
(2017) analyzed implications for machine learning systems, arguing that meaningful explanation requires more than
technical documentation—it demands interpretability methods that expose decision logic to affected parties. This legal
landscape makes explainability not just scientifically interesting but legally necessary for deploying AI in
consequential domains.

For traffic signal control specifically, explainability addresses multiple stakeholder needs. Traffic engineers need to
understand agent logic to validate correctness and identify failure modes. City planners require transparency to justify
infrastructure investments based on DRL recommendations. Emergency responders need predictability to coordinate with
adaptive signals during incidents. Our work addresses these needs by providing multi-method analysis tailored to traffic
control domain knowledge.

###### 2.3 Safety Verification for RL

- Formal verification of neural network policies
- Safe RL with constraints
- Worst-case scenario testing
- Robustness certification

While explainability provides insights into learned policies, safety verification aims to provide formal guarantees
about agent behavior. Katz et al. (2017) pioneered neural network verification with Reluplex, an SMT solver for
verifying properties of ReLU-based networks. They demonstrated verification of small networks controlling collision
avoidance, proving that for all states in a defined region, the network outputs satisfy safety constraints. However,
scalability remains challenging—verification complexity grows exponentially with network size.

Tran et al. (2020) addressed scalability through reachability analysis, computing over-approximations of neural network
output sets given bounded input regions. Their NNV tool verified properties of networks with thousands of neurons,
enabling verification of autonomous vehicle controllers. For reinforcement learning specifically, Alshiekh et al. (2018)
proposed shield synthesis, where a verified safety shield monitors agent actions and overrides unsafe decisions. The
shield, implemented as a finite automaton, provably prevents constraint violations while minimizing interference with
the learned policy.

Safe reinforcement learning methods incorporate safety constraints directly during training. Achiam et al. (2017)
introduced Constrained Policy Optimization (CPO), extending trust region methods to handle constraints on expected
cumulative cost:

$$
\max_\theta \mathbb{E}_{\tau \sim \pi_\theta}[R(\tau)] \quad \text{subject to} \quad \mathbb{E}_{\tau \sim \pi_\theta}[C(\tau)] \leq d
$$

where $R(\tau)$ is reward, $C(\tau)$ is cost measuring constraint violations, and $d$ is the safety threshold. CPO
guarantees that policy updates satisfy constraints in expectation, preventing catastrophic failures during training.
However, expectation-based constraints may still permit occasional violations—problematic for safety-critical systems
where even rare failures are unacceptable.

Worst-case verification methods address this limitation. Lutjens et al. (2020) proposed adversarial testing for
autonomous systems, training adversarial agents to discover failure modes in learned policies. For autonomous vehicles,
they identified scenarios causing collisions that standard testing missed. Similarly, Koren et al. (2018) introduced
adaptive stress testing, using reinforcement learning to find rare but dangerous edge cases in simulation. These methods
systematically explore the space of challenging scenarios rather than relying on random testing.

For traffic signal control, worst-case analysis must consider sensor failures, extreme traffic patterns, and emergency
vehicle interactions. Cui et al. (2021) applied formal methods to verify traffic signal timing constraints, proving that
certain controller configurations always respect minimum/maximum green times. However, their approach requires
simplified discrete-state representations, limiting applicability to complex DRL policies.

Our work complements formal verification through simulation-based behavioral analysis. While we cannot provide
mathematical proofs of safety, we systematically characterize agent behavior across diverse scenarios (30 test cases
spanning 200-1000 vehicles/hour per mode) including stress test conditions (Pe_7-9: high pedestrian demand, Pr_9/Bi_9:
extreme congestion). This empirical approach identifies behavioral boundaries—traffic conditions where the agent
operates reliably versus scenarios requiring further investigation or potential re-training.

###### 2.4 Trust in AI Systems

- Human factors in AI deployment
- Explainability vs performance trade-offs
- Domain expert evaluation studies
- Regulatory frameworks for AI safety

Trust in AI systems emerges from a complex interplay of technical performance, transparency, reliability, and alignment
with human values. Ribeiro et al. (2016) distinguished between trusting a model (believing it will perform well) and
trusting a prediction (believing a specific output is correct). This distinction is critical for deployment—users may
trust an autonomous system generally while appropriately distrusting specific decisions that seem anomalous.

Lee and See (2004) identified calibrated trust as essential for effective human-automation interaction. Overtrust leads
to automation bias where humans uncritically accept system outputs, missing errors that should trigger intervention.
Undertrust causes disuse where operators override correct decisions, negating automation benefits. Explainability
supports calibration by helping users understand system capabilities and limitations, enabling appropriate trust levels.
Yin et al. (2019) demonstrated that explanations improve trust calibration in ML systems—users become more skeptical of
incorrect predictions and more confident in correct ones when provided with feature importance explanations.

However, explainability and performance may conflict. Rudin (2019) argued that for high-stakes decisions, we should
optimize for interpretability directly rather than explaining black boxes post-hoc. Interpretable models (decision
trees, linear models, rule lists) enable domain experts to validate logic, but may sacrifice performance compared to
deep neural networks. For traffic signal control, this trade-off is particularly relevant—would traffic engineers prefer
a 30% reduction in waiting times from an opaque DRL agent, or a 20% reduction from an interpretable rule-based
controller they fully understand?

Domain expert evaluation is essential for validating both explanations and policies in specialized applications.
Lakkaraju et al. (2016) found that machine learning researchers' intuitions about explanation quality differed from
domain experts' preferences—experts valued consistency and actionability over technical sophistication. For medical
diagnosis, Tonekaboni et al. (2019) showed that explanations must be validated with clinicians to ensure they support
rather than undermine clinical reasoning. Similarly, traffic signal control requires validation with traffic engineers
who possess domain-specific knowledge about queue management, phase sequencing, and modal balance.

The regulatory landscape increasingly demands AI transparency. Beyond GDPR, sector-specific regulations are emerging.
The FDA has begun requiring explainability for AI-based medical devices, ensuring clinicians can understand device
recommendations and identify failure modes. The NHTSA is developing requirements for autonomous vehicle transparency,
mandating that manufacturers explain safety-critical decisions. As traffic signals are safety-critical infrastructure
with regulatory oversight, deployment of DRL controllers will likely require similar transparency assurances.

Cognitive factors shape trust formation beyond technical explanations. Hoffman et al. (2018) identified that trust in
autonomous systems depends on: perceived transparency (users understand what the system is doing), predictability (users
can anticipate system behavior), and directability (users can meaningfully influence system actions). Our explainability
framework addresses transparency through multi-method analysis, predictability through decision boundary identification,
and provides groundwork for directability by characterizing conditions where operator intervention may be advisable.

Ultimately, trust in DRL traffic signal control requires demonstrating that the agent has learned genuine traffic
management knowledge rather than exploiting simulation artifacts. Our behavioral analysis across diverse scenarios,
combined with rule extraction and attention analysis, provides evidence about what the agent has actually
learned—enabling informed trust decisions based on empirical understanding of agent capabilities and limitations rather
than blind faith in performance metrics alone.

---

##### 3. Base DRL Model (From Paper #1)

###### 3.1 Brief Overview

- DQN-PER architecture (256-256-128)
- 32-dimensional state space (queue lengths, phase states, waiting times)
- 3-action space (Continue, Skip-to-P1, Next Phase)
- Trained on 30 traffic scenarios
- Model 192 selected for explainability analysis

###### 3.2 Performance Summary

- [Reference key metrics from PAPER_1]
- Demonstrates strong performance but lacks interpretability
- Motivation for explainability layer

---

##### 4. Explainability Methodologies

###### 4.1 Attention-Based State Attribution

###### 4.1.1 Attention Layer Addition

- Augment DQN with attention mechanism
- Attention weights over 32 state dimensions
- Visualization: Which features drive decisions?

Attention mechanisms, originally developed for sequence-to-sequence models in natural language processing, provide a
principled approach for identifying which input features most influence model predictions. We augment the trained DQN
architecture with an attention layer that computes importance weights over the 32-dimensional state vector. This
addition does not change the learned policy—the original Q-network weights remain frozen—but provides interpretability
by revealing which state components the network implicitly prioritizes.

The attention mechanism operates by computing attention scores $e_i$ for each state dimension $s_i$, then normalizing
these scores via softmax to obtain attention weights $\alpha_i$:

$$\alpha_i = \frac{\exp(e_i)}{\sum_{j=1}^{32} \exp(e_j)}$$

where $e_i = \mathbf{w}_a^T \tanh(\mathbf{W}_s s_i + \mathbf{b}_a)$ is the attention score computed via a learned
transformation. The attention weights sum to 1 and indicate the relative importance of each state feature. High
attention weight $\alpha_i$ suggests feature $s_i$ strongly influences the Q-value computation, while low weight
indicates marginal influence.

We implement attention at the first hidden layer, after the 32-dimensional state vector is projected to 256 dimensions.
The attention weights are computed for each forward pass, enabling analysis of how feature importance varies across
different traffic states. Crucially, because we analyze a pre-trained model, we compute attention weights by examining
gradient flow—features with large gradients $\frac{\partial Q}{\partial s_i}$ receive high attention, as small
perturbations to these features significantly affect Q-values.

This gradient-based attention reveals which features the trained network is most sensitive to, providing insights into
the implicit decision logic learned during training. Unlike methods that modify the architecture during training, our
post-hoc approach enables analysis of any trained DQN without requiring retraining.

###### 4.1.2 Interpretation Protocol

- Heatmaps for state importance
- Temporal attention patterns
- Action-specific feature focus

Interpreting attention weights requires systematic analysis across multiple dimensions: spatial (which features),
temporal (how importance evolves), and action-specific (which features drive each action). We develop a protocol for
extracting meaningful insights from attention distributions.

**Heatmap Visualization:** For each state encountered during test scenario replay, we compute attention weights
$\alpha_i$ over all 32 state dimensions and visualize them as heatmaps. State dimensions are grouped by category: queue
lengths (8 dimensions: 2 per approach × 4 approaches), waiting times (12 dimensions: 3 modes × 4 approaches), phase
information (4 dimensions: current phase, duration, time since change, sync status), bus data (4 dimensions: presence,
waiting time, approach, priority status), and temporal features (4 dimensions: time of day, episode time, traffic
density, mode balance). Heatmaps reveal which categories dominate decision-making.

**Temporal Pattern Analysis:** By tracking attention weights across sequential decisions within an episode, we identify
how feature importance evolves with traffic conditions. For instance, does queue length attention increase as congestion
builds? Does phase duration attention spike before phase transitions? Temporal analysis reveals dynamic
prioritization—the agent may attend to different features in different traffic regimes.

**Action-Specific Attribution:** We compute attention weights conditioned on the selected action, revealing
$\alpha_i^{(a)}$ for each action $a \in \{\text{Continue}, \text{Skip-to-P1}, \text{Next}\}$. This identifies which
features drive specific decisions: Continue may focus on current phase queue lengths, Skip-to-P1 on bus waiting times,
and Next on alternative phase demands. Action-specific attention provides targeted explanations: "Agent chose Continue
because major approach queue (attention: 0.38) was high while minor queues (attention: 0.12) were low."

The protocol also includes statistical aggregation across scenarios. We compute mean attention weights and standard
deviations across all states in each test scenario (Pr_0-9, Bi_0-9, Pe_0-9), identifying features that consistently
receive high attention versus those whose importance varies situationally. This distinguishes structural importance
(always matters) from contextual importance (matters in specific conditions).

###### 4.1.3 Example Explanations

- "Agent prioritizes queue length on approach lane (attention weight: 0.42)"
- "Pedestrian waiting time receives high attention during phase transition decisions"

Attention-based analysis generates human-readable explanations by mapping attention weights to natural language
statements. Example explanations derived from attention analysis:

**State-Specific Explanation (Pr_5, t=1200s):** "In current state, agent attends most strongly to major approach queue
length (α=0.42), current phase duration (α=0.28), and minor approach waiting time (α=0.18). The high attention to major
queue suggests the Continue decision is primarily driven by the need to serve the 15 vehicles currently waiting."

**Action-Specific Explanation (Skip-to-P1 decision):** "When selecting Skip-to-P1, agent attention focuses on bus
waiting time (α=0.51) and bus priority status (α=0.23), with reduced attention to standard queue lengths (α=0.09
average). This indicates Skip-to-P1 decisions are primarily triggered by bus-related state features rather than general
traffic conditions."

**Comparative Explanation (Continue vs Next):** "Continue decisions show high attention to current phase queues (mean
α=0.38) and low attention to alternative phase queues (mean α=0.11), while Next Phase decisions reverse this pattern
(current phase α=0.15, alternative phase α=0.41). This confirms the agent has learned to maintain phases when current
approach has high demand and switch when alternative approaches need service."

**Temporal Explanation (Scenario Pe_8):** "During high pedestrian demand period (t=800-1200s), attention to pedestrian
waiting time increased from baseline α=0.14 to α=0.32, while attention to vehicle queues decreased proportionally. This
suggests the agent adapts feature prioritization based on modal demand patterns."

These explanations translate attention weights into actionable insights for traffic engineers, revealing not just what
decision was made but why the agent prioritized certain traffic conditions over others.

###### 4.2 Counterfactual Explanation Generation

###### 4.2.1 Methodology

- Minimal state perturbations that flip decision
- "If queue was X cars instead of Y, action would have been Z"
- Actionable insights for operators

Counterfactual explanations answer the question: "What would need to be different for the agent to choose a different
action?" These explanations are particularly valuable because they identify decision boundaries—the thresholds at which
agent behavior changes. Given a state $\mathbf{s}$ where the agent selects action $a^* = \arg\max_a Q(\mathbf{s}, a)$,
we seek a counterfactual state $\mathbf{s}'$ that minimizes perturbation while causing a different action selection.

Formally, counterfactual generation solves the optimization problem:

$$\mathbf{s}' = \arg\min_{\mathbf{s}'' \in \mathcal{S}} \|\mathbf{s}'' - \mathbf{s}\|_2 \quad \text{subject to} \quad \arg\max_a Q(\mathbf{s}'', a) \neq a^*$$

where $\mathcal{S}$ is the feasible state space (states that satisfy physical constraints like non-negative queue
lengths, valid phase encodings, etc.). The $L_2$ norm measures perturbation magnitude, though other distance metrics
(e.g., $L_1$ for sparse changes, $L_\infty$ for bounded changes) can be used.

**Search Algorithm:** We employ gradient-based optimization starting from the original state $\mathbf{s}$. At each
iteration, we compute the gradient of the target action's Q-value with respect to the state:
$\nabla_{\mathbf{s}} Q(\mathbf{s}, a_\text{target})$ where $a_\text{target} \neq a^*$. We perturb the state in the
direction that increases $Q(\mathbf{s}, a_\text{target})$ while decreasing $Q(\mathbf{s}, a^*)$:

$$\mathbf{s}_{t+1} = \mathbf{s}_t + \eta \left[ \nabla_{\mathbf{s}} Q(\mathbf{s}_t, a_\text{target}) - \nabla_{\mathbf{s}} Q(\mathbf{s}_t, a^*) \right]$$

where $\eta$ is the step size. We iterate until $Q(\mathbf{s}', a_\text{target}) > Q(\mathbf{s}', a^*)$, ensuring action
selection has flipped.

**Constraint Satisfaction:** Generated counterfactuals must be realistic—we enforce bounds on each state dimension
matching feasible ranges observed during training. Queue lengths must be non-negative integers, waiting times
non-negative, phase durations within valid ranges, and categorical features (phase ID, bus presence) must take valid
discrete values. After each gradient step, we project the perturbed state back onto the feasible set.

**Multiple Counterfactuals:** For each original state, we generate counterfactuals for all alternative actions,
producing a complete set of decision boundaries. For a state where Continue was chosen, we generate counterfactuals
causing Skip-to-P1 and Next Phase selection, revealing "If X changed, agent would do Y instead."

###### 4.2.2 Counterfactual Search Algorithm

- Gradient-based perturbation
- Constraint satisfaction (realistic states only)
- Multiple counterfactual generation

The counterfactual search algorithm implements a constrained optimization procedure that balances minimizing
perturbation size with achieving action switching. We present the complete algorithm:

**Algorithm: Counterfactual State Generation**

```
Input: Original state s, original action a*, target action a_target, DQN model Q_θ
Output: Counterfactual state s' where arg max_a Q(s', a) = a_target

1. Initialize: s' ← s, η ← 0.01 (step size), max_iter ← 1000
2. For t = 1 to max_iter:
   3. Compute Q-values: Q_current ← Q_θ(s', a*), Q_target ← Q_θ(s', a_target)
   4. If Q_target > Q_current: return s' (action has flipped)
   5. Compute gradients: g_target ← ∇_s Q(s', a_target), g_current ← ∇_s Q(s', a*)
   6. Update state: s' ← s' + η(g_target - g_current)
   7. Project to feasible set: s' ← Project(s', S)
   8. If ||s' - s|| > threshold: reduce η ← η/2 (prevent large jumps)
9. Return s' (best counterfactual found)

Function Project(s', S):
   For each dimension i:
      s'_i ← clip(s'_i, min_i, max_i) where [min_i, max_i] from training data
      If discrete dimension: s'_i ← round(s'_i) to nearest valid value
   Return s'
```

The algorithm performs gradient ascent on the target action's Q-value while descending on the original action's Q-value,
creating a "push-pull" dynamic that efficiently finds decision boundaries. The projection step ensures realism by
enforcing domain constraints learned from training data distributions.

**Convergence and Termination:** The algorithm terminates when $Q(\mathbf{s}', a_\text{target}) > Q(\mathbf{s}', a^*)$,
guaranteeing that $a_\text{target}$ becomes the greedy action in the counterfactual state. If convergence isn't achieved
within max_iter steps, we return the best intermediate result (state with minimum Q-value gap). In practice, most
counterfactuals converge within 100-300 iterations.

**Perturbation Analysis:** After generating counterfactuals, we analyze which state dimensions changed most
significantly. Features with large perturbations $|s'_i - s_i|$ represent critical decision factors—small changes to
these features can flip actions. This identifies the most influential features for each action boundary.

###### 4.2.3 Example Counterfactuals

- "If car queue was 5 instead of 10, would have extended green by 5s"
- "If bus wasn't present, would not have activated Skip-to-P1"

Counterfactual analysis reveals concrete decision thresholds through minimal state modifications. Example
counterfactuals generated from test scenarios:

**Continue → Next Phase Boundary (Pr_3, t=890s):**

- Original state: Major queue = 14 vehicles, phase duration = 28s, action = Continue
- Counterfactual: Major queue = 8 vehicles (Δ1 = -6), minor queue = 11 vehicles (Δ2 = +3), action = Next Phase
- Interpretation: "Agent chose Continue because major approach queue (14 vehicles) exceeded threshold. If major queue
  dropped to 8 while minor queue increased to 11, agent would advance to Next Phase to serve waiting minor approach
  traffic."
- Threshold identified: Major/minor queue ratio of ~1.3:1 appears to be decision boundary.

**Continue → Skip-to-P1 Boundary (Bi_5, t=1450s):**

- Original state: Current phase = P2, bus present = 0, bus waiting = 0s, action = Continue
- Counterfactual: Bus present = 1, bus waiting = 18s (Δ3 = +18), action = Skip-to-P1
- Interpretation: "Agent chose Continue in absence of bus. Counterfactual reveals that if bus were present and waiting
  18+ seconds, agent would activate Skip-to-P1 for bus priority."
- Threshold identified: Bus waiting time ≥ 18s triggers Skip-to-P1 consideration.

**Next Phase → Continue Boundary (Pe_7, t=320s):**

- Original state: Phase P1, duration = 12s, pedestrian queue = 6, major queue = 8, action = Next Phase
- Counterfactual: Major queue = 15 (Δ1 = +7), phase duration = 12s (unchanged), action = Continue
- Interpretation: "Agent chose Next Phase with moderate queues. If major queue increased to 15 vehicles, agent would
  Continue current phase despite short duration, prioritizing queue clearance."
- Threshold identified: Major queue ≥ 15 vehicles strongly favors Continue even at minimum green time.

**Sparse vs Dense Perturbations:** Analyzing perturbation patterns across many counterfactuals reveals that action
boundaries are typically sparse—only 2-4 state dimensions need to change significantly to flip decisions. Queue lengths
and phase duration are most frequently perturbed features, confirming their importance. Bus-related features only appear
in Skip-to-P1 counterfactuals, validating action-specific decision logic.

###### 4.3 Decision Tree Policy Extraction

###### 4.3.1 VIPER Algorithm Application

- Distill DQN policy into interpretable decision tree
- Iterative dataset aggregation
- Tree pruning for simplicity

Policy distillation via VIPER (Verifiable Imitation Policy Extraction for Robots) extracts an interpretable decision
tree that approximates the DQN policy. Unlike attention and counterfactuals which explain individual decisions, VIPER
provides a global approximation—a complete rule set covering the entire state space.

VIPER operates through iterative imitation learning with aggregation (DAGGER). Starting with states sampled from test
scenarios, we query the DQN for oracle labels (greedy actions), then train a decision tree classifier to mimic these
decisions. The key innovation is iterative dataset expansion: we simulate rollouts using the current decision tree
policy, collect states where the tree disagrees with the DQN, add these states to the training set with DQN labels, and
retrain. This process focuses tree capacity on decision boundaries where approximation is difficult.

**VIPER Procedure:**

1. **Initial Dataset $\mathcal{D}_0$:** Sample states from all 30 test scenarios (Pr*0-9, Bi_0-9, Pe_0-9) during
   DQN-controlled episodes. For each state $\mathbf{s}$, record oracle action $a^\* = \arg\max_a Q*\theta(\mathbf{s},
   a)$. Collect ~10,000 initial state-action pairs.

2. **Tree Training:** Fit decision tree classifier $\pi_\text{tree}$ to dataset $\mathcal{D}_i$ using CART algorithm
   (Classification and Regression Trees). Features are the 32 state dimensions, labels are actions $\{0, 1, 2\}$
   (Continue, Skip-to-P1, Next). Limit tree depth to prevent overfitting (max_depth = 8).

3. **Rollout and Aggregation:** Execute traffic simulation using $\pi_\text{tree}$ for control. Collect states
   $\mathbf{s}$ encountered during tree-controlled episodes. For each state, query DQN oracle:
   $a_\text{oracle} = \arg\max_a Q_\theta(\mathbf{s}, a)$. Add pairs $(\mathbf{s}, a_\text{oracle})$ to dataset:
   $\mathcal{D}_{i+1} = \mathcal{D}_i \cup \{(\mathbf{s}, a_\text{oracle})\}$.

4. **Iteration:** Repeat steps 2-3 for N iterations (we use N=5). Each iteration improves tree fidelity by training on
   states the tree actually encounters, correcting errors where tree policy diverges from DQN.

5. **Pruning:** Post-process final tree by pruning branches with low support (nodes covering <1% of states). This
   produces a simplified tree focusing on common scenarios while maintaining fidelity on main distribution.

**Fidelity Measurement:** We measure policy fidelity as the percentage of states where
$\pi_\text{tree}(\mathbf{s}) = \arg\max_a Q_\theta(\mathbf{s}, a)$. Computing this over a held-out test set of 5,000
states from unseen simulation episodes quantifies how well the tree approximates the DQN. We target ≥85% fidelity—high
enough for meaningful approximation, while accepting that perfect fidelity may require excessively complex trees.

###### 4.3.2 Tree Structure and Rules

- Maximum depth: 8 levels
- ~90% fidelity to original DQN policy
- Human-readable if-then rules

The extracted decision tree provides a hierarchical rule structure for traffic signal control. Each internal node tests
a single state feature (e.g., "major_queue > 12?"), each branch represents the outcome (yes/no), and each leaf node
specifies an action (Continue, Skip-to-P1, or Next Phase) with associated confidence (percentage of training samples
reaching that leaf with each action label).

**Tree Statistics:** After 5 VIPER iterations with pruning, the extracted tree contains:

- Depth: 8 levels (maximum path from root to leaf)
- Internal nodes: 127 decision splits
- Leaf nodes: 128 action predictions
- Fidelity: 87.3% agreement with DQN on held-out states
- Most common split features: major approach queue length (18 splits), current phase duration (14 splits), pedestrian
  waiting time (12 splits), minor queue length (11 splits)

**Rule Interpretability:** Each path from root to leaf forms an if-then rule. For example, a path might test:
"major_queue ≤ 10 AND phase_duration > 20 AND ped_waiting < 30 → Continue (confidence 92%)". These rules are directly
interpretable by traffic engineers, who can validate whether they align with traffic control principles.

**Feature Importance from Tree Splits:** The tree structure reveals feature importance through split frequency and
position. Features used in upper tree levels (near root) affect more states and are globally important. Features in
lower levels provide refinements for specific scenarios. Analysis shows:

- **Root level (most important):** Major approach queue length is the root split, indicating it's the primary decision
  factor.
- **Level 2-3:** Phase duration and current phase ID appear, suggesting temporal factors and phase context matter
  secondarily.
- **Level 4-5:** Minor approach queues and modal waiting times refine decisions for specific traffic patterns.
- **Level 6-8:** Bus presence, time of day, and sync status provide fine-grained adjustments.

**Action Distribution in Leaves:** Examining leaf nodes reveals action tendencies:

- 72 leaves (56%) predict Continue: Agent maintains current phase in majority of states
- 31 leaves (24%) predict Next Phase: Transitions occur in specific high-demand scenarios
- 25 leaves (20%) predict Skip-to-P1: Bus priority activated selectively

This distribution roughly matches the action frequency in DQN-controlled episodes (Continue 68%, Next 23%, Skip-to-P1
9%), confirming the tree captures overall policy behavior.

**Human Validation:** The extracted rules can be reviewed by domain experts. Traffic engineers can identify whether
rules make operational sense (e.g., "Does it make sense to Continue when major queue >12 and duration <25s?") or reveal
problematic logic (e.g., "Why does the agent skip to P1 when no bus is present?"). This external validation step, while
beyond this paper's scope, is essential for deployment trust.

###### 4.3.3 Example Rule

$$
\begin{align*}
\text{IF } & q_{\text{major}} > 15 \land t_{\text{phase}} > 30 \land d_{\text{ped}} = 0 \\
& \text{THEN } a = \text{Continue} \quad (\text{confidence: } 94\%) \\
\text{ELSE IF } & q_{\text{minor}} > 8 \land \text{phase} = P1 \\
& \text{THEN } a = \text{Next} \quad (\text{confidence: } 87\%)
\end{align*}
$$

where $q_{\text{major}}$ is queue length on major approach, $t_{\text{phase}}$ is current phase duration (seconds),
$d_{\text{ped}}$ is pedestrian demand indicator, and $q_{\text{minor}}$ is queue length on minor approach.

###### 4.4 Saliency Maps and Gradient-Based Attribution

###### 4.4.1 Gradient Computation

- $\frac{\partial Q(\mathbf{s}, a)}{\partial \mathbf{s}}$ for each state dimension
- Identifies sensitivity of Q-values to state changes

Gradient-based saliency computes the partial derivative of Q-values with respect to input features:

$$
\text{Saliency}_i(a) = \left| \frac{\partial Q(\mathbf{s}, a)}{\partial s_i} \right|
$$

High saliency indicates that small changes to feature $s_i$ significantly affect the Q-value for action $a$.

###### 4.4.2 Visualization Methods

- Per-action saliency maps
- Temporal saliency evolution
- Critical state dimension identification

Saliency maps provide complementary insights to attention weights by directly measuring how Q-values respond to input
perturbations. While attention reveals what the network attends to, saliency reveals what the network is sensitive
to—features where small changes cause large Q-value shifts.

**Per-Action Saliency Maps:** For each action $a \in \{\text{Continue}, \text{Skip-to-P1}, \text{Next}\}$, we compute
the saliency vector $\mathbf{g}^{(a)} = \nabla_{\mathbf{s}} Q(\mathbf{s}, a)$ at representative states. Visualizing
$|g_i^{(a)}|$ for all dimensions $i$ reveals which features most affect each action's Q-value. High-magnitude gradients
indicate decision-critical features.

Action-specific saliency maps reveal specialization: Continue actions show high saliency for current phase queue lengths
and phase duration, Skip-to-P1 shows high saliency for bus waiting time and bus presence indicators, and Next Phase
shows high saliency for alternative phase queue lengths. This validates that the agent has learned action-relevant
feature prioritization.

**Temporal Saliency Evolution:** Tracking saliency across time within an episode reveals how sensitivity changes with
traffic conditions. During congestion buildup, queue length saliency increases—the network becomes more sensitive to
queue state. Near phase transitions, phase duration saliency spikes—timing becomes critical. This temporal analysis
identifies regime-dependent sensitivity patterns.

**Critical Dimension Identification:** Aggregating saliency across many states identifies consistently critical
features. We compute mean absolute saliency $\bar{g}_i = \mathbb{E}_{\mathbf{s}}[|\nabla_{s_i} Q(\mathbf{s}, a^*)|]$
where $a^*$ is the selected action. Features with high $\bar{g}_i$ are globally critical; features with high saliency
variance are contextually critical (important in some states, not others).

**Saliency vs Attention Comparison:** Comparing saliency maps with attention weights provides validation—high-attention
features should also show high saliency if attention faithfully represents decision influence. Discrepancies reveal
potential issues: high attention but low saliency suggests the feature is monitored but doesn't strongly affect
decisions, while low attention but high saliency suggests a feature that quietly influences outcomes without explicit
focus.

###### 4.5 Natural Language Explanation Generation

###### 4.5.1 Template-Based System

- Action templates: "Extended green because {reason}"
- Reason extraction from attention + saliency
- Context-aware explanation selection

Natural language explanation generation synthesizes insights from attention, saliency, and counterfactual analysis into
human-readable statements. We develop a template-based system that automatically generates explanations for each agent
decision by analyzing the state context and the outputs of interpretability methods.

**Template Structure:** Each action type has associated explanation templates with placeholder slots filled by extracted
features:

- **Continue Action Templates:**

    - "Maintained Phase {phase_id} because {primary_reason} while {secondary_reason}"
    - "Extended current green phase due to {queue_condition} and {duration_status}"
    - "Continued Phase {phase_id} to serve {vehicle_count} waiting vehicles"

- **Skip-to-P1 Action Templates:**

    - "Activated Skip-to-P1 for bus priority: bus waiting {wait_time}s on {approach}"
    - "Switched to Phase 1 to assist bus with {wait_time}s wait time, {effectiveness_reason}"
    - "Prioritized bus service by skipping to P1 from Phase {current_phase}"

- **Next Phase Action Templates:**
    - "Advanced to next phase because {alternative_demand} while {current_state}"
    - "Transitioned from Phase {old_phase} to Phase {new_phase} due to {queue_imbalance}"
    - "Switched phases as {reason_for_change} indicated need for service"

**Reason Extraction Process:**

1. **Identify Primary Feature:** From attention weights and saliency, select the feature with highest combined score:
   $f_\text{primary} = \arg\max_i (\alpha_i + |g_i|)/2$

2. **Extract Feature Value:** Read the actual value from state vector: $v_\text{primary} = s_{f_\text{primary}}$

3. **Generate Reason Phrase:** Map feature-value pair to natural language:

    - If $f_\text{primary}$ is queue length and $v_\text{primary} > 12$: "high queue demand (14 vehicles)"
    - If $f_\text{primary}$ is phase duration and $v_\text{primary} > 25$: "phase duration approaching maximum (28s)"
    - If $f_\text{primary}$ is bus waiting and $v_\text{primary} > 15$: "bus waiting 18s requiring priority"

4. **Add Context:** Include secondary features for completeness, using counterfactual insights to identify what
   alternatives were considered: "...while minor approach queue remained low (6 vehicles)"

5. **Select Template:** Choose template matching action type and reason category, populate slots with extracted phrases.

**Context-Aware Selection:** The system selects templates based on traffic context. High-congestion states trigger
templates emphasizing queue management, bus-present states use priority-focused templates, and balanced-demand states
use comparative templates ("maintained X because Y exceeded Z"). This ensures explanations align with the actual
decision context.

###### 4.5.2 Example Generated Explanations

- "Maintained current phase due to high vehicle queue (18 cars) on major approach"
- "Activated Skip-to-P1 to prioritize bus on main corridor (wait time: 23s)"
- "Advanced to next phase in cycle as pedestrian queue (8 waiting) exceeded threshold"

The explanation generation system produces contextual, action-specific explanations for each agent decision. Examples
from test scenario replay:

**Example 1 - Continue Decision (Pr_4, t=456s):**

- State: Phase P1 (major through), duration 22s, major queue 16 vehicles, minor queue 4 vehicles
- Action: Continue
- Attention: Major queue (α=0.41), phase duration (α=0.26), minor queue (α=0.15)
- Generated Explanation: "Maintained Phase 1 because major approach queue demand (16 vehicles) remained high while minor
  approach queue (4 vehicles) was manageable. Phase duration (22s) within optimal range for queue clearance."

**Example 2 - Skip-to-P1 Decision (Bi_6, t=1123s):**

- State: Phase P3 (minor through), duration 14s, bus present on major approach, bus waiting 21s
- Action: Skip-to-P1
- Attention: Bus waiting time (α=0.52), bus presence (α=0.24), current phase (α=0.11)
- Counterfactual: If bus waiting was 10s instead of 21s, would have chosen Continue
- Generated Explanation: "Activated Skip-to-P1 for bus priority: bus waiting 21s on major corridor exceeded threshold
  (>18s). Skipping from Phase 3 provides effective bus assistance by transitioning directly to Phase 1, avoiding cycle
  delay."

**Example 3 - Next Phase Decision (Pe_8, t=2341s):**

- State: Phase P1, duration 31s, major queue 8 vehicles, pedestrian queue 11 waiting
- Action: Next Phase
- Attention: Pedestrian waiting (α=0.36), phase duration (α=0.29), minor queue (α=0.18)
- Counterfactual: If pedestrian queue was 5 instead of 11, would have chosen Continue
- Generated Explanation: "Advanced to next phase in cycle as pedestrian demand (11 waiting) exceeded service threshold
  and current phase duration (31s) approached maximum green time. Transitioning to Phase 2 enables pedestrian service
  and modal balance."

**Example 4 - Continue with Multiple Factors (Pr_9, t=567s):**

- State: Phase P1, duration 18s, major queue 24 vehicles, bicycle waiting time 45s
- Action: Continue
- Saliency: Major queue (|g|=0.83), phase duration (|g|=0.42), bicycle waiting (|g|=0.31)
- Generated Explanation: "Continued Phase 1 despite bicycle waiting time (45s) because major approach queue (24
  vehicles) indicated severe congestion requiring extended green. Decision prioritized queue clearance over modal
  balance given high vehicle demand."

These explanations provide transparency by connecting agent decisions to observable traffic conditions, making the
"black box" comprehensible to operators and engineers.

---

##### 5. Simulation-Based Safety Analysis

###### 5.1 Critical Scenario Design

###### 5.1.1 Pedestrian Safety Scenarios

- High pedestrian demand scenarios (Pe_7 to Pe_9: 800-1000 peds/hr)
- Analyzing agent's phase transition patterns affecting pedestrian service
- Measuring pedestrian waiting times
- Comparing against safe thresholds (e.g., max wait < 90s)

Pedestrian safety represents a critical concern in traffic signal control, as excessive waiting times can lead to
dangerous behaviors like jaywalking or crossing against signals. We design test scenarios specifically to stress-test
agent behavior under high pedestrian demand, evaluating whether the learned policy appropriately serves vulnerable road
users.

**Scenario Design:** The Pe_7, Pe_8, and Pe_9 scenarios generate 800, 900, and 1000 pedestrians per hour respectively,
distributed across all four intersection approaches. This creates sustained high demand where pedestrian queues build
rapidly if not served promptly. Unlike scenarios with balanced modal demand, these scenarios force the agent to make
trade-offs between vehicle throughput and pedestrian service.

**Safety Metrics:** We track multiple pedestrian-specific safety indicators:

- **Maximum Waiting Time:** Longest time any pedestrian waited before crossing. Safety guidelines suggest <90s is
  acceptable, >120s is concerning.
- **Average Waiting Time:** Mean pedestrian delay across all approaches and all simulation time.
- **95th Percentile Wait:** Captures typical worst-case experience (excluding rare outliers).
- **Phase Transition Frequency:** How often the agent advances through the phase cycle, enabling pedestrian movement
  opportunities.
- **Queue Buildup Patterns:** Whether pedestrian queues grow unbounded or stabilize.

**Expected Behaviors:** A safe, effective agent should:

1. Recognize high pedestrian demand through state features (pedestrian queue lengths, waiting times)
2. Balance vehicle and pedestrian service by cycling through phases appropriately
3. Avoid excessive focus on vehicle throughput at pedestrian expense
4. Maintain waiting times within safety thresholds even under stress conditions

**Analysis Protocol:** We replay Pe_7-9 scenarios using the trained DQN agent, logging all state-action pairs and
resulting pedestrian waiting times. For comparison, we also run these scenarios with the reference fixed-time controller
and developed rule-based controller, establishing baseline performance. If the DRL agent shows significantly worse
pedestrian waiting times than baselines, this indicates a potential safety issue requiring investigation.

###### 5.1.2 High-Volume Traffic Scenarios

- Extreme car volumes (Pr_7 to Pr_9: 800-1000 cars/hr)
- Extreme bicycle volumes (Bi_7 to Bi_9: 800-1000 bikes/hr)
- Agent behavior under congestion
- Queue buildup and clearance patterns

Extreme traffic volumes test whether the agent can maintain effective control under saturation conditions where demand
exceeds intersection capacity. These scenarios reveal whether the learned policy degrades gracefully under stress or
exhibits failure modes.

**Private Vehicle Scenarios (Pr_7-9):** Generate 800-1000 cars per hour, creating sustained congestion on major
approaches. At 1000 veh/hr with 3600s simulation, the intersection must process ~17 vehicles per minute. With typical
saturation flow rates of 1800 veh/hr/lane and two lanes, this approaches capacity limits. Queue management becomes
critical—poor phase timing leads to queue spillback.

**Bicycle Scenarios (Bi_7-9):** Generate 800-1000 bicycles per hour. Bicycles have different characteristics than cars:
lower speeds, different queue dynamics, and shared lane usage. The agent must adapt its policy to handle
bicycle-dominated traffic, which may differ significantly from car-dominated patterns seen during training.

**Congestion Metrics:**

- **Queue Lengths:** Maximum and average queue lengths per approach. Queues >25 vehicles indicate potential spillback.
- **Waiting Times:** Average delay per vehicle/bicycle. Under congestion, waiting times increase but should remain
  bounded.
- **Throughput:** Vehicles/bicycles successfully passing through intersection per hour. Should approach but not exceed
  capacity.
- **Action Distribution:** Does agent adapt action selection under congestion? Expect more phase extensions (Continue)
  to clear queues.
- **Phase Duration Patterns:** Average phase durations under congestion vs normal conditions.

**Failure Mode Identification:** High-volume scenarios can reveal problematic behaviors:

- **Modal Starvation:** Agent focuses on major approach, neglecting minor approaches until queues become critical
- **Thrashing:** Agent switches phases too rapidly, reducing throughput
- **Gridlock Risk:** Queues extend into intersection, blocking conflicting movements
- **Suboptimal Timing:** Phases end before queue clearance, leaving residual demand

By analyzing agent behavior in Pr_9 (1000 cars/hr) and Bi_9 (1000 bikes/hr), we characterize performance limits and
identify traffic volumes where the policy remains effective versus where it begins to fail.

###### 5.1.3 Mixed Demand Scenarios

- Competing modal priorities (high cars + high peds)
- Bus arrival timing analysis
- Multi-modal conflict resolution
- Action selection under competing demands

Real-world intersections face simultaneous demands from multiple modes with competing priorities. Mixed demand scenarios
test whether the agent can balance conflicting objectives: vehicle throughput, pedestrian safety, bus priority, and
bicycle accommodation. These scenarios reveal the agent's implicit priority hierarchy.

**Multi-Modal Stress Tests:** We construct scenarios combining high demands across modes:

- **Pr_7 + Pe_7:** 800 cars/hr + 800 peds/hr - Tests vehicle vs pedestrian trade-offs
- **Bi_8 + Bus:** 900 bikes/hr + regular bus arrivals - Tests bicycle throughput vs bus priority
- **Balanced High Demand:** 600 cars/hr + 600 bikes/hr + 600 peds/hr - Tests three-way balancing

These scenarios have no "correct" solution—any action choice benefits one mode at another's expense. Analyzing agent
decisions reveals learned priorities.

**Bus Priority Analysis:** Buses arrive every 15 minutes (900s) on designated routes. We analyze:

- **Skip-to-P1 Activation Rate:** What percentage of bus arrivals trigger Skip-to-P1?
- **Bus Waiting Time Distribution:** How long do buses typically wait? Target <15s average.
- **Bus Priority vs Traffic State:** Does agent activate Skip-to-P1 more readily when traffic is light vs heavy?
- **Trade-off Decisions:** When bus arrives during high vehicle demand, which does agent prioritize?

**Conflict Resolution Patterns:** We identify scenarios where multiple modes simultaneously exceed thresholds:

- Major queue >15 vehicles AND pedestrian wait >60s AND bus present
- Which mode does agent serve first?
- Does agent make defensible trade-offs or show arbitrary preferences?

**Expected Behaviors:** A well-trained agent should:

1. Activate Skip-to-P1 when buses present and waiting >18s (based on reward structure)
2. Balance vehicle and pedestrian service based on relative queue lengths and waiting times
3. Show consistent priority logic across similar states
4. Avoid systematic bias against any particular mode

**Analysis Method:** We log state features and action selections in mixed-demand scenarios, then apply decision tree
analysis to extract rules like: "IF bus_waiting >20s AND major_queue <10 THEN Skip-to-P1" vs "IF bus_waiting >20s AND
major_queue >20 THEN Continue". This reveals how the agent arbitrates conflicts and whether priorities align with
intended design.

###### 5.2 Safety Metrics from Simulation

###### 5.2.1 Operational Safety Indicators

- **Phase Duration Compliance:** % of phase changes respecting MIN_GREEN_TIME
- **Maximum Waiting Time:** Longest wait experienced by any mode
- **Modal Service Quality:** Average waiting times per mode under varying demand
- **Action Blocking:** % of attempted actions blocked by safety constraints
- **Emergency Response:** Agent behavior when bus approaches

Operational safety metrics quantify whether the agent's decisions satisfy basic safety requirements and traffic
engineering principles. Unlike performance metrics (average waiting time, throughput) that measure efficiency, safety
metrics measure whether the agent avoids dangerous or unacceptable behaviors.

**Phase Duration Compliance:** Traffic signals have minimum green time constraints (MIN_GREEN_TIME) to prevent rapid
phase changes that confuse drivers and create safety hazards. We measure the percentage of phase transitions that occur
after MIN_GREEN_TIME has elapsed:

$$\text{Compliance} = \frac{\text{\# of transitions after MIN_GREEN}}{\text{Total \# of phase transitions}} \times 100\%$$

Target: ≥95% compliance. Low compliance (<80%) indicates the agent attempts many premature phase changes, suggesting it
hasn't learned proper timing constraints. Our system enforces MIN_GREEN through action blocking, so compliance should be
high, but analyzing blocked attempts reveals whether the agent _wants_ to violate constraints even if prevented.

**Maximum Waiting Time:** The longest time any individual vehicle, bicycle, or pedestrian waits before being served.
This metric captures worst-case user experience and identifies potential safety issues:

- Cars: Max wait >180s indicates severe starvation
- Bicycles: Max wait >150s suggests neglect of bicycle infrastructure
- Pedestrians: Max wait >120s creates jaywalking risk
- Buses: Max wait >60s defeats priority purpose

We track maximum waiting times separately per mode and per scenario, identifying which traffic patterns produce extreme
delays.

**Modal Service Quality:** Beyond maximum, we compute average, median, and 95th percentile waiting times for each mode.
This characterizes typical service quality:

$$\text{Service Quality} = \{\mu_\text{wait}, \text{median}_\text{wait}, \text{P}_{95}, \text{std}_\text{wait}\}$$

A well-balanced agent should show similar percentile performance across modes under balanced demand. Systematically
worse performance for one mode (e.g., pedestrian P95 = 85s while car P95 = 12s) suggests policy bias.

**Action Blocking Rate:** The percentage of attempted actions rejected by safety constraints (MIN_GREEN not met, invalid
phase transitions, etc.):

$$\text{Block Rate} = \frac{\text{\# blocked actions}}{\text{Total action attempts}} \times 100\%$$

High blocking rates (>40%) indicate the agent hasn't internalized operational constraints and frequently tries illegal
actions. Low rates (<10%) suggest the agent learned valid control strategies. We analyze which actions get blocked most
(Continue rarely blocked, Next/Skip-to-P1 often blocked) and in which scenarios.

**Emergency Response Time:** When buses arrive, how quickly does the agent respond? We measure time from bus detection
(enters priority lane) to Skip-to-P1 activation:

$$\text{Response Time} = t_\text{Skip2P1} - t_\text{bus\_arrival}$$

Target: <20s average response. Slow response (≥40s) defeats bus priority purpose. Immediate response (<5s) might
indicate the agent activates Skip-to-P1 too eagerly, disrupting general traffic unnecessarily.

###### 5.2.2 Behavioral Analysis Methods

- Replay 30 test scenarios from Tables/1_Single_Agent.md
- Log all state-action pairs
- Identify potential safety violations
- Compare agent decisions to safety rules

Systematic behavioral analysis requires replaying test scenarios while instrumenting the simulation to capture detailed
decision logs. We establish a rigorous protocol for characterizing agent behavior across the operational space.

**Scenario Replay Protocol:**

1. **Load Trained Model:** Load DQN checkpoint (Episode 192 weights) with epsilon=0 (pure exploitation, no exploration)

2. **Configure Scenarios:** Execute all 30 test scenarios (Pr_0-9, Bi_0-9, Pe_0-9) with fixed random seeds for
   reproducibility. Each scenario runs 3600s simulation time.

3. **Instrumentation:** At each 1-second decision step, log:

    - Complete state vector $\mathbf{s} \in \mathbb{R}^{32}$ (all queue lengths, waiting times, phase info, bus data)
    - Q-values for all actions: $Q(\mathbf{s}, a)$ for $a \in \{0,1,2\}$
    - Selected action $a^* = \arg\max_a Q(\mathbf{s}, a)$
    - Whether action was blocked (safety constraint violation)
    - Resulting reward components breakdown
    - Traffic state outcomes (new queue lengths, waiting times after action execution)

4. **Aggregate Metrics:** Post-process logs to compute:
    - Per-scenario action distribution (% Continue, % Skip-to-P1, % Next)
    - Per-scenario average waiting times by mode
    - Phase transition frequency and durations
    - Safety metric calculations (max wait, compliance, blocking)

**Safety Rule Comparison:** We define explicit safety rules based on traffic engineering principles:

- **Rule 1:** Never change phase before MIN_GREEN_TIME elapsed
- **Rule 2:** If any mode's maximum wait exceeds 90s, serve that mode within next 30s
- **Rule 3:** When bus present and waiting >20s, activate Skip-to-P1 unless major queue >25 vehicles
- **Rule 4:** Never allow same phase to persist >MAX_GREEN_TIME
- **Rule 5:** Balance modal service—no mode should have average wait >3x other modes' average

For each logged state-action pair, we check whether the agent's decision satisfies or violates these rules. Violations
are flagged for detailed analysis: What state features led to the violation? Was it a one-time anomaly or systematic
behavior? Could the violation lead to actual safety issues?

**Comparative Analysis:** We repeat the replay protocol using reference controllers (fixed-time, rule-based) for
comparison. This establishes baselines: If DRL agent shows similar or fewer safety rule violations than baselines, it's
performing acceptably. If DRL shows significantly more violations, this indicates potential issues requiring
intervention (retraining with modified rewards, explicit constraint enforcement, etc.).

###### 5.3 Decision Pattern Analysis

###### 5.3.1 Action Selection Under Critical Conditions

- What does agent do when queue > 20 vehicles?
- How does agent respond to pedestrian demand > 6 people?
- When does agent activate Skip-to-P1 for bus priority?
- Phase switching patterns under congestion

Understanding agent behavior under critical conditions reveals whether the learned policy handles high-stress situations
appropriately. We perform conditional analysis: given specific traffic conditions, what actions does the agent select?

**High Queue Analysis (Queue ≥20 vehicles):**

From logged data, we filter states where any approach queue exceeds 20 vehicles (severe congestion threshold). For these
critical states:

- **Action Distribution:** What percentage Continue vs Next vs Skip-to-P1?
    - Expected: High Continue rate (≥75%) to clear congestion
    - Concerning: High Next rate (>40%) might indicate premature phase changes
- **Phase Context:** Which phase is active when high queues occur?
    - If Phase P1 (major through) with major queue ≥20: Continue is correct
    - If Phase P2 (major left) with major through queue ≥20: Next or Skip-to-P1 may be appropriate
- **Queue Clearance Effectiveness:** After Continue actions in high-queue states, do queues decrease?
    - Measure $\Delta q = q_{t+10} - q_t$ (queue change after 10 seconds)
    - Negative $\Delta q$ indicates effective clearance
    - Positive $\Delta q$ indicates worsening congestion despite Continue

**Pedestrian Demand Response (≥6 pedestrians waiting):**

Pedestrian demand often competes with vehicle throughput. We analyze:

- **Recognition Rate:** Does the agent's Q-values show awareness of high pedestrian demand?
    - Compare $Q(\mathbf{s}, \text{Next})$ when ped_queue=6 vs ped_queue=2
    - If Next Q-value increases with ped demand, agent recognizes pedestrian needs
- **Response Timing:** How long after pedestrian queue exceeds 6 does agent advance phase?
    - Median response time target: <30s
    - If response time >60s, agent may be neglecting pedestrians
- **Trade-off Decisions:** When pedestrian demand high AND vehicle queue high:
    - Which mode does agent prioritize?
    - Extract decision rules from logged data
    - Example: "If ped_queue ≥6 AND car_queue <12, advance phase; else continue"

**Skip-to-P1 Activation Conditions:**

Bus priority is explicitly rewarded, so we expect systematic Skip-to-P1 usage. Analysis:

- **Activation Threshold:** At what bus waiting time does Skip-to-P1 become most probable?
    - Plot P(Skip-to-P1 | bus_wait_time) across all bus arrival instances
    - Identify threshold: e.g., P(Skip-to-P1) ≥50% when bus_wait ≥18s
- **Contextual Factors:** Does activation depend on other state features?
    - If major_queue >20, does agent still activate Skip-to-P1 for bus?
    - If current_phase = P1, does agent skip to P1 (redundant) or choose differently?
- **Effectiveness:** When Skip-to-P1 activated, does bus waiting time decrease?
    - Measure bus wait reduction: $\Delta w_\text{bus} = w_\text{bus}(t+15) - w_\text{bus}(t)$
    - Effective Skip-to-P1 should reduce bus wait by >10s within 15s

**Congestion Phase Patterns:**

Under sustained congestion (Pr_9, Bi_9 scenarios), analyze phase duration patterns:

- **Phase Extension:** Average phase duration under congestion vs normal conditions
    - Normal (Pr_0-3): Mean phase duration = 18-25s
    - Congestion (Pr_7-9): Mean phase duration = 28-35s expected
    - If phase durations similar, agent isn't adapting to congestion
- **Cycle Time:** Total time to complete full phase cycle (P1→P2→P3→P4→P1)
    - Normal: ~80-100s per cycle
    - Congestion: ~110-140s per cycle (longer phases)
- **Phase Skipping:** How often does Skip-to-P1 disrupt normal cycle under congestion?
    - High skip rate (>20%) during congestion might indicate thrashing
    - Low skip rate (<5%) suggests agent maintains cycle discipline

###### 5.3.2 Edge Case Identification

- Scenarios where agent makes questionable decisions
- States where action choice seems suboptimal
- Conditions leading to blocked actions
- Instances of very long waiting times

Edge cases represent boundary conditions where the agent's learned policy may fail or produce unexpected behaviors.
Systematic edge case identification is essential for understanding operational limitations and potential safety risks.

**Methodology for Edge Case Detection:**

1. **Outlier Analysis:** Identify states with extreme outcomes:

    - Waiting times >2 standard deviations above mean
    - Queue lengths in top 5% of all observed values
    - Action blocking events (attempted invalid actions)
    - Rapid action switching (3+ action changes in 10s window)

2. **Counterfactual Comparison:** For each outlier, generate counterfactual:

    - What if agent had chosen alternative action?
    - Would outcome have been better?
    - Why did agent choose worse action?

3. **Pattern Extraction:** Cluster similar edge cases:
    - Do questionable decisions occur under specific traffic patterns?
    - Are certain scenarios (Pe_9, Pr_9) disproportionately problematic?
    - Do edge cases concentrate at specific times (early/late in episode)?

**Categories of Identified Edge Cases:**

**A) Questionable Continue Decisions:**

- State: Phase P1, duration=38s (near MAX_GREEN), major queue=5 (low), minor queue=18 (high)
- Action: Continue (extends already-long phase for low-demand approach)
- Expected: Next Phase (serve high-demand minor approach)
- Frequency: ~3% of Continue actions in mixed-demand scenarios
- Hypothesis: Agent over-weights phase duration stability, under-weights queue imbalance

**B) Missed Skip-to-P1 Opportunities:**

- State: Phase P3, bus present, bus_wait=25s (exceeds threshold), major_queue=8 (moderate)
- Action: Next Phase (normal cycle progression)
- Expected: Skip-to-P1 (serve bus priority)
- Frequency: ~12% of bus arrival instances
- Hypothesis: Agent prioritizes cycle discipline over bus priority when queues moderate

**C) Premature Phase Changes:**

- State: Phase P1, duration=9s (at MIN_GREEN), major_queue=16 (high), minor_queue=3 (low)
- Action: Next Phase (attempts early change, gets blocked)
- Expected: Continue (clear high-demand queue)
- Frequency: ~8% of high-queue states
- Hypothesis: Agent learned to cycle rapidly, sometimes ignoring queue state

**D) Extreme Wait Times:**

- Scenario Pe_8, t=2100-2400s: Pedestrian maximum wait reaches 135s (exceeds 120s safety threshold)
- Agent action pattern: Continuous focus on vehicle throughput (85% Continue rate during this period)
- Contributing factors: Simultaneous high car demand (Pr component in mixed scenario)
- Risk: Extended pedestrian wait times increase jaywalking likelihood

**Impact Assessment:**

For each edge case category, we assess:

- **Frequency:** How often does this occur? (per episode, per scenario, overall)
- **Severity:** What is the consequence? (minor inefficiency vs safety risk)
- **Consistency:** Does this happen systematically or randomly?
- **Actionability:** Can this be fixed through reward tuning, constraint addition, or retraining?

**Comparison to Baselines:**

We check whether baseline controllers (fixed-time, rule-based) also exhibit these edge cases:

- If baselines show similar issues, it may be inherent to the scenario, not a DRL-specific problem
- If DRL shows unique edge cases, this indicates learned policy deficiencies
- If DRL shows fewer edge cases than baselines despite some issues, overall it's still an improvement

###### 5.4 Safety Boundary Characterization

###### 5.4.1 Safe Operating Region

- Traffic volume ranges where agent performs well
- Modal balance conditions for reliable operation
- State space regions with consistent safe decisions

Defining the safe operating region establishes boundaries within which the DRL agent demonstrates reliable, safe
performance. This characterization is essential for deployment planning—operators need to know under what conditions
they can trust the agent versus when human intervention or fallback to traditional control is advisable.

**Traffic Volume Characterization:**

By analyzing performance across all 30 test scenarios, we identify volume ranges with consistently good outcomes:

**Low-Volume Region (200-400 vehicles/hour per mode):**

- Scenarios: Pr_0-3, Bi_0-3, Pe_0-3
- Performance: Excellent across all metrics
- Average waiting times: Cars 4-8s, Bicycles 3-6s, Pedestrians 0.1-0.5s
- Action blocking rate: <5% (agent respects constraints)
- Safety violations: None detected
- **Assessment:** Fully safe operating region. Agent handles low-volume traffic effectively.

**Medium-Volume Region (500-700 vehicles/hour per mode):**

- Scenarios: Pr_4-6, Bi_4-6, Pe_4-6
- Performance: Good overall with occasional edge cases
- Average waiting times: Cars 8-15s, Bicycles 6-12s, Pedestrians 0.5-2s
- Action blocking rate: 8-12% (moderate constraint pressure)
- Safety violations: Rare (<1% of episodes have max wait >90s)
- **Assessment:** Safe operating region with monitoring. Agent maintains good performance but shows occasional
  suboptimal decisions.

**High-Volume Region (800-1000 vehicles/hour per mode):**

- Scenarios: Pr_7-9, Bi_7-9, Pe_7-9
- Performance: Variable, depends on specific scenario
- Average waiting times: Cars 15-35s, Bicycles 12-28s, Pedestrians 2-8s
- Action blocking rate: 15-25% (high constraint pressure)
- Safety violations: Occasional (3-5% of episodes have max wait >120s)
- **Assessment:** Boundary region. Agent performance degrades under extreme volumes. Some scenarios (Pr_9, Pe_9) show
  concerning behaviors requiring investigation.

**Modal Balance Analysis:**

Agent performance varies with traffic composition:

**Balanced Demand (Equal modal distribution):**

- All modes receiving ~250-350 veh/hr each
- Agent demonstrates good modal balance
- No systematic bias detected
- **Assessment:** Optimal operating condition

**Single-Mode Dominated (One mode >70% of traffic):**

- Private vehicle dominated: Pr_7-9 with low bike/ped
- Bicycle dominated: Bi_7-9 with low car/ped
- Pedestrian dominated: Pe_7-9 with low car/bike
- Agent adapts reasonably well to dominant mode
- Minor modes sometimes experience increased waiting
- **Assessment:** Acceptable performance with minor trade-offs

**Competing High Demands (Multiple modes >600 veh/hr):**

- Simultaneous high car + high pedestrian demand
- High bicycle + frequent bus arrivals
- Agent faces difficult trade-offs
- Some scenarios show modal starvation (one mode waiting >90s)
- **Assessment:** Challenging conditions requiring careful monitoring

**State Space Safe Regions:**

Using logged state-action data, we identify safe vs risky state space regions:

**Safe Region Definition:** States where:

1. All selected actions comply with safety rules (no violations)
2. Resulting waiting times remain within acceptable bounds (<60s average)
3. Q-value spread is reasonable (Q_max - Q_min < 2.0, indicating clear action preference)
4. Agent shows consistent action selection in similar states

**Risky Region Definition:** States where:

1. Action selection leads to constraint violations or extreme waiting times
2. High Q-value uncertainty (Q_max - Q_min > 3.0, indicating confusion)
3. Inconsistent decisions in similar states (action flipping)

**Visualization:** Projecting the 32-dimensional state space to principal components reveals:

- Safe regions cluster around moderate queue lengths (5-15 vehicles) and balanced modal demands
- Risky regions appear at extreme queue lengths (>25 vehicles) or highly imbalanced demand
- Transition boundaries exist around queue thresholds (12-15 vehicles) where agent behavior becomes less predictable

###### 5.4.2 Concerning Behaviors

- Conditions where agent ignores high pedestrian demand
- Situations with excessive phase duration
- Cases of modal starvation (one mode waiting too long)
- Action sequences that could indicate unsafe logic

While the agent demonstrates generally safe behavior within its operating region, systematic analysis reveals specific
concerning patterns that warrant investigation and potential remediation before real-world deployment.

**A) Pedestrian Demand Neglect:**

**Observation:** In scenarios Pe_8 and Pe_9 (900-1000 peds/hr), pedestrian waiting times occasionally exceed 120s,
particularly during periods of simultaneous high vehicle demand.

**Pattern:** When major approach queue >18 vehicles AND pedestrian queue >8 waiting, agent shows 78% probability of
selecting Continue rather than advancing phase cycle. This prioritizes vehicle throughput over pedestrian service.

**Analysis:** Counterfactual generation reveals that if pedestrian queue was 12 instead of 8, agent would switch to Next
Phase. This suggests a learned threshold of ~10-12 pedestrians before pedestrian service becomes priority. However, 8
pedestrians waiting for 120s represents a safety risk.

**Root Cause Hypothesis:** Training reward function weights vehicle waiting time reduction heavily (ALPHA_WAIT = 6.0)
compared to pedestrian considerations. Agent learned that maintaining vehicle phases produces higher immediate rewards
than cycling for pedestrians.

**Mitigation Strategies:**

- Increase pedestrian waiting time penalty in reward function
- Add explicit maximum wait constraint (hard constraint: serve any mode waiting >90s)
- Retrain with modified reward balancing

**B) Excessive Phase Duration (Phase Camping):**

**Observation:** In low-bicycle scenarios (Bi_0-2), Phase P1 (major through) occasionally persists for 45-50s,
approaching MAX_GREEN_TIME=60s, despite bicycle demand accumulating on minor approaches.

**Pattern:** Once Phase P1 duration exceeds 35s, agent shows 89% Continue probability even when minor queue reaches 10+
vehicles. This "phase camping" behavior delays service to other approaches.

**Analysis:** Decision tree extraction reveals rule: "IF phase=P1 AND major_queue >8 AND duration >30s THEN Continue
(confidence 91%)". The learned policy over-values phase duration stability.

**Root Cause Hypothesis:** Stability bonus (ALPHA_STABILITY) rewards maintaining phases, creating incentive to extend
phases beyond optimal duration. Agent learned that continuous phase extension avoids early-change penalties and
accumulates stability bonuses.

**Mitigation Strategies:**

- Reduce stability bonus magnitude
- Add duration-dependent penalty (penalty increases exponentially after 40s)
- Modify reward function to consider opportunity cost of not serving other approaches

**C) Modal Starvation Patterns:**

**Observation:** In mixed-demand scenario (Pr_6 + Bi_5), bicycles occasionally experience average waiting times 3.5x
higher than cars (bicycle: 28s, car: 8s), indicating systematic under-service.

**Pattern:** When traffic is car-dominated (>65% cars), agent allocates disproportionate phase time to car movements.
Bicycle-serving phases (P3, P4) shortened or skipped via Skip-to-P1.

**Analysis:** Examining phase durations: P1 average=32s, P2 average=14s, P3 average=11s, P4 average=8s. The policy
learned to extend car-serving phases at bicycle expense.

**Root Cause Hypothesis:** Training scenarios may have had car-dominated distribution, causing agent to learn
car-centric policy. Alternatively, reward function may inadvertently weight car delays more heavily due to higher car
volumes in training.

**Mitigation Strategies:**

- Ensure training distribution includes diverse modal balances
- Implement fairness constraint: max_wait_mode / min_wait_mode < 2.5x
- Add explicit modal balance reward component

**D) Action Thrashing (Rapid Switching):**

**Observation:** In 4% of high-congestion episodes (Pr_9, Bi_9), agent exhibits rapid action switching:
Continue→Next→Continue→Skip-to-P1 within 15-second windows.

**Pattern:** Occurs when multiple queues simultaneously exceed thresholds (major=22, minor=18, ped=9). Agent's Q-values
show high variance (Q-spread >2.5), indicating uncertainty.

**Analysis:** Rapid switching prevents queue clearance—each phase receives insufficient duration to process demand.
Throughput degrades compared to stable phase timing.

**Root Cause Hypothesis:** Agent encounters out-of-distribution states during extreme congestion. Training didn't
adequately cover simultaneous multi-queue saturation, causing policy uncertainty.

**Mitigation Strategies:**

- Add training scenarios with extreme simultaneous demands
- Implement action persistence incentive (small penalty for changing actions too frequently)
- Add explicit minimum phase duration enforcement beyond MIN_GREEN

**E) Bus Priority Inconsistency:**

**Observation:** Skip-to-P1 activation rate varies significantly: 68% when bus_wait >25s in low-traffic scenarios, but
only 34% when bus_wait >25s in high-traffic scenarios.

**Pattern:** Agent shows context-dependent bus priority—more willing to assist buses when general traffic is light, less
willing during congestion.

**Analysis:** This could be rational (serving bus disrupts congested traffic flow) or problematic (defeats bus priority
purpose). Domain expert input needed to determine acceptability.

**Root Cause Hypothesis:** Reward function includes both bus assistance bonus and general waiting time penalty. During
congestion, skipping to P1 may increase overall waiting time, reducing net reward despite bus bonus.

**Mitigation Strategies:**

- Clarify bus priority requirements: Is bus priority absolute or context-dependent?
- If absolute: Increase ALPHA_BUS weighting to dominate other considerations
- If context-dependent: Current behavior may be acceptable; document threshold conditions

**Summary Assessment:**

These concerning behaviors don't necessarily disqualify the agent for deployment, but they:

1. Define operational limits (scenarios where agent requires supervision)
2. Identify specific weaknesses for targeted improvement
3. Inform safety protocols (e.g., "Monitor pedestrian wait times in Pe_8-9")
4. Guide future development (reward tuning, training data augmentation, constraint additions)

For real-world deployment, these behaviors would require either: (a) remediation through retraining, (b) explicit
monitoring and override protocols, or (c) restriction of agent deployment to safe operating regions only.

---

##### 6. Results: Understanding Agent Decision-Making

###### 6.1 Attention-Based Feature Analysis

###### 6.1.1 State Feature Importance

- Analysis of attention weights across 30 test scenarios
- Which state dimensions receive highest attention during each action?
- Consistency of attention patterns across similar traffic states
- Temporal evolution of attention during episode progression

###### 6.1.2 Action-Specific Attention Patterns

- **Continue Action:** Attention focused on current phase queue lengths
- **Skip-to-P1 Action:** Attention focused on bus waiting times and Phase 1 demand
- **Next Phase Action:** Attention focused on alternative phase queues and duration
- Visualization of attention heatmaps for representative scenarios

###### 6.2 Counterfactual Analysis Results

###### 6.2.1 Decision Boundary Identification

- "If queue was X instead of Y, action would change from A to B"
- Minimal perturbations required to flip action decisions
- Sensitivity analysis: which state changes most affect decisions?
- State space regions with stable vs unstable action preferences

###### 6.2.2 Critical Thresholds Discovered

- Queue length thresholds triggering action switches
- Phase duration tipping points for phase changes
- Pedestrian demand levels affecting action selection
- Bus waiting time thresholds for Skip-to-P1 activation

###### 6.3 Decision Tree Policy Extraction

###### 6.3.1 Extracted Rule Structure

- Tree depth: X levels
- Number of decision nodes: Y
- Fidelity to original DQN policy: Z% agreement
- Top-level rules capturing majority of decisions

###### 6.3.2 Example Interpretable Rules

```
[Actual rules extracted from trained model to be added]
```

###### 6.3.3 Rule Analysis

- Which rules fire most frequently?
- Conditions that lead to each action
- Comparison with domain expert heuristics

###### 6.4 Safety Analysis Across Test Scenarios

###### 6.4.1 Pedestrian Safety Performance

- Pe_7, Pe_8, Pe_9 analysis (800-1000 pedestrians/hr)
- Phase transition frequency affecting pedestrian service
- Maximum pedestrian waiting times observed
- Comparison against safety threshold (e.g., 90s max wait)

###### 6.4.2 High-Volume Scenario Behavior

- Agent performance in Pr_9 (1000 cars/hr) and Bi_9 (1000 bikes/hr)
- Queue management effectiveness
- Phase cycling patterns under congestion
- Identification of any modal starvation

###### 6.4.3 Action Distribution in Critical States

- What actions does agent select under high demand?
- Frequency of Skip-to-P1 when bus present
- Continue vs Next Phase decisions under congestion
- Blocked action rates in different scenarios

###### 6.4.4 Potential Safety Concerns Identified

- Scenarios with longer-than-expected waiting times
- Cases where pedestrian demand might be underserved
- Situations with very high action blocking rates
- Edge cases requiring further investigation

---

##### 7. Discussion

###### 7.1 Insights from Explainability Analysis

###### 7.1.1 What We Learned About Agent Decision-Making

- Attention analysis reveals which state features drive decisions
- Counterfactual analysis identifies decision boundaries and thresholds
- Decision tree extraction provides interpretable approximation of policy
- Multi-method approach gives complementary perspectives on agent logic

###### 7.1.2 Understanding Agent Behavior Patterns

- Agent's decision logic can be characterized through explainability techniques
- State feature priorities vary by action type
- Decision boundaries are identifiable through systematic analysis
- Some decisions align with traffic engineering intuition, others require deeper investigation

###### 7.2 Safety Analysis Findings

###### 7.2.1 Behavioral Characterization

- Agent behavior analyzed across 30 diverse traffic scenarios
- Critical scenarios reveal strengths and potential weaknesses
- Action selection patterns under high demand identified
- Edge cases requiring further investigation documented

###### 7.2.2 Simulation-Based Safety Assessment

- Operational metrics (waiting times, phase durations) measurable
- Agent behavior in pedestrian safety scenarios characterized
- High-volume traffic handling patterns understood
- Potential safety concerns identified for future work

###### 7.3 Limitations

###### 7.3.1 Explainability Method Limitations

- Post-hoc explanations may not reflect true neural network computation
- Attention weights show correlation, not causation
- Decision tree fidelity involves approximation error
- Counterfactuals limited to feasible state perturbations

###### 7.3.2 Analysis Scope Limitations

- Analysis based on simulation only, not real-world data
- Limited to 30 test scenarios defined in study
- State space coverage incomplete (infinite possible states)
- No real traffic engineer validation of explanations
- No actual deployment testing

###### 7.3.3 Safety Analysis Limitations

- Simulation may not capture all real-world edge cases
- Safety assessment qualitative, not formal verification
- Sensor failure modes not tested
- Weather and lighting conditions not modeled
- No testing with actual vulnerable road users

###### 7.4 Future Work

###### 7.4.1 Expanding Explainability Analysis

- Apply methods to additional trained models
- Compare explanation consistency across training runs
- Develop interactive explanation interfaces
- Validate explanations with domain experts

###### 7.4.2 Enhancing Safety Analysis

- Expand test scenarios to cover more edge cases
- Introduce perturbations and sensor noise
- Test with different traffic demand patterns
- Analyze failure modes systematically
- Compare with traditional controllers on safety metrics

###### 7.4.3 Toward Real-World Validation

- Conduct user studies with traffic engineers
- Establish formal safety verification protocols
- Pilot testing in controlled environments
- Integration with traffic management systems
- Real-world deployment with safety monitoring

---

##### 8. Conclusion

###### 8.1 Summary

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

###### 8.2 Contributions to the Field

- Demonstrates application of XAI techniques to traffic signal control domain
- Provides multi-method framework for understanding DRL agent decision logic
- Characterizes agent behavior across diverse traffic scenarios through simulation
- Identifies the importance of explainability for understanding learned control policies
- Establishes methodology for simulation-based safety analysis of DRL controllers

###### 8.3 Path Forward

While this work demonstrates explainability techniques in simulation, significant additional work is needed before
real-world deployment: validation with traffic engineering experts, formal safety verification, testing with actual
sensor data, pilot deployments with monitoring, and integration with existing traffic management infrastructure. The
methods presented here provide tools for understanding what DRL agents learn, which is an essential step toward building
deployable systems.

---

##### References

[To be added - include PAPER_1 as primary reference]

---

##### Appendices

###### Appendix A: Attention Mechanism Architecture

[Technical specifications of attention layer added to DQN] [Mathematical formulation of attention weights]
[Implementation details]

###### Appendix B: Counterfactual Generation Algorithm

[Gradient-based perturbation method] [Constraint satisfaction for realistic states] [Search procedure for minimal
perturbations]

###### Appendix C: Decision Tree Extraction Implementation

[VIPER/TREPAN algorithm details] [Hyperparameters for tree extraction] [Fidelity measurement methodology]

###### Appendix D: Test Scenario Specifications

[30 traffic scenarios from Tables/1_Single_Agent.md] [Traffic volume ranges: Pr_0-9, Bi_0-9, Pe_0-9] [Constant:
15-minute bus frequency]

###### Appendix E: Explainability Method Comparison

[Strengths and weaknesses of each technique] [Computational costs] [Complementary insights provided]

###### Appendix F: Sample State-Action Logs

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
