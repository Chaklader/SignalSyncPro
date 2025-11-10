# Deep Reinforcement Learning with Prioritized Experience Replay for Adaptive Multi-Modal Traffic Signal Control

**Abstract**

Urban traffic signal control systems face increasing complexity as cities prioritize multi-modal transportation
infrastructure serving private vehicles, bicycles, pedestrians, and public transit. Traditional approaches either
optimize for vehicular throughput at the expense of other modes (Reference Control) or rely on fixed rule-based
heuristics for modal coordination (Developed Control), both proving inadequate for dynamic, high-density urban
environments. This paper presents a Deep Q-Network (DQN) architecture augmented with Prioritized Experience Replay (PER)
that learns adaptive signal control policies for multi-modal intersections through reinforcement learning. The PER
mechanism addresses the challenge of rare but critical traffic events—such as bus priority conflicts, signal
synchronization opportunities, and extreme traffic volume conditions—by preferentially sampling high-temporal-difference
experiences during training, accelerating convergence and improving policy quality. Our agent operates on a
32-dimensional state space capturing queue lengths, phase states, waiting times, and modal demands across a
two-intersection corridor network with four signal phases (major through, major left, minor through, minor left),
selecting from three actions: Continue current phase, Skip to Phase 1 (arterial coordination), or advance to Next Phase.
Training employed a two-phase methodology over 200 episodes with progressive reward function recalibration to achieve
target action distribution ratios (85% Continue, 2.5% Skip, 12.5% Next) while maintaining multi-modal service equity.
Extensive evaluation across 30 systematically designed traffic scenarios (varying private car, bicycle, and pedestrian
volumes from 100-1000/hour) using SUMO simulation demonstrates that DRL-PER achieves transformational improvements for
vulnerable road users: 88.6% reduction in bicycle waiting times (from 208.5s to 23.8s), 93.6% reduction in pedestrian
waiting times (from 48.4s to 3.1s), and 83.3% reduction in bus waiting times (from 25.2s to 4.2s) compared to Reference
Control. Compared to the rule-based Developed Control, the agent achieves 50.5% improvement for bicycles, 81.8% for
pedestrians, and 74.1% for buses. This multi-modal optimization comes with a trade-off of 20.0% higher private car
waiting times (43.8s vs 36.5s) compared to Developed Control, reflecting the agent's learned priority for vulnerable
road users and public transit. Our results validate that combining deep reinforcement learning with prioritized
experience replay enables adaptive, equity-focused traffic signal coordination that fundamentally rebalances urban
intersection priorities toward sustainable and inclusive mobility.

**Keywords:** Deep Reinforcement Learning, Traffic Signal Control, Multi-Modal Transportation, Prioritized Experience
Replay, DQN, Adaptive Control, Urban Mobility

---

---

TODO:

1. Add image to the peper using the following HTML format:

<div align="center">
<img src="images/1/phase_structure.png" alt="Phase Structure Diagram" width="400" height=auto/>
<p align="center">figure: Four-phase signal control structure showing permitted movements and transitions.</p>
</div>

2. Copy table from the table MarkDown file and add it to the paper without deleteing the original table.

---

---

##### 1. Introduction

###### 1.1 Motivation and Background

Urban traffic congestion imposes substantial economic, environmental, and social costs on cities worldwide, with
estimates suggesting that congestion-related delays cost the U.S. economy alone over $120 billion annually in lost
productivity and wasted fuel. As cities transition toward sustainable mobility paradigms, transportation infrastructure
must accommodate increasingly diverse user populations: private vehicles, public transit, bicycles, and pedestrians.
This multi-modal reality fundamentally challenges traditional traffic signal control systems, which were predominantly
designed to optimize vehicular throughput on road networks conceived for automobile-centric mobility.

Contemporary urban planning prioritizes **Complete Streets** frameworks that provide equitable access across all
transportation modes. However, signal control systems have not evolved commensurately. Conventional fixed-time
controllers assign predetermined green intervals to each traffic phase based on historical average demand, proving
inflexible to real-time traffic fluctuations. Actuated control systems respond to vehicle detector presence but
typically prioritize motorized traffic, offering limited accommodation for vulnerable road users (cyclists, pedestrians)
whose demand patterns differ fundamentally from vehicular flow. Even sophisticated adaptive systems like SCOOT and SCATS
optimize primarily for vehicle delay minimization, treating non-motorized modes as constraints rather than co-equal
objectives.

The result is a persistent tension: maximizing vehicle throughput often occurs at the expense of cyclist and pedestrian
service quality, manifesting as excessive waiting times, abbreviated crossing intervals, and safety conflicts.
Buses—carrying 30-50 passengers per vehicle—frequently experience delays comparable to single-occupancy automobiles,
undermining the attractiveness of public transit. This inequity contradicts sustainable transportation goals and
perpetuates automobile dependence, particularly among populations with modal alternatives.

###### 1.2 Limitations of Traditional Approaches

**Fixed-Time Control** assigns static green time allocations derived from time-of-day demand patterns, offering
predictability but no responsiveness to actual traffic conditions. During off-peak periods, intersections waste green
time on empty approaches; during peak periods, undersaturated phases fail to clear accumulated queues. Multi-modal
considerations are incorporated through conservative minimum green times for pedestrian crossings, which often prove
insufficient under high pedestrian demand yet wasteful when crosswalks remain empty.

**Actuated Control** improves upon fixed timing by extending green phases when vehicle detectors register continued
demand, terminating phases early during gap-outs (extended periods without detector activation). However, standard
actuation logic employs **fixed decision thresholds**: detector occupancy triggers phase extensions, detector absence
triggers phase termination. These thresholds cannot adapt to cross-modal trade-offs. For instance, extending a vehicular
green phase benefits car throughput but delays waiting cyclists, yet the controller possesses no mechanism to evaluate
whether the marginal vehicle delay reduction justifies the incremental bicycle delay increase.

**Rule-Based Multimodal Control** systems (such as the "Developed Control" baseline in this study) introduce
hierarchical decision logic: maximum green constraints prevent starvation, bus priority rules trigger phase skipping,
bicycle detection windows extend phases to accommodate slower-moving cyclists. While representing a significant advance
over single-mode optimization, these systems suffer from **combinatorial complexity** in rule design. Balancing seven
competing objectives—minimizing car, bicycle, pedestrian, and bus waiting times; ensuring safety; reducing emissions;
maintaining coordination—requires manual specification of hundreds of condition-action rules with fixed priority
orderings. The resulting policies exhibit brittleness: they perform well under anticipated conditions but degrade when
traffic patterns deviate from design assumptions.

Fundamentally, these approaches lack a **unified optimization framework** capable of discovering near-optimal control
policies through experience rather than manual engineering. Traffic signal control constitutes a sequential
decision-making problem under uncertainty, where the consequences of actions (phase changes) materialize over time
horizons spanning minutes to hours. Traditional methods decompose this problem into myopic rules, sacrificing long-term
optimality for computational tractability and interpretability.

###### 1.3 Deep Reinforcement Learning for Traffic Control

Deep Reinforcement Learning (DRL) addresses these limitations by framing traffic signal control as a **Markov Decision
Process (MDP)**, where an agent learns a control policy $\pi: \mathcal{S} \to \mathcal{A}$ mapping observed traffic
states to control actions through trial-and-error interaction with a simulated environment. Unlike supervised learning,
which requires labeled examples of "correct" signal timings, reinforcement learning discovers optimal behavior by
maximizing a cumulative reward signal that encodes system objectives (e.g., minimize total waiting time across all
modes, prevent safety violations, maintain coordination).

The **Deep Q-Network (DQN)** architecture, which achieved superhuman performance on Atari games, approximates the
action-value function $Q(s,a)$—the expected cumulative reward from taking action $a$ in state $s$ and following the
optimal policy thereafter—using a deep neural network. This function approximation overcomes the curse of dimensionality
inherent in tabular methods, enabling generalization across the continuous, high-dimensional state spaces characteristic
of real-world traffic systems. A 32-dimensional state vector capturing queue lengths, phase durations, detector
occupancies, and bus presence across two intersections would require intractably large lookup tables in classical
Q-learning but maps naturally to a compact neural network with ~100,000 parameters.

**Prioritized Experience Replay (PER)** further enhances learning efficiency by preferentially sampling training
experiences with high temporal-difference (TD) error—instances where the agent's predictions were most incorrect. In
traffic control, critical events like bus arrivals, coordination opportunities with upstream signals, and near-safety
violations occur infrequently but carry disproportionate importance for policy quality. PER ensures the agent learns
intensively from these rare but informative experiences rather than treating all timesteps uniformly, accelerating
convergence and improving asymptotic performance.

The multi-modal traffic signal control problem exhibits characteristics ideally suited to DRL:

- **High-dimensional state space**: 32 features per two-intersection corridor (queue occupancies, phase states, detector
  readings, modal demands)
- **Delayed consequences**: Signal timing decisions affect traffic conditions minutes downstream
- **Complex reward structure**: 14 competing objectives spanning efficiency, equity, safety, and emissions
- **Partial observability**: The agent observes detector measurements, not complete traffic state
- **Non-stationary environment**: Traffic demand patterns vary by scenario, time of day, and stochastic arrival
  processes

Traditional control methods struggle with this complexity; DRL thrives in it, discovering nonlinear control policies
that balance competing objectives through end-to-end optimization.

###### 1.4 Research Contributions

This paper presents a novel application of DQN with Prioritized Experience Replay to multi-modal urban traffic signal
control, demonstrating transformational performance improvements for vulnerable road users while maintaining vehicular
service quality. Our key contributions include:

1. **Multi-Objective Reward Architecture**: A 14-component reward function decomposing traffic signal control into
   environmental feedback (waiting times, emissions, safety), meta-level guidance (action diversity, stability), and
   constraint enforcement (minimum green times, blocked actions). The hierarchical structure separates actual traffic
   consequences from training statistics, preventing pathological reward hacking.

2. **Centralized Coordination Strategy**: A single-agent architecture controlling two intersections simultaneously
   achieves natural signal coordination without requiring explicit synchronization mechanisms. Both intersections
   transition to the same phase concurrently, creating implicit green wave progression through learned phase timing
   rather than engineered offsets.

3. **Phase-Aware Duration Hierarchy**: Five nested timing thresholds (minimum green, stability, next bonus, consecutive
   continue, maximum green) encode safety constraints, efficiency incentives, and equity guarantees. The agent learns
   context-dependent phase durations within these bounds, achieving traffic-responsive timing while respecting
   engineering standards (ITE, MUTCD).

4. **Two-Phase Training Methodology**: After 100 episodes of initial training, reward function recalibration refined
   Skip-to-Phase-1 incentives and stability bonuses to achieve target action distributions (85% Continue, 2.5% Skip,
   12.5% Next), balancing exploration efficiency with operational realism.

5. **Comprehensive Multi-Modal Evaluation**: Testing across 30 systematically designed scenarios (varying car, bicycle,
   pedestrian demand from 100-1000/hour) reveals that DRL-PER achieves 88.6% bicycle waiting time reduction, 93.6%
   pedestrian reduction, and 83.3% bus reduction compared to baseline vehicular-optimized control, with 50.5%, 81.8%,
   and 74.1% improvements respectively over rule-based multi-modal control.

Our results validate that deep reinforcement learning can discover adaptive, equity-focused traffic signal policies that
fundamentally rebalance urban intersection priorities toward vulnerable road users and public transit—a paradigm shift
from automobile-centric optimization to truly multi-modal transportation systems.

---

##### 2. Related Work

###### 2.1 Traditional Traffic Signal Control

Traffic signal control research spans over a century, beginning with the first electric traffic light installation in
Cleveland, Ohio (1914) and evolving through successive generations of increasingly sophisticated control logic.

**Fixed-Time Control** remains the dominant approach in practice, with signal timings computed offline using historical
traffic counts and Webster's delay minimization formula (Webster, 1958). These controllers partition each signal cycle
into fixed green intervals for each phase, with timing plans switching by time of day (AM peak, midday, PM peak,
overnight). While offering predictability and simplicity, fixed-time control cannot respond to real-time demand
fluctuations, resulting in inefficient green time allocation during non-peak periods and insufficient capacity during
demand surges.

**Actuated Control** introduced in the 1950s-1960s employs vehicle detectors to extend green phases when demand persists
and terminate phases early during detector gap-outs. The NEMA (National Electrical Manufacturers Association) and Type
170/2070 controller standards formalize this logic through programmable minimum/maximum green times, vehicle/pedestrian
extensions, and gap-out timers. However, actuation parameters (detector placement, extension intervals, gap-out
thresholds) require manual tuning, and most implementations prioritize vehicular movements over non-motorized modes.

**Adaptive Control Systems** emerged in the 1980s-1990s to optimize signal timing in real-time based on measured traffic
conditions. SCOOT (Split, Cycle, Offset Optimization Technique) developed in the UK employs a hill-climbing optimization
algorithm to adjust cycle length, green splits, and offsets every few minutes based on upstream detector data (Hunt et
al., 1981). SCATS (Sydney Coordinated Adaptive Traffic System) developed in Australia uses a library of pre-computed
timing plans, selecting and adapting the best-matching plan to current traffic patterns (Lowrie, 1990). Both systems
demonstrate 8-15% delay reductions compared to fixed-time control in field deployments but remain fundamentally
vehicle-centric, with bicycle and pedestrian accommodations treated as constraints rather than optimization objectives.

###### 2.2 Adaptive and Actuated Control Systems

Recent adaptive systems incorporate limited multi-modal considerations. **InSync** (Rhythm Engineering) employs
continuous detector monitoring with real-time optimization algorithms, claiming 25-35% delay reductions through dynamic
phase sequencing. **Opticom** (Global Traffic Technologies) provides emergency vehicle and transit signal priority
through GPS-based preemption requests. However, these systems employ **rule-based priority logic**: when a bus
approaches, extend the current green phase or advance to the bus-serving phase via pre-programmed rules. This approach
lacks the ability to evaluate trade-offs: should a bus carrying 40 passengers receive priority over 20 waiting cyclists,
or does the total person-delay minimize through bicycle service first?

**Multi-Objective Optimization** approaches frame signal control as explicit optimization problems. The
**Back-Pressure** algorithm (Varaiya, 2013) developed for network-level control adjusts green times proportionally to
queue length differences between upstream and downstream links, providing maximal stability guarantees under certain
traffic conditions. Extensions incorporate multiple vehicle classes with weighted priorities (Gregoire et al., 2015),
but these weights require manual specification and remain static across traffic conditions.

Recent work explores **Model Predictive Control (MPC)** for traffic signals, formulating finite-horizon optimization
problems that predict future traffic states under candidate control sequences and select actions minimizing predicted
delay (Aboudolas et al., 2013). MPC offers theoretical optimality guarantees but requires accurate traffic flow models
(macroscopic cell transmission models or microscopic car-following models) and suffers from computational complexity
limiting real-time applicability to small networks. Multi-modal MPC formulations (Lin et al., 2021) incorporate
pedestrian and bicycle phases but rely on simplified flow models that may not capture mode-specific behaviors (e.g.,
bicycle platoon dispersion, pedestrian clustering at crosswalks).

###### 2.3 Deep Reinforcement Learning in Traffic Management

The application of deep reinforcement learning to traffic signal control has accelerated dramatically since 2016,
enabled by advances in DRL algorithms (DQN, A3C, PPO) and traffic simulation platforms (SUMO, VISSIM, CityFlow).

**Single-Intersection Control**: Early DRL applications focused on isolated intersections. Genders and Razavi (2016)
applied DQN to a four-approach intersection, demonstrating 25% average delay reduction compared to actuated control
through learned phase selection policies. Li et al. (2016) incorporated convolutional neural networks to process traffic
state images (queue lengths visualized as occupancy grids), achieving improved generalization across demand patterns.
Wei et al. (2018) introduced **pressure-based rewards** measuring queue imbalance between competing movements, aligning
DRL objectives with provably stable back-pressure control.

**Multi-Intersection Coordination**: Coordinating signals across arterial corridors or grid networks introduces
scalability challenges. **Independent Learning** approaches train separate agents per intersection with local
observations, achieving computational scalability but potentially conflicting policies (Gao et al., 2017). **Multi-Agent
RL** methods enable inter-agent coordination through communication channels (Chu et al., 2019) or centralized training
with decentralized execution (Nishi et al., 2020), demonstrating 15-40% network delay reductions compared to independent
control.

**Graph Neural Networks** (GNNs) provide a natural representation for traffic network topology, with intersections as
nodes and road segments as edges. Wu et al. (2020) proposed Graph Convolutional Reinforcement Learning, enabling agent
policies to generalize across variable network topologies and scale to city-wide networks (100+ intersections) through
parameter sharing across nodes.

**Transfer Learning and Meta-Learning**: Training DRL agents for traffic control requires extensive simulation (millions
of timesteps), limiting deployment to new intersections. Recent work explores transfer learning from source to target
intersections with different geometries (Wang et al., 2021) and meta-learning approaches that enable rapid adaptation to
new demand patterns with minimal fine-tuning (Zhou et al., 2022).

However, most DRL traffic control research **prioritizes vehicular throughput**, measuring performance exclusively
through vehicle delay, queue length, or throughput metrics. Explicit multi-modal objectives remain underexplored.

###### 2.4 Multi-Modal Intersection Control

Multi-modal traffic signal optimization represents a nascent but growing research area, driven by urban planning trends
toward **Vision Zero** (eliminating traffic fatalities), **Complete Streets** (equitable infrastructure), and
**sustainable mobility** (mode shift from cars to active transportation).

**Pedestrian-Responsive Signals**: Traditional pedestrian phases employ fixed crossing times derived from crosswalk
length and assumed walking speed (3.5 ft/s for general population, 2.8 ft/s for elderly). Responsive systems use video
detection or thermal cameras to estimate pedestrian counts and extend clearance intervals when necessary (Kattan et al.,
2009). However, these systems remain reactive rather than anticipatory, failing to minimize pedestrian delay through
proactive phase scheduling.

**Bicycle Signal Accommodations**: Protected bicycle signal phases (dedicated green intervals with vehicular movements
stopped) improve safety but reduce vehicular capacity. Partial accommodations include **leading bicycle intervals** (3-5
second head start before vehicular green) and **bicycle detection extensions** (extending vehicular green when bicycle
detectors remain occupied). Lopez et al. (2018) developed a hierarchy of bicycle-specific signal timing parameters
(minimum bicycle green, bicycle extension intervals) calibrated to observed bicycle approach speeds and queue discharge
headways.

**Transit Signal Priority (TSP)**: Bus and light rail priority systems grant preferential signal timing when transit
vehicles approach intersections. **Passive priority** uses pre-programmed timing plans favoring transit routes (e.g.,
longer major-street greens on bus corridors). **Active priority** employs GPS-based transit vehicle detection,
triggering green extensions (holding current green for approaching buses) or early greens (advancing to bus-serving
phase). Evaluation studies report 8-15% transit travel time reductions but note adverse impacts on cross-street
vehicular and pedestrian delays (Smith et al., 2005).

**Multi-Objective Signal Timing Optimization**: Several studies formulate multi-modal signal control as **weighted
multi-objective optimization**, minimizing a composite function combining vehicle delay, pedestrian delay, bicycle
delay, emissions, and safety risk (Ma et al., 2019). Genetic algorithms, particle swarm optimization, and simulated
annealing discover Pareto-optimal timing plans trading off competing objectives. However, these approaches require
manual specification of objective weights (e.g., "pedestrian delay is 2× as important as vehicle delay"), which
inherently embed normative judgments and may not generalize across contexts.

**Rule-Based Multi-Modal Control**: Hierarchical rule systems provide a pragmatic alternative, prioritizing objectives
through tiered decision logic (safety → bus priority → actuation → coordination). The "Developed Control" baseline in
this study exemplifies this approach, employing maximum green constraints, bus-triggered phase skipping, bicycle
detection windows, and semi-synchronization between adjacent intersections. Such systems achieve 30-50% delay reductions
for vulnerable road users compared to vehicle-only actuation but exhibit brittleness when traffic conditions violate
design assumptions.

###### 2.5 Experience Replay Mechanisms

**Experience Replay** emerged as a critical stabilization technique in deep reinforcement learning, first popularized by
DQN (Mnih et al., 2015). By storing observed transitions $(s_t, a_t, r_t, s_{t+1})$ in a replay buffer and sampling
random mini-batches during training, experience replay breaks temporal correlation between consecutive samples, reducing
the risk of policy oscillation and catastrophic forgetting.

**Prioritized Experience Replay (PER)** introduced by Schaul et al. (2016) extends this concept by **non-uniformly
sampling** transitions based on their temporal-difference (TD) error magnitude:

$$p_i = (|\delta_i| + \epsilon)^\alpha$$

where $\delta_i = r_i + \gamma \max_{a'} Q(s_i', a') - Q(s_i, a_i)$ is the TD error for transition $i$, $\epsilon$
prevents zero probabilities, and $\alpha$ controls prioritization strength. Transitions where the agent's predictions
were most incorrect receive higher sampling probability, focusing learning on "surprising" experiences.

To correct for the bias introduced by non-uniform sampling, importance sampling weights $w_i = (N \cdot p_i)^{-\beta}$
are applied during gradient computation, with $\beta$ annealing from 0.4 to 1.0 over training to ensure convergence to
the optimal policy. Schaul et al. demonstrated that PER accelerates learning by 2-3× on Atari benchmarks, achieving
higher asymptotic performance than uniform replay.

In traffic signal control, PER addresses the challenge of **rare but critical events**: bus arrivals (4 buses/hour),
signal coordination opportunities (occur only when platoons arrive at specific phase timings), and near-safety
violations (infrequent but high-consequence). Uniform sampling would under-represent these events; PER ensures the agent
learns intensively from them. Wang et al. (2019) applied PER to single-intersection DRL control, reporting 15% faster
convergence than standard DQN, but did not explore multi-modal objectives or multi-intersection coordination.

###### 2.6 Research Gap and Positioning

Despite extensive research in adaptive traffic control, deep reinforcement learning, and multi-modal transportation, a
critical gap persists: **no prior work combines DRL with Prioritized Experience Replay for multi-modal,
multi-intersection traffic signal control with explicit equity objectives**.

Existing limitations include:

- **DRL applications optimize primarily for vehicular throughput**, measuring success through vehicle delay reduction
  without evaluating impacts on vulnerable road users
- **Multi-modal optimization approaches employ manual objective weighting**, requiring a priori specification of
  relative priorities rather than discovering trade-offs through experience
- **Rule-based multi-modal systems** achieve reasonable performance but lack adaptability, requiring re-engineering when
  traffic patterns change
- **Experience replay mechanisms remain underutilized** in traffic control, despite their potential to accelerate
  learning from rare critical events (bus priority, signal coordination)

This paper addresses these gaps by:

1. **Integrating PER into multi-modal DRL traffic control**, enabling efficient learning from infrequent but high-impact
   events (bus arrivals, coordination opportunities)
2. **Designing a 14-component multi-objective reward function** that encodes safety, efficiency, equity, and
   sustainability objectives without requiring manual inter-objective weighting
3. **Demonstrating 88.6-93.6% waiting time reductions for vulnerable road users** through learned policies that
   fundamentally rebalance intersection priorities
4. **Validating centralized single-agent coordination** as an effective approach for closely-spaced intersections
   (300m), achieving synchronization through learned phase timing rather than engineered offsets
5. **Providing comprehensive multi-modal evaluation** across 30 systematically designed scenarios spanning
   low-to-saturation demand for cars, bicycles, and pedestrians

Our approach represents a paradigm shift from automobile-centric optimization to truly multi-modal traffic signal
control, demonstrating that DRL can discover adaptive, equitable policies aligning with contemporary sustainable urban
mobility goals.

---

##### 3. Problem Formulation

###### 3.1 Markov Decision Process Framework

We formulate multi-modal traffic signal control as a **Markov Decision Process (MDP)** defined by the tuple
$\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$, where:

- $\mathcal{S}$: State space representing traffic conditions
- $\mathcal{A}$: Discrete action space of signal control decisions
- $\mathcal{P}: \mathcal{S} \times \mathcal{A} \times \mathcal{S} \to [0,1]$: Transition probability function
- $\mathcal{R}: \mathcal{S} \times \mathcal{A} \times \mathcal{S} \to \mathbb{R}$: Reward function encoding objectives
- $\gamma \in [0,1]$: Discount factor balancing immediate vs. long-term rewards

The **Markov property** assumption holds that the current state $s_t$ contains sufficient information to predict future
states and rewards, independent of history. In traffic control, detector measurements (queue occupancies, phase states,
modal demands) combined with current phase timing provide a sufficient statistic for predicting near-term traffic
evolution under alternative control actions.

The agent learns a policy $\pi: \mathcal{S} \to \mathcal{A}$ maximizing expected cumulative discounted reward:

$$
\pi^* = \arg\max_{\pi} \mathbb{E}\left[\sum_{t=0}^{\infty} \gamma^t r_t \mid \pi\right]
$$

where $r_t = \mathcal{R}(s_t, a_t, s_{t+1})$ is the immediate reward at timestep $t$. With $\gamma = 0.99$, the
effective planning horizon spans approximately 100 seconds, capturing multi-phase traffic dynamics while maintaining
computational tractability.

###### 3.2 State Space Definition

The state space $\mathcal{S} \subseteq \mathbb{R}^{32}$ provides a comprehensive representation of current traffic
conditions at both intersections through a 32-dimensional feature vector:

$$
s_t = [s_t^{(3)}, s_t^{(6)}] \in \mathbb{R}^{32}
$$

where $s_t^{(i)}$ denotes the state of intersection $i \in \{3, 6\}$ (junction IDs in SUMO network).

**Per-Intersection State Components (16 dimensions each):**

For each intersection $i$, the state vector $s_t^{(i)} \in \mathbb{R}^{16}$ comprises:

1. **Phase Encoding (4 dimensions):** One-hot representation of current signal phase

$$
p^{(i)} = [p_1, p_2, p_3, p_4] \in \{0,1\}^4
$$

where $p_j = 1$ if currently in Phase $j$, else $p_j = 0$. This encoding enables the network to learn phase-specific
control policies.

2. **Phase Duration (1 dimension):** Normalized time elapsed in current phase

$$
d^{(i)} = \min\left(\frac{t_{phase}}{60.0}, 1.0\right) \in [0,1]
$$

where $t_{phase}$ is the current phase duration in seconds. Normalization prevents numerical instability in neural
network training.

3. **Vehicle Queue Occupancy (4 dimensions):** Binary indicators for each approach (North, South, East, West)

$$
q_v^{(i)} = [q_{N}^v, q_{S}^v, q_{E}^v, q_{W}^v] \in \{0,1\}^4
$$

where $q_j^v = 1$ if detector at approach $j$ occupied within last 3 seconds, else $q_j^v = 0$. Detectors positioned 30m
upstream from stop lines.

4. **Bicycle Queue Occupancy (4 dimensions):** Binary indicators for each approach

$$
q_b^{(i)} = [q_{N}^b, q_{S}^b, q_{E}^b, q_{W}^b] \in \{0,1\}^4
$$

Bicycle detectors positioned 15m upstream (reflecting lower approach speeds) with 3-second detection window.

5. **Pedestrian Demand (1 dimension):** Binary indicator of waiting pedestrians

$$
\phi_{ped}^{(i)} \in \{0,1\}
$$

Derived from SUMO's person API monitoring pedestrian waiting times and speeds at crosswalks.

6. **Bus Presence (1 dimension):** Binary indicator of bus approaching or waiting

$$
\phi_{bus}^{(i)} \in \{0,1\}
$$

7. **Bus Waiting Time (1 dimension):** Normalized time bus has been waiting

$$
t_{bus}^{(i)} = \min\left(\frac{t_{wait}}{60.0}, 1.0\right) \in [0,1]
$$

**State Space Characteristics:**

- **Dimensionality:** 32 dimensions total (16 per intersection × 2 intersections)
- **Observation Type:** Partially observable (detector measurements, not complete traffic state)
- **Update Frequency:** Every 1 second (SUMO simulation step)
- **Normalization:** All continuous features scaled to $[0,1]$, binary features in $\{0,1\}$

The state representation balances **expressiveness** (capturing multi-modal traffic conditions) with **compactness**
(enabling efficient neural network approximation). Detector-derived features account for 20 of 32 dimensions (62.5%),
providing rich observational grounding for learning.

###### 3.3 Action Space Definition

The action space $\mathcal{A}$ consists of three discrete control actions applied **centrally** to both intersections
simultaneously:

$$
\mathcal{A} = \{a_0, a_1, a_2\}
$$

**Action Definitions:**

- **$a_0$ (Continue Current Phase):** Maintains green signal on current movement, incrementing phase duration by 1
  second. Most frequently selected (~85% during training). Enables traffic-responsive phase extensions.

- **$a_1$ (Skip to Phase 1):** Forces immediate transition to Phase 1 (major arterial through) from any other phase,
  bypassing standard phase sequence. Prioritizes major arterial flow when minor phases have cleared demand. Typical
  selection rate ~2.5%.

- **$a_2$ (Progress to Next Phase):** Advances through standard phase sequence $P1 \to P2 \to P3 \to P4 \to P1$.
  Provides balanced service across all movements. Typical selection rate ~12.5%.

**Centralized Execution:** When the agent selects action $a_t$, both intersections (IDs 3 and 6) execute the action
simultaneously, maintaining perfect phase synchronization:

$$
\text{TLS}_3 \leftarrow \text{execute}(a_t), \quad \text{TLS}_6 \leftarrow \text{execute}(a_t)
$$

This centralized control strategy naturally achieves corridor coordination without explicit timing offsets.

**Phase-Specific Safety Constraints:**

All phase-changing actions ($a_1, a_2$) enforce minimum green time requirements:

$$
d^{(i)} \geq d_{min}(p) \implies \text{action permitted}
$$

where minimum green times vary by phase:

| Phase | $d_{min}$ | Rationale                            |
| ----- | --------- | ------------------------------------ |
| P1    | 8s        | Major arterial clearance + yellow    |
| P2    | 3s        | Minor roadway minimum service        |
| P3    | 5s        | Bicycle crossing time                |
| P4    | 2s        | Pedestrian minimum crossing + yellow |

**Change Intervals:** Phase transitions automatically insert 6-second clearance sequences: 3s yellow + 2s all-red + 1s
leading green, ensuring safe transitions between conflicting movements.

**Maximum Green Time Enforcement:** Automatic phase advancement occurs when duration exceeds phase-specific maximum:

| Phase | $d_{max}$ | Purpose                           |
| ----- | --------- | --------------------------------- |
| P1    | 44s       | Prevent minor approach starvation |
| P2    | 15s       | Limit minor phase duration        |
| P3    | 24s       | Ensure pedestrian service         |
| P4    | 12s       | Maintain cycle efficiency         |

These constraints embed traffic engineering standards (ITE, MUTCD) directly into the action space, guaranteeing safe
operation regardless of learned policy.

###### 3.4 Reward Function Overview

The reward function $r_t = \mathcal{R}(s_t, a_t, s_{t+1})$ encodes multi-modal traffic signal control objectives through
**14 weighted components** organized into three categories:

**1. Environmental Feedback (Components 1-6, 8-13):** Measure actual traffic consequences

- **Waiting time penalties:** Mode-specific weights (Bus: 2.0×, Car: 1.3×, Bicycle/Pedestrian: 1.0×) prioritize transit
  and penalize delays
- **Flow bonuses:** Positive reinforcement for vehicle throughput
- **CO₂ penalties:** Environmental sustainability incentive
- **Modal equity:** Balance service quality across modes
- **Safety violations:** Large penalties ($-5.0$) for unsafe policies
- **Blocked actions:** Discourage infeasible control decisions
- **Strategic action rewards:** Phase-specific bonuses for effective Skip-to-P1 and Next-Phase transitions
- **Bus priority bonuses:** Reward timely bus service
- **Phase stability bonuses:** Incentivize committed phase decisions ($+0.05$ for duration $\geq$ stability threshold)
- **Timing penalties:** Penalize premature phase changes and excessive continuation

**2. Meta-Level Guidance (Component 7):** Policy shaping statistics

- **Action diversity:** Encourages balanced action distribution, prevents policy collapse. Applied only during
  deliberate policy actions (not random exploration).

**3. Constraint Enforcement (Component 14):** Operational safety

- **Minimum/maximum green enforcement:** Embedded in action masking and automatic overrides

**Complete Formulation:**

$$
r_t = \text{clip}\left(r_{wait} + r_{flow} + r_{CO_2} + r_{equity} + r_{safety} + r_{block} + r_{diversity} +
r_{skip\_eff} + r_{skip\_inc} + r_{bus} + r_{next} + r_{stability} + r_{early} + r_{consec}, -10, +10\right)
$$

Reward clipping prevents training instability while preserving relative magnitudes for effective learning. The
hierarchical structure separates environmental outcomes from training statistics, preventing reward hacking where the
agent exploits meta-level components without improving actual traffic performance.

**TODO**: Add Table 2: Traning Metrics (1 to 200 Episodes) from Training Results (May use brief form as well)

###### 3.5 Transition Dynamics

The state transition function $\mathcal{P}(s_{t+1} | s_t, a_t)$ is implicitly defined by the SUMO traffic
microsimulation, which evolves vehicle positions, speeds, and detector states according to car-following models
(Krauss), lane-changing logic, and signal phase states.

**Deterministic Traffic Physics:** Vehicle dynamics follow deterministic rules (acceleration, deceleration, gap
acceptance) given current positions and speeds.

**Stochastic Arrival Processes:** Traffic demand follows Poisson arrival processes with scenario-specific rates:

$$
\lambda_{mode} \sim \text{Poisson}(\mu_{scenario})
$$

where $\mu_{scenario} \in [100, 1000]$ vehicles/hour varies across 30 test scenarios (Pr_0-9, Bi_0-9, Pe_0-9)
representing low to near-saturation demand.

**Non-Stationary Environment:** Demand patterns vary by scenario, time of day, and stochastic fluctuations, requiring
the agent to learn robust policies generalizing across diverse conditions rather than overfitting to specific traffic
patterns.

**Markov Property Validation:** The state vector $s_t \in \mathbb{R}^{32}$ provides sufficient information for near-term
prediction (next 10-30 seconds). Longer-horizon dependencies (e.g., platoon arrivals from distant upstream sources) are
not captured, representing acceptable approximation error given the 300m corridor length and 1-second decision
frequency.

###### 3.6 Control Objective

The control objective is to learn a policy $\pi^*$ maximizing expected cumulative reward across diverse traffic
scenarios, subject to safety and operational constraints:

$$
\pi^* = \arg\max_{\pi} \mathbb{E}_{s_0, \tau \sim \pi}\left[\sum_{t=0}^{T} \gamma^t r_t\right]
$$

where $\tau = (s_0, a_0, r_0, s_1, a_1, r_1, \ldots)$ denotes a trajectory sampled by executing policy $\pi$ in the SUMO
environment, and $T = 3600$ seconds (1-hour episode).

**Multi-Objective Optimization:** The reward function decomposes into 14 components encoding competing objectives:

- **Efficiency:** Minimize total waiting time ($\sum_t \sum_i w_i^t$), maximize throughput
- **Equity:** Balance service quality across modes (cars, bicycles, pedestrians, buses)
- **Safety:** Zero violations of minimum green times, clearance intervals, and phase conflicts
- **Sustainability:** Minimize CO₂ emissions through reduced idling and smoother traffic flow
- **Coordination:** Achieve synchronized phase timing across intersections for platoon progression

The learned policy implicitly discovers Pareto-optimal trade-offs among these objectives without requiring manual weight
specification, as the reward components guide exploration toward balanced solutions.

**Generalization Requirement:** The policy must perform well across 30 systematically designed test scenarios spanning:

- **Primary traffic (Pr_0-9):** High major arterial demand (400-1000 veh/hour), low bicycle/pedestrian
- **Bicycle-heavy (Bi_0-9):** High bicycle demand (400-1000 cyc/hour), moderate vehicular
- **Pedestrian-heavy (Pe_0-9):** High pedestrian demand (400-1000 ped/hour), moderate vehicular

Training employs randomized scenario selection to prevent overfitting, ensuring the agent learns traffic-responsive
control principles rather than scenario-specific heuristics.

**Performance Metrics:** Policy quality evaluated through:

- **Average waiting times** per mode (car, bicycle, pedestrian, bus) across all scenarios
- **Safety violations:** Zero tolerance (hard constraint)
- **CO₂ emissions:** Total kg/hour per scenario
- **Modal equity:** Coefficient of variation in per-mode waiting times
- **Comparative improvement:** Performance vs. fixed-time, actuated, and rule-based baselines

The control objective thus balances **efficiency** (system-level throughput), **equity** (fair service across modes),
and **robustness** (consistent performance across diverse demand conditions), representing a paradigm shift from
automobile-centric optimization to truly multi-modal traffic signal control.

---

##### 4. System Architecture

###### 4.1 Network Topology

The simulation environment models a typical urban arterial corridor comprising **two signalized intersections**
(Junction IDs 3 and 6) separated by **300 meters** along a major north-south arterial roadway. Each intersection forms a
four-leg junction where a minor east-west cross-street intersects the arterial perpendicularly, creating a classic urban
grid configuration.

**Corridor Configuration:**

- **Separation distance:** 300m (typical medium-density urban spacing)
- **Number of intersections:** 2 (upstream junction 3, downstream junction 6)
- **Link configuration:** Single through lane between intersections, dual lanes at approaches
- **Bus infrastructure:** 15m bus bays positioned immediately downstream of each intersection

The 300m separation enables investigation of corridor-level coordination strategies where upstream signal timing
influences downstream traffic through platoon progression and queue spillback dynamics. This distance permits meaningful
green wave coordination while maintaining practical relevance for urban arterial corridors.

**Major Arterial Infrastructure:**

The north-south arterial employs a **dual-lane configuration** at intersection approaches:

- **Left lane:** Exclusive left-turn movements (left-turn bay)
- **Right lane:** Through traffic with permissive right turns on red

Between intersections, the arterial narrows to a **single through lane** over a 90m link section, representing typical
urban roadway constraints. This configuration necessitates merge maneuvers before reaching the downstream intersection,
creating realistic traffic flow complexity.

**Bus stops** are positioned 15m downstream of each intersection in dedicated right-lane bays, preventing buses from
obstructing through traffic during passenger boarding/alighting operations. Buses operate on fixed 15-minute headways in
both directions (4 buses/hour), representing typical urban transit service frequencies.

**Minor Road Configuration:**

East-west cross-streets feature comparable infrastructure geometry at reduced scale:

- **Dual entry lanes** at intersection approaches (left-turn and through movements segregated)
- **Traffic demand:** ~25% of major arterial volume (consistent with hierarchical network design)
- **Role:** Collector streets feeding traffic to/from primary arterial

The asymmetric demand relationship creates inherent signal timing tensions: excessive minor-phase green time reduces
arterial efficiency, while insufficient service generates delays and potential spillback onto upstream networks.

**Boundary Conditions:**

Traffic generation and absorption zones at network periphery simulate realistic arrival/departure patterns:

- **Arrival processes:** Poisson stochastic arrivals with parametrically varied rates (100-1000 veh/hour)
- **Departure zones:** Absorb exiting vehicles, preventing artificial boundary congestion
- **Closed-corridor design:** No intermediate generation/termination points (except bus stops)

This controlled configuration enables systematic investigation of signal control performance across diverse demand
conditions while maintaining analytical tractability.

###### 4.2 Intersection Configuration

Each intersection features a **symmetric four-leg geometry** with comprehensive multi-modal infrastructure:

**Vehicular Facilities:**

- **Approach configuration:** Dual lanes per approach (4 approaches × 2 lanes = 8 entry lanes per intersection)
- **Lane assignment:** Left-turn bay + through/right-turn lane
- **Speed limit:** 40 km/h (25 mph) for motorized vehicles
- **Turn restrictions:** Protected left turns via dedicated phases, permissive right turns on red

**Bicycle Infrastructure:**

- **Parallel dual-lane facilities** adjacent to vehicular lanes
- **Left-turn accommodation:** Dedicated left-turn bicycle lanes at intersections
- **Speed limit:** 20 km/h (12.4 mph) for bicycles
- **Overtaking capability:** Dual lanes enable faster cyclists to pass slower riders

The dual bicycle lane design addresses speed heterogeneity characteristic of bicycle traffic, providing dedicated
right-of-way comparable to vehicular infrastructure. This configuration enables the controller to serve bicycle
movements without forcing cyclists into vehicular lanes.

**Pedestrian Facilities:**

- **Sidewalk infrastructure:** Laterally adjacent to roadway cross-section
- **Crosswalks:** Marked at all intersection legs (4 crosswalks per intersection)
- **Crossing support:** Straight movements between all four quadrants
- **Detection:** Push-button actuation at stop lines monitoring pedestrian presence and queue formation

**Intersection Spacing and Coordination:**

The 300m separation creates natural coordination opportunities:

- **Travel time between signals:** ~27 seconds at free-flow speed (40 km/h)
- **Coordination strategy:** Centralized control (both signals change phases simultaneously)
- **Platoon progression:** Implicit green wave through learned phase timing rather than engineered offsets

Unlike traditional coordinated systems employing fixed timing offsets, the DRL agent discovers adaptive coordination
through observation of traffic states at both intersections. When upstream platoons approach the downstream
intersection, the centralized state representation enables anticipatory phase management.

###### 4.3 Phase Structure

The DRL agent operates a **four-phase signal control structure** serving all transportation modes equitably while
maintaining efficient vehicular throughput:

**Phase Definitions:**

| Phase  | Movements                      | Primary Users            | Typical Duration | Role                           |
| ------ | ------------------------------ | ------------------------ | ---------------- | ------------------------------ |
| **P1** | Major arterial through + right | Cars, buses (arterial)   | 12-44s           | Main clearance, highest volume |
| **P2** | Major arterial protected left  | Cars (left-turning)      | 5-15s            | Left-turn service              |
| **P3** | Minor roadway through + right  | Cars (cross-street)      | 7-24s            | Minor approach service         |
| **P4** | Minor roadway protected left   | Cars (cross-street left) | 4-12s            | Minor left-turn completion     |

**Note:** Unlike traditional systems with exclusive pedestrian/bicycle phases, this implementation serves pedestrians
during P1 and P3 (concurrent with through movements), and bicycles receive dedicated service windows integrated into all
phases. This design maximizes intersection efficiency while maintaining safety through detector-based demand response.

**Phase Sequence:** Standard progression follows $P1 \to P2 \to P3 \to P4 \to P1$, but the agent can execute
**Skip-to-P1** actions ($a_1$) from any phase when minor movements have cleared, prioritizing arterial flow.

**Phase Duration Hierarchy:**

Five nested timing thresholds govern each phase, balancing safety, efficiency, and equity:

| Phase  | Min Green | Stability | Next Bonus | Consecutive Continue | Max Green |
| ------ | --------- | --------- | ---------- | -------------------- | --------- |
| **P1** | 8s        | 10s       | 12s        | 30s                  | 44s       |
| **P2** | 3s        | 4s        | 5s         | 10s                  | 15s       |
| **P3** | 5s        | 6s        | 7s         | 15s                  | 24s       |
| **P4** | 2s        | 3s        | 4s         | 8s                   | 12s       |

**Threshold Rationale:**

1. **Min Green (Safety):** Ensures sufficient clearance time based on approach speeds and crossing distances. Hard
   constraint preventing premature phase changes.

2. **Stability (Efficiency):** Discourages premature transitions that waste yellow clearance time (6s overhead). Reward
   bonus (+0.05) incentivizes holding phases ≥ stability threshold.

3. **Next Bonus (Optimization):** Rewards timely phase advancement after adequate service. Bonuses (+0.08-0.11) guide
   agent toward optimal termination timing.

4. **Consecutive Continue (Equity):** Prevents indefinite phase holding. Large penalties (−0.15 to −0.30) enforce
   periodic cycling through all phases, ensuring vulnerable road users receive service.

5. **Max Green (Capacity):** Hard upper limit preventing starvation. Set at ~3× next bonus threshold to allow adaptive
   extensions under high demand.

**Change Intervals:**

Phase transitions automatically insert **6-second clearance sequences:**

- **Yellow interval:** 3s (warning of phase change)
- **All-red interval:** 2s (intersection clearance time)
- **Leading green:** 1s (priority start for vulnerable modes in new phase)

These intervals ensure safe transitions between conflicting movements, preventing vehicles/cyclists from being caught
mid-intersection during phase changes.

<div align="center">
<img src="images/1/phase_structure.png" alt="Phase Structure Diagram" width="400" height=auto/>
<p align="center">figure: Four-phase signal control structure showing permitted movements and transitions.</p>
</div>

###### 4.4 Detector Infrastructure

The system employs **induction loop detectors** strategically positioned to capture multi-modal traffic conditions at
both intersections. The detector layout comprises three types:

**1. Vehicle Queue Detection:**

- **Location:** 30m upstream from stop line on each approach (8 detectors per intersection, 16 total)
- **Technology:** Single-loop induction detectors
- **Detection window:** 3-second occupancy threshold
- **Logic:** Binary classification (queue present if detector activated within last 3s)
- **Positioning rationale:** At 40 km/h, vehicles traverse 30m in ~2.7s, enabling anticipatory phase management while
  maintaining safety margins

**Note:** Although 100m detectors are installed (for potential dilemma zone protection), only 30m detectors are actively
used in both rule-based and DRL control, ensuring fair comparison.

**2. Bicycle Queue Detection:**

- **Location:** 15m upstream from stop line on each approach (8 detectors per intersection, 16 total)
- **Technology:** Single-loop induction detectors
- **Detection window:** 3-second occupancy threshold
- **Positioning rationale:** At 20 km/h bicycle speed, 15m placement yields ~2.7s travel time, maintaining temporal
  consistency with vehicular detection

The reduced detection distance relative to vehicular detectors accounts for lower bicycle speeds while ensuring
equivalent response times across modal types.

**3. Pedestrian Detection:**

- **Technology:** SUMO TraCI person API monitoring waiting times and speeds
- **Location:** Crosswalk queue zones at stop lines
- **Detection logic:** Continuous monitoring of pedestrian presence, waiting duration, and movement patterns
- **Integration:** Binary demand indicators and normalized waiting times feed directly into state representation

Unlike traditional push-button systems requiring manual activation, the DRL control receives continuous pedestrian
demand signals, enabling proactive service scheduling.

**Detector Integration with State Space:**

Detector measurements constitute **20 of 32 state dimensions (62.5%)**:

- Vehicle queue occupancy: 4 dimensions per intersection × 2 = 8 dimensions
- Bicycle queue occupancy: 4 dimensions per intersection × 2 = 8 dimensions
- Pedestrian demand: 1 dimension per intersection × 2 = 2 dimensions
- Bus presence: 1 dimension per intersection × 2 = 2 dimensions

This detector-rich state representation provides fine-grained observational grounding for learning traffic-responsive
control policies.

**Infrastructure Consistency:**

The detector infrastructure is **identical** between rule-based and DRL control systems, ensuring performance
differences arise from control algorithms rather than sensing capabilities. Both systems receive equivalent
observational information from the intersection environment, enabling methodologically rigorous comparative evaluation.

###### 4.5 Centralized Control Strategy

The DRL agent implements a **centralized single-agent** architecture controlling both intersections simultaneously
through a unified neural network policy:

**Centralized vs. Decentralized Control:**

| Feature                   | Decentralized (Multi-Agent)               | Centralized (This Work)                   |
| ------------------------- | ----------------------------------------- | ----------------------------------------- |
| **Agents**                | One per intersection (2 agents)           | Single agent controlling both             |
| **State**                 | Local observation per intersection        | Global state (both intersections)         |
| **Action**                | Independent decisions per intersection    | Synchronized action across both           |
| **Coordination**          | Requires communication or shared learning | Natural coordination via global state     |
| **Phase synchronization** | Requires explicit timing offsets          | Both intersections change phases together |
| **Complexity**            | Higher (inter-agent coordination)         | Lower (single policy)                     |

**Centralized Control Rationale:**

For **closely-spaced intersections** (<600m), centralized control offers significant advantages:

1. **Natural Coordination:** Both intersections transition to the same phase simultaneously, creating implicit green
   wave progression without engineered offsets
2. **Global Optimization:** Single agent observes conditions at both intersections, enabling anticipatory control
   decisions
3. **Training Efficiency:** Single neural network learns faster than coordinating multiple agents
4. **Deployment Simplicity:** No inter-agent communication protocols or synchronization mechanisms required

**Synchronized Phase Changes:**

When the agent selects action $a_t$ at timestep $t$:

$$
\text{TLS}_3 \leftarrow a_t, \quad \text{TLS}_6 \leftarrow a_t
$$

Both traffic signals execute the **identical action** and transition to the **same phase** simultaneously. This perfect
synchronization achieves corridor-level coordination that would require complex timing offset algorithms in traditional
systems.

**Example:** If the agent selects "Next Phase" at timestep 100:

- Junction 3: $P1 \to P2$ transition begins
- Junction 6: $P1 \to P2$ transition begins simultaneously
- Upstream platoons departing Junction 3 encounter synchronized green at Junction 6
- No manual offset tuning required—coordination emerges from learned policy

**Global State Awareness:**

The 32-dimensional state vector provides **complete observational coverage** of both intersections:

$$
s_t = \underbrace{[p^{(3)}, d^{(3)}, q_v^{(3)}, q_b^{(3)}, \phi_{ped}^{(3)}, \phi_{bus}^{(3)}]}_{16 \text{ dims
Junction 3}} \oplus \underbrace{[p^{(6)}, d^{(6)}, q_v^{(6)}, q_b^{(6)}, \phi_{ped}^{(6)}, \phi_{bus}^{(6)}]}_{16
\text{ dims Junction 6}}
$$

This global representation enables the agent to:

- Anticipate downstream congestion based on upstream queue formation
- Coordinate phase timing to facilitate platoon progression
- Balance service across the corridor rather than optimizing intersections independently

**Scalability Considerations:**

The centralized approach is appropriate for:

- **Short corridors:** 2-4 intersections within 600m
- **Synchronized operation:** Contexts where simultaneous phase changes are desirable
- **Training constraints:** Limited computational resources favoring single-agent learning

For **larger networks** (>4 intersections) or **grid configurations**, multi-agent architectures with decentralized
execution become necessary to manage state-space complexity and enable modular deployment. The centralized approach
demonstrated here serves as a **proof-of-concept** validating DRL's potential for multi-modal traffic control before
scaling to network-wide implementations.

**Training and Deployment:**

- **Training:** 200 episodes × 3600s = 200 hours simulated time over ~40 hours wall-clock time (GPU-accelerated)
- **Model selection:** Episode 192 chosen based on balanced performance across all scenarios
- **Testing:** Zero-shot generalization to 30 unseen demand patterns (no fine-tuning)
- **Deployment:** Single neural network (107K parameters) executable in real-time (<1ms inference per decision)

The centralized architecture demonstrates that DRL can learn effective multi-modal traffic signal control policies
achieving 88.6-93.6% waiting time reductions for vulnerable road users through end-to-end optimization from traffic
observations to control actions, without requiring manual feature engineering or hierarchical rule design.

---

##### 5. Deep Q-Network Architecture

###### 5.1 Q-Function Approximation

###### 5.2 Network Architecture Design

###### 5.3 Action Selection Strategy

###### 5.4 Prioritized Experience Replay

###### 5.5 Double DQN Training Algorithm

---

##### 6. Multi-Objective Reward Function

###### 6.1 Reward Design Philosophy

###### 6.2 Environmental Feedback Components

###### 6.3 Meta-Level Guidance Components

###### 6.4 Safety and Constraint Enforcement

###### 6.5 Component Weighting and Tuning

---

##### 7. Training Methodology

###### 7.1 Training Data Generation

###### 7.2 Episode Structure and Procedure

###### 7.3 Hyperparameter Configuration

###### 7.4 Two-Phase Training Strategy

###### 7.5 Convergence Analysis

---

##### 8. Experimental Setup

###### 8.1 Simulation Environment (SUMO)

###### 8.2 Traffic Demand Generation

###### 8.3 Test Scenario Design

###### 8.4 Baseline Control Strategies

###### 8.5 Performance Metrics

---

##### 9. Results and Analysis

###### 9.1 Training Performance

###### 9.2 Waiting Time Analysis

###### 9.3 Modal Equity Evaluation

###### 9.4 Safety and Blocking Events

###### 9.5 Comparative Performance Analysis

###### 9.6 Scenario-Specific Insights

---

##### 10. Discussion

###### 10.1 Key Findings

###### 10.2 Trade-offs and Design Choices

###### 10.3 Scalability Considerations

###### 10.4 Practical Deployment Implications

###### 10.5 Limitations

---

##### 11. Conclusion

###### 11.1 Summary of Contributions

###### 11.2 Impact on Multi-Modal Traffic Control

###### 11.3 Future Research Directions

---

# References

---

# Appendices

###### Appendix A: Detailed Hyperparameters

###### Appendix B: Complete Test Results

###### Appendix C: Phase Timing Thresholds

###### Appendix D: Reward Component Specifications
