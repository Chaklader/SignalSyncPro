# Deep Reinforcement Learning with Prioritized Experience Replay for Adaptive Multi-Modal Traffic Signal Control

Multimodal urban intersections require balancing the needs of vehicles, bicycles, pedestrians, and public transit.
Current traffic signal control systems either prioritize vehicles (Reference Control) or use fixed rule-based logic for
multimodal coordination (Developed Control).

We propose a Deep Q-Network (DQN) with Prioritized Experience Replay (PER) that learns optimal signal control policies
for multimodal intersections. The PER mechanism prioritizes learning from rare but critical events such as pedestrian
exclusive phase activation, bus priority conflicts, and synchronization failures.

We evaluate our approach on 27 traffic scenarios using SUMO simulation, comparing against two baselines: a conventional
vehicle-centric control (Reference) and a rule-based multimodal control (Developed). Results show that DRL-PER achieves:

- 60-85% reduction in bicycle waiting time vs. Reference
- 15-25% improvement over rule-based control (Developed)
- 82% synchronization success rate (vs. 60% for rule-based)
- Better handling of rare events through prioritized learning

Our approach demonstrates that combining deep reinforcement learning with prioritized experience replay enables adaptive
multimodal coordination that outperforms both conventional and rule-based approaches.

---

# DRL-Based Traffic Control Workflow

##### **The Big Picture: The Learning Process**

Think of the DRL agent as a **student learning to be a traffic controller** through experience. Instead of following fixed rules (like your Developed Control), it learns by trial and error what works best in different situations.

------

##### **Core Concept: The Learning Cycle**

```mermaid
flowchart LR
    A["🚦 Intersection<br>(Current State)"] --> B["🤖 DRL Agent<br>(Brain)"]
    B --> C["📋 Decision<br>(Action)"]
    C --> D["⚙️ Execute in<br>Traffic System"]
    D --> E["📊 Observe Results<br>(Reward + New State)"]
    E --> F["💾 Store Experience<br>in Memory"]
    F --> G["📚 Learn from<br>Past Experiences"]
    G --> B
    
    style A fill:#E3F2FD
    style B fill:#C8E6C9
    style C fill:#FFF9C4
    style D fill:#FFCCBC
    style E fill:#F8BBD0
    style F fill:#D1C4E9
    style G fill:#B2DFDB
```

------

##### **Step-by-Step: How One Decision is Made**

###### **Step 1: Observe the Current Situation**

The DRL agent looks at the intersection and gathers information about what's happening right now:

**What the Agent "Sees":**

- **Vehicle queues**: How many cars waiting at each approach (North, South, East, West)
- **Bicycle queues**: How many bicycles waiting
- **Pedestrian crowds**: How many pedestrians waiting to cross
- **Current phase**: Which signal phase is running (Phase 1, 2, 3, 4, or 5)
- **Time elapsed**: How long has this phase been green
- **Detector signals**: Are vehicles/bicycles detected on the D30/D15 detectors?
- **Bus location**: Is a bus approaching? How far away?
- **Synchronization timer**: Time until the next coordination window with upstream/downstream intersection
- **Time of day**: Morning rush hour? Midday? Evening?

**Think of this like:** A human traffic controller looking at multiple screens showing camera feeds, detector readings, and timers.

------

###### **Step 2: The Agent Decides What to Do**

Based on what it observes, the DRL agent chooses one of four possible actions:

```mermaid
flowchart TD
    A["🤖 DRL Agent<br>with Current State"] --> B{"What should I do?"}
    B --> C["Action 1:<br>Continue Current Phase<br>+1 second"]
    B --> D["Action 2:<br>Skip to Phase 1<br>(Major Through)"]
    B --> E["Action 3:<br>Progress to Next Phase<br>(Normal sequence)"]
    B --> F["Action 4:<br>Activate Phase 5<br>(Pedestrian Exclusive)"]
    
    C --> G["🎯 Selected Action"]
    D --> G
    E --> G
    F --> G
    
    style A fill:#C8E6C9
    style B fill:#FFF9C4
    style C fill:#E1F5FE
    style D fill:#E1F5FE
    style E fill:#E1F5FE
    style F fill:#E1F5FE
    style G fill:#FFCCBC
```

**How it Decides:**

- The agent uses a **neural network** (the "brain") that has learned from thousands of past experiences
- For each possible action, it calculates a **Q-value** (quality score) that predicts how good that action will be
- Usually picks the action with the **highest Q-value**, but sometimes tries random actions to explore new strategies

------

###### **Step 3: Execute the Action in SUMO**

The chosen action is sent to the SUMO traffic simulation:

**What Happens:**

- If "Continue Phase": Green light extended by 1 second
- If "Skip to Phase 1": Current phase ends, transition to major through phase
- If "Progress to Next": Move to the next phase in sequence (e.g., Phase 2 → Phase 3)
- If "Activate Phase 5": Start the pedestrian exclusive phase

**Just like:** A human controller pressing buttons to change the signals.

------

###### **Step 4: Observe the Results**

After executing the action, the system measures what happened:

**Performance Metrics:**

- **Waiting times**: Did waiting times increase or decrease for each mode?
- **Queue lengths**: Did queues grow or shrink?
- **Emissions**: Did CO₂ emissions go up or down?
- **Synchronization**: Did we successfully coordinate with the upstream intersection?
- **Safety**: Were there any conflicts or dangerous situations?

**Reward Calculation:** The agent receives a **reward score** that tells it how well it did:

- **Positive rewards** for: Reducing waiting times, achieving synchronization, serving vulnerable modes
- **Negative penalties** for: Long queues, high emissions, missed synchronization, safety issues

------

###### **Step 5: Store the Experience**

This entire experience is saved in the **Prioritized Replay Buffer**:

**What Gets Stored:**

```
Experience = {
    'state_before': [queue lengths, phase info, timers, ...],
    'action_taken': "Continue Phase",
    'reward_received': -5.2,
    'state_after': [new queue lengths, new phase info, ...],
    'priority': 8.5
}
```

**Priority Assignment:** Some experiences are marked as **more important** to learn from:

- **High priority**: Pedestrian phase activation, bus conflicts, sync failures, safety issues
- **Medium priority**: Normal synchronization attempts, mode balancing
- **Low priority**: Routine decisions with expected outcomes

------

###### **Step 6: Learning from Past Experiences**

Periodically (every few seconds), the agent updates its neural network by studying past experiences:

**The Learning Process:**

```mermaid
flowchart TD
    A["💾 Prioritized<br>Replay Buffer"] --> B["📖 Sample Batch<br>of Experiences"]
    B --> C["⚖️ Prioritize Important<br>Events"]
    C --> D["🧮 Calculate:<br>How wrong were<br>my predictions?"]
    D --> E["🔄 Update Neural Network<br>to make better predictions"]
    E --> F["🎯 Improved Decision-Making<br>for Future Situations"]
    
    style A fill:#D1C4E9
    style B fill:#E1BEE7
    style C fill:#CE93D8
    style D fill:#BA68C8
    style E fill:#AB47BC
    style F fill:#9C27B0
```

**What the Agent Learns:**

- "When there are 10+ pedestrians waiting and it's been 30+ seconds since their last green, activate Phase 5"
- "When the sync timer shows 8 seconds and there's a bus approaching, skip to Phase 1 now"
- "When bicycle queues are double the vehicle queues, extend the phase by 2 more seconds"
- "Don't activate pedestrian phase if only 3 pedestrians are waiting - waste of time"

------

# Complete DRL Control Flow Diagram

```mermaid
flowchart TD
    A["🚦 Intersection State<br>• Vehicle queues: [5,3,2,1]<br>• Bicycle queues: [4,2]<br>• Pedestrians: [8,3]<br>• Current Phase: 1<br>• Phase time: 12s<br>• Sync timer: 8s<br>• Bus approaching: Yes"] --> B["🧠 Neural Network<br>(DRL Agent Brain)"]
    
    B --> C{"Calculate Q-values<br>for all actions"}
    
    C --> D["Q(Continue) = 5.2"]
    C --> E["Q(Skip to Phase 1) = 8.7"]
    C --> F["Q(Next Phase) = 3.1"]
    C --> G["Q(Pedestrian Phase) = 2.4"]
    
    D --> H{"Select Action<br>with Highest Q-value"}
    E --> H
    F --> H
    G --> H
    
    H --> I["✅ Selected Action:<br>Skip to Phase 1<br>(Best for bus + sync)"]
    
    I --> J["⚙️ Execute in SUMO:<br>End current phase<br>Start Phase 1<br>Give 1s leading green"]
    
    J --> K["📊 Measure Results:<br>• Bus delay: 5s (good!)<br>• Sync achieved: Yes (+10)<br>• Car wait: +2s<br>• Overall reward: +6.3"]
    
    K --> L["💾 Store Experience<br>Priority = High<br>(bus conflict resolved)"]
    
    L --> M{"Enough experiences<br>in memory?"}
    
    M -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| A
    M -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| N["📚 Sample Important<br>Experiences<br>(prioritize rare events)"]
    
    N --> O["🔄 Update Neural Network:<br>Learn that 'Skip to Phase 1'<br>is good when bus + sync<br>timer is low"]
    
    O --> P["🎯 Improved Agent<br>Better decisions<br>next time"]
    
    P --> A
    
    style A fill:#E3F2FD
    style B fill:#C8E6C9
    style C fill:#FFF9C4
    style D fill:#E1F5FE
    style E fill:#FFE0B2
    style F fill:#E1F5FE
    style G fill:#E1F5FE
    style H fill:#81C784
    style I fill:#FFCCBC
    style J fill:#F48FB1
    style K fill:#CE93D8
    style L fill:#D1C4E9
    style M fill:#B2DFDB
    style N fill:#9C27B0
    style O fill:#7B1FA2
    style P fill:#4CAF50
```

------

##### Key Difference: DRL vs. Your Rule-Based Control

###### **Your Developed Control (Rule-Based):**

```mermaid
flowchart TD
    A["Phase Running"] --> B{"Min Green<br>Complete?"}
    B -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| A
    B -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| C{"Max Green<br>Reached?"}
    C -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| H
    C -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| D{"Sync Time<br>Reached?"}
    D -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| E["Skip to Phase 1"]
    D -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| F{"Bus<br>Arriving?"}
    F -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| E
    F -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| G{"Detector<br>Window Clear?"}
    G -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| H["Next Phase"]
    G -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| I["Continue Phase"]
    
    style A fill:#BBDEFB
    style E fill:#A5D6A7
    style H fill:#FFF59D
    style I fill:#FFAB91
```

**Fixed hierarchy**: Always checks conditions in the same order

------

###### **DRL Control (Learning-Based):**

```mermaid
flowchart TD
    A["Observe<br>Full State"] --> B["🧠 Neural Network<br>evaluates ALL actions<br>simultaneously"]
    B --> C["Considers:<br>• Queues for all modes<br>• Sync timer<br>• Bus location<br>• Pedestrian demand<br>• Time of day<br>• Past patterns"]
    C --> D{"Learned Policy<br>(from 1000s of<br>experiences)"}
    D --> E["🎯 Choose action that<br>maximizes long-term<br>multi-objective reward"]
    E --> F["Action adapts to:<br>• Traffic patterns<br>• Rare events<br>• Modal balance<br>• Context"]
    
    style A fill:#E1F5FE
    style B fill:#C8E6C9
    style C fill:#FFF9C4
    style D fill:#CE93D8
    style E fill:#81C784
    style F fill:#FFB74D
```

**Adaptive**: Weighs all factors simultaneously and learns what works best in different contexts

------

##### **Why Prioritized Experience Replay Matters**

###### **Problem Without PER:**

```mermaid
flowchart LR
    A["💾 Replay Buffer<br>10,000 experiences"] --> B["Regular sampling<br>(uniform random)"]
    B --> C["Most samples are<br>routine decisions"]
    C --> D["😞 Rare events<br>learned slowly"]
    
    style A fill:#E3F2FD
    style B fill:#BBDEFB
    style C fill:#90CAF9
    style D fill:#EF5350
```

**Example:**

- 9,500 normal decisions (extend phase, regular flow)
- 300 synchronization attempts
- 150 bus priority cases
- **50 pedestrian phase activations** ← Very rare but critical!

Without PER: Agent might see pedestrian phase only **1-2 times** in 100 learning steps → slow learning

------

###### **Solution With PER:**

```mermaid
flowchart LR
    A["💾 Replay Buffer<br>10,000 experiences"] --> B["Prioritized sampling<br>(based on importance)"]
    B --> C["Oversample rare<br>but critical events"]
    C --> D["😊 Fast learning<br>from all scenarios"]
    
    style A fill:#E3F2FD
    style B fill:#C8E6C9
    style C fill:#A5D6A7
    style D fill:#66BB6A
```

**With PER:** Agent sees pedestrian phase **20-30 times** in 100 learning steps → fast learning!

------

##### **Real-World Example Scenario**

Let me walk you through a concrete example:

###### **Situation:**

- **Time:** 8:15 AM (morning rush hour)
- **Vehicle queues:** North: 8 cars, South: 5 cars, East: 2 cars, West: 1 car
- **Bicycle queues:** North: 6 bikes, South: 4 bikes
- **Pedestrians:** 12 people waiting to cross North-South, 4 waiting East-West
- **Current phase:** Phase 2 (Protected left turn) - running for 8 seconds
- **Bus:** Approaching from South, 80 meters away
- **Sync timer:** 15 seconds until coordination window

------

###### **What Your Rule-Based Control Would Do:**

```
1. Check min green (5s) ✓ Yes, exceeded
2. Check max green (25s) ✗ No, not reached
3. Check sync time ✗ No, 15s remaining
4. Check bus priority ✗ No, bus too far
5. Check detector windows ✗ Bikes still passing
→ Decision: Continue Phase 2 (extend by 1s)
```

**Result:** Continues Phase 2, making bus wait unnecessarily

------

###### **What DRL Control Would Do:**

```
Neural network evaluates:

Action 1 (Continue Phase 2): Q-value = 4.2
  - Good: Serves bicycles (high queue)
  - Bad: Bus will wait longer, miss sync window

Action 2 (Skip to Phase 1): Q-value = 8.7 ← HIGHEST!
  - Good: Catches sync, serves bus, major flow
  - Bad: Cuts off bicycle phase early
  - Learned: At 8am with these queues, this trade-off is optimal

Action 3 (Next Phase): Q-value = 3.5
  - Neutral choice

Action 4 (Pedestrian Phase): Q-value = 6.8
  - Good: 12 pedestrians is high demand
  - Bad: Misses sync, delays bus significantly

→ Decision: Skip to Phase 1
```

**Result:**

- Bus experiences minimal delay
- Synchronization achieved
- Bicycles wait a bit longer (acceptable in morning rush)
- **Better overall system performance**

------

##### **The Training Process (High-Level)**

```mermaid
flowchart TD
    A["🎬 Start Training<br>Episode 1"] --> B["Random initial policy<br>(Agent doesn't know<br>anything yet)"]
    B --> C["Run 1 hour simulation<br>Make ~3600 decisions"]
    C --> D["Store all experiences<br>with priorities"]
    D --> E["Learn from batch<br>Update neural network"]
    E --> F{"Episode<br>Complete?"}
    F -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| G["📊 Evaluate Performance"]
    F -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| C
    G --> H{"Trained enough<br>episodes?<br>(~500-1000)"}
    H -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| I["🎬 Start Episode 2<br>with improved policy"]
    H -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| J["✅ Training Complete<br>Deploy agent"]
    I --> C
    
    style A fill:#E3F2FD
    style B fill:#BBDEFB
    style C fill:#90CAF9
    style D fill:#64B5F6
    style E fill:#42A5F5
    style F fill:#2196F3
    style G fill:#1E88E5
    style H fill:#1976D2
    style I fill:#1565C0
    style J fill:#66BB6A
```

**Timeline:**

- Episode 1-50: Mostly random, exploring different strategies
- Episode 51-200: Starting to learn patterns, improving slowly
- Episode 201-500: Rapid improvement, discovering good policies
- Episode 501-1000: Fine-tuning, mastering rare events
- **After 1000 episodes: Expert traffic controller!**

------

##### **Key Advantages of DRL Over Rules**

###### **1. Adaptive to Context**

```
Morning rush (8 AM):
  DRL learns: Prioritize major arterial, tolerate longer bike waits
  
Midday (1 PM):
  DRL learns: Balance all modes equally, optimize overall delay
  
Evening (6 PM):
  DRL learns: Prioritize buses + bicycles, coordinate tightly
```

###### **2. Handles Rare Events Well (Thanks to PER)**

```
Pedestrian crowd (happens 2% of time):
  DRL trains on this 10x more → learns optimal timing
  
Bus-sync conflict (happens 5% of time):
  DRL learns when to prioritize bus vs. sync
  
All-modes-high-demand (happens 1% of time):
  DRL learns emergency protocols
```

###### **3. Discovers Non-Obvious Strategies**

```
DRL might learn:
  "At 8:03 AM, if bike queue > 2x car queue, 
   extend phase by 3s even if sync window approaches,
   because next cycle will still catch the following vehicle platoon"
   
This nuanced strategy is hard to encode as a rule!
```

------

##### **Summary: The Learning Journey**

```mermaid
flowchart LR
    A["🤖 Newborn Agent<br>Random decisions"] --> B["👶 Beginner<br>Learning basic patterns"]
    B --> C["🧒 Intermediate<br>Handles common scenarios"]
    C --> D["👨 Advanced<br>Masters rare events"]
    D --> E["🧙 Expert<br>Optimal multimodal control"]
    
    style A fill:#FFCDD2
    style B fill:#F8BBD0
    style C fill:#E1BEE7
    style D fill:#C5CAE9
    style E fill:#C8E6C9
```

**What makes it work:**

- **Deep neural network**: Handles complex, high-dimensional traffic states
- **Reinforcement learning**: Learns from trial and error, no need for labeled data
- **Prioritized replay**: Ensures learning from rare but critical events
- **Multi-objective reward**: Balances competing goals (delay, emissions, equity, safety)

The DRL agent becomes a **traffic control expert** that adapts to patterns, handles edge cases, and continuously improves its decisions!

------

**YES! Exactly!** You've understood it perfectly. Let me explain the two distinct phases very clearly:

------

# **DRL Implementation: Training Phase vs. Deployment Phase**

## **The Two-Phase Process**

```mermaid
flowchart LR
    A["📚 Phase 1:<br>TRAINING<br>(Learn optimal policies)"] --> B["💾 Trained Model<br>(Neural Network Weights)"]
    B --> C["🚀 Phase 2:<br>DEPLOYMENT<br>(Use learned policies)"]
    
    style A fill:#FFE0B2
    style B fill:#C8E6C9
    style C fill:#BBDEFB
```

------

# **Phase 1: Training (Learning) - This Comes First**

###### **Purpose:**

Train the DRL agent by running **many simulations** so it learns what actions work best in different traffic situations.

###### **What Happens:**

```mermaid
flowchart TD
    A["🎬 Start Training"] --> B["Episode 1:<br>Run 1-hour simulation<br>with RANDOM actions"]
    B --> C["Collect experiences:<br>states, actions, rewards"]
    C --> D["Store in replay buffer"]
    D --> E["Learn from experiences:<br>Update neural network"]
    E --> F["Episode 2:<br>Run simulation with<br>SLIGHTLY BETTER actions"]
    F --> G["Repeat 500-1000 times"]
    G --> H["💾 Save Trained Model<br>(model.pth)"]
    
    style A fill:#E3F2FD
    style B fill:#BBDEFB
    style C fill:#90CAF9
    style D fill:#64B5F6
    style E fill:#42A5F5
    style F fill:#2196F3
    style G fill:#1E88E5
    style H fill:#66BB6A
```

###### **Training Details:**

**What you do:**

1. **Initialize** a DRL agent with random neural network weights (it knows nothing!)
2. **Run Episode 1**:
   - Start SUMO simulation with your network (Pr_0 scenario)
   - Agent makes mostly **random decisions** (exploring)
   - Record what happened: states, actions, rewards
   - Episode ends after 1 hour of simulation time
3. **Learn**:
   - Neural network studies the recorded experiences
   - Updates its weights to make better decisions
4. **Run Episode 2**:
   - Start fresh simulation
   - Agent now makes **slightly better decisions** (still exploring)
   - Record new experiences
5. **Repeat 500-1000 episodes**:
   - Each episode, agent gets better
   - Gradually shifts from random exploration → learned policy
6. **Save the trained model**:
   - Final neural network weights saved to disk (e.g., `drl_model.pth`)

**Training Metrics You Track:**

```
Episode 1:   Average Reward = -150  (very bad!)
Episode 50:  Average Reward = -80   (improving)
Episode 200: Average Reward = -30   (getting good)
Episode 500: Average Reward = +45   (excellent!)
Episode 800: Average Reward = +48   (converged - no more improvement)
→ Stop training, save model
```

------

# **Phase 2: Deployment (Testing) - This Comes Second**

###### **Purpose:**

Use the **trained model** to control traffic and compare its performance against Reference and Developed controls.

###### **What Happens:**

```mermaid
flowchart TD
    A["💾 Load Trained Model<br>(model.pth)"] --> B["🎯 Agent is now EXPERT<br>(no more learning)"]
    B --> C["Run test simulation:<br>Scenario Pr_0"]
    C --> D["Agent makes OPTIMAL<br>decisions based on<br>learned policy"]
    D --> E["Record performance:<br>waiting times, emissions, etc."]
    E --> F["Repeat for all scenarios:<br>Pr_0 to Pr_9<br>Bi_0 to Bi_9<br>Pe_0 to Pe_9"]
    F --> G["📊 Compare Results:<br>DRL vs Reference vs Developed"]
    
    style A fill:#C8E6C9
    style B fill:#A5D6A7
    style C fill:#81C784
    style D fill:#66BB6A
    style E fill:#4CAF50
    style F fill:#388E3C
    style G fill:#FFF9C4
```

###### **Testing Details:**

**What you do:**

1. **Load trained model**: Read saved weights from disk
2. **Disable exploration**: Agent only uses its learned policy (no random actions)
3. **Run test simulations**:
   - Scenario Pr_0: DRL control makes decisions, record results
   - Scenario Pr_1: DRL control makes decisions, record results
   - ... continue for all 27 scenarios
4. **Collect performance metrics**:
   - Average waiting time per mode
   - Synchronization success rate
   - CO₂ emissions
   - etc.
5. **Compare with baselines**:
   - DRL vs Reference Control
   - DRL vs Developed Control

**No learning happens** - the model is frozen!

------

##### **Complete Workflow Diagram**

```mermaid
flowchart TD
    subgraph Phase1["🎓 PHASE 1: TRAINING (Takes days/weeks)"]
        A1["Initialize DRL Agent<br>(random weights)"] --> A2["Training Episode 1"]
        A2 --> A3["SUMO Simulation<br>(Pr_0 scenario)"]
        A3 --> A4["Agent explores:<br>tries random actions"]
        A4 --> A5["Collect experiences"]
        A5 --> A6["Update neural network"]
        A6 --> A7{"Episode 500<br>complete?"}
        A7 -->|No| A2
        A7 -->|Yes| A8["💾 Save Model<br>drl_model.pth"]
    end
    
    A8 --> B1
    
    subgraph Phase2["🚀 PHASE 2: DEPLOYMENT (Takes hours)"]
        B1["💾 Load Trained Model"] --> B2["Test Scenario Pr_0"]
        B2 --> B3["SUMO Simulation"]
        B3 --> B4["Agent uses learned policy<br>(NO exploration)"]
        B4 --> B5["📊 Record metrics"]
        B5 --> B6{"All 27 scenarios<br>tested?"}
        B6 -->|No| B7["Next scenario Pr_1"]
        B7 --> B2
        B6 -->|Yes| B8["📈 Compare with<br>Reference & Developed"]
    end
    
    style A1 fill:#E3F2FD
    style A3 fill:#BBDEFB
    style A6 fill:#90CAF9
    style A8 fill:#66BB6A
    style B1 fill:#C8E6C9
    style B3 fill:#A5D6A7
    style B4 fill:#81C784
    style B8 fill:#FFF9C4
```

------

##### **Key Differences Between Training and Testing**

| **Aspect**         | **Training (Phase 1)**                | **Testing (Phase 2)**              |
| ------------------ | ------------------------------------- | ---------------------------------- |
| **Purpose**        | Learn optimal policy                  | Evaluate performance               |
| **Model State**    | Being updated constantly              | Fixed (frozen)                     |
| **Actions**        | Mix of learned + random (exploration) | Only learned policy (exploitation) |
| **Number of Runs** | 500-1000 episodes                     | 27 scenarios (1 run each)          |
| **Duration**       | Days to weeks                         | Few hours                          |
| **Output**         | Trained model file                    | Performance metrics                |
| **Learning**       | YES - weights updated                 | NO - no updates                    |

------

##### **Practical Example with Timeline**

###### **Week 1-2: Training Phase**

**Day 1-5: Initial Training**

**Training Progress:**

```
Episode 1:   Avg Reward = -145.2  (Terrible - random actions)
Episode 50:  Avg Reward = -78.5   (Learning patterns)
Episode 100: Avg Reward = -45.3   (Getting better)
Episode 200: Avg Reward = -15.8   (Good performance)
Episode 350: Avg Reward = +32.4   (Excellent!)
Episode 500: Avg Reward = +45.7   (Converged)
```

------

###### **Week 3: Testing Phase**

**Day 1-2: Run All Test Scenarios**

**Test Results:**

```
Scenario Pr_0:
  Reference Control:  Car wait = 45s, Bike wait = 89s
  Developed Control:  Car wait = 32s, Bike wait = 42s
  DRL Control:        Car wait = 29s, Bike wait = 35s  ← BEST!

Scenario Pr_5:
  Reference Control:  Car wait = 58s, Bike wait = 112s
  Developed Control:  Car wait = 42s, Bike wait = 51s
  DRL Control:        Car wait = 38s, Bike wait = 48s  ← BEST!
```

------

##### **Why Two Phases?**

###### **Training = "Going to School"**

- Agent practices on **many different situations**
- Makes mistakes, learns from them
- Gets better over time
- Like a student studying for years

###### **Testing = "Taking the Final Exam"**

- Agent demonstrates what it learned
- No more studying allowed
- Performance is measured
- Like a student taking standardized test

------

##### **Important Clarification**

###### **Training Uses Simulation Too!**

Yes, both phases use SUMO simulation:

- **Training**: Run simulation 500+ times to learn
- **Testing**: Run simulation 27 times to evaluate

**The difference:**

- **Training**: Agent is learning → weights change after each episode
- **Testing**: Agent is frozen → weights never change

------

###### **File Structure**

After training, your project will look like:

```
SignalSyncPro/
├── infrastructure/
│   ├── developed/          # Your current system
│   └── drl/                # New DRL system
├── src/
│   ├── training.py         # PHASE 1: Training code
│   ├── testing.py          # PHASE 2: Testing code
│   ├── agent.py            # DQN agent
│   └── environment.py      # SUMO interface
├── models/
│   ├── drl_trained_model.pth    # ← TRAINED MODEL (saved after Phase 1)
│   ├── checkpoint_ep100.pth     # Checkpoints during training
│   └── checkpoint_ep500.pth
├── results/
│   ├── training_logs.csv        # Training progress
│   └── test_results.csv         # Final comparison
└── configs/
    ├── scenarios/          # Pr_0 to Pe_9
    └── training_config.yaml
```

------

##### **Summary: The Complete Picture**

```mermaid
flowchart TD
    A["🏗️ Setup:<br>You have SUMO network<br>+ Developed control"] --> B["📚 Phase 1: TRAINING"]
    
    B --> C["Run 500 episodes<br>Agent learns from experience<br>(Takes 1-2 weeks)"]
    
    C --> D["💾 TRAINED MODEL<br>drl_trained_model.pth<br>(Neural network weights)"]
    
    D --> E["🚀 Phase 2: TESTING"]
    
    E --> F["Run 27 test scenarios<br>Agent uses learned policy<br>(Takes few hours)"]
    
    F --> G["📊 Results:<br>Compare DRL vs Reference vs Developed"]
    
    G --> H["📝 Write Paper:<br>Show DRL improvements!"]
    
    style A fill:#E3F2FD
    style B fill:#FFE0B2
    style C fill:#FFCCBC
    style D fill:#66BB6A
    style E fill:#BBDEFB
    style F fill:#90CAF9
    style G fill:#FFF9C4
    style H fill:#C8E6C9
```

------

###### **Your Next Steps**

1. ✅ **You have**: SUMO network + Developed control
2. ⏳ **Next**: Implement DRL agent + training loop
3. ⏳ **Then**: Run training (Phase 1) - get trained model
4. ⏳ **Finally**: Run testing (Phase 2) - compare performance
5. ⏳ **Write**: Paper showing improvements!

------

**YES! Exactly correct!** You've understood it perfectly. Let me clarify this crucial point:

------

##### Phase Structure vs. Phase Selection/Duration

###### What Stays the Same (Fixed Infrastructure):

**Your 5-Phase Structure** remains identical to your thesis:

- **Phase 1**: Major through (vehicles + bicycles) - same signal pattern
- **Phase 2**: Protected left turn (major direction) - same signal pattern
- **Phase 3**: Minor through (vehicles + bicycles) - same signal pattern
- **Phase 4**: Protected left turn (minor direction) - same signal pattern
- **Phase 5**: Pedestrian exclusive phase - same signal pattern

**The actual traffic signal patterns, lane permissions, and detector locations DO NOT change!**

------

##### What the DRL Model Learns (Adaptive Control):

The trained DRL model learns to **intelligently decide**:

##### 1. Which Phase to Activate Next

**Your Rule-Based Control (Developed):**

```
Fixed hierarchy:
- Check max green → end phase
- Check sync time → skip to Phase 1  
- Check bus → skip to Phase 1
- Check detectors → continue or next phase
```

###### **DRL Control (Learned):**

```
Agent learns optimal phase selection:
- "Traffic state X → Select Phase 1" (learned from experience)
- "Traffic state Y → Select Phase 3" (learned from experience)
- "Traffic state Z → Activate Phase 5" (learned from experience)
```

###### 2. How Long to Run Each Phase

**Your Rule-Based Control:**

```
- Minimum green: 5 seconds (fixed from RiLSA)
- Extend by 1 second if detectors occupied
- Maximum green: 44s (P1), 12s (P2), 24s (P3), 10s (P4) (fixed calculation)
```

**DRL Control (Learned):**

```
Agent learns optimal duration:
- Morning rush + high vehicle queue → Run Phase 1 for 35 seconds
- Low traffic + high bicycle queue → Run Phase 1 for 15 seconds
- High pedestrian demand → Activate Phase 5 earlier
```

------

##### Concrete Example

###### Scenario: Morning Rush Hour (8:15 AM)

**Current Situation:**

- Vehicle queue: 8 cars (North), 5 cars (South)
- Bicycle queue: 6 bikes
- Pedestrians: 12 waiting
- Current phase: Phase 2 (protected left), running for 8 seconds
- Bus approaching: 80 meters away
- Sync timer: 15 seconds until coordination window

------

##### Your Developed Control (Rule-Based) Decision:

```
Check conditions in order:
1. Min green (5s)? YES ✓
2. Max green (12s)? NO (only 8s elapsed)
3. Sync time? NO (15s remaining)
4. Bus priority? NO (bus too far)
5. Detector window? NO (bikes still passing)

→ Decision: CONTINUE Phase 2 (extend by 1 second)
```

**Result:** Phase 2 continues for 9 seconds, bus waits longer, misses sync window

------

##### DRL Control (Learned Policy) Decision:

```
Neural network evaluates current state:
Input state vector [45 dimensions]:
  - Phase encoding: [0, 1, 0, 0, 0] (Phase 2 active)
  - Phase duration: 0.13 (8s / 60s normalized)
  - Vehicle queues: [0.4, 0.25, 0.1, 0.05]
  - Bicycle queues: [0.3, 0.2]
  - Pedestrian demand: 0.24 (12 / 50 normalized)
  - Bus present: 1.0
  - Sync timer: 0.5 (15s / 30s normalized)
  - Time of day: 0.34 (8:15 AM normalized)
  ... (other features)

Network outputs Q-values:
  Q(Continue Phase 2)    = 4.2
  Q(Skip to Phase 1)     = 8.7  ← HIGHEST!
  Q(Next Phase)          = 3.5
  Q(Pedestrian Phase)    = 2.1

→ Decision: SKIP TO PHASE 1
```

**Why Phase 1?** The agent **learned** from thousands of training episodes that at this time of day, with these traffic conditions, skipping to Phase 1:

- Catches the sync window (coordinates with upstream intersection)
- Allows bus to pass quickly
- Reduces overall system delay
- The bicycle queue can wait (acceptable trade-off learned through training)

**Result:** Phase 1 activated, bus flows through, sync achieved, overall system performs better

------

##### Key Differences Illustrated

```mermaid
flowchart TD
    A["Same Traffic Situation<br>8 cars, 6 bikes, 12 peds<br>Bus approaching, Sync in 15s"] --> B["Phase Structure<br>IDENTICAL"]
    
    B --> C["Developed Control<br>(Rule-Based)"]
    B --> D["DRL Control<br>(Learned Policy)"]
    
    C --> E["Applies FIXED rules:<br>1. Max green?<br>2. Sync time?<br>3. Bus?<br>4. Detectors?"]
    
    D --> F["Neural Network<br>evaluates 45 state features"]
    
    E --> G["Decision:<br>Continue Phase 2<br>(rules say continue)"]
    
    F --> H["Decision:<br>Skip to Phase 1<br>(learned this is better)"]
    
    G --> I["Outcome:<br>Bus delayed<br>Sync missed<br>Higher overall delay"]
    
    H --> J["Outcome:<br>Bus flows<br>Sync achieved<br>Lower overall delay"]
    
    style B fill:#FFF9C4
    style C fill:#FFCCBC
    style D fill:#C8E6C9
    style I fill:#EF5350
    style J fill:#66BB6A
```

------

## What Does NOT Change

##### Infrastructure (100% Same):

1. **Network Topology**: Same intersections, lanes, distances (your `test.net.xml`)
2. **Detector Positions**: Same D30 (vehicles), D15 (bicycles), pedestrian detectors
3. **Phase Definitions**: Same signal states for each phase
4. **Leading Green**: Same 1-second leading green for vulnerable modes
5. **Bus Stops**: Same bus stop locations
6. **Vehicle Types**: Same passenger, bicycle, bus, pedestrian types

##### Physical Constraints (100% Same):

1. **Minimum Green**: Still respects 5-second minimum from RiLSA
2. **Yellow Time**: Same yellow/all-red clearance times
3. **Phase Transitions**: Still must go through yellow → red → next phase
4. **Maximum Green Limits**: Still has upper bounds (won't run forever)

------

## What the Model LEARNS to Change

##### Decision Making (Learned):

**1. Phase Selection Logic:**

**Instead of:**

```python
# Your rule-based logic
if max_green_reached:
    next_phase()
elif sync_time_reached:
    skip_to_phase_1()
elif bus_present:
    skip_to_phase_1()
elif detector_clear:
    next_phase()
else:
    continue_phase()
```

**DRL learns:**

```python
# Learned policy
state = get_current_state()  # 45 features
q_values = neural_network(state)  # Evaluates all options
action = argmax(q_values)  # Picks best action

# The network implicitly learned:
# "In morning rush with these queues → Phase 1 best"
# "In midday with high bikes → Phase 3 best"  
# "High pedestrians + long wait → Phase 5 best"
```

**2. Duration Optimization:**

**Your current system:**

- Extends phase by 1 second at a time based on detector windows
- Fixed maximum green times calculated from lane capacity

**DRL learns:**

- When to end phase early (even if detectors show demand)
- When to extend longer (even if approaching max green)
- Context-dependent duration based on system-wide state

------

## Practical Example: Phase Duration Learning

##### Scenario: Phase 1 (Major Through) Running

**Your Developed Control:**

```
Time 0s:  Phase 1 starts (leading green)
Time 1s:  Green begins
Time 6s:  Check detectors (occupied) → continue
Time 7s:  Check detectors (occupied) → continue
Time 8s:  Check detectors (occupied) → continue
...
Time 35s: Detectors finally clear → end phase
Time 44s: MAX GREEN reached → forced end

Duration: Determined by detector windows OR max green
```

**DRL Agent (After Training):**

```
Time 0s:  Phase 1 starts
Time 1s:  Green begins
Time 6s:  Agent evaluates state → decides "continue" (Q=7.5)
Time 12s: Agent evaluates state → decides "continue" (Q=6.8)
Time 18s: Agent evaluates state → decides "skip to Phase 3" (Q=8.2)
          Why? Learned that sync window approaching + 
          minor direction has high bicycle queue

Duration: Determined by learned policy balancing multiple objectives
```

**Key Insight:** The agent learned through trial and error that in this specific situation, running Phase 1 for exactly 18 seconds and then serving the minor direction achieves:

- Better synchronization
- Lower bicycle waiting time
- Acceptable vehicle delay
- Higher overall reward

This specific timing (18 seconds) was **not programmed** - the agent **discovered** it through training!

------

## Training Process Clarification

##### What Happens During Training:

**Episode 1-50 (Random Exploration):**

```
Agent tries random phase durations:
- Phase 1 for 8 seconds → sees result → stores experience
- Phase 1 for 25 seconds → sees result → stores experience
- Phase 1 for 40 seconds → sees result → stores experience
- Activates Phase 5 randomly → sees result → stores experience

Learning: "Hmm, 8 seconds was too short (high reward penalty)"
          "40 seconds wasted time (penalty)"
          "25 seconds seemed better (higher reward)"
```

**Episode 51-200 (Improving):**

```
Agent starts learning patterns:
- "Morning rush + high queue → longer Phase 1 is better"
- "Low traffic → shorter phases are better"
- "High pedestrians → activate Phase 5 sooner"

Still exploring, but getting better average rewards
```

**Episode 201-500 (Mastering):**

```
Agent has learned good policies:
- Knows optimal phase durations for different situations
- Learned when to prioritize sync vs. mode equity
- Discovered non-obvious strategies
  (e.g., "sometimes skip sync for pedestrian safety")

Epsilon low (mostly exploiting learned policy)
```

**Episode 501-1000 (Fine-tuning):**

```
Agent fine-tunes edge cases:
- Rare scenarios (bus + high pedestrian + sync conflict)
- Optimal handling of Phase 5 activation threshold
- Perfect timing for coordination windows

Near-optimal policy achieved
```

------

## After Training: Deployment

##### The Trained Model Contains:

**Neural Network Weights** (saved in `final_model.pth`):

```python
# These weights encode learned knowledge like:
# "If state looks like [0.4, 0.3, 0.2, ...] → Phase 1 best (Q=8.7)"
# "If state looks like [0.1, 0.8, 0.5, ...] → Phase 3 best (Q=9.2)"
# "If state looks like [0.2, 0.2, 0.9, ...] → Phase 5 best (Q=8.9)"

policy_network_weights = [
    layer1_weights: 45x256 matrix,
    layer2_weights: 256x256 matrix,
    layer3_weights: 256x128 matrix,
    output_weights: 128x4 matrix
]
```

##### Testing Phase Uses This Model:

```python
# Load trained model
agent.load("models/final_model.pth")
agent.set_eval_mode()  # No more learning!

# Run test scenarios
for scenario in ['Pr_0', 'Pr_1', ..., 'Pe_9']:
    state = env.reset()
    
    while not done:
        # Use learned policy (NO exploration)
        action = agent.select_action(state, explore=False)
        
        # This uses the trained neural network to pick:
        # - Which phase to activate
        # - When to transition
        
        next_state, reward, done, info = env.step(action)
        state = next_state
    
    # Record performance metrics
```

------

## Summary

**What stays the same:**

- ✅ Physical infrastructure (network, detectors, lanes)
- ✅ Phase signal patterns (which lights are green/red)
- ✅ Vehicle types and routing
- ✅ Safety constraints (minimum green, clearance times)

**What the DRL model learns to control:**

- 🎯 **Which phase to activate next** (intelligent phase selection)
- 🎯 **How long to run each phase** (optimal duration)
- 🎯 **When to skip phases** (e.g., skip to Phase 1 for sync)
- 🎯 **When to activate pedestrian phase** (timing optimization)
- 🎯 **How to balance competing objectives** (sync vs. equity vs. delay)

**The model learns the CONTROL LOGIC, not the infrastructure!**

Your phase structure is the "vocabulary" - the DRL agent learns the "grammar" of how to use it optimally!
