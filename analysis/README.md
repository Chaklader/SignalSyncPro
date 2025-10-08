# Analysis Scripts

This directory contains post-processing scripts for analyzing SUMO simulation outputs.

## Scripts

### 1. `analyze_waiting_time.py`
**Purpose:** Analyzes vehicle waiting times from simulation output

**Input:** Trip info file (e.g., `tripinfo.xml`)

**Output:** `waitingSenarioNumber_1.csv`

**Usage:**
```bash
python analyze_waiting_time.py <tripinfo_file>
```

**Analyzes:**
- Private car waiting times
- Bicycle waiting times
- Pedestrian waiting times
- Bus waiting times (adjusted for bus stop time)

---

### 2. `analyze_CO2.py`
**Purpose:** Calculates total CO2 emissions from vehicles

**Input:** Vehicle emission file

**Output:** `emission_CO2_Senario_1.csv`

**Usage:**
```bash
python analyze_CO2.py <emission_file>
```

**Analyzes:**
- Total CO2 emissions (in kg) for private cars and buses
- Excludes bicycles and pedestrians

---

### 3. `analyze_phase_streching.py`
**Purpose:** Analyzes traffic light phase durations

**Input:** Traffic light state file

**Output:** `Pr_1_t_phase_stretching.csv`

**Usage:**
```bash
python analyze_phase_streching.py <tls_state_file>
```

**Analyzes:**
- Average duration of Phase 1
- Average duration of Phase 2
- Average duration of Phase 3
- Average duration of Phase 4

---

## Workflow

1. **Run simulation:**
   ```bash
   cd ..
   python main.py
   ```

2. **Analyze results:**
   ```bash
   cd analysis
   python analyze_waiting_time.py ../tripinfo.xml
   python analyze_CO2.py ../emission_output.xml
   python analyze_phase_streching.py ../tls_state.xml
   ```

## Output Files

All analysis scripts generate CSV files with statistical summaries and scenario descriptions.

**Note:** These scripts require SUMO tools to be in your Python path.
