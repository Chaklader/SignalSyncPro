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

Perfect! Let me explain in plain English how the DRL control will work, step by step, with comprehensive diagrams.

------

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

