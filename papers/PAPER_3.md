# PAPER_3: Multi-Agent Deep Reinforcement Learning for Coordinated Traffic Signal Control

## Working Title

**"QMIX-Based Multi-Agent Deep Q-Learning for Coordinated Traffic Signal Control in Urban Corridors"**

Alternative titles:

- "Emergent Coordination in Multi-Agent Traffic Control via Value Decomposition Networks"
- "Scalable Multi-Agent Reinforcement Learning for Arterial Traffic Signal Coordination"

---

## Abstract (Concept)

Traditional traffic signal control treats each intersection independently or uses rigid fixed-time coordination. We
propose a multi-agent deep reinforcement learning approach where five traffic signals in an urban corridor learn to
coordinate autonomously through value decomposition. Using QMIX architecture, we enable centralized training with
decentralized execution (CTDE), allowing each intersection to make independent decisions during deployment while
coordination is learned through a mixing network. Our approach shows X% reduction in average travel time and Y%
reduction in stops compared to independent control and traditional green wave timing. The learned coordination emerges
naturally without explicit programming, demonstrating the viability of multi-agent RL for real-world traffic management.

---
Semi-Synchronization

Exactly right! This is a crucial insight.

## Key Principle

**Minimum Warning Time = f(phase structure, MIN durations, transition times)**

**NOT** dependent on distance!

## The Formula

```
MIN_WARNING = Σ (MIN_GREEN[phase] + TRANSITION_TIME) for phases between current and P1

Worst case (from P2):
MIN_WARNING = (P2_MIN + 6) + (P3_MIN + 6) + (P4_MIN + 6)
            = (3 + 6) + (5 + 6) + (2 + 6)
            = 9 + 11 + 8
            = 28s
```

## What Distance Actually Affects

| Parameter | Depends On |
|-----------|------------|
| **MIN_WARNING** | Phase structure only (28s) |
| **Travel time** | Distance ÷ Speed |
| **When to send warning** | Travel time - MIN_WARNING |

### Comparison

| Network | Distance | Travel Time | MIN_WARNING | Send Warning At |
|---------|----------|-------------|-------------|-----------------|
| 2-TLS Corridor | 300m | 27s | 28s | ⚠️ **Impossible!** |
| 5-TLS Network | 1000m | 85s | 28s | T + 57s |

## Critical Discovery for 300m Corridor!

```
Travel time (27s) < MIN_WARNING (28s)

This means: Platoon arrives BEFORE TLS-2 can reach P1 in worst case!
```

The 22s offset in the 2-TLS corridor **cannot guarantee** green in all cases - it relies on TLS-2 being close to P1 naturally, or having different phase durations.

## Summary

You're correct:
- **28s is constant** (phase structure)
- **Distance only changes WHEN to warn**, not the warning duration itself
- For 1000m: plenty of margin (85s - 28s = 57s buffer)
- For 300m: tight/impossible (27s - 28s = -1s deficit)

---

## Research Questions

### Primary Questions:

1. **Can multiple traffic signal agents learn coordinated policies through value decomposition?**

    - Does QMIX enable emergent green wave behavior?
    - How does coordination quality compare to traditional methods?

2. **What is the performance gain of multi-agent coordination vs. independent control?**

    - Travel time reduction
    - Number of stops reduction
    - Throughput improvement

3. **How does multi-agent QMIX compare to centralized single-agent control?**
    - Performance trade-off
    - Computational efficiency
    - Scalability implications

### Secondary Questions:

4. **What reward structure enables effective multi-agent coordination?**

    - Local vs. global reward balance
    - Coordination incentive design
    - Credit assignment across agents

5. **How robust is the learned coordination?**
    - Performance with varying traffic demand
    - Graceful degradation with agent failures
    - Adaptation to traffic incidents

---

## Core Contribution

### Main Contributions:

1. **Novel Application of QMIX to Traffic Signal Control**

    - First application of monotonic value decomposition to 5-intersection corridor
    - Demonstrates feasibility of CTDE for real-time traffic control

2. **Multi-Agent Reward Design for Traffic Coordination**

    - Hybrid reward: 70% local performance + 30% global coordination
    - Coordination bonus for green wave progression
    - Network-level throughput incentives

3. **Comprehensive Baseline Comparison**

    - vs. Independent Q-Learning (no coordination)
    - vs. Single centralized agent (monolithic control)
    - vs. Fixed-time coordination (traditional green wave)
    - vs. Actuated control with offset optimization

4. **Scalability Analysis**
    - Computational cost comparison: QMIX vs. centralized
    - Memory requirements
    - Real-time feasibility (inference time < 1 second)

---

## Methodology

### 1. Network Architecture

**Physical Network:**

- 5 signalized intersections along arterial corridor
- 1 km spacing between intersections
- 4-approach intersections with bicycle lanes and pedestrian crossings
- Total corridor length: 5 km

**Multi-Agent Setup:**

- 5 independent DQN agents (one per intersection)
- Each agent controls local traffic signal (3 actions: Continue, Next, Skip2P1)
- Agents share experiences through common replay buffer

### 2. QMIX Architecture

**Individual Q-Networks:**

- Input: Local state (15 features per agent)
    - Queue lengths (4 approaches)
    - Waiting times (4 approaches)
    - Current phase (one-hot)
    - Time in phase
    - Neighbor phase information (TLS i-1, TLS i+1)
- Output: Q-values for 3 actions
- Architecture: 3-layer MLP (15 → 128 → 128 → 3)

**Mixing Network:**

- Input: Individual Q-values (Q_1, Q_2, Q_3, Q_4, Q_5) + Global state
- Global state (47 features):
    - All queue lengths (5 × 4 = 20)
    - All waiting times (20)
    - All current phases (5)
    - System-wide sync rate (1)
    - Total throughput (1)
- Output: Q_tot (global Q-value)
- Architecture: Hypernetwork with monotonic mixing

**Training:**

- Centralized: Mixing network sees all agents
- Loss: MSE between Q_tot and target Q_tot
- Target network updated every 1000 steps
- Experience replay buffer: 100k transitions

**Execution:**

- Decentralized: Each agent uses only local Q-network
- No communication between agents during deployment
- Action selection: argmax Q_i(local_state_i)

### 3. State Representation

**Local State (per agent):**

```
state_i = [
    queue_lengths_4_approaches,      # [4]
    waiting_times_4_approaches,      # [4]
    current_phase_one_hot,           # [4]
    time_in_phase_normalized,        # [1]
    neighbor_left_phase,             # [1]
    neighbor_right_phase             # [1]
]  # Total: 15 features
```

**Global State (for mixing network):**

```
global_state = [
    all_queue_lengths,               # [20]
    all_waiting_times,               # [20]
    all_current_phases,              # [5]
    sync_rate,                       # [1]
    total_throughput                 # [1]
]  # Total: 47 features
```

### 4. Reward Design

**Individual Reward (r_i):**

```
r_i = -α_wait × avg_waiting_time_i
      - α_queue × queue_length_i
      + α_throughput × throughput_i
```

**Coordination Reward (r_coord):**

```
r_coord = α_sync × green_wave_bonus
          + α_offset × offset_maintenance_bonus
```

**Final Reward:**

```
reward_i = 0.7 × r_i + 0.3 × r_coord
```

**Key Parameters:**

- α_wait = 0.3
- α_queue = 0.2
- α_throughput = 0.1
- α_sync = 0.2
- α_offset = 0.15

### 5. Training Protocol

**Exploration:**

- ε-greedy with decay: ε_start = 0.9, ε_end = 0.01, decay = 0.995
- Coordinated exploration: 10% of time, all agents explore simultaneously

**Training Episodes:**

- 200 episodes total
- Each episode: 3600 simulation seconds (1 hour)
- Time step: 5 seconds (720 steps per episode)

**Traffic Scenarios:**

- Morning rush: 80% arterial, 20% cross-street
- Evening rush: 70% arterial, 30% cross-street
- Off-peak: 50% arterial, 50% cross-street
- Random: Uniform distribution

**Convergence Criteria:**

- Average reward stable for 20 episodes (< 5% variation)
- Action distribution stable
- Q-value convergence (gap < 0.1)

---

## Experiments

### Experiment 1: QMIX vs. Baselines

**Baselines:**

1. **Independent Q-Learning (IQL)**

    - 5 separate DQN agents, no coordination
    - Only local rewards
    - Establishes lower bound

2. **Single Centralized Agent**

    - One DQN controlling all 5 signals
    - State: All 75 features (15 × 5)
    - Action space: 3^5 = 243 joint actions
    - Establishes upper bound

3. **Fixed-Time Coordination**

    - Traditional green wave with optimized offsets
    - 60-second cycle
    - Progression speed: 50 km/h

4. **Actuated Control + Offset**
    - Vehicle-responsive green times
    - Fixed offsets for progression
    - Industry standard

**Metrics:**

- Average travel time (seconds)
- Number of stops per vehicle
- Average delay per vehicle
- Throughput (vehicles/hour)
- Fuel consumption (estimated)
- Green wave efficiency (% vehicles not stopping)

**Traffic Patterns:**

- Light: 400 veh/hr/approach
- Medium: 800 veh/hr/approach
- Heavy: 1200 veh/hr/approach
- Rush hour: 1500 veh/hr/approach (arterial)

### Experiment 2: Scalability Analysis

**Test configurations:**

- 2 intersections (baseline)
- 5 intersections (main)
- 10 intersections (extended corridor)

**Metrics:**

- Training time (wall-clock hours)
- Inference time (ms per decision)
- Memory usage (GB)
- Performance degradation with scale

### Experiment 3: Ablation Study

**Test variants:**

1. **Reward composition:**

    - 100% local reward (no coordination)
    - 50% local + 50% coordination
    - 70% local + 30% coordination (proposed)
    - 30% local + 70% coordination

2. **State representation:**

    - No neighbor information
    - Only immediate neighbors (i-1, i+1)
    - All neighbor states

3. **Mixing network depth:**
    - Single layer
    - Two layers (proposed)
    - Three layers

### Experiment 4: Robustness Analysis

**Scenarios:**

1. **Demand variation:**

    - Sudden spike (+50% demand)
    - Gradual increase (morning ramp-up)
    - Special event (2x normal demand)

2. **Agent failure:**

    - Single agent failure (TLS-3)
    - Multiple agent failures (TLS-2, TLS-4)
    - Sequential failures

3. **Sensor noise:**
    - ±10% queue length error
    - ±20% waiting time error
    - Missing detector data (20% dropout)

### Experiment 5: Generalization

**Transfer scenarios:**

1. **Different time-of-day:**

    - Train on morning rush
    - Test on evening rush (different flow patterns)

2. **Different demand levels:**

    - Train on medium traffic
    - Test on light and heavy traffic

3. **Different network:**
    - Train on straight corridor
    - Test on corridor with irregular spacing

---

## Expected Results

### Performance Comparison:

| Method          | Avg Travel Time | Stops/Vehicle | Throughput      | Green Wave % |
| --------------- | --------------- | ------------- | --------------- | ------------ |
| IQL (no coord)  | 180s            | 2.8           | 4200 veh/hr     | 35%          |
| Fixed-Time      | 165s            | 2.3           | 4500 veh/hr     | 55%          |
| Actuated+Offset | 155s            | 2.1           | 4700 veh/hr     | 62%          |
| QMIX (proposed) | **140s**        | **1.6**       | **5000 veh/hr** | **75%**      |
| Centralized     | 135s            | 1.5           | 5100 veh/hr     | 78%          |

**Key Findings:**

- QMIX achieves 90% of centralized performance with decentralized execution
- 15% improvement over actuated control
- 22% improvement over independent learning
- Near-optimal green wave coordination emerges

### Scalability:

| # Intersections | Training Time | Inference Time | Memory |
| --------------- | ------------- | -------------- | ------ |
| 2               | 4 hours       | 0.8 ms         | 500 MB |
| 5               | 12 hours      | 1.2 ms         | 800 MB |
| 10              | 30 hours      | 2.1 ms         | 1.5 GB |

**QMIX scales reasonably to 10 intersections, but challenges beyond that.**

---

## Paper Outline

### 1. Introduction

- Problem: Inefficient independent traffic signal control
- Gap: Existing multi-agent methods lack coordination guarantees
- Contribution: QMIX enables emergent coordination with decentralized execution
- Results preview: X% improvement over baselines

### 2. Related Work

**2.1 Traditional Traffic Signal Control**

- Fixed-time control and green wave theory
- Actuated control and offset optimization
- Limitations for dynamic traffic

**2.2 Single-Agent Reinforcement Learning for Traffic**

- DQN, DDQN, Dueling DQN applications
- Limitations: scalability, single intersection focus

**2.3 Multi-Agent Reinforcement Learning**

- Independent Q-Learning
- Joint action learning
- CTDE paradigm (MADDPG, COMA)

**2.4 Value Decomposition Methods**

- VDN (Value Decomposition Networks)
- QMIX (monotonic value factorization)
- Applications in cooperative tasks

**2.5 Multi-Agent Traffic Control**

- Existing approaches and limitations
- Need for scalable coordination

### 3. Methodology

**3.1 Problem Formulation**

- Multi-agent MDP
- State space, action space, reward function
- Coordination challenges

**3.2 QMIX Architecture**

- Individual Q-networks
- Mixing network design
- Monotonic value factorization property
- Training vs. execution

**3.3 State Representation**

- Local observations
- Global state for coordination
- Neighbor information integration

**3.4 Reward Design**

- Individual performance rewards
- Coordination incentives
- Hybrid reward formulation

**3.5 Training Protocol**

- Experience replay
- Exploration strategy
- Hyperparameters

### 4. Experimental Setup

**4.1 Simulation Environment**

- SUMO traffic simulator
- 5-intersection corridor network
- Traffic demand patterns

**4.2 Baselines**

- IQL, Centralized, Fixed-Time, Actuated+Offset

**4.3 Evaluation Metrics**

- Travel time, stops, throughput, green wave efficiency

**4.4 Training Details**

- Network architectures
- Hyperparameters
- Computational resources

### 5. Results

**5.1 Performance Comparison**

- QMIX vs. all baselines
- Statistical significance tests
- Performance across traffic patterns

**5.2 Scalability Analysis**

- Computational cost
- Performance with 2, 5, 10 intersections

**5.3 Ablation Study**

- Reward composition impact
- State representation impact
- Architecture design choices

**5.4 Robustness Analysis**

- Performance under demand variation
- Agent failure scenarios
- Sensor noise impact

**5.5 Coordination Analysis**

- Green wave emergence
- Offset patterns learned
- Phase synchronization

### 6. Discussion

**6.1 Why QMIX Works for Traffic**

- Monotonic mixing ensures coordination
- CTDE enables scalable deployment
- Learned offsets adapt to traffic

**6.2 Comparison to Centralized Control**

- 90% performance with decentralized execution
- Robustness advantages
- Deployment feasibility

**6.3 Limitations**

- Scalability ceiling (~10-20 intersections)
- Training time requirements
- Assumption of communication during training

**6.4 Real-World Deployment Considerations**

- Computational requirements per intersection
- Offline training, online deployment
- Incremental rollout strategy

### 7. Conclusion

- QMIX enables effective multi-agent coordination for traffic signals
- Emergent green wave without explicit programming
- 15% improvement over state-of-practice
- Foundation for scalable city-wide control

### 8. Future Work

- Extension to GNN-DRL for larger networks (PAPER_5)
- Real-world field testing
- Integration with connected vehicles
- Adaptive coordination for special events

---

## Key Novelty Points

1. **First QMIX application to traffic signal control** with empirical validation
2. **Emergent coordination** - green wave learned, not programmed
3. **Hybrid reward design** - balances local and global objectives
4. **Comprehensive baseline comparison** - establishes clear improvements
5. **Scalability analysis** - shows practical limits and future directions

---

## Target Venues

**Primary:**

- IEEE Transactions on Intelligent Transportation Systems (T-ITS)
- Transportation Research Part C: Emerging Technologies

**Secondary:**

- International Conference on Intelligent Transportation Systems (ITSC)
- IEEE Intelligent Vehicles Symposium (IV)
- Transportation Research Board (TRB) Annual Meeting

**Timeline:**

- Experiments: 2-3 months
- Writing: 1-2 months
- Submission: Month 6
- Expected publication: Month 12-18

---

## Connection to Other Papers

**Builds on:**

- PAPER_1: Single-agent DRL methodology (state/action/reward design)
- PAPER_2: Single-agent explainability (foundation for multi-agent analysis)

**Enables:**

- PAPER_4: Multi-agent explainability (analyze coordination from this paper)
- PAPER_5: GNN-DRL scalability (use this as baseline comparison)

**Research continuity:**

```
PAPER_1 (Single Methodology) → PAPER_3 (Multi-Agent Methodology)
PAPER_2 (Single Explainability) → PAPER_4 (Multi-Agent Explainability)
PAPER_3 (QMIX 5 signals) → PAPER_5 (GNN-DRL city-scale)
```
