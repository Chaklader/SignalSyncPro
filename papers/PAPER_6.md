# PAPER_6: Learned Communication Masks for Scalable Multi-Agent Traffic Control

## Working Title

**"Bayesian Ego-Graph Communication for Scalable Multi-Agent Traffic Signal Coordination"**

Alternative titles:

- "Learning When to Communicate: Sparse Communication Masks for Traffic Signal Control"
- "Scalable Multi-Agent Traffic Control via Learned Communication Topology"
- "From Fixed to Learned: Adaptive Communication in Multi-Agent Traffic Signal Coordination"

---

## Abstract (Concept)

Multi-agent traffic signal control traditionally relies on fixed communication topologies where each intersection
exchanges information with immediate neighbors. However, this approach scales poorly and may exchange unnecessary
information in stable traffic conditions. Inspired by recent advances in networked multi-agent reinforcement learning,
we propose a Bayesian communication framework where each traffic signal agent learns a sparse, context-aware
communication mask that determines which neighbors to consult based on current traffic conditions. Building on our prior
QMIX work (PAPER_3), we extend the 5-intersection corridor to 10-20 intersections and demonstrate that learned
communication achieves comparable coordination quality (within 3%) while reducing communication overhead by 55%. The
framework naturally discovers that upstream agents require more communication during platoon arrivals while downstream
agents can operate more independently, aligning with traffic flow physics.

---

## Inspiration

**Based on:** BayesG (Bayesian Ego-graph Inference for Networked Multi-Agent Reinforcement Learning, NeurIPS 2025)

**Original Paper Contribution:**

- Decentralized agents learn sparse communication structures via Bayesian variational inference
- Each agent operates over an ego-graph and samples latent communication masks
- Tested on up to 167 agents in traffic control

**Our Extension:**

- Apply to multi-modal traffic (cars, bikes, pedestrians, buses)
- Combine with QMIX value decomposition from PAPER_3
- Focus on corridor-level coordination with realistic phase structures
- Add interpretability layer (connecting to PAPER_4)

---

## Research Questions

### Primary Questions:

1. **Can agents learn when to communicate vs. always communicating?**

    - Does sparse communication maintain coordination quality?
    - What triggers communication (queue buildup, platoon arrival, phase transition)?

2. **How does learned communication scale to larger networks?**

    - 5 → 10 → 20 intersection scalability
    - Communication overhead vs. coordination quality trade-off

3. **What communication patterns emerge from learning?**
    - Upstream-downstream asymmetry
    - Traffic-dependent communication intensity
    - Phase-dependent communication needs

### Secondary Questions:

4. **Can learned communication improve robustness?**

    - Performance with communication failures
    - Graceful degradation

5. **How does multi-modal traffic affect communication needs?**
    - Do bus priority events trigger more communication?
    - Pedestrian phase coordination across intersections

---

## Core Contribution

### Main Contributions:

1. **Bayesian Communication Masks for Traffic Control**

    - First application of learned communication topology to traffic signal coordination
    - Variational inference for communication mask sampling
    - Integration with QMIX value decomposition

2. **Multi-Modal Communication Requirements**

    - Analyze how different traffic modes affect communication needs
    - Bus priority requires upstream notification
    - Pedestrian phases can coordinate with less communication

3. **Scalability Analysis**

    - Demonstrate 10-20 intersection coordination
    - Quantify communication-performance trade-off
    - Compare: Fixed topology vs. Learned topology

4. **Emergent Communication Patterns**
    - Discover traffic-dependent communication rules
    - Connect to green wave physics
    - Interpretable communication decisions

---

## Methodology

### 1. Building on PAPER_3

**From QMIX (PAPER_3):**

- 5 independent DQN agents with mixing network
- Local state: queue lengths, waiting times, phases
- Actions: Continue, Next, Skip2P1
- Fixed neighbor communication: TLS i talks to TLS i-1 and TLS i+1

**Extension for PAPER_6:**

- Replace fixed communication with learned communication masks
- Scale from 5 to 10-20 intersections
- Add Bayesian sampling for communication decisions

### 2. Communication Mask Architecture

**Ego-Graph Construction:**

```
For each agent i:
├─ Physical neighbors: All TLS within k hops (k=2 for corridor)
├─ Potential communication partners: {TLS_1, TLS_2, ..., TLS_n}
└─ Communication mask: m_i ∈ {0,1}^n (learned binary mask)
```

**Bayesian Mask Sampling:**

```
Prior: p(m_i) = Bernoulli(0.5)  # Uniform prior

Posterior: q(m_i | s_i, global_context)
├─ Input: Local state s_i + global traffic features
├─ Network: 2-layer MLP → Bernoulli parameters
└─ Output: Probability of communicating with each neighbor

Sampling: m_i ~ q(m_i | s_i, global_context)
```

**Training Objective:**

```
ELBO = E_q[log p(reward | actions, masks)] - KL(q(m) || p(m))

Components:
├─ Reconstruction: Maximize expected reward (from QMIX)
├─ Regularization: Encourage sparse communication (KL to sparse prior)
└─ Balance: λ controls sparsity-performance trade-off
```

### 3. State Representation

**Local State (per agent):**

```
state_i = [
    queue_lengths_4_approaches,      # [4]
    waiting_times_4_approaches,      # [4]
    current_phase_one_hot,           # [4]
    time_in_phase_normalized,        # [1]
    bus_present_flag,                # [1]
    pedestrian_demand_flag           # [1]
]  # Total: 15 features
```

**Communication Context (for mask generation):**

```
context_i = [
    own_queue_summary,               # [1] - Total queue
    traffic_trend,                   # [1] - Increasing/decreasing
    time_since_last_communication,   # [1]
    neighbor_queue_estimates         # [n] - From last communication
]
```

**Received Messages (from selected neighbors):**

```
messages_i = [state_j for j in active_neighbors(mask_i)]
# Variable size depending on mask
```

### 4. Extended Network Architecture

**Individual Q-Network with Communication:**

```
Input: Local state + Aggregated neighbor messages
├─ Local encoder: MLP(15 → 64)
├─ Message aggregator: Attention over received messages
├─ Combined: Concat(local_enc, msg_agg) → 128
└─ Output: Q-values for 3 actions
```

**Communication Mask Network:**

```
Input: Local state + Global context (optional)
├─ Encoder: MLP(15 → 32 → 32)
├─ Output: Bernoulli parameters for each potential neighbor
└─ Sampling: Gumbel-softmax for differentiable sampling
```

**Mixing Network (from QMIX):**

```
Same as PAPER_3, but now receives:
├─ Individual Q-values
├─ Communication masks (for analysis)
└─ Global state
```

### 5. Training Protocol

**Phase 1: Pre-training with Full Communication**

- Train standard QMIX (PAPER_3 approach)
- All agents communicate with all neighbors
- Establish baseline performance

**Phase 2: Learn Communication Masks**

- Introduce mask network
- Gradually increase sparsity penalty λ
- Fine-tune Q-networks with sparse communication

**Phase 3: Joint Optimization**

- End-to-end training of masks + Q-networks
- ELBO objective balances performance and sparsity

**Curriculum:**

- Start with 5 intersections (from PAPER_3)
- Add intersections progressively: 5 → 7 → 10 → 15 → 20
- Transfer learned communication patterns

---

## Experiments

### Experiment 1: Communication Sparsity vs. Performance

**Setup:**

- Fix network size: 10 intersections
- Vary sparsity penalty λ: 0 (full comm) → 0.5 (very sparse)

**Metrics:**

- Communication rate: % of possible messages actually sent
- Coordination quality: Green wave efficiency, travel time
- Performance gap: vs. full communication baseline

**Expected Results:**

| Sparsity (λ) | Comm Rate | Green Wave % | Gap vs. Full |
| ------------ | --------- | ------------ | ------------ |
| 0.0 (full)   | 100%      | 75%          | 0%           |
| 0.1          | 65%       | 74%          | -1.3%        |
| 0.2          | 45%       | 73%          | -2.7%        |
| 0.3          | 30%       | 71%          | -5.3%        |
| 0.5          | 15%       | 62%          | -17.3%       |

**Sweet Spot:** λ = 0.15-0.2 achieves 45-55% communication with <3% performance loss

### Experiment 2: Scalability Analysis

**Configurations:**

- 5 intersections (baseline from PAPER_3)
- 10 intersections (medium scale)
- 15 intersections (large corridor)
- 20 intersections (stress test)

**Comparisons:**

1. Full communication (every agent talks to every neighbor)
2. Fixed 1-hop (only immediate neighbors)
3. Fixed 2-hop (neighbors within 2 intersections)
4. Learned masks (our approach)

**Metrics:**

- Training time (wall-clock hours)
- Inference time (ms per decision)
- Communication messages per step
- Coordination quality

**Expected Results:**

| # TLS | Full Comm | Fixed 1-hop | Learned Masks |
| ----- | --------- | ----------- | ------------- |
| 5     | 8 msg/s   | 8 msg/s     | 4 msg/s       |
| 10    | 18 msg/s  | 18 msg/s    | 8 msg/s       |
| 15    | 28 msg/s  | 28 msg/s    | 11 msg/s      |
| 20    | 38 msg/s  | 38 msg/s    | 14 msg/s      |

### Experiment 3: Emergent Communication Patterns

**Analysis:**

- When does each agent choose to communicate?
- Which traffic events trigger increased communication?
- Upstream vs. downstream communication asymmetry

**Hypotheses:**

1. Platoon arrivals increase upstream → downstream communication
2. Cross-street demand spikes increase neighbor communication
3. Stable flow periods reduce communication

**Visualization:**

- Heatmaps: Communication intensity by agent pair over time
- Event-triggered analysis: Communication around queue buildups
- Role discovery: Which agents are "hubs" vs. "leaves"

### Experiment 4: Multi-Modal Communication Needs

**Traffic Scenarios:**

- Car-only: 800 veh/hr
- With buses: 800 cars + bus every 10 min
- With pedestrians: 800 cars + 400 peds/hr
- Full multi-modal: Cars + bikes + peds + buses

**Analysis:**

- Does bus priority trigger more communication?
- Do pedestrian phases require coordination messages?
- How does bike traffic affect communication patterns?

**Expected Insights:**

```
Bus arrives at TLS-2:
├─ TLS-2 → TLS-3: "Bus incoming, prepare green"
├─ TLS-3 → TLS-4: "Upstream bus, extend arterial"
└─ Communication spike: 3x normal rate

Normal car flow:
├─ TLS-2 → TLS-3: (no message needed)
└─ Communication: Baseline rate
```

### Experiment 5: Robustness to Communication Failures

**Failure Scenarios:**

1. Random message drops (10%, 20%, 30%)
2. Single agent communication failure
3. Intermittent connectivity

**Metrics:**

- Performance degradation vs. failure rate
- Recovery time after failures
- Comparison: Learned masks vs. fixed topology

**Expected Result:** Learned masks more robust because agents already operate with sparse communication

---

## Expected Results

### Performance Summary:

| Method               | 10 TLS Travel Time | Communication | Scalability |
| -------------------- | ------------------ | ------------- | ----------- |
| Fixed 1-hop          | 145s               | 18 msg/step   | Medium      |
| Full communication   | 138s               | 45 msg/step   | Poor        |
| Learned masks (ours) | 142s               | 20 msg/step   | **Good**    |

**Key Finding:** 3% performance sacrifice for 55% communication reduction

### Communication Pattern Discovery:

```
Discovered Rules:
1. IF upstream_queue > 15 THEN communicate downstream
2. IF bus_approaching THEN communicate 2-hop downstream
3. IF phase_transition THEN communicate immediate neighbors
4. IF stable_flow AND low_queue THEN skip communication
```

### Scalability:

- 5 TLS: Baseline (same as PAPER_3)
- 10 TLS: Linear scaling with learned masks
- 20 TLS: Sub-linear communication growth

---

## Paper Outline

### 1. Introduction

- Problem: Fixed communication scales poorly for large traffic networks
- Gap: Existing multi-agent traffic control assumes full neighbor communication
- Contribution: Learned sparse communication with minimal performance loss
- Preview: 55% communication reduction, 3% performance gap, 20 TLS scale

### 2. Related Work

**2.1 Multi-Agent Communication Learning**

- CommNet, TarMAC, DIAL
- BayesG and ego-graph inference

**2.2 Multi-Agent Traffic Control**

- Independent Q-learning, QMIX, MAPPO
- Communication assumptions in prior work

**2.3 Scalable Traffic Signal Coordination**

- Traditional green wave
- Hierarchical control

### 3. Methodology

**3.1 QMIX Foundation (Brief)**

- Recap from PAPER_3

**3.2 Bayesian Communication Masks**

- Ego-graph construction
- Variational inference for mask learning
- ELBO objective

**3.3 Integration with QMIX**

- Message aggregation
- Training protocol

### 4. Experiments

**4.1 Sparsity-Performance Trade-off** **4.2 Scalability Analysis** **4.3 Emergent Communication Patterns** **4.4
Multi-Modal Communication** **4.5 Robustness Analysis**

### 5. Results

**5.1 Quantitative Performance** **5.2 Communication Pattern Analysis** **5.3 Scalability Demonstration**

### 6. Discussion

**6.1 Why Sparse Communication Works** **6.2 Traffic-Aware Communication** **6.3 Deployment Implications** **6.4
Limitations**

### 7. Conclusion

- Learned communication enables scalable multi-agent traffic control
- 55% reduction in communication overhead
- Maintains coordination quality for 10-20 intersections
- Foundation for city-scale deployment

---

## Key Novelty Points

1. **First learned communication for traffic signals** - Extends BayesG to realistic traffic domain
2. **Multi-modal communication analysis** - How buses, bikes, peds affect communication needs
3. **Integration with QMIX** - Combines value decomposition with learned communication
4. **Practical scalability** - Demonstrates 20-intersection coordination
5. **Interpretable communication patterns** - Connect to traffic flow physics

---

## Target Venues

**Primary:**

- NeurIPS (if strong ML contribution)
- AAMAS (multi-agent systems)
- IEEE Transactions on Intelligent Transportation Systems

**Secondary:**

- AAAI
- IJCAI
- ITSC Conference

**Timeline:**

- After PAPER_5 completion
- Implementation: 3-4 months
- Experiments: 2-3 months
- Writing: 1-2 months

---

## Connection to Other Papers

**Builds on:**

- PAPER_3: QMIX foundation, 5-intersection setup
- PAPER_4: Emergent role discovery (informs communication patterns)
- PAPER_5: GNN-DRL scalability (parallel approach)

**Enables:**

- PAPER_7: Role-aware control can leverage learned communication
- City-scale deployment: Foundation for 50+ intersection networks

**Research Arc:**

```
PAPER_3 (QMIX, 5 TLS)
    ↓
PAPER_5 (GNN-DRL) ←→ PAPER_6 (Learned Communication)
    ↓                      ↓
PAPER_7 (Role-Aware)  ←────┘
    ↓
City-Scale Deployment
```

---

## Technical Challenges

1. **Differentiable Sampling:** Gumbel-softmax for mask learning
2. **Variable Message Size:** Attention aggregation for variable neighbors
3. **Credit Assignment:** Which communication helped coordination?
4. **Exploration:** Encouraging communication during training

---

## Future Extensions

- Hierarchical communication (local clusters + global coordinators)
- Temporal communication patterns (periodic vs. event-driven)
- Heterogeneous communication (different message types for different events)
- Real-world bandwidth constraints
