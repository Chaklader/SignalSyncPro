# Isolated Control Logic Without Semi-Synchronization (5-TLS Multi-Agent Network)

This section describes the **isolated actuated control** for the 5-intersection multi-agent network. Each intersection
operates **independently** based solely on its local detector readings—no coordination or synchronization between
intersections.

###### Key Differences from Semi-Synchronized Control

| Feature             | Isolated (5-TLS Network)          |
| ------------------- | --------------------------------- |
| **Coordination**    | None - fully independent          |
| **Phase Structure** | P1→P2→P3→P4→P1                    |
| **Actuation Logic** | Cars gap-out AND Bicycles gap-out |
| **Bus Skip to P1**  | Always WITH leading green         |
| **Priority Levels** | 3 tiers (MAX→Bus→Actuation)       |

###### Bus Signal Detection (Background Process)

When a bus enters the signal emit lane (64s-72s from TLS), the controller stores $\text{bus\_detected\_time}$ and sets
$\text{bus\_approaching} = True$. The controller then waits until $(\text{travel\_time} - 15s)$ has elapsed before
emitting $\text{bus\_priority\_active} = True$, ensuring the bus is exactly 15s away when the signal priority is
activated. This 15s warning guarantees sufficient time to either hold P1 (if G < 30s) or cycle through P2 (if G ≥ 30s),
ensuring zero bus delay in all scenarios.

###### Green Actuation Logic: Isolated Control Decision Hierarchy

```mermaid
flowchart TD

    GreenStart["GREEN PHASE ACTIVE<br>Increment green_steps counter"] --> MinGreenCheck{"green_steps ≥<br>MIN_GREEN?"}

    MinGreenCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Continue0["Continue Current Phase<br>(Safety: Must serve minimum)"]

    MinGreenCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Priority1{"PRIORITY 1:<br>Max Green Reached?<br>green_steps = MAX_GREEN?"}

    Priority1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Action1["TERMINATE PHASE<br>P1→P2→P3→P4→P1"]

    Priority1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Priority2a{"PRIORITY 2a:<br>bus_priority_active?<br>(THIS TLS only - isolated)"}

    Priority2a -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Priority2b{"PRIORITY 2b:<br>Current Phase?"}

    Priority2b -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P2, P3, or P4</span>| Action2["SKIP TO PHASE 1<br>Set skipStartingPhase flag<br>Set busArrival = True"]

    Priority2b -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P1, G < 30s</span>| ContinueP1["HOLD Phase 1<br>(Bus arrives at G+15s ≤ 44s)"]

    Priority2b -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P1, G ≥ 30s</span>| CycleP1["CYCLE via P2<br>(15s to new P1)"]

    Priority2a -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Priority3{"PRIORITY 3:<br>Actuation Logic<br>Vehicle detectors gap-out (>3s)<br>AND Bicycle detectors gap-out (>3s)?"}

    Priority3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Action3["TERMINATE PHASE<br>Gap-out detected<br>Ensure flow<br>P1→P2→P3→P4→P1"]

    Priority3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Continue2["Continue Current Phase<br>(Vehicles OR Bicycles<br>still approaching)"]

    style GreenStart fill:#E3F2FD
    style MinGreenCheck fill:#BBDEFB
    style Priority1 fill:#EF5350
    style Priority2a fill:#FFA726
    style Priority2b fill:#FFB74D
    style Priority3 fill:#FFCA28
    style Action1 fill:#66BB6A
    style Action2 fill:#9CCC65
    style Action3 fill:#AED581
    style ContinueP1 fill:#81C784
    style CycleP1 fill:#9CCC65
    style Continue0 fill:#E0E0E0
    style Continue2 fill:#F5F5F5
```

###### Isolated Control: Complete Phase Transition Flow

```mermaid
flowchart TD
    subgraph P1_PHASE["PHASE 1: Major Through"]
        P1_LG["Leading Green"] --> P1_Green["P1 GREEN"]
        P1_Green --> P1_Min{"green_steps ≥ MIN_GREEN?"}
        P1_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Green
        P1_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P1_Pr1{"Priority 1:<br>MAX_GREEN?"}
        P1_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P1_Term["Terminate P1"]
        P1_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Pr2{"Priority 2:<br>bus_priority_active?"}
        P1_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes, G < 30s</span>| P1_Hold["Hold P1 for bus<br>(G+15s ≤ 44s)"]
        P1_Hold --> P1_Green
        P1_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes, G ≥ 30s</span>| P1_Cycle["Cycle via P2<br>(15s to new P1)"]
        P1_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Pr3{"Priority 3:<br>Both Cars and Bicycles Gap-out?"}
        P1_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P1_Term
        P1_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Green
    end

    P1_Term --> Y1["YELLOW"] --> R1["RED"]
    P1_Cycle --> Y1
    R1 --> P2_LG

    subgraph P2_PHASE["PHASE 2: Major Left"]
        P2_LG["Leading Green"] --> P2_Green["P2 GREEN"]
        P2_Green --> P2_Min{"green_steps ≥ MIN_GREEN?"}
        P2_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P2_Green
        P2_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P2_Pr1{"Priority 1:<br>MAX_GREEN?"}
        P2_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P2_Term["Terminate P2"]
        P2_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P2_Pr2{"Priority 2:<br>bus_priority_active?"}
        P2_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P2_Skip["Skip to P1"]
        P2_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P2_Pr3{"Priority 3:<br>Both Cars and Bicycles Gap-out?"}
        P2_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P2_Term
        P2_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P2_Green
    end

    P2_Term --> Y2["YELLOW"] --> R2["RED"]
    P2_Skip --> Y2S["YELLOW"] --> R2S["RED"] --> P1_LG
    R2 --> P3_LG

    subgraph P3_PHASE["PHASE 3: Minor Through"]
        P3_LG["Leading Green"] --> P3_Green["P3 GREEN"]
        P3_Green --> P3_Min{"green_steps ≥ MIN_GREEN?"}
        P3_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P3_Green
        P3_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P3_Pr1{"Priority 1:<br>MAX_GREEN?"}
        P3_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P3_Term["Terminate P3"]
        P3_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P3_Pr2{"Priority 2:<br>bus_priority_active?"}
        P3_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P3_Skip["Skip to P1"]
        P3_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P3_Pr3{"Priority 3:<br>Both Cars and Bicycles Gap-out?"}
        P3_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P3_Term
        P3_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P3_Green
    end

    P3_Term --> Y3["YELLOW"] --> R3["RED"]
    P3_Skip --> Y3S["YELLOW"] --> R3S["RED"] --> P1_LG
    R3 --> P4_LG

    subgraph P4_PHASE["PHASE 4: Minor Left"]
        P4_LG["Leading Green"] --> P4_Green["P4 GREEN"]
        P4_Green --> P4_Min{"green_steps ≥ MIN_GREEN?"}
        P4_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P4_Green
        P4_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P4_Pr1{"Priority 1:<br>MAX_GREEN?"}
        P4_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P4_Term["Terminate P4"]
        P4_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P4_Pr2{"Priority 2:<br>bus_priority_active?"}
        P4_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P4_Skip["Skip to P1"]
        P4_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P4_Pr3{"Priority 3:<br>Both Cars and Bicycles Gap-out?"}
        P4_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P4_Term
        P4_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P4_Green
    end

    P4_Term --> Y4["YELLOW"] --> R4["RED"] --> P1_LG
    P4_Skip --> Y4S["YELLOW"] --> R4S["RED"] --> P1_LG

    style P1_PHASE fill:#E3F2FD
    style P2_PHASE fill:#BBDEFB
    style P3_PHASE fill:#90CAF9
    style P4_PHASE fill:#64B5F6
    style Y1 fill:#FDD835
    style Y2 fill:#FDD835
    style Y3 fill:#FDD835
    style Y4 fill:#FDD835
    style Y2S fill:#FDD835
    style Y3S fill:#FDD835
    style Y4S fill:#FDD835
    style R1 fill:#EF5350
    style R2 fill:#EF5350
    style R3 fill:#EF5350
    style R4 fill:#EF5350
    style R2S fill:#EF5350
    style R3S fill:#EF5350
    style R4S fill:#EF5350
```

###### Isolated Control: Simplified Phase Transition Flow

```mermaid
flowchart TD
    subgraph P1_PHASE["PHASE 1: Major Through (Bus Priority: HOLD or CYCLE)"]
        P1_LG["Leading Green"] --> P1_Green["P1 GREEN"]
        P1_Green --> P1_Min{"green_steps ≥ MIN_GREEN?"}
        P1_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Green
        P1_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P1_Pr1{"Priority 1:<br>MAX_GREEN?"}
        P1_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P1_Term["Terminate P1"]
        P1_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Pr2{"Priority 2:<br>bus_priority_active?"}
        P1_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes, G < 30s</span>| P1_Hold["Hold P1 for bus<br>(G+15s ≤ 44s)"]
        P1_Hold --> P1_Green
        P1_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes, G ≥ 30s</span>| P1_Cycle["Cycle via P2"]
        P1_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Pr3{"Priority 3:<br>Both Cars and Bicycles Gap-out?"}
        P1_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P1_Term
        P1_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Green
    end

    P1_Term --> Y1["YELLOW"] --> R1["RED"]
    P1_Cycle --> Y1
    R1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P1→P2 ALWAYS</span>| Px_LG

    subgraph Px_PHASE["PHASE 2/3/4 (Bus Priority: SKIP TO P1)"]
        Px_LG["Leading Green"] --> Px_Green["Px GREEN"]
        Px_Green --> Px_Min{"green_steps ≥ MIN_GREEN?"}
        Px_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Px_Green
        Px_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Px_Pr1{"Priority 1:<br>MAX_GREEN?"}
        Px_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Px_Term["Terminate Px"]
        Px_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Px_Pr2{"Priority 2:<br>bus_priority_active?"}
        Px_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Px_Skip["Skip to P1"]
        Px_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Px_Pr3{"Priority 3:<br>Both Cars and Bicycles Gap-out?"}
        Px_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Px_Term
        Px_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Px_Green
    end

    Px_Term --> Yx["YELLOW"] --> Rx["RED"]
    Px_Skip --> Yx
    Rx -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P2→P3, P3→P4</span>| Px_LG
    Rx -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P4→P1, Skip to P1</span>| P1_LG

    style P1_PHASE fill:#E3F2FD
    style Px_PHASE fill:#90CAF9
    style Y1 fill:#FDD835
    style Yx fill:#FDD835
    style R1 fill:#EF5350
    style Rx fill:#EF5350
```

###### Key Characteristics of Isolated Control

1. **Fully Independent**: Each TLS makes decisions based only on its local detectors
2. **No Coordination Overhead**: No sync timers or inter-TLS communication
3. **AND Actuation Logic**: Both cars AND bicycles must gap-out before phase termination
4. **No Pedestrian Phase**: 4-phase cycle only (P1→P2→P3→P4→P1)
5. **Bus Priority with 15s Warning**: Hold P1 (G < 30s) or cycle via P2 (G ≥ 30s) for zero bus delay
6. **Circular Flow Guaranteed**: MAX_GREEN always triggers next phase in sequence

---

###### Time Duration Analysis: Switching to P1 from Any Point in Cycle

This analysis calculates the minimum time required to reach Phase 1 (P1) from any point in the traffic signal cycle,
considering bus priority coordination requirements.

###### Constraints and Fixed Parameters

| Parameter           | Value | Purpose                                              |
| ------------------- | ----- | ---------------------------------------------------- |
| **Leading Green**   | 1s    | Bicycle priority start before main green             |
| **Yellow**          | 3s    | Warning interval (fixed, safety requirement)         |
| **Red Clearance**   | 2s    | Intersection clearance (fixed, safety requirement)   |
| **Transition Time** | 6s    | Yellow + Red per phase change (3s + 2s + 1s leading) |

**Critical Rule**: Cannot skip from P1 directly back to P1. Must pass through at least P2 before returning to P1.

###### Phase Timing Reference

| Phase              | MIN_GREEN | MAX_GREEN |
| ------------------ | --------- | --------- |
| P1 (Major Through) | 8s        | 44s       |
| P2 (Major Left)    | 3s        | 15s       |
| P3 (Minor Through) | 5s        | 24s       |
| P4 (Minor Left)    | 2s        | 12s       |

##### Case Analysis: Time to Reach P1

###### From P1 (Can HOLD - No Switching Needed)

If bus priority signal arrives while already at P1, the controller simply **holds P1 green** until bus passes. No
"switching to P1" is required since we're already there.

**Key constraint**: P1 green time G must satisfy: G + extension ≤ MAX_GREEN (44s)

**Case 1a: P1 green time G < 30s (Can extend)**

```
Bus signal arrives: Bus is 15s away
Current P1 green: G seconds (where G < 30s)
────────────────────────────────────────────
Action: HOLD P1 green
Bus arrives at: G + 15s (≤ 44s) ✓
No phase transition needed.
```

**Case 1b: P1 green time G ≥ 30s (Cannot extend, must cycle)**

```
Bus signal arrives: Bus is 15s away
Current P1 green: G seconds (where G ≥ 30s)
G + 15s > 44s (exceeds MAX_GREEN)
────────────────────────────────────────────
Action: Must cycle through P2 and return to P1

P1 Yellow: 3s
+ P1 Red: 2s
+ P2 Leading Green: 1s
+ P2 MIN_GREEN: 3s
+ P2 Yellow: 3s
+ P2 Red: 2s
+ P1 Leading Green: 1s
────────────────────────
Total: 15 seconds (via P2)
```

##### From P2 (Can skip to P1)

###### **Case 2a: At start of P2 MIN_GREEN**

```
P2 MIN_GREEN remaining: 3s
+ P2 Yellow: 3s
+ P2 Red: 2s
+ P1 Leading Green: 1s
────────────────────────
Total: 9 seconds
```

###### **Case 2b: In P2 actuation period (MIN served, can terminate)**

```
P2 Yellow: 3s
+ P2 Red: 2s
+ P1 Leading Green: 1s
────────────────────────
Total: 6 seconds
```

##### From P3 (Can skip to P1)

###### **Case 3a: At start of P3 MIN_GREEN**

```
P3 MIN_GREEN remaining: 5s
+ P3 Yellow: 3s
+ P3 Red: 2s
+ P1 Leading Green: 1s
────────────────────────
Total: 11 seconds
```

###### **Case 3b: In P3 actuation period (MIN served, can terminate)**

```
P3 Yellow: 3s
+ P3 Red: 2s
+ P1 Leading Green: 1s
────────────────────────
Total: 6 seconds
```

##### From P4 (Can skip to P1)

###### **Case 4a: At start of P4 MIN_GREEN**

```
P4 MIN_GREEN remaining: 2s
+ P4 Yellow: 3s
+ P4 Red: 2s
+ P1 Leading Green: 1s
────────────────────────
Total: 8 seconds
```

###### **Case 4b: In P4 actuation period (MIN served, can terminate)**

```
P4 Yellow: 3s
+ P4 Red: 2s
+ P1 Leading Green: 1s
────────────────────────
Total: 6 seconds
```

##### Summary Table

| Current Phase | At P1 G < 30s | P1 Duration When Bus Arrived | Bus Delay | At P1 G ≥ 30s | P1 Duration When Bus Arrived | Bus Delay | At Start of MIN_GREEN | P1 Duration When Bus Arrived | Bus Delay | In Actuation Period | P1 Duration When Bus Arrived | Bus Delay |
| ------------- | ------------- | ---------------------------- | --------- | ------------- | ---------------------------- | --------- | --------------------- | ---------------------------- | --------- | ------------------- | ---------------------------- | --------- |
| **P1**        | Hold (0s)     | G+15s                        | 0s        | 15s (via P2)  | 0                            | 0s        | -                     |                              |           | -                   |                              |           |
| **P2**        | -             |                              |           | -             |                              |           | 9s                    | 6s (15-9)                    | 0s        | 6s                  | 9s (15-6)                    | 0s        |
| **P3**        | -             |                              |           | -             |                              |           | 11s                   | 4s (15-11)                   | 0s        | 6s                  | 9s (15-6)                    | 0s        |
| **P4**        | -             |                              |           | -             |                              |           | 8s                    | 7s (15-8)                    | 0s        | 6s                  | 9s (15-6)                    | 0s        |

##### Worst Case Analysis

**Worst Case: 15 seconds**

Two scenarios lead to 15s delay:

1. At P1 with G ≥ 30s → must cycle through P2 (15s)
2. At P3 start of MIN_GREEN → skip to P1 (11s) - still under 15s

**Best Case: 0 seconds (Hold)**

- Occurs when already at P1 with G < 30s
- Simply hold P1 green, no transition needed

**Transition Best Case: 6 seconds**

- Occurs when in actuation period of P2, P3, or P4
- Only requires: Yellow (3s) → Red (2s) → P1 Leading (1s)

##### Implication for Bus Coordination: 15s Warning Window

**Why 15s is the optimal warning time:**

The 15s warning window enables both **P1 extension** (when possible) and **P2 cycling** (when necessary), while
supporting bi-directional bus coordination.

**Key constraint**: G + 15s ≤ 44s → G ≤ 29s for extension

###### Bi-Directional Coordination Scenario

**Scenario A: Bus arrives early in P1 (G=0)**

```
P1 green time: G = 0s
Bus A signal arrives: Bus is 15s away
────────────────────────────────────────
Action: Hold P1 green
Bus A arrives at G = 15s

Then Bus B from opposite direction signals (15s away)
────────────────────────────────────────
Action: Continue holding P1
Bus B arrives at G = 30s
Total P1 green: 30s (< 44s MAX_GREEN) ✓
```

**Scenario B: Bus arrives late in P1 (G=30s)**

```
P1 green time: G = 30s
Bus signal arrives: Bus is 15s away
G + 15s = 45s > 44s (exceeds MAX_GREEN)
────────────────────────────────────────
Action: Must cycle through P2 (15s)
Bus arrives exactly when new P1 starts ✓
```

###### Controller Check Point: G = 29s

At P1 green time G = 29s, controller checks:

- **If bus within 15s window**: Extend P1 (bus arrives at G ≤ 44s)
- **If no bus signal**: Continue normal actuation

This ensures the controller can decide whether to extend or cycle before hitting the critical threshold.

###### Confirmation: 15s Warning Guarantees Green for All Cases

| Current State   | Bus Signal Action | Time to P1 Green   | P1 Duration at Arrival | Bus Delay |
| --------------- | ----------------- | ------------------ | ---------------------- | --------- |
| P1, G < 30s     | Hold P1           | 0s (already green) | G + 15s                | 0s        |
| P1, G ≥ 30s     | Cycle via P2      | 15s                | 0s (new P1)            | 0s        |
| P2 at MIN start | Skip to P1        | 9s                 | 6s                     | 0s        |
| P2 actuation    | Skip to P1        | 6s                 | 9s                     | 0s        |
| P3 at MIN start | Skip to P1        | 11s                | 4s                     | 0s        |
| P3 actuation    | Skip to P1        | 6s                 | 9s                     | 0s        |
| P4 at MIN start | Skip to P1        | 8s                 | 7s                     | 0s        |
| P4 actuation    | Skip to P1        | 6s                 | 9s                     | 0s        |

**Key Result**: With a 15s warning window, **all scenarios achieve 0s bus delay**. The bus always arrives when P1 green
is active.

###### Why 15s is the Optimal Warning Time

With 64-72s warning from emission lanes, we could use a longer window. However, 15s is optimal because:

1. **Guaranteed zero delay**: 15s covers worst-case transition (P1→P2→P1 = 15s)
2. **Bi-directional support**: Two consecutive buses (15s + 15s = 30s) fit within MAX_GREEN (44s)
3. **Fairness to other phases**: Limits P1 extension to reasonable duration
4. **Simple decision rule**: Check at G = 29s whether to extend or cycle

**Conclusion**: A 15s warning window enables:

1. **P1 extension** when G < 30s (most common case)
2. **P2 cycling** when G ≥ 30s (fallback)
3. **Bi-directional coordination** within MAX_GREEN limits
4. **Zero bus delay** in all scenarios

---

##### Isolated Actuated Control Mechanism

The isolated actuated control implements a three-tier priority hierarchy operating at each intersection independently,
without inter-signal coordination. This design prioritizes local responsiveness while maintaining safety constraints and
providing bus priority service.

###### Control Architecture

The controller evaluates phase termination decisions every simulation step (1 second) during the green phase, following
a strict priority order:

**Priority 1 - Maximum Green Enforcement**: The highest priority ensures no phase exceeds its maximum green time
(MAX_GREEN). When green duration reaches MAX_GREEN, the phase terminates unconditionally, guaranteeing fairness across
all traffic movements and preventing indefinite phase extension.

**Priority 2 - Bus Priority**: When a bus is detected in the emission lane (providing 64-72 seconds advance warning),
the controller activates bus priority mode. The response depends on current phase:

- **If at Phase 1 (Major Through)**: Hold green until bus clears the intersection
- **If at Phase 2, 3, or 4**: Skip remaining phases and transition to Phase 1 via yellow-red sequence

**Priority 3 - Gap-Out Actuation**: In the absence of higher-priority conditions, phase termination follows
detector-based actuation logic. A phase terminates when both vehicle detectors AND bicycle detectors indicate gap-out
(no detection for ≥3 seconds), ensuring all approaching traffic clears before phase change.

###### Phase Transition Rules

The control enforces a circular phase sequence: P1 → P2 → P3 → P4 → P1. A critical constraint prevents skipping directly
from P1 back to P1; transitions must pass through at least P2. This ensures minimum service for left-turn movements on
the major street.

Each phase transition follows a fixed sequence:

1. **Yellow interval** (3 seconds): Warning to clear the intersection
2. **All-red clearance** (2 seconds): Safety buffer for intersection clearing
3. **Leading green** (1 second): Bicycle priority start before main vehicle green

###### Bus Priority Implementation

The bus priority mechanism uses a 15-second warning window, calculated as the minimum time required to guarantee green
for an arriving bus from any phase state. This timing enables:

- **Phase 1 extension**: When P1 green duration G < 30s, the controller holds P1 green (G + 15s ≤ 44s MAX_GREEN)
- **Phase cycling**: When G ≥ 30s, the controller cycles through P2 (15 seconds) to start a fresh P1 when the bus
  arrives

The analysis confirms zero bus delay across all scenarios:

| Initial State  | Controller Action | Bus Delay |
| -------------- | ----------------- | --------- |
| At P1, G < 30s | Hold P1 green     | 0 seconds |
| At P1, G ≥ 30s | Cycle via P2      | 0 seconds |
| At P2/P3/P4    | Skip to P1        | 0 seconds |

###### Detector Configuration

The control relies on two detector types positioned upstream of the stop line:

- **Vehicle detectors (D30)**: Located 30 meters upstream, detecting cars and trucks with a 3-second memory window
- **Bicycle detectors (D15)**: Located 15 meters upstream, detecting cyclists with a 3-second memory window

The AND logic for gap-out (both vehicle AND bicycle detectors must indicate no traffic) ensures vulnerable road users
clear the intersection before phase termination.

###### Design Rationale

This isolated control approach offers several advantages for the multi-agent network:

1. **Scalability**: No communication overhead between intersections enables deployment at any network size
2. **Robustness**: Each intersection operates autonomously; failures do not cascade
3. **Responsiveness**: Local detector feedback provides immediate adaptation to traffic conditions
4. **Bus priority**: Guaranteed zero-delay service for transit vehicles without complex coordination
5. **Safety**: Fixed minimum green times, mandatory yellow/red sequences, and bicycle protection

The control serves as the baseline for comparison with DRL-based approaches, representing well-tuned conventional
practice in adaptive signal control.

---

# Isolated Control Logic With Semi-Synchronization (5-TLS Multi-Agent Network)

Your system implements a **four-tier priority hierarchy** that evaluates conditions every second after minimum green
time. The control operates independently at each intersection but includes coordination mechanisms.

###### Green Actuation Logic: The Core Decision Hierarchy

This is where the four-tier priority system operates during the actuated green phase:

```mermaid
flowchart TD
    GreenStart["GREEN PHASE ACTIVE<br>Increment green_steps counter"] --> MinGreenCheck{"green_steps ≥<br>MIN_GREEN?"}

    MinGreenCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Continue0["Continue Current Phase<br>(Safety: Must serve minimum)"]

    MinGreenCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Priority1{"PRIORITY 1:<br>Max Green Reached?<br>green_steps = MAX_GREEN?"}

    Priority1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Action1["TERMINATE PHASE<br>P1→P2→P3→P4→P1"]

    Priority1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Priority2a{"PRIORITY 2a:<br>Sync Timer Expired?<br>step ≥ syncTime?"}

    Priority2a -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Priority2b{"PRIORITY 2b:<br>Current Phase?"}

    Priority2b -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P2, P3, or P4</span>| Action2["SKIP TO PHASE 1<br>Set skipStartingPhase flag<br>Set syncValue = True<br>Reset sync timer"]

    Priority2b -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P1</span>| ContinueSync["Reset Sync Timer<br>Continue Phase 1<br>(Already synchronized)"]

    Priority2a -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Priority3a{"PRIORITY 3a:<br>bus_priority_active?"}

    Priority3a -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Priority3b{"PRIORITY 3b:<br>Current Phase?"}

    Priority3b -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P2, P3, or P4</span>| Action3["SKIP TO PHASE 1<br>Set skipStartingPhase flag<br>Set busArrival = True"]

    Priority3b -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P1</span>| ContinueP1["Continue Phase 1<br>(Hold green for bus arrival)"]

    Priority3a -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Priority4{"PRIORITY 4:<br>Actuation Logic<br>Vehicle detectors gap-out (>3s)<br>AND Bicycle detectors gap-out (>3s)?"}

    Priority4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Action4["TERMINATE PHASE<br>Gap-out detected<br>P1→P2→P3→P4→P1"]

    Priority4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Continue2["Continue Current Phase<br>(Vehicles OR Bicycles<br>still approaching)"]

    style GreenStart fill:#E3F2FD
    style MinGreenCheck fill:#BBDEFB
    style Priority1 fill:#EF5350
    style Priority2a fill:#FF7043
    style Priority2b fill:#FF8A65
    style Priority3a fill:#FFA726
    style Priority3b fill:#FFB74D
    style Priority4 fill:#FFCA28
    style Action1 fill:#66BB6A
    style Action2 fill:#81C784
    style Action3 fill:#9CCC65
    style Action4 fill:#AED581
    style ContinueSync fill:#E0E0E0
    style ContinueP1 fill:#EEEEEE
    style Continue0 fill:#E0E0E0
    style Continue2 fill:#F5F5F5
```

##### Synchronization Mechanism

###### Complete Phase Transition Flow (Semi-Sync)

```mermaid
flowchart TD
    subgraph P1_PHASE["PHASE 1: Major Through (Sync: RESET, Bus: HOLD)"]
        P1_LG["Leading Green"] --> P1_Green["P1 GREEN"]
        P1_Green --> P1_Min{"green_steps ≥ MIN_GREEN?"}
        P1_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Green
        P1_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P1_Pr1{"Priority 1:<br>MAX_GREEN?"}
        P1_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P1_Term["Terminate P1"]
        P1_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Pr2{"Priority 2:<br>Sync Timer Expired?"}
        P1_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P1_Sync["Reset Sync Timer<br>Continue P1"]
        P1_Sync --> P1_Green
        P1_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Pr3{"Priority 3:<br>bus_priority_active?"}
        P1_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P1_Hold["Hold P1 for bus"]
        P1_Hold --> P1_Green
        P1_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Pr4{"Priority 4:<br>Both Cars AND Bicycles Gap-out?"}
        P1_Pr4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| P1_Term
        P1_Pr4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| P1_Green
    end

    P1_Term --> Y1["YELLOW"] --> R1["RED"]
    R1 --> Px_LG

    subgraph Px_PHASE["PHASE 2/3/4 (Sync: SKIP, Bus: SKIP TO P1)"]
        Px_LG["Leading Green"] --> Px_Green["Px GREEN"]
        Px_Green --> Px_Min{"green_steps ≥ MIN_GREEN?"}
        Px_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Px_Green
        Px_Min -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Px_Pr1{"Priority 1:<br>MAX_GREEN?"}
        Px_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Px_Term["Terminate Px"]
        Px_Pr1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Px_Pr2{"Priority 2:<br>Sync Timer Expired?"}
        Px_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Px_SyncSkip["Skip to P1<br>(syncValue=True)"]
        Px_Pr2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Px_Pr3{"Priority 3:<br>bus_priority_active?"}
        Px_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Px_BusSkip["Skip to P1<br>(busArrival=True)"]
        Px_Pr3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Px_Pr4{"Priority 4:<br>Both Cars AND Bicycles Gap-out?"}
        Px_Pr4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Px_Term
        Px_Pr4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Px_Green
    end

    Px_Term --> Yx["YELLOW"] --> Rx["RED"]
    Px_SyncSkip --> Yx
    Px_BusSkip --> Yx
    Rx -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P2→P3, P3→P4</span>| Px_LG
    Rx -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P4→P1, Skip to P1</span>| P1_LG

    style P1_PHASE fill:#E3F2FD
    style Px_PHASE fill:#90CAF9
    style Y1 fill:#FDD835
    style Yx fill:#FDD835
    style R1 fill:#EF5350
    style Rx fill:#EF5350
```

###### Key Implementation Details from Code

###### Priority Values and Timing

| Parameter                | Value                               | Purpose                                  |
| ------------------------ | ----------------------------------- | ---------------------------------------- |
| **MIN_GREEN_TIME**       | 5 seconds                           | Safety: Minimum service before decisions |
| **YELLOW_TIME**          | 3 seconds                           | Warning interval before red              |
| **ALL_RED_TIME**         | 2 seconds                           | Clearance interval between phases        |
| **Leading Green**        | 1 second                            | Priority start for bicycles/pedestrians  |
| **Detector Gap-Out**     | 3 seconds (critical delay duration) | No detector activation threshold         |
| **Sync Offset**          | 22 seconds                          | Coordination delay between intersections |
| **Pedestrian Threshold** | ≥12 waiting                         | Triggers exclusive Phase 5               |
| **Phase 5 Duration**     | 15 seconds                          | Fixed pedestrian service time            |

###### Detector Logic

**Vehicle Detectors (D30)**:

- Positioned 30m upstream
- 3-second detection window
- Binary: Occupied if activation within last 3s

**Bicycle Detectors (D15)**:

- Positioned 15m upstream
- 3-second detection window
- Checked AFTER vehicle gap-out
- Provides bicycle protection

**Pedestrian Detectors**:

- Uses SUMO inductionloop API
- Counts pedestrians with speed < 0.1 m/s
- Threshold: ≥12 triggers Phase 5

###### Bus Priority Implementation

- Checks bus presence in specific entry lanes
- Triggers immediate phase skip during P2, P3, P4
- Holds Phase 1 if bus already being served
- Phase skip leads to P1 **without leading green** for buses

##### Summary of Control Philosophy

The code implements a **pragmatic hierarchical control** with these characteristics:

1. **Safety First**: Minimum green and maximum green are hard constraints
2. **Coordination Attempted**: Semi-sync tries 60% success rate through timing
3. **Bus Priority**: Active detection with context-aware skipping
4. **Bicycle Protection**: Two-tier gap-out ensures vulnerable road user service
5. **Pedestrian Accommodation**: Dedicated phase when demand exceeds threshold
6. **Graceful Degradation**: When priority conditions fail, normal actuation takes over

This represents a sophisticated rule-based system that balances multiple competing objectives through careful priority
ordering and detector-based responsiveness—a substantial advancement over simple fixed-time or single-mode actuated
control.

---
