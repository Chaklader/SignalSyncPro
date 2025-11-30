# Controlling Logic: Hierarchical Decision Framework

Your system implements a **four-tier priority hierarchy** that evaluates conditions every second after minimum green
time. The control operates independently at each intersection but includes coordination mechanisms.

###### Overall Control Flow

```mermaid
flowchart TD
    Start["Simulation Step<br>(Every 1 second)"] --> ForEach["For Each Intersection<br>(Node 0, Node 1)"]

    ForEach --> GetPhase["Get Current Phase<br>from Traffic Light"]

    GetPhase --> CheckP1{"Current Phase<br>= Phase 1?"}

    CheckP1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| StartSync["Start Synchronization Timer<br>for Other Intersection<br>(22 seconds)"]

    CheckP1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| PhaseLogic["Execute Phase-Specific Logic"]

    StartSync --> PhaseLogic

    PhaseLogic --> GreenCheck{"Is Phase<br>GREEN?"}
    PhaseLogic --> YellowCheck{"Is Phase<br>YELLOW?"}
    PhaseLogic --> RedCheck{"Is Phase<br>RED?"}

    GreenCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| GreenActuation["Green Actuation Logic<br>(Hierarchical Decision Tree)"]
    YellowCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| YellowActuation["Yellow Actuation Logic<br>(Fixed 3-second timer)"]
    RedCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| RedActuation["Red Actuation Logic<br>(Phase Skip Decision)"]

    GreenActuation --> NextStep["Next Simulation Step"]
    YellowActuation --> NextStep
    RedActuation --> NextStep

    style Start fill:#E3F2FD
    style ForEach fill:#BBDEFB
    style GetPhase fill:#90CAF9
    style CheckP1 fill:#64B5F6
    style StartSync fill:#42A5F5
    style PhaseLogic fill:#2196F3
    style GreenCheck fill:#81C784
    style YellowCheck fill:#AED581
    style RedCheck fill:#C5E1A5
    style GreenActuation fill:#FFB74D
    style YellowActuation fill:#FFA726
    style RedActuation fill:#FF9800
    style NextStep fill:#FB8C00
```

###### Green Actuation Logic: The Core Decision Hierarchy

This is where the four-tier priority system operates during the actuated green phase:

```mermaid
flowchart TD
    GreenStart["GREEN PHASE ACTIVE<br>Increment green_steps counter"] --> MinGreenCheck{"green_steps ≥<br>MIN_GREEN (5s)?"}

    MinGreenCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Continue0["Continue Current Phase<br>(Safety: Must serve minimum)"]

    MinGreenCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Priority1{"PRIORITY 1:<br>Max Green Reached?<br>green_steps = MAX_GREEN?"}

    Priority1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Action1["TERMINATE PHASE<br>Call mainCircularFlow()<br>Advance to next phase"]

    Priority1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Priority2{"PRIORITY 2:<br>Sync Timer Expired?<br>step ≥ syncTime?"}

    Priority2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| CheckPhase2{"Current Phase<br>= Phase 1?"}

    CheckPhase2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Action2A["Reset Sync Timer<br>Continue Phase 1<br>(Already synchronized)"]

    CheckPhase2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Action2B["SKIP TO NEXT PHASE<br>Set skipStartingPhase flag<br>Set syncValue = True<br>Reset sync timer"]

    Priority2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Priority3{"PRIORITY 3:<br>Bus in Entry Lane?<br>(Phases 2, 3, 4 only)"}

    Priority3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Action3["SKIP TO NEXT PHASE<br>Set skipStartingPhase flag<br>Set busArrival = True<br>(Will skip to P1 after red)"]

    Priority3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Priority4{"PRIORITY 4:<br>Actuation Logic<br>All vehicle detectors<br>gap-out (>3s)?"}

    Priority4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| BikeCheck{"All bicycle detectors<br>gap-out (>3s)?"}

    BikeCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| BusP1Check{"Phase 1 AND<br>Bus Present?"}

    BusP1Check -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Continue1["Continue Phase 1<br>(Hold for bus clearance)"]

    BusP1Check -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Action4["TERMINATE PHASE<br>Call mainCircularFlow()<br>Gap-out detected"]

    BikeCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Continue2["Continue Current Phase<br>(Bicycles still approaching)<br>BICYCLE PROTECTION"]

    Priority4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Continue3["Continue Current Phase<br>(Vehicles still approaching)"]

    style GreenStart fill:#E3F2FD
    style MinGreenCheck fill:#BBDEFB
    style Priority1 fill:#EF5350
    style Priority2 fill:#FF7043
    style Priority3 fill:#FFA726
    style Priority4 fill:#FFCA28
    style Action1 fill:#66BB6A
    style Action2A fill:#81C784
    style Action2B fill:#81C784
    style Action3 fill:#9CCC65
    style Action4 fill:#AED581
    style CheckPhase2 fill:#FFB74D
    style BikeCheck fill:#FFD54F
    style BusP1Check fill:#FFE082
    style Continue0 fill:#E0E0E0
    style Continue1 fill:#EEEEEE
    style Continue2 fill:#F5F5F5
    style Continue3 fill:#FAFAFA
```

###### Red Actuation Logic: Phase Skip Decision Implementation

After the red time completes, the system implements decisions made during the green phase:

```mermaid
flowchart TD
    RedStart["RED PHASE ACTIVE<br>Increment red_steps counter"] --> RedTimeCheck{"red_steps =<br>ALL_RED_TIME (2s)?"}

    RedTimeCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Wait["Continue Red Phase<br>(Safety clearance)"]

    RedTimeCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| PedestrianCheck{"Pedestrian Priority Phase<br>AND ≥12 pedestrians<br>waiting?"}

    PedestrianCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| PedPhase["ACTIVATE PHASE 5<br>(Pedestrian Exclusive)<br>Fixed 15-second duration<br>Log: intersection, time, count"]

    PedestrianCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| SkipCheck{"Skip Flag Set?<br>currentPhase =<br>skipStartingPhase + 2?"}

    SkipCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| NormalFlow["NORMAL PROGRESSION<br>Advance to next phase<br>in sequence<br>(P1→P2→P3→P4→P1)"]

    SkipCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| SkipReason{"What caused<br>the skip?"}

    SkipReason -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Synchronization<br>syncValue = True</span>| SyncSkip["SKIP TO PHASE 1<br>(With leading green)<br>Reset syncValue = False<br>Reset skipFlag = 9999"]

    SkipReason -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Bus Priority<br>busArrival = True</span>| BusSkip["SKIP TO PHASE 1<br>(NO leading green)<br>Reset busArrival = False<br>Reset skipFlag = 9999"]

    SkipReason -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Max Green or<br>Actuation Gap-Out</span>| MaxGreenSkip["SKIP TO PHASE 1<br>(With leading green)<br>Reset skipFlag = 9999"]

    style RedStart fill:#E3F2FD
    style RedTimeCheck fill:#BBDEFB
    style PedestrianCheck fill:#90CAF9
    style SkipCheck fill:#64B5F6
    style SkipReason fill:#42A5F5
    style PedPhase fill:#9C27B0
    style NormalFlow fill:#4CAF50
    style SyncSkip fill:#66BB6A
    style BusSkip fill:#81C784
    style MaxGreenSkip fill:#9CCC65
    style Wait fill:#E0E0E0
```

###### Yellow Actuation Logic: Simple Timer

```mermaid
flowchart LR
    YellowStart["YELLOW PHASE ACTIVE<br>Increment yellow_steps counter"] --> YellowCheck{"yellow_steps =<br>YELLOW_TIME (3s)?"}

    YellowCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Continue["Continue Yellow Phase"]

    YellowCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Advance["Advance to RED Phase<br>Reset yellow_steps = 0"]

    style YellowStart fill:#FDD835
    style YellowCheck fill:#FBC02D
    style Continue fill:#F9A825
    style Advance fill:#F57F17
```

##### Synchronization Mechanism

The semi-synchronization operates bidirectionally between the two intersections:

```mermaid
flowchart TD
    P1Start["Phase 1 Starts at<br>INTERSECTION 0"] --> SetTimer0["Set Timer for<br>INTERSECTION 1:<br>syncTime[1] = current_step + 22"]

    P1Start2["Phase 1 Starts at<br>INTERSECTION 1"] --> SetTimer1["Set Timer for<br>INTERSECTION 0:<br>syncTime[0] = current_step + 22"]

    SetTimer0 --> Wait0["Wait 22 seconds..."]
    SetTimer1 --> Wait1["Wait 22 seconds..."]

    Wait0 --> Trigger0["At INTERSECTION 1:<br>Sync condition checked<br>during green actuation"]
    Wait1 --> Trigger1["At INTERSECTION 0:<br>Sync condition checked<br>during green actuation"]

    Trigger0 --> Decision0{"Which phase is<br>active at INT 1?"}
    Trigger1 --> Decision1{"Which phase is<br>active at INT 0?"}

    Decision0 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Phase 1</span>| DoNothing0["Do Nothing<br>(Already synchronized)<br>Reset timer"]
    Decision0 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Phase 2, 3, or 4</span>| Skip0["Skip to next phase<br>Will trigger P1 after red<br>Achieves coordination"]

    Decision1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Phase 1</span>| DoNothing1["Do Nothing<br>(Already synchronized)<br>Reset timer"]
    Decision1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Phase 2, 3, or 4</span>| Skip1["Skip to next phase<br>Will trigger P1 after red<br>Achieves coordination"]

    style P1Start fill:#E3F2FD
    style P1Start2 fill:#E3F2FD
    style SetTimer0 fill:#BBDEFB
    style SetTimer1 fill:#BBDEFB
    style Wait0 fill:#90CAF9
    style Wait1 fill:#90CAF9
    style Trigger0 fill:#64B5F6
    style Trigger1 fill:#64B5F6
    style Decision0 fill:#42A5F5
    style Decision1 fill:#42A5F5
    style DoNothing0 fill:#81C784
    style DoNothing1 fill:#81C784
    style Skip0 fill:#FFA726
    style Skip1 fill:#FFA726
```

###### Complete Phase Transition Flow

```mermaid
flowchart TD
    P1["PHASE 1<br>Major Through<br>Min: 5s, Max: 69s<br>1s Leading Green"] --> Y1["YELLOW 1<br>3 seconds"]

    Y1 --> R1["RED 1<br>2 seconds"]

    R1 --> Decision1{"Skip Flag Set OR<br>High Pedestrian<br>Demand?"}

    Decision1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Skip to P1</span>| P1
    Decision1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Pedestrian Phase</span>| P5["PHASE 5<br>Pedestrian Exclusive<br>Fixed: 15s<br>No Leading Green"]
    Decision1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Normal Flow</span>| P2["PHASE 2<br>Protected Left<br>Min: 5s, Max: 15s<br>1s Leading Green"]

    P2 --> Y2["YELLOW 2<br>3 seconds"]
    Y2 --> R2["RED 2<br>2 seconds"]

    R2 --> Decision2{"Skip Flag Set?"}
    Decision2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Skip to P1</span>| P1
    Decision2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Normal Flow</span>| P3["PHASE 3<br>Minor Through<br>Min: 5s, Max: 24s<br>1s Leading Green"]

    P3 --> Y3["YELLOW 3<br>3 seconds"]
    Y3 --> R3["RED 3<br>2 seconds"]

    R3 --> Decision3{"Skip Flag Set?"}
    Decision3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Skip to P1</span>| P1
    Decision3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Normal Flow</span>| P4["PHASE 4<br>Protected Left<br>Min: 5s, Max: 12s<br>1s Leading Green"]

    P4 --> Y4["YELLOW 4<br>3 seconds"]
    Y4 --> R4["RED 4<br>2 seconds"]

    R4 --> Decision4{"Skip Flag Set OR<br>High Pedestrian<br>Demand?"}
    Decision4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Skip to P1</span>| P1
    Decision4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Pedestrian Phase</span>| P5
    Decision4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Normal Flow</span>| P1

    P5 --> Y5["YELLOW 5<br>3 seconds"]
    Y5 --> R5["RED 5<br>2 seconds"]
    R5 --> P1

    style P1 fill:#E3F2FD
    style P2 fill:#BBDEFB
    style P3 fill:#90CAF9
    style P4 fill:#64B5F6
    style P5 fill:#9C27B0
    style Y1 fill:#FDD835
    style Y2 fill:#FDD835
    style Y3 fill:#FDD835
    style Y4 fill:#FDD835
    style Y5 fill:#FDD835
    style R1 fill:#EF5350
    style R2 fill:#EF5350
    style R3 fill:#EF5350
    style R4 fill:#EF5350
    style R5 fill:#EF5350
    style Decision1 fill:#FFB74D
    style Decision2 fill:#FFA726
    style Decision3 fill:#FF9800
    style Decision4 fill:#FB8C00
```

###### Key Implementation Details from Code

###### Priority Values and Timing

| Parameter                | Value                        | Purpose                                  |
| ------------------------ | ---------------------------- | ---------------------------------------- |
| **MIN_GREEN_TIME**       | 5 seconds                    | Safety: Minimum service before decisions |
| **YELLOW_TIME**          | 3 seconds                    | Warning interval before red              |
| **ALL_RED_TIME**         | 2 seconds                    | Clearance interval between phases        |
| **Leading Green**        | 1 second                     | Priority start for bicycles/pedestrians  |
| **Detector Gap-Out**     | 3 seconds (`critical_delay`) | No detector activation threshold         |
| **Sync Offset**          | 22 seconds                   | Coordination delay between intersections |
| **Pedestrian Threshold** | ≥12 waiting                  | Triggers exclusive Phase 5               |
| **Phase 5 Duration**     | 15 seconds                   | Fixed pedestrian service time            |

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

# Isolated Control Logic (5-TLS Multi-Agent Network)

This section describes the **isolated actuated control** for the 5-intersection multi-agent network. Each intersection
operates **independently** based solely on its local detector readings—no coordination or synchronization between
intersections.

###### Key Differences from Semi-Synchronized Control

| Feature             | Semi-Sync (2-TLS Corridor)                              | Isolated (5-TLS Network)         |
| ------------------- | ------------------------------------------------------- | -------------------------------- |
| **Coordination**    | 22s sync timer between TLS                              | None - fully independent         |
| **Phase Structure** | P1→P2→P3→P4→P5(ped)→P1                                  | P1→P2→P3→P4→P1 (no ped phase)    |
| **Actuation Logic** | Cars gap-out AND Bicycles gap-out                       | Cars gap-out OR Bicycles gap-out |
| **Bus Skip to P1**  | With leading green (sync) / Without Leading Green (bus) | Always WITHOUT leading green     |
| **Priority Levels** | 4 tiers (MAX→Sync→Bus→Actuation)                        | 3 tiers (MAX→Bus→Actuation)      |

###### Green Actuation Logic: Isolated Control Decision Hierarchy

```mermaid
flowchart TD
    subgraph BusDetection["BUS SIGNAL DETECTION <br>(Background Process)<br>"]
        BusEnter["<br>Bus enters emit lane<br>(64s-72s from TLS)"] --> StoreVar["Store in bus_detected_time<br>bus_approaching = True"]
        StoreVar --> WaitTimer{"Time elapsed ≥<br>(travel_time - 23s)?"}
        WaitTimer -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| WaitTimer
        WaitTimer -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| EmitSignal["Emit bus_priority_active = True<br>(Bus now 23s away)"]
    end

    GreenStart["GREEN PHASE ACTIVE<br>Increment green_steps counter"] --> MinGreenCheck{"green_steps ≥<br>MIN_GREEN?"}

    MinGreenCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Continue0["Continue Current Phase<br>(Safety: Must serve minimum)"]

    MinGreenCheck -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Priority1{"PRIORITY 1:<br>Max Green Reached?<br>green_steps = MAX_GREEN?"}

    Priority1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Action1["TERMINATE PHASE<br>Call mainCircularFlow()<br>P1→P2→P3→P4→P1"]

    Priority1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Priority2a{"PRIORITY 2a:<br>bus_priority_active?<br>(THIS TLS only - isolated)"}

    Priority2a -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Priority2b{"PRIORITY 2b:<br>Current Phase?"}

    Priority2b -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P2, P3, or P4</span>| Action2["SKIP TO PHASE 1<br>Set skipStartingPhase flag<br>Set busArrival = True<br>(NO leading green for bicycles)"]

    Priority2b -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>P1</span>| ContinueP1["Continue Phase 1<br>(Hold green for bus arrival,<br>max 44s capacity)"]

    Priority2a -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Priority3{"PRIORITY 3:<br>Actuation Logic<br>Vehicle detectors gap-out (>3s)<br>OR Bicycle detectors gap-out (>3s)?"}

    Priority3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Yes</span>| Action3["TERMINATE PHASE<br>Call mainCircularFlow()<br>Gap-out detected"]

    Priority3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>No</span>| Continue2["Continue Current Phase<br>(Vehicles OR Bicycles<br>still approaching)"]

    style BusDetection fill:#E1BEE7
    style BusEnter fill:#CE93D8
    style StoreVar fill:#BA68C8
    style WaitTimer fill:#AB47BC
    style EmitSignal fill:#9C27B0
    style GreenStart fill:#E3F2FD
    style MinGreenCheck fill:#BBDEFB
    style Priority1 fill:#EF5350
    style Priority2a fill:#FFA726
    style Priority2b fill:#FFB74D
    style Priority3 fill:#FFCA28
    style Action1 fill:#66BB6A
    style Action2 fill:#9CCC65
    style Action3 fill:#AED581
    style ContinueP1 fill:#EEEEEE
    style Continue0 fill:#E0E0E0
    style Continue2 fill:#F5F5F5
```

##### Isolated Control: Complete Phase Transition Flow

```mermaid
flowchart TD
    P1["PHASE 1<br>Major Through<br>Min: 8s, Max: 44s<br>1s Leading Green"] --> Y1["YELLOW 1<br>3 seconds"]

    Y1 --> R1["RED 1<br>2 seconds"]

    R1 --> Decision1{"Bus Skip Flag?"}

    Decision1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Skip to P1, NO leading green</span>| P1
    Decision1 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Normal Flow</span>| P2["PHASE 2<br>Major Left<br>Min: 3s, Max: 15s<br>1s Leading Green"]

    P2 --> Y2["YELLOW 2<br>3 seconds"]
    Y2 --> R2["RED 2<br>2 seconds"]

    R2 --> Decision2{"Bus Skip Flag?"}
    Decision2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Skip to P1, NO leading green</span>| P1
    Decision2 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Normal Flow</span>| P3["PHASE 3<br>Minor Through<br>Min: 5s, Max: 24s<br>1s Leading Green"]

    P3 --> Y3["YELLOW 3<br>3 seconds"]
    Y3 --> R3["RED 3<br>2 seconds"]

    R3 --> Decision3{"Bus Skip Flag?"}
    Decision3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Skip to P1, NO leading green</span>| P1
    Decision3 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Normal Flow</span>| P4["PHASE 4<br>Minor Left<br>Min: 2s, Max: 12s<br>1s Leading Green"]

    P4 --> Y4["YELLOW 4<br>3 seconds"]
    Y4 --> R4["RED 4<br>2 seconds"]

    R4 --> Decision4{"Bus Skip Flag?"}
    Decision4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Skip to P1, NO leading green</span>| P1
    Decision4 -->|<span style='background-color:khaki; color:black; padding:2px 6px; border-radius:3px'>Normal Flow</span>| P1

    style P1 fill:#E3F2FD
    style P2 fill:#BBDEFB
    style P3 fill:#90CAF9
    style P4 fill:#64B5F6
    style Y1 fill:#FDD835
    style Y2 fill:#FDD835
    style Y3 fill:#FDD835
    style Y4 fill:#FDD835
    style R1 fill:#EF5350
    style R2 fill:#EF5350
    style R3 fill:#EF5350
    style R4 fill:#EF5350
    style Decision1 fill:#FFB74D
    style Decision2 fill:#FFA726
    style Decision3 fill:#FF9800
    style Decision4 fill:#FB8C00
```

###### Isolated Control: Priority Values and Timing

| Parameter            | Value      | Purpose                           |
| -------------------- | ---------- | --------------------------------- |
| **MIN_GREEN (P1)**   | 8 seconds  | Minimum service for major through |
| **MIN_GREEN (P2)**   | 3 seconds  | Minimum service for major left    |
| **MIN_GREEN (P3)**   | 5 seconds  | Minimum service for minor through |
| **MIN_GREEN (P4)**   | 2 seconds  | Minimum service for minor left    |
| **MAX_GREEN (P1)**   | 44 seconds | Maximum arterial through service  |
| **MAX_GREEN (P2)**   | 15 seconds | Maximum major left service        |
| **MAX_GREEN (P3)**   | 24 seconds | Maximum minor through service     |
| **MAX_GREEN (P4)**   | 12 seconds | Maximum minor left service        |
| **YELLOW_TIME**      | 3 seconds  | Warning interval before red       |
| **ALL_RED_TIME**     | 2 seconds  | Clearance interval between phases |
| **Leading Green**    | 1 second   | Priority start for bicycles       |
| **Detector Gap-Out** | 3 seconds  | No detector activation threshold  |

###### Key Characteristics of Isolated Control

1. **Fully Independent**: Each TLS makes decisions based only on its local detectors
2. **No Coordination Overhead**: No sync timers or inter-TLS communication
3. **Simplified Actuation**: OR logic (cars OR bikes gap-out) reduces phase holding
4. **No Pedestrian Phase**: 4-phase cycle only (P1→P2→P3→P4→P1)
5. **Bus Priority Preserved**: Skip to P1 for bus, but without bicycle leading green
6. **Circular Flow Guaranteed**: MAX_GREEN always triggers next phase in sequence

---

## Time Duration Analysis: Switching to P1 from Any Point in Cycle

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

###### From P1 (Must go through P2 minimum)

**Case 1a: At start of P1 MIN_GREEN**

```
P1 MIN_GREEN remaining: 8s
+ P1 Yellow: 3s
+ P1 Red: 2s
+ P2 Leading Green: 1s
+ P2 MIN_GREEN: 3s
+ P2 Yellow: 3s
+ P2 Red: 2s
+ P1 Leading Green: 1s
────────────────────────
Total: 23 seconds
```

###### **Case 1b: In P1 actuation period (MIN served, can terminate)**

```
P1 Yellow: 3s
+ P1 Red: 2s
+ P2 Leading Green: 1s
+ P2 MIN_GREEN: 3s
+ P2 Yellow: 3s
+ P2 Red: 2s
+ P1 Leading Green: 1s
────────────────────────
Total: 15 seconds
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

| Current Phase | At Start of MIN_GREEN | In Actuation Period |
| ------------- | --------------------- | ------------------- |
| **P1**        | 23s (via P2)          | 15s (via P2)        |
| **P2**        | 9s                    | 6s                  |
| **P3**        | 11s                   | 6s                  |
| **P4**        | 8s                    | 6s                  |

##### Worst Case Analysis

**Absolute Worst Case: 23 seconds**

- Occurs when bus signal arrives at the exact start of P1 MIN_GREEN
- Must complete: P1 MIN (8s) → P1 Yellow (3s) → P1 Red (2s) → P2 Leading (1s) → P2 MIN (3s) → P2 Yellow (3s) → P2 Red
  (2s) → P1 Leading (1s)

**Best Case: 6 seconds**

- Occurs when in actuation period of P2, P3, or P4
- Only requires: Yellow (3s) → Red (2s) → P1 Leading (1s)

##### Implication for Bus Coordination

With bus signal emission lanes providing 64-72 seconds warning:

- **64s warning** (middle TLS): Covers worst case (23s) with 41s margin
- **72s warning** (edge TLS): Covers worst case (23s) with 49s margin

This ensures the controller can always guarantee green for bus arrival regardless of current phase state.

##### Why 23s Warning is Sufficient for All Cases

**Question**: If we inform the TLS 23s before bus arrival (worst case timing), what happens in best case scenarios where
only 6s is needed?

**Analysis: Best Case Scenario (In Actuation Period of P2/P3/P4)**

```
Bus signal received: Bus is 23s away
Time to switch to P1: 6s (best case)
────────────────────────────────────
After P1 starts: Bus is 23s - 6s = 17s away

P1 sequence:
- Leading Green: 1s → Bus is 16s away
- MIN_GREEN: 8s → Bus is 8s away
- Actuation period: Hold green until bus passes

Bus arrives 8s after MIN_GREEN ends.
Controller simply holds P1 green for 8s more.
Total P1 green time: 1s + 8s + 8s = 17s (well under MAX of 44s)
```

**Analysis: Intermediate Case (At Start of P3 MIN_GREEN)**

```
Bus signal received: Bus is 23s away
Time to switch to P1: 11s (P3 case)
────────────────────────────────────
After P1 starts: Bus is 23s - 11s = 12s away

P1 sequence:
- Leading Green: 1s → Bus is 11s away
- MIN_GREEN: 8s → Bus is 3s away
- Actuation period: Hold green 3s more until bus passes

Bus arrives 3s after MIN_GREEN ends.
Controller holds P1 green for 3s more.
Total P1 green time: 1s + 8s + 3s = 12s (well under MAX of 44s)
```

**Analysis: Worst Case (At Start of P1 MIN_GREEN)**

```
Bus signal received: Bus is 23s away
Time to switch to P1: 23s (must go through P2)
────────────────────────────────────
Bus arrives exactly when P1 Leading Green starts.
Bus gets green immediately with no wait.
```

###### Confirmation: 23s Warning Guarantees Green for All Cases

| Scenario                       | Time to P1 | Bus Arrival After P1 Start | Action Required             |
| ------------------------------ | ---------- | -------------------------- | --------------------------- |
| Best case (actuation P2/P3/P4) | 6s         | 17s after P1 start         | Hold P1 green 9s after MIN  |
| P4 at MIN start                | 8s         | 15s after P1 start         | Hold P1 green 7s after MIN  |
| P2 at MIN start                | 9s         | 14s after P1 start         | Hold P1 green 6s after MIN  |
| P3 at MIN start                | 11s        | 12s after P1 start         | Hold P1 green 4s after MIN  |
| P1 actuation period            | 15s        | 8s after P1 start          | Hold P1 green at MIN        |
| Worst case (P1 at MIN start)   | 23s        | 0s (arrives at P1 start)   | Green immediately available |

**Key Insight**: Since P1 MAX_GREEN is 44s, the controller has ample capacity to hold P1 green until bus passes in all
scenarios. The only requirement is that the controller must NOT transition away from P1 while bus is approaching
(detected via bus priority lanes).

**Conclusion**: A fixed 23s warning time is sufficient to guarantee uninterrupted green for bus arrival regardless of
current phase state. The controller logic simply needs to:

1. Receive bus signal when bus enters emit lane
2. Switch to P1 as fast as possible (respecting MIN_GREEN and transitions)
3. Hold P1 green until bus clears the intersection
