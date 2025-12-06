# PAPER_7: Role-Aware Multi-Modal Traffic Signal Control

## Working Title

**"Dynamic Role Learning for Equity-Aware Multi-Agent Traffic Signal Coordination"**

Alternative titles:

- "Role-Aware Multi-Agent Reinforcement Learning for Multi-Modal Traffic Control"
- "Learning Adaptive Roles: Priority-Aware Coordination for Cars, Buses, Bikes, and Pedestrians"
- "From Homogeneous to Heterogeneous: Role Specialization in Multi-Agent Traffic Control"

---

## Abstract (Concept)

Traditional multi-agent traffic control treats all intersection agents homogeneously, with identical reward structures
and action spaces. However, real-world corridors have heterogeneous traffic demands: some intersections serve as
corridor entry points, others as transit hubs, and others as pedestrian-heavy zones. Inspired by role-aware
reinforcement learning, we propose a framework where traffic signal agents dynamically discover and assume specialized
roles based on real-time traffic context. Building on our QMIX coordination (PAPER_3) and emergent role discovery
(PAPER_4), we formalize five role types—Entry Regulator, Transit Coordinator, Pedestrian Manager, Flow Balancer, and
Exit Controller—each with tailored reward functions. Our role-aware approach achieves 25% improvement in multi-modal
equity (balanced waiting times across cars, buses, bikes, pedestrians) while maintaining corridor throughput within 3%
of homogeneous QMIX. The framework naturally handles priority conflicts when buses and pedestrians compete for green
time.

---

## Inspiration

**Based on:** RMTC (Role-aware Multi-agent Traffic Control, NeurIPS 2025)

**Original Paper Contribution:**

- Heterogeneous Temporal Traffic Graph (HTTG) construction
- Dynamic role learning for emergency vehicle prioritization
- 15-23% reduction in emergency vehicle travel times

**Our Extension:**

- Focus on **multi-modal equity** (not just emergency vehicles)
- Include cars, buses, bicycles, AND pedestrians
- Build on PAPER_4's discovered roles (formalize and extend)
- Add equity metrics as first-class optimization objective

---

## Research Questions

### Primary Questions:

1. **Can agents discover optimal roles without predefined assignment?**

    - Entry regulator, transit coordinator, pedestrian manager
    - Role emergence vs. role assignment

2. **How should role-specific rewards be designed?**

    - Transit coordinator: prioritize bus wait times
    - Pedestrian manager: prioritize ped safety and wait
    - Entry regulator: balance throughput and queue prevention

3. **Does role specialization improve multi-modal equity?**
    - Define and measure equity across modes
    - Trade-off: equity vs. overall throughput

### Secondary Questions:

4. **How do roles adapt when traffic patterns change?**

    - Morning rush vs. evening rush
    - Special events (concerts, sports)

5. **Can role-aware control handle priority conflicts?**

    - Bus vs. pedestrian priority
    - Emergency vehicle preemption

6. **How does role awareness affect coordination patterns?**
    - Role-to-role communication
    - Hierarchical coordination

---

## Core Contribution

### Main Contributions:

1. **Dynamic Role Learning for Traffic Control**

    - Extend RMTC from emergency vehicles to multi-modal traffic
    - Unsupervised role discovery based on traffic context
    - Role-specific reward functions

2. **Multi-Modal Equity Framework**

    - Define equity metrics for cars, buses, bikes, pedestrians
    - Pareto-optimal coordination across modes
    - Configurable priority hierarchy

3. **Priority Conflict Resolution**

    - When bus and pedestrian priorities conflict
    - Hierarchical priority: Emergency > Bus > Ped > Bike > Car
    - Context-dependent priority adjustment

4. **Integration with QMIX Coordination**

    - Role-aware mixing network
    - Role-based attention weights
    - Seamless integration with PAPER_3 framework

5. **Practical Deployment Guidelines**
    - Role assignment for new corridors
    - Monitoring role health
    - Fallback strategies

---

## Methodology

### 1. Role Taxonomy

**Five Role Types (Extended from PAPER_4 Discovery):**

```
1. ENTRY_REGULATOR (TLS-1 in corridor)
├─ Primary goal: Control corridor entry, prevent queue spillback
├─ Key metrics: Entry rate, upstream queue prevention
├─ Communication: High out-degree (informs downstream)
└─ Priority: Throughput > Wait time reduction

2. TRANSIT_COORDINATOR (High bus traffic intersections)
├─ Primary goal: Minimize bus waiting time
├─ Key metrics: Bus delay, schedule adherence
├─ Communication: Upstream notification of bus arrivals
└─ Priority: Bus > Ped > Car

3. PEDESTRIAN_MANAGER (High ped demand intersections)
├─ Primary goal: Serve pedestrian demand with low wait
├─ Key metrics: Ped wait time, crossing frequency
├─ Communication: Coordinate with neighbors for ped waves
└─ Priority: Ped safety > Ped wait > Vehicle throughput

4. FLOW_BALANCER (Middle corridor, cross-street demand)
├─ Primary goal: Balance arterial vs. cross-street
├─ Key metrics: Queue equity across approaches
├─ Communication: Bidirectional with neighbors
└─ Priority: Balance all modes

5. EXIT_CONTROLLER (TLS-N at corridor end)
├─ Primary goal: Clear corridor, prevent backup
├─ Key metrics: Exit rate, queue clearance
├─ Communication: High in-degree (responds to upstream)
└─ Priority: Throughput > Wait time
```

### 2. Role Discovery

**Method 1: Unsupervised Role Clustering**

```python
# Cluster agents based on traffic context features
features = [
    bus_frequency,           # High → TRANSIT_COORDINATOR
    ped_demand,              # High → PEDESTRIAN_MANAGER
    position_in_corridor,    # Start → ENTRY, End → EXIT
    cross_street_demand,     # High → FLOW_BALANCER
    queue_asymmetry          # High → specialized role
]

role = KMeans(n_clusters=5).fit(features).predict(agent_context)
```

**Method 2: Attention-Based Role Inference**

```python
# Learn role from attention patterns (from PAPER_4)
role_embedding = RoleEncoder(
    mixing_network_weights,   # Agent importance in coordination
    dependency_graph,         # Position in coordination structure
    traffic_context          # Current traffic demands
)

role = RoleClassifier(role_embedding)  # Soft assignment
```

**Method 3: Dynamic Role Assignment**

```python
# Role changes based on real-time traffic
def assign_role(agent_i, current_context):
    if bus_approaching(agent_i):
        return TRANSIT_COORDINATOR  # Temporary role
    elif ped_demand_high(agent_i):
        return PEDESTRIAN_MANAGER
    else:
        return base_role[agent_i]  # Default role
```

### 3. Role-Specific Reward Functions

**Base Reward (All Roles):**

```
r_base = -α_wait × avg_waiting_time - α_queue × queue_length
```

**Entry Regulator Bonus:**

```
r_entry = +α_entry × throughput_rate
          - α_spillback × upstream_queue_penalty
          + α_metering × smooth_entry_bonus
```

**Transit Coordinator Bonus:**

```
r_transit = -α_bus_wait × bus_waiting_time
            + α_schedule × schedule_adherence_bonus
            + α_bus_priority × bus_served_green_bonus
```

**Pedestrian Manager Bonus:**

```
r_ped = -α_ped_wait × ped_waiting_time
        + α_ped_served × pedestrians_served
        + α_ped_safety × safety_bonus (no conflicts)
```

**Flow Balancer Bonus:**

```
r_balance = -α_equity × queue_variance_across_approaches
            + α_throughput × total_throughput
```

**Exit Controller Bonus:**

```
r_exit = +α_clearance × queue_clearance_rate
         - α_backup × downstream_queue_penalty
```

**Final Reward:**

```
reward_i = r_base + role_bonus[role_i]
```

### 4. Role-Aware Mixing Network

**Extension of QMIX Mixing Network:**

```
Standard QMIX:
Q_tot = MixingNetwork(Q_1, Q_2, ..., Q_n, global_state)

Role-Aware QMIX:
Q_tot = RoleAwareMixing(
    Q_1, Q_2, ..., Q_n,
    role_1, role_2, ..., role_n,
    global_state
)

Role-based attention:
α_i = f(role_i, traffic_context)  # Role affects agent weight
```

**Role Compatibility Matrix:**

```
                Entry  Transit  Ped    Balance  Exit
Entry           1.0    0.8      0.6    0.9      0.7
Transit         0.8    1.0      0.5    0.7      0.6
Ped             0.6    0.5      1.0    0.7      0.5
Balance         0.9    0.7      0.7    1.0      0.9
Exit            0.7    0.6      0.5    0.9      1.0

# High compatibility → Strong coordination
# Low compatibility → Potential conflicts (needs resolution)
```

### 5. Priority Conflict Resolution

**Conflict Scenarios:**

1. Bus approaching + High ped demand → Who gets priority?
2. Emergency vehicle + Pedestrian crossing → Safety vs. emergency
3. Bicycle green wave + Bus priority → Coordination challenge

**Resolution Hierarchy:**

```
Priority Order:
1. Emergency vehicles (preemption)
2. Safety (active pedestrian crossings)
3. Transit (buses, scheduled priority)
4. Bicycles (vulnerable road users)
5. Regular vehicles
```

**Conflict Resolution Algorithm:**

```python
def resolve_priority(agent_i, current_demands):
    priorities = []

    if emergency_vehicle_approaching(agent_i):
        return PREEMPTION  # Highest priority

    if ped_actively_crossing(agent_i):
        priorities.append((SAFETY, 1.0))

    if bus_approaching(agent_i):
        bus_urgency = calculate_schedule_delay(bus)
        priorities.append((TRANSIT, bus_urgency))

    if bike_platoon(agent_i):
        priorities.append((BIKE, 0.7))

    # Weighted combination for soft priority
    return weighted_priority_action(priorities)
```

### 6. Multi-Modal Equity Metrics

**Equity Definition:**

```
Equity = 1 - CV(wait_times)

where CV = Coefficient of Variation = std(wait) / mean(wait)

Per-mode wait times:
- W_car = average car waiting time
- W_bus = average bus waiting time
- W_bike = average bicycle waiting time
- W_ped = average pedestrian waiting time

Equity Score = 1 - std([W_car, W_bus, W_bike, W_ped]) / mean([...])

Perfect equity (1.0): All modes wait equally
Poor equity (0.0): Large disparities between modes
```

**Normalized Wait Times (Mode-Specific Expectations):**

```
# Different modes have different acceptable waits
Normalized waits:
- N_car = W_car / 30s   (30s acceptable for cars)
- N_bus = W_bus / 15s   (15s target for transit)
- N_bike = W_bike / 20s (20s acceptable for bikes)
- N_ped = W_ped / 25s   (25s acceptable for peds)

Equity Score = 1 - std([N_car, N_bus, N_bike, N_ped])
```

---

## Experiments

### Experiment 1: Role Discovery Accuracy

**Setup:**

- 5-intersection corridor with known characteristics:
    - TLS-1: Entry point, high inflow
    - TLS-2: Bus stop, transit priority
    - TLS-3: School zone, high pedestrian
    - TLS-4: Commercial area, balanced
    - TLS-5: Exit to highway, high outflow

**Evaluation:**

- Compare discovered roles vs. ground truth
- Role stability over episodes
- Role switching frequency

**Expected Results:**

| Agent | Ground Truth        | Discovered Role       | Match |
| ----- | ------------------- | --------------------- | ----- |
| TLS-1 | Entry Regulator     | Entry Regulator       | ✓     |
| TLS-2 | Transit Coordinator | Transit Coordinator   | ✓     |
| TLS-3 | Pedestrian Manager  | Ped Manager / Balance | ~     |
| TLS-4 | Flow Balancer       | Flow Balancer         | ✓     |
| TLS-5 | Exit Controller     | Exit Controller       | ✓     |

### Experiment 2: Role-Aware vs. Homogeneous QMIX

**Baselines:**

1. QMIX (PAPER_3): Same reward for all agents
2. Role-Aware QMIX: Role-specific rewards
3. Hand-coded roles: Expert-assigned roles
4. Independent role learning: Roles without coordination

**Metrics:**

- Multi-modal equity score
- Per-mode waiting times
- Total corridor throughput
- Coordination quality (sync rate)

**Expected Results:**

| Method             | Equity | Car Wait | Bus Wait | Ped Wait | Throughput |
| ------------------ | ------ | -------- | -------- | -------- | ---------- |
| QMIX (homogeneous) | 0.65   | 28s      | 45s      | 32s      | 5000 v/hr  |
| Hand-coded roles   | 0.72   | 30s      | 35s      | 28s      | 4850 v/hr  |
| **Role-Aware**     | 0.82   | 31s      | 32s      | 26s      | 4900 v/hr  |
| Independent roles  | 0.58   | 35s      | 40s      | 35s      | 4500 v/hr  |

### Experiment 3: Priority Conflict Resolution

**Scenarios:**

1. **Bus + Pedestrian Conflict:**

    - Bus approaching TLS-3 (high ped demand)
    - How does agent resolve priority?

2. **Emergency + All Modes:**

    - Emergency vehicle during rush hour
    - Measure disruption and recovery

3. **Bike Wave + Bus:**
    - Bicycle platoon on arterial
    - Bus on cross-street

**Metrics:**

- Conflict resolution time
- Mode-specific delay during conflicts
- Recovery time to normal operation

### Experiment 4: Dynamic Role Adaptation

**Time-Varying Scenarios:**

- 6-8 AM: Morning rush (heavy car traffic)
- 8-9 AM: School start (high pedestrian)
- 9 AM-4 PM: Off-peak (balanced)
- 4-6 PM: Evening rush (high car + transit)
- 6-8 PM: Leisure (high pedestrian + bike)

**Analysis:**

- How often do roles change?
- Role transition patterns
- Performance during role changes

**Expected Insight:**

```
Morning Rush (6-8 AM):
├─ TLS-1: Entry Regulator (high car inflow)
├─ TLS-2: Flow Balancer (manage queues)
└─ TLS-3: Flow Balancer (no school yet)

School Start (8-9 AM):
├─ TLS-1: Entry Regulator (still high car)
├─ TLS-2: Transit Coordinator (school buses)
└─ TLS-3: Pedestrian Manager (students crossing)

Role Change: TLS-3 switches Balancer → Ped Manager at 8 AM
```

### Experiment 5: Equity-Throughput Trade-off

**Pareto Analysis:**

- Vary equity weight in reward: α_equity = 0.1, 0.2, 0.3, 0.4, 0.5
- Plot equity score vs. total throughput
- Identify Pareto frontier

**Expected Result:**

```
α_equity | Equity | Throughput
0.1      | 0.68   | 5100 v/hr
0.2      | 0.75   | 4950 v/hr
0.3      | 0.82   | 4900 v/hr  ← Sweet spot
0.4      | 0.86   | 4750 v/hr
0.5      | 0.89   | 4500 v/hr
```

### Experiment 6: Comparison with RMTC

**Setup:**

- Implement simplified RMTC (emergency focus)
- Add emergency vehicles to our scenarios
- Compare role discovery and performance

**Expected Results:**

| Aspect               | RMTC            | Our Approach      |
| -------------------- | --------------- | ----------------- |
| Focus                | Emergency only  | All modes         |
| Role types           | 3 (EV-specific) | 5 (multi-modal)   |
| Emergency EV time    | -23%            | -20% (comparable) |
| Multi-modal equity   | 0.55 (poor)     | 0.82 (good)       |
| Regular traffic wait | +5% (sacrifice) | -8% (improvement) |

---

## Expected Results

### Performance Summary:

**Multi-Modal Equity:**

```
Homogeneous QMIX: 0.65
Role-Aware (ours): 0.82
Improvement: +26%
```

**Per-Mode Improvements:**

```
Bus wait:  45s → 32s  (-29%)
Ped wait:  32s → 26s  (-19%)
Bike wait: 28s → 23s  (-18%)
Car wait:  28s → 31s  (+11%)  ← Acceptable trade-off
```

**Throughput:**

```
QMIX: 5000 veh/hr
Role-Aware: 4900 veh/hr (-2%)  ← Acceptable for equity gains
```

### Role Discovery Insights:

```
Discovered Role Characteristics:

Entry Regulator:
- High mixing weight (0.28)
- Focuses on own arterial queue (saliency 0.45)
- Low response to neighbor states

Transit Coordinator:
- Responds to bus detector (saliency 0.52)
- Communicates upstream (bus arriving notifications)
- Phase extension patterns for bus clearance

Pedestrian Manager:
- High pedestrian saliency (0.48)
- Shorter phase cycles (serve peds frequently)
- Lower throughput optimization
```

---

## Paper Outline

### 1. Introduction

- Problem: Homogeneous multi-agent control ignores mode-specific needs
- Gap: Existing role-aware methods focus on emergency vehicles only
- Contribution: Multi-modal role learning with equity optimization
- Preview: 26% equity improvement, 5 role types discovered

### 2. Related Work

**2.1 Multi-Modal Traffic Control**

- Transit signal priority
- Pedestrian-friendly signal timing
- Complete Streets policies

**2.2 Role-Aware Multi-Agent Systems**

- RMTC and emergency vehicle focus
- Role learning in cooperative games
- Hierarchical multi-agent systems

**2.3 Equity in Transportation**

- Definition and measurement
- Equity-efficiency trade-offs
- Policy implications

### 3. Methodology

**3.1 Role Taxonomy** **3.2 Role Discovery Methods** **3.3 Role-Specific Rewards** **3.4 Role-Aware Mixing Network**
**3.5 Priority Conflict Resolution** **3.6 Equity Metrics**

### 4. Experiments

**4.1 Role Discovery Accuracy** **4.2 Role-Aware vs. Homogeneous** **4.3 Priority Conflict Resolution** **4.4 Dynamic
Role Adaptation** **4.5 Equity-Throughput Trade-off** **4.6 Comparison with RMTC**

### 5. Results

**5.1 Equity Improvements** **5.2 Per-Mode Performance** **5.3 Role Characteristics** **5.4 Conflict Resolution
Effectiveness**

### 6. Discussion

**6.1 Why Roles Improve Equity** **6.2 Role Design Guidelines** **6.3 Policy Implications** **6.4 Limitations**

### 7. Conclusion

- Role-aware control improves multi-modal equity by 26%
- Five distinct roles emerge from traffic context
- Priority conflicts resolved through learned hierarchy
- Foundation for equitable urban traffic management

---

## Key Novelty Points

1. **Multi-modal role learning** - Extends RMTC from emergency to all modes
2. **Equity as first-class objective** - Novel metric and optimization
3. **Dynamic role adaptation** - Roles change with traffic patterns
4. **Priority conflict resolution** - Learned hierarchical priorities
5. **Integration with QMIX** - Role-aware mixing network
6. **Formalization of PAPER_4 discoveries** - Roles from explainability to design

---

## Target Venues

**Primary:**

- Transportation Research Part C: Emerging Technologies (equity focus)
- IEEE Transactions on Intelligent Transportation Systems
- Journal of Intelligent Transportation Systems

**Secondary:**

- AAMAS (multi-agent role learning)
- ITSC Conference
- TRB Annual Meeting

**Timeline:**

- After PAPER_6 completion
- Implementation: 2-3 months
- Experiments: 2-3 months
- Writing: 1-2 months

---

## Connection to Other Papers

**Builds on:**

- PAPER_3: QMIX foundation
- PAPER_4: Emergent role discovery (formalize and extend)
- PAPER_6: Learned communication (role-aware communication)

**Connects to your existing work:**

- Bus priority system (already implemented!)
- Pedestrian detection (already implemented!)
- Multi-modal traffic generation (already implemented!)

**Research Arc:**

```
PAPER_4 (Role Discovery - Descriptive)
    ↓
PAPER_7 (Role-Aware Control - Prescriptive)
    ↓
Equitable City-Scale Traffic Management
```

---

## Practical Implications

### For Traffic Engineers:

1. **Role assignment guidelines** for new corridors
2. **Equity monitoring dashboards** for operations
3. **Priority tuning** based on community needs

### For Policy Makers:

1. **Evidence for Complete Streets** implementation
2. **Quantified equity improvements** for transit investment
3. **Trade-off analysis** for political decisions

### For Future Research:

1. **Equity across different demographics** (not just modes)
2. **Environmental justice** considerations
3. **Accessibility** for mobility-impaired users

---

## Future Extensions

- **Emergency integration:** Combine with RMTC for complete priority system
- **Connected vehicles:** Role-based V2I communication
- **Adaptive hierarchy:** Learn priority order from community preferences
- **City-scale equity:** Neighborhood-level role coordination
- **Temporal equity:** Fairness over time (no mode consistently disadvantaged)
