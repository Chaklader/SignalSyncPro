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
$$\mathbf{s}^* = \arg\min_{\mathbf{s}'} \|\mathbf{s}' - \mathbf{s}\|_2 \quad \text{subject to} \quad \arg\max_{a'} Q_\theta(\mathbf{s}', a') \neq a$$

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

###### 1.5 Paper Organization

Section 2 reviews XAI literature. Section 3 summarizes the base DRL model. Section 4 presents explainability
methodologies. Section 5 describes simulation-based safety analysis. Section 6 shows results from applying these methods
to the trained agent across 30 test scenarios. Section 7 discusses findings and limitations. Section 8 concludes.

The remainder of this paper is organized as follows. **Section 2** reviews related work in explainable AI, focusing on
post-hoc interpretation methods for neural networks, XAI applications in autonomous systems, and safety verification
approaches for reinforcement learning agents. We position our work within the broader landscape of interpretable machine
learning and identify gaps our research addresses.

**Section 3** briefly summarizes the base DRL model from our previous work (PAPER_1): the DQN-PER architecture with
32-dimensional state representation, 3-action space, multi-component reward function incorporating waiting times and
safety penalties, training methodology using prioritized experience replay, and performance results showing 15-40%
waiting time reductions across 30 test scenarios. This establishes the trained agent (Episode 192, checkpoint file:
`dqn_model_episode_192.pth`) as the subject of explainability analysis.

**Section 4** presents our explainability methodologies in detail. We describe attention mechanism integration for
feature attribution, counterfactual generation algorithms for decision boundary identification, decision tree extraction
via VIPER for rule-based policy approximation, and gradient-based saliency analysis. Each method includes mathematical
formulation, implementation details, and interpretation protocols.

**Section 5** details the simulation-based safety analysis framework. We define critical test scenarios focusing on
pedestrian safety (Pe_7-9: 800-1000 peds/hour), extreme traffic volumes (Pr_9, Bi_9: 1000 vehicles/hour), and bus
priority situations. We specify safety metrics including maximum waiting times, phase activation patterns, minimum green
time compliance, and action distribution under high demand. The section describes how we systematically analyze agent
behavior across these scenarios using SUMO microsimulation replays.

**Section 6** presents results from applying explainability methods and safety analysis to the trained agent. We report
attention weight distributions revealing which state features drive decisions, counterfactual thresholds identifying
decision boundaries (e.g., "queue > 10 triggers phase change"), extracted decision tree rules approximating the policy
with measured fidelity, and behavioral analysis showing agent responses in critical scenarios including pedestrian
safety performance and bus priority activation patterns.

**Section 7** discusses findings, limitations, and implications. We synthesize insights from multiple explainability
techniques, assess alignment between learned policies and traffic engineering principles, identify concerning edge cases
requiring further investigation, acknowledge limitations of simulation-based analysis and post-hoc explanation methods,
and propose directions for future work toward real-world validation.

**Section 8** concludes by summarizing contributions, reflecting on the necessity of interpretability for deploying DRL
in safety-critical domains, and outlining the path from simulation-based explainability analysis to real-world
deployment with appropriate safety monitoring.

---

##### 2. Related Work

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

$$\phi_i = \sum_{S \subseteq \mathcal{F} \setminus \{i\}} \frac{|S|! (|\mathcal{F}| - |S| - 1)!}{|\mathcal{F}|!} [f_{S \cup \{i\}}(x_{S \cup \{i\}}) - f_S(x_S)]$$

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

$$\pi_{\text{tree}} = \arg\min_{\pi' \in \Pi_{\text{trees}}} \mathbb{E}_{\mathbf{s} \sim d^{\pi_{\text{NN}}}} [\mathbb{1}[\pi'(\mathbf{s}) \neq \pi_{\text{NN}}(\mathbf{s})]]$$

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

$$\max_\theta \mathbb{E}_{\tau \sim \pi_\theta}[R(\tau)] \quad \text{subject to} \quad \mathbb{E}_{\tau \sim \pi_\theta}[C(\tau)] \leq d$$

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

###### 4.1.2 Interpretation Protocol

- Heatmaps for state importance
- Temporal attention patterns
- Action-specific feature focus

###### 4.1.3 Example Explanations

- "Agent prioritizes queue length on approach lane (attention weight: 0.42)"
- "Pedestrian waiting time receives high attention during phase transition decisions"

###### 4.2 Counterfactual Explanation Generation

###### 4.2.1 Methodology

- Minimal state perturbations that flip decision
- "If queue was X cars instead of Y, action would have been Z"
- Actionable insights for operators

###### 4.2.2 Counterfactual Search Algorithm

- Gradient-based perturbation
- Constraint satisfaction (realistic states only)
- Multiple counterfactual generation

###### 4.2.3 Example Counterfactuals

- "If car queue was 5 instead of 10, would have extended green by 5s"
- "If bus wasn't present, would not have activated Skip-to-P1"

###### 4.3 Decision Tree Policy Extraction

###### 4.3.1 VIPER Algorithm Application

- Distill DQN policy into interpretable decision tree
- Iterative dataset aggregation
- Tree pruning for simplicity

###### 4.3.2 Tree Structure and Rules

- Maximum depth: 8 levels
- ~90% fidelity to original DQN policy
- Human-readable if-then rules

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

$$\text{Saliency}_i(a) = \left| \frac{\partial Q(\mathbf{s}, a)}{\partial s_i} \right|$$

High saliency indicates that small changes to feature $s_i$ significantly affect the Q-value for action $a$.

###### 4.4.2 Visualization Methods

- Per-action saliency maps
- Temporal saliency evolution
- Critical state dimension identification

###### 4.5 Natural Language Explanation Generation

###### 4.5.1 Template-Based System

- Action templates: "Extended green because {reason}"
- Reason extraction from attention + saliency
- Context-aware explanation selection

###### 4.5.2 Example Generated Explanations

- "Maintained current phase due to high vehicle queue (18 cars) on major approach"
- "Activated Skip-to-P1 to prioritize bus on main corridor (wait time: 23s)"
- "Advanced to next phase in cycle as pedestrian queue (8 waiting) exceeded threshold"

---

##### 5. Simulation-Based Safety Analysis

###### 5.1 Critical Scenario Design

###### 5.1.1 Pedestrian Safety Scenarios

- High pedestrian demand scenarios (Pe_7 to Pe_9: 800-1000 peds/hr)
- Analyzing agent's phase transition patterns affecting pedestrian service
- Measuring pedestrian waiting times
- Comparing against safe thresholds (e.g., max wait < 90s)

###### 5.1.2 High-Volume Traffic Scenarios

- Extreme car volumes (Pr_7 to Pr_9: 800-1000 cars/hr)
- Extreme bicycle volumes (Bi_7 to Bi_9: 800-1000 bikes/hr)
- Agent behavior under congestion
- Queue buildup and clearance patterns

###### 5.1.3 Mixed Demand Scenarios

- Competing modal priorities (high cars + high peds)
- Bus arrival timing analysis
- Multi-modal conflict resolution
- Action selection under competing demands

###### 5.2 Safety Metrics from Simulation

###### 5.2.1 Operational Safety Indicators

- **Phase Duration Compliance:** % of phase changes respecting MIN_GREEN_TIME
- **Maximum Waiting Time:** Longest wait experienced by any mode
- **Modal Service Quality:** Average waiting times per mode under varying demand
- **Action Blocking:** % of attempted actions blocked by safety constraints
- **Emergency Response:** Agent behavior when bus approaches

###### 5.2.2 Behavioral Analysis Methods

- Replay 30 test scenarios from Tables/1_Single_Agent.md
- Log all state-action pairs
- Identify potential safety violations
- Compare agent decisions to safety rules

###### 5.3 Decision Pattern Analysis

###### 5.3.1 Action Selection Under Critical Conditions

- What does agent do when queue > 20 vehicles?
- How does agent respond to pedestrian demand > 6 people?
- When does agent activate Skip-to-P1 for bus priority?
- Phase switching patterns under congestion

###### 5.3.2 Edge Case Identification

- Scenarios where agent makes questionable decisions
- States where action choice seems suboptimal
- Conditions leading to blocked actions
- Instances of very long waiting times

###### 5.4 Safety Boundary Characterization

###### 5.4.1 Safe Operating Region

- Traffic volume ranges where agent performs well
- Modal balance conditions for reliable operation
- State space regions with consistent safe decisions

###### 5.4.2 Concerning Behaviors

- Conditions where agent ignores high pedestrian demand
- Situations with excessive phase duration
- Cases of modal starvation (one mode waiting too long)
- Action sequences that could indicate unsafe logic

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
