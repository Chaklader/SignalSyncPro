# DRL Agent State Structure (VERIFIED FROM CODE)

## State Dimension: 32 features

### Structure (2 Intersections × 16 features each)

#### **TLS 3 (Intersection 1) - Features 0-15:**

| Index | Feature Name                | Description                                      | Range  |
|-------|----------------------------|--------------------------------------------------|--------|
| 0     | TLS3_Phase_P1              | One-hot: Phase 1 active                         | 0 or 1 |
| 1     | TLS3_Phase_P2              | One-hot: Phase 2 active                         | 0 or 1 |
| 2     | TLS3_Phase_P3              | One-hot: Phase 3 active                         | 0 or 1 |
| 3     | TLS3_Phase_P4              | One-hot: Phase 4 active                         | 0 or 1 |
| 4     | TLS3_Phase_Duration        | Current phase duration (normalized)             | 0-1    |
| 5     | TLS3_Vehicle_Det1_P*       | Vehicle detector 1 for current phase P* (binary)| 0 or 1 |
| 6     | TLS3_Vehicle_Det2_P*       | Vehicle detector 2 for current phase P* (binary)| 0 or 1 |
| 7     | TLS3_Vehicle_Det3_P*       | Vehicle detector 3 for current phase P* (binary)| 0 or 1 |
| 8     | TLS3_Vehicle_Det4_P*       | Vehicle detector 4 for current phase P* (binary)| 0 or 1 |
| 9     | TLS3_Bicycle_Det1_P*       | Bicycle detector 1 for current phase P* (binary)| 0 or 1 |
| 10    | TLS3_Bicycle_Det2_P*       | Bicycle detector 2 for current phase P* (binary)| 0 or 1 |
| 11    | TLS3_Bicycle_Det3_P*       | Bicycle detector 3 for current phase P* (binary)| 0 or 1 |
| 12    | TLS3_Bicycle_Det4_P*       | Bicycle detector 4 for current phase P* (binary)| 0 or 1 |
| 13    | TLS3_Bus_Present           | Bus presence (binary)                           | 0 or 1 |
| 14    | TLS3_Bus_Wait              | Bus wait time (normalized)                      | 0-1    |
| 15    | TLS3_Sim_Time              | Simulation time (normalized)                    | 0-1    |

#### **TLS 6 (Intersection 2) - Features 16-31:**

| Index | Feature Name                | Description                                      | Range  |
|-------|----------------------------|--------------------------------------------------|--------|
| 16    | TLS6_Phase_P1              | One-hot: Phase 1 active                         | 0 or 1 |
| 17    | TLS6_Phase_P2              | One-hot: Phase 2 active                         | 0 or 1 |
| 18    | TLS6_Phase_P3              | One-hot: Phase 3 active                         | 0 or 1 |
| 19    | TLS6_Phase_P4              | One-hot: Phase 4 active                         | 0 or 1 |
| 20    | TLS6_Phase_Duration        | Current phase duration (normalized)             | 0-1    |
| 21    | TLS6_Vehicle_Det1_P*       | Vehicle detector 1 for current phase P* (binary)| 0 or 1 |
| 22    | TLS6_Vehicle_Det2_P*       | Vehicle detector 2 for current phase P* (binary)| 0 or 1 |
| 23    | TLS6_Vehicle_Det3_P*       | Vehicle detector 3 for current phase P* (binary)| 0 or 1 |
| 24    | TLS6_Vehicle_Det4_P*       | Vehicle detector 4 for current phase P* (binary)| 0 or 1 |
| 25    | TLS6_Bicycle_Det1_P*       | Bicycle detector 1 for current phase P* (binary)| 0 or 1 |
| 26    | TLS6_Bicycle_Det2_P*       | Bicycle detector 2 for current phase P* (binary)| 0 or 1 |
| 27    | TLS6_Bicycle_Det3_P*       | Bicycle detector 3 for current phase P* (binary)| 0 or 1 |
| 28    | TLS6_Bicycle_Det4_P*       | Bicycle detector 4 for current phase P* (binary)| 0 or 1 |
| 29    | TLS6_Bus_Present           | Bus presence (binary)                           | 0 or 1 |
| 30    | TLS6_Bus_Wait              | Bus wait time (normalized)                      | 0-1    |
| 31    | TLS6_Sim_Time              | Simulation time (normalized)                    | 0-1    |

---

## Important: Phase-Specific Detectors

The 4 vehicle detectors (features 5-8, 21-24) and 4 bicycle detectors (features 9-12, 25-28) are **phase-dependent**.

Each phase has its own set of 4 detectors monitoring different approaches:
- **P1 detectors:** Edges 2→3, 4→3, 5→6, 7→6
- **P2 detectors:** Different set of 4 approaches
- **P3 detectors:** Different set of 4 approaches
- **P4 detectors:** Different set of 4 approaches

When the agent observes the state, the detector values correspond to **whichever phase is currently active** (indicated by the one-hot encoding in features 0-3 or 16-19).

**Example:**
- If Phase P1 is active (feature [0]=1), then features [5-8] contain queue status for P1's 4 vehicle detectors
- If Phase P2 is active (feature [1]=1), then features [5-8] contain queue status for P2's 4 vehicle detectors

**Source:** `detectors/developed/drl/detectors.py` and `traffic_management.py::_get_detector_queues()`

---

## Action Space: 3 actions

| Action | Name     | Description                        |
|--------|----------|------------------------------------|
| 0      | Continue | Continue current phase             |
| 1      | Skip2P1  | Skip to Phase 1 (major arterial)   |
| 2      | Next     | Advance to next phase in sequence  |

---

## Phase Structure: 4 Controllable Phases

| Phase ID | Name        | Description                                              | Max Green Time |
|----------|-------------|----------------------------------------------------------|----------------|
| 1        | PHASE_ONE   | Major roadway through + permissible right turn          | 44s            |
| 5        | PHASE_TWO   | Major roadway protected left turn                       | 15s            |
| 9        | PHASE_THREE | Minor roadway through + permissible right turn          | 24s            |
| 13       | PHASE_FOUR  | Minor roadway protected left turn                       | 12s            |

**Movement Types:**
- **Through + Permissible Right (P1, P3):** Car, bicycle, and pedestrian movements with green signal; right turns on permissible basis
- **Protected Left Turn (P2, P4):** Car left turns with protected green arrow; bicycles and pedestrians allowed but not protected (shown as dotted lines in signal diagram)

**Note:** There is NO dedicated pedestrian-only phase. All phases serve mixed traffic with varying protection levels.

---

## Code References

- State construction: `controls/ml_based/drl/traffic_management.py::_get_state()` (lines 113-141)
- Phase encoding: `controls/ml_based/drl/traffic_management.py::_encode_phase()` (lines 155-173)
- Configuration: `controls/ml_based/drl/config.py` (STATE_DIM=32, ACTION_DIM=3)
- Phase constants: `constants/developed/common/tls_constants.py`
