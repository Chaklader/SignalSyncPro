# SignalSyncPro 🚦

**Advanced Traffic Signal Control using Deep Reinforcement Learning**

SignalSyncPro is a sophisticated traffic management system that uses Deep Q-Network (DQN) reinforcement learning to
optimize traffic signal timing at intersections. The system learns to minimize vehicle waiting times while maintaining
safe and efficient traffic flow across multiple vehicle types (cars, bicycles, buses, and pedestrians).

<img src="images/simulation.png" width="400" height="auto" alt="SUMO Traffic Simulation">

---

## 🌟 Features

### **Intelligent Traffic Control**

- **Deep Reinforcement Learning**: DQN-based agent that learns optimal signal timing policies
- **Multi-Modal Support**: Handles cars, bicycles, buses, and pedestrians
- **Adaptive Learning**: Trains on diverse traffic scenarios for robust performance
- **Real-Time Optimization**: Minimizes waiting times while ensuring safety

### **Comprehensive Testing**

- **30 Test Scenarios**: Systematic evaluation across varying traffic conditions
- **Baseline Comparison**: Rule-based "developed" control for performance benchmarking
- **Detailed Metrics**: Tracks waiting times, sync rates, safety violations, and emissions

### **Production-Ready Architecture**

- **Modular Design**: Clean separation of concerns (controls, routes, infrastructure)
- **Reusable Utilities**: Centralized path setup and traffic configuration
- **Flexible Configuration**: Easy-to-modify constants and parameters
- **Comprehensive Logging**: Detailed training and testing logs

---

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Training](#training)
- [Testing](#testing)
- [Configuration](#configuration)
- [Results](#results)
- [Architecture](#architecture)
- [Contributing](#contributing)

---

## 🚀 Installation

### Prerequisites

1. **SUMO (Simulation of Urban MObility)**

    ```bash
    # macOS
    brew install sumo

    # Ubuntu/Debian
    sudo apt-get install sumo sumo-tools sumo-doc

    # Set SUMO_HOME environment variable
    export SUMO_HOME="/path/to/sumo"
    ```

2. **Python 3.9+**
    ```bash
    python --version  # Should be 3.9 or higher
    ```

### Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/SignalSyncPro.git
    cd SignalSyncPro
    ```

2. **Create virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment**
    ```bash
    cp .env.example .env
    # Edit .env if needed (optional)
    ```

---

## ⚡ Quick Start

### Train a DRL Agent

```bash
# Start training (runs in background)
./scripts/drl/run/run_training.sh

# Monitor progress
tail -100f training.log
```

### Test Trained Agent

```bash
# Test on all 30 scenarios
./scripts/drl/run/run_testing.sh models/training_YYYYMMDD_HHMMSS/final_model.pth
```

### Test Baseline (Rule-Based Control)

```bash
# Test developed control on all scenarios
./scripts/rule_based/run_developed_test.sh
```

---

## 📁 Project Structure

```
SignalSyncPro/
├── common/                      # Shared utilities
│   ├── utils.py                 # General utilities (traffic load calculation)
│   └── sumo_utils.py           # SUMO path setup utilities
│
├── constants/                   # Configuration constants
│   ├── developed/              # Developed control constants
│   └── reference/              # Reference control constants
│
├── controls/                    # Traffic control implementations
│   ├── ml_based/               # Machine learning controls
│   │   └── drl/                # Deep Reinforcement Learning
│   │       ├── agent.py        # DQN Agent
│   │       ├── config.py       # DRL configuration
│   │       ├── reward.py       # Reward function
│   │       └── traffic_management.py  # Environment
│   └── rule_based/             # Rule-based controls
│       ├── developed/          # Optimized rule-based control
│       └── reference/          # Baseline control
│
├── infrastructure/              # SUMO network files
│   ├── developed/              # Developed control infrastructure
│   └── reference/              # Reference control infrastructure
│
├── route_generator/            # Traffic route generation
│   ├── traffic_config.py       # Traffic configuration
│   ├── developed/              # Route generators for developed control
│   └── reference/              # Route generators for reference control
│
├── run/                        # Execution scripts
│   ├── training/               # Training scripts
│   │   └── train_drl.py        # Main training script
│   └── testing/                # Testing scripts
│       ├── test_drl.py         # DRL testing
│       └── test_developed.py   # Rule-based testing
│
├── scripts/                    # Shell scripts
│   ├── drl/run/               # DRL execution scripts
│   └── rule_based/            # Rule-based execution scripts
│
├── logs/                       # Training/testing logs
├── models/                     # Saved model checkpoints
├── results/                    # Test results and metrics
└── .env                        # Environment configuration
```

---

## 🎓 Training

### Training Process

The DRL agent learns through experience by:

1. **Observing** traffic state (queue lengths, waiting times, phase info)
2. **Taking actions** (advance phase, skip to P1, activate pedestrian phase)
3. **Receiving rewards** based on performance (waiting times, sync rate, safety)
4. **Learning** optimal policies through Q-learning

### Training Configuration

Key parameters in `constants/developed/common/constants.py`:

```python
NUM_EPISODES_TRAIN = 100        # Number of training episodes
SIMULATION_LIMIT_TRAIN = 3600   # Simulation duration (seconds)
EPSILON_START = 0.9             # Initial exploration rate
EPSILON_DECAY = 0.98            # Exploration decay rate
LEARNING_RATE = 0.0001          # Neural network learning rate
```

### Reward Function

The agent optimizes a weighted reward:

- **Waiting Time** (α=6.0): Penalizes vehicle waiting
- **Sync Rate** (α=0.15): Rewards coordinated signals
- **Pedestrian Demand** (α=0.8): Responds to pedestrian needs
- **Safety**: Monitors headway, distance, and red light violations

### Monitoring Training

```bash
# Watch training progress
tail -100f training.log

# Check if training is running
ps aux | grep train_drl.py

# Stop training
kill <PID>
```

---

## 🧪 Testing

### Test Scenarios

**30 predefined scenarios** for consistent evaluation:

- **Pr_0 to Pr_9**: Varying car volumes (100-1000/hr), constant bikes/peds (400/hr)
- **Bi_0 to Bi_9**: Varying bicycle volumes (100-1000/hr), constant cars/peds (400/hr)
- **Pe_0 to Pe_9**: Varying pedestrian volumes (100-1000/hr), constant cars/bikes (400/hr)

### Performance Metrics

- **Average Waiting Time**: Cars, bicycles, pedestrians
- **Sync Rate**: Percentage of synchronized signal changes
- **Pedestrian Phases**: Number of dedicated pedestrian phases activated
- **Safety Violations**: Headway, distance, and red light violations
- **CO2 Emissions**: Environmental impact

### Running Tests

```bash
# Test DRL agent
./scripts/drl/run/run_testing.sh models/training_20241019/final_model.pth

# Test rule-based control
./scripts/rule_based/run_developed_test.sh

# Results saved to:
# - results/drl_testing/
# - results/developed_testing/
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```bash
# SUMO GUI settings
SUMO_GUI=false              # Set to 'true' to visualize simulation

# Logging level
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR
```

### DRL Configuration

Edit `controls/ml_based/drl/config.py`:

```python
class DRLConfig:
    # Neural Network
    HIDDEN_LAYERS = [128, 128]
    LEARNING_RATE = 0.0001

    # Training
    BATCH_SIZE = 64
    GAMMA = 0.95
    MEMORY_SIZE = 10000

    # Exploration
    EPSILON_START = 0.9
    EPSILON_END = 0.005
    EPSILON_DECAY = 0.98
```

### Traffic Configuration

Modify `route_generator/traffic_config.py` for custom scenarios:

```python
# Training: Random volumes
config = get_traffic_config(mode='training')

# Testing: Specific scenario
config = get_traffic_config(mode='test', scenario='Pr_5')
```

---

## 📊 Results

### Expected Performance

**Target Metrics** (after 100 episodes):

- Car waiting time: 20-30s average
- Bicycle waiting time: 15-25s average
- Pedestrian phases: 150-250 per episode
- Sync rate: 60-70%
- Episode rewards: -0.5 to +0.3

### Comparison with Baseline

The DRL agent typically outperforms rule-based control by:

- **15-25%** reduction in average waiting times
- **Better adaptation** to varying traffic conditions
- **Higher sync rates** for coordinated flow

---

## 🏗️ Architecture

### Key Components

1. **DQN Agent** (`controls/ml_based/drl/agent.py`)

    - Neural network with experience replay
    - ε-greedy exploration strategy
    - Target network for stable learning

2. **Traffic Management** (`controls/ml_based/drl/traffic_management.py`)

    - SUMO environment wrapper
    - State observation and action execution
    - Reward calculation and safety monitoring

### System Interaction Flow

```
┌──────────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│ Traffic          │     │ SUMO         │     │ traci        │     │ SUMO             │
│ Management       │     │ Process      │     │ module       │     │ Simulation       │
└────────┬─────────┘     └──────┬───────┘     └──────┬───────┘     └────────┬─────────┘
         │                      │                    │                      │
         │ Launch sumo-gui/sumo │                    │                      │
         │─────────────────────>│                    │                      │
         │                      │                    │                      │
         │    traci.init(8816)  │                    │                      │
         │──────────────────────┼───────────────────>│                      │
         │                      │                    │  Connect to port 8816│
         │                      │                    │─────────────────────>│
         │                      │                    │                      │
         │                      │         [Episode Loop]                    │
         │                      │                    │                      │
         │              Get state via TraCI          │                      │
         │──────────────────────┼───────────────────>│─────────────────────>│
         │<─────────────────────┼────────────────────┼──────────────────────│
         │              Traffic metrics               │                      │
         │                      │                    │                      │
         │             Set phase via TraCI           │                      │
         │──────────────────────┼───────────────────>│─────────────────────>│
         │                      │                    │                      │
         │                      │                    │   simulationStep()   │
         │                      │                    │                 ────┐│
         │                      │                    │                 <───┘│
         │                      │                    │                      │
         │<─────────────────────┼────────────────────┼──────────────────────│
         │              Updated state                 │                      │
         │                      │                    │                      │
         │           Close connection                 │                      │
         │──────────────────────┼───────────────────>│─────────────────────>│
         │                      │                    │                      │
         │   Terminate process  │                    │                      │
         │─────────────────────>│                    │                      │
         │                      │                    │                      │
┌────────┴─────────┐     ┌──────┴───────┐     ┌──────┴───────┐     ┌────────┴─────────┐
│ Traffic          │     │ SUMO         │     │ traci        │     │ SUMO             │
│ Management       │     │ Process      │     │ module       │     │ Simulation       │
└──────────────────┘     └──────────────┘     └──────────────┘     └──────────────────┘
```

**Key Operations:**

- **Initialization:** `reset()` launches SUMO and connects via TraCI on port 8816
- **Episode Loop:** `step(action)` gets state, sets phase, advances simulation
- **Cleanup:** `close()` terminates TraCI connection and SUMO process

3. **Route Generator** (`route_generator/`)

    - Dynamic traffic generation
    - Multi-modal support (cars, bikes, buses, pedestrians)
    - Configurable traffic volumes

4. **Reward Function** (`controls/ml_based/drl/reward.py`)
    - Multi-objective optimization
    - Weighted components for different priorities
    - Safety violation penalties

### Design Principles

- **Modularity**: Clean separation of concerns
- **Reusability**: Shared utilities and configurations
- **Extensibility**: Easy to add new controls or scenarios
- **Maintainability**: Well-documented code with type hints

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Code Style

- Follow PEP 8 guidelines
- Use `snake_case` for variables and functions
- Add docstrings to all functions
- Include type hints where appropriate

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **SUMO**: Eclipse SUMO traffic simulation platform
- **PyTorch**: Deep learning framework
- **Research**: Based on DRL traffic control research

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ for smarter traffic management**

---

---

# DRL Agent State Structure (VERIFIED FROM CODE)

## State Dimension: 32 features

### Structure (2 Intersections × 16 features each)

#### **TLS 3 (Intersection 1) - Features 0-15:**

| Index | Feature Name          | Description                                       | Range  |
| ----- | --------------------- | ------------------------------------------------- | ------ |
| 0     | TLS3_Phase_P1         | One-hot: Phase 1 active                           | 0 or 1 |
| 1     | TLS3_Phase_P2         | One-hot: Phase 2 active                           | 0 or 1 |
| 2     | TLS3_Phase_P3         | One-hot: Phase 3 active                           | 0 or 1 |
| 3     | TLS3_Phase_P4         | One-hot: Phase 4 active                           | 0 or 1 |
| 4     | TLS3_Phase_Duration   | Current phase duration (normalized)               | 0-1    |
| 5     | TLS3_Vehicle_Det1_P\* | Vehicle detector 1 for current phase P\* (binary) | 0 or 1 |
| 6     | TLS3_Vehicle_Det2_P\* | Vehicle detector 2 for current phase P\* (binary) | 0 or 1 |
| 7     | TLS3_Vehicle_Det3_P\* | Vehicle detector 3 for current phase P\* (binary) | 0 or 1 |
| 8     | TLS3_Vehicle_Det4_P\* | Vehicle detector 4 for current phase P\* (binary) | 0 or 1 |
| 9     | TLS3_Bicycle_Det1_P\* | Bicycle detector 1 for current phase P\* (binary) | 0 or 1 |
| 10    | TLS3_Bicycle_Det2_P\* | Bicycle detector 2 for current phase P\* (binary) | 0 or 1 |
| 11    | TLS3_Bicycle_Det3_P\* | Bicycle detector 3 for current phase P\* (binary) | 0 or 1 |
| 12    | TLS3_Bicycle_Det4_P\* | Bicycle detector 4 for current phase P\* (binary) | 0 or 1 |
| 13    | TLS3_Bus_Present      | Bus presence (binary)                             | 0 or 1 |
| 14    | TLS3_Bus_Wait         | Bus wait time (normalized)                        | 0-1    |
| 15    | TLS3_Sim_Time         | Simulation time (normalized)                      | 0-1    |

#### **TLS 6 (Intersection 2) - Features 16-31:**

| Index | Feature Name          | Description                                       | Range  |
| ----- | --------------------- | ------------------------------------------------- | ------ |
| 16    | TLS6_Phase_P1         | One-hot: Phase 1 active                           | 0 or 1 |
| 17    | TLS6_Phase_P2         | One-hot: Phase 2 active                           | 0 or 1 |
| 18    | TLS6_Phase_P3         | One-hot: Phase 3 active                           | 0 or 1 |
| 19    | TLS6_Phase_P4         | One-hot: Phase 4 active                           | 0 or 1 |
| 20    | TLS6_Phase_Duration   | Current phase duration (normalized)               | 0-1    |
| 21    | TLS6_Vehicle_Det1_P\* | Vehicle detector 1 for current phase P\* (binary) | 0 or 1 |
| 22    | TLS6_Vehicle_Det2_P\* | Vehicle detector 2 for current phase P\* (binary) | 0 or 1 |
| 23    | TLS6_Vehicle_Det3_P\* | Vehicle detector 3 for current phase P\* (binary) | 0 or 1 |
| 24    | TLS6_Vehicle_Det4_P\* | Vehicle detector 4 for current phase P\* (binary) | 0 or 1 |
| 25    | TLS6_Bicycle_Det1_P\* | Bicycle detector 1 for current phase P\* (binary) | 0 or 1 |
| 26    | TLS6_Bicycle_Det2_P\* | Bicycle detector 2 for current phase P\* (binary) | 0 or 1 |
| 27    | TLS6_Bicycle_Det3_P\* | Bicycle detector 3 for current phase P\* (binary) | 0 or 1 |
| 28    | TLS6_Bicycle_Det4_P\* | Bicycle detector 4 for current phase P\* (binary) | 0 or 1 |
| 29    | TLS6_Bus_Present      | Bus presence (binary)                             | 0 or 1 |
| 30    | TLS6_Bus_Wait         | Bus wait time (normalized)                        | 0-1    |
| 31    | TLS6_Sim_Time         | Simulation time (normalized)                      | 0-1    |

---

## Important: Phase-Specific Detectors

The 4 vehicle detectors (features 5-8, 21-24) and 4 bicycle detectors (features 9-12, 25-28) are **phase-dependent**.

Each phase has its own set of 4 detectors monitoring different approaches:

- **P1 detectors:** Edges 2→3, 4→3, 5→6, 7→6
- **P2 detectors:** Different set of 4 approaches
- **P3 detectors:** Different set of 4 approaches
- **P4 detectors:** Different set of 4 approaches

When the agent observes the state, the detector values correspond to **whichever phase is currently active** (indicated
by the one-hot encoding in features 0-3 or 16-19).

**Example:**

- If Phase P1 is active (feature [0]=1), then features [5-8] contain queue status for P1's 4 vehicle detectors
- If Phase P2 is active (feature [1]=1), then features [5-8] contain queue status for P2's 4 vehicle detectors

**Source:** `detectors/developed/drl/detectors.py` and `traffic_management.py::_get_detector_queues()`

---

## Action Space: 3 actions

| Action | Name     | Description                       |
| ------ | -------- | --------------------------------- |
| 0      | Continue | Continue current phase            |
| 1      | Skip2P1  | Skip to Phase 1 (major arterial)  |
| 2      | Next     | Advance to next phase in sequence |

---

## Phase Structure: 4 Controllable Phases

| Phase ID | Name        | Description                                    | Max Green Time |
| -------- | ----------- | ---------------------------------------------- | -------------- |
| 1        | PHASE_ONE   | Major roadway through + permissible right turn | 44s            |
| 5        | PHASE_TWO   | Major roadway protected left turn              | 15s            |
| 9        | PHASE_THREE | Minor roadway through + permissible right turn | 24s            |
| 13       | PHASE_FOUR  | Minor roadway protected left turn              | 12s            |

**Movement Types:**

- **Through + Permissible Right (P1, P3):** Car, bicycle, and pedestrian movements with green signal; right turns on
  permissible basis
- **Protected Left Turn (P2, P4):** Car left turns with protected green arrow; bicycles and pedestrians allowed but not
  protected (shown as dotted lines in signal diagram)

**Note:** There is NO dedicated pedestrian-only phase. All phases serve mixed traffic with varying protection levels.

---

## Code References

- State construction: `controls/ml_based/drl/traffic_management.py::_get_state()` (lines 113-141)
- Phase encoding: `controls/ml_based/drl/traffic_management.py::_encode_phase()` (lines 155-173)
- Configuration: `controls/ml_based/drl/config.py` (STATE_DIM=32, ACTION_DIM=3)
- Phase constants: `constants/developed/common/tls_constants.py`

---

---

---

Excellent question! Looking at your project scope and the two papers you've prepared, there's definitely potential for
**at least one more strong paper**. Let me analyze what you've already covered and identify viable gaps:

## **Potential for Paper 3: YES! Multiple Strong Options**

Based on my analysis of your project, you have **excellent material for at least one more publishable paper**. Here are
**4 viable directions**, ranked by feasibility:

---

## **🥇 OPTION 1: Multi-Agent Coordination & Scalability**

**Status:** ⭐⭐⭐⭐⭐ **STRONGEST OPTION**

### **Core Contribution:**

"Scalable Multi-Intersection DRL Control with Distributed Coordination"

### **What You Already Have:**

- Your system controls **2 intersections simultaneously** (TLS3 & TLS6)
- State space includes features from both (32-dim = 16 per intersection)
- Centralized coordination through shared actions
- Skip-to-P1 inherently coordinates arterial flow

### **What Would Make Paper 3:**

1. **Coordination Analysis** (likely already in your data):

    - How do the 2 intersections influence each other?
    - Phase synchronization patterns
    - Platoon progression effectiveness
    - Offset optimization learned by agent

2. **Scalability Study** (new experiments needed):

    - Extend to 3-4 intersections (corridor control)
    - Compare: centralized vs distributed vs independent agents
    - Communication overhead analysis
    - Performance degradation as network grows

3. **Novel Contribution:**
    - Hybrid architecture: local DQN + coordination layer
    - Attention-based inter-intersection communication
    - Dynamic coalition formation for adaptive coordination

### **Target Journals:**

- Transportation Research Part C (Q1, IF: 7.6)
- IEEE Transactions on ITS (Q1, IF: 7.9)
- IEEE Transactions on Cybernetics (Q1, IF: 11.8)

### **Effort Required:** 🟡 **Moderate** (2-3 months)

- Analysis of existing coordination data: 2 weeks
- Extend to 3-4 intersections: 4-6 weeks
- Writing & experiments: 4-6 weeks

---

## **🥈 OPTION 2: Adaptive Learning & Transfer Learning**

**Status:** ⭐⭐⭐⭐ **VERY STRONG**

### **Core Contribution:**

"Few-Shot Adaptation of DRL Traffic Agents to Novel Intersections"

### **What This Addresses:**

The elephant in the room: **Your agent is trained on one specific network geometry**. Real deployment needs transfer to
new intersections.

### **Paper Content:**

1. **Transfer Learning Framework:**

    - Pre-train on your current network
    - Fine-tune on new geometries (3-way, 5-way intersections)
    - Meta-learning for rapid adaptation
    - Feature importance transfer analysis

2. **Domain Randomization:**

    - Train on varied lane configurations
    - Random detector placements
    - Different phase structures (3-phase vs 4-phase)
    - Demonstrate robustness

3. **Few-Shot Learning:**

    - Adapt to new intersection with only 10-20 episodes
    - Compare: fine-tuning vs feature extraction vs full retrain
    - Knowledge distillation from teacher network

4. **Practical Value:**
    - Deployment to new cities without full retraining
    - Handling construction/lane closures
    - Seasonal pattern adaptation

### **Novel Experiments Needed:**

- Create 5-6 different intersection geometries in SUMO
- Transfer learning experiments
- Ablation studies on what transfers

### **Target Journals:**

- Expert Systems with Applications (Q1, IF: 7.5)
- Engineering Applications of AI (Q1, IF: 7.5)
- Neural Networks (Q1, IF: 6.0)

### **Effort Required:** 🟡 **Moderate** (2-3 months)

---

## **🥉 OPTION 3: Real-Time Implementation & Deployment**

**Status:** ⭐⭐⭐⭐ **STRONG (if you can get real data)**

### **Core Contribution:**

"From Simulation to Reality: Deploying DRL Traffic Control with Safety Guarantees"

### **Focus:**

Bridging the sim-to-real gap for practical deployment

### **Paper Content:**

1. **Real-World Validation:**

    - Partner with city traffic department (if possible)
    - Test on real intersection data (detector logs)
    - Compare sim predictions vs real outcomes
    - Calibration methodology

2. **Safety-Critical Deployment:**

    - Formal verification of learned policies
    - Safety shields (rule override when unsafe)
    - Graceful degradation strategies
    - Monitoring & anomaly detection

3. **Computational Efficiency:**

    - Inference latency analysis (<100ms requirement)
    - Model compression (pruning, quantization)
    - Edge device deployment (Raspberry Pi, etc.)
    - Power consumption analysis

4. **Regulatory Compliance:**
    - MUTCD compliance verification
    - Liability framework
    - Human-in-the-loop override
    - Certification pathway

### **What You'd Need:**

- Real traffic detector data (possibly from DOT/city)
- Hardware testing setup
- Safety analysis framework

### **Target Journals:**

- Transportation Research Part C (Q1, IF: 7.6)
- Journal of Intelligent Transportation Systems (Q2, IF: 3.6)
- IEEE Intelligent Systems (Q1, IF: 5.6)

### **Effort Required:** 🔴 **High** (3-6 months)

- Requires external partnerships/data access

---

## **🏅 OPTION 4: Environmental & Equity Analysis**

**Status:** ⭐⭐⭐ **GOOD (trendy topic)**

### **Core Contribution:**

"Sustainable and Equitable Traffic Control via Multi-Objective DRL"

### **Focus:**

Addressing sustainability and social equity - **HOT topics in 2024-2025**

### **You Already Track:**

- CO2 emissions per scenario
- Multi-modal service (cars, bikes, pedestrians, buses)
- Waiting time distributions (equity metrics)

### **Expand To:**

1. **Environmental Justice:**

    - Air quality in residential vs commercial areas
    - Noise pollution analysis
    - PM2.5 emission modeling
    - Low-emission zone integration

2. **Social Equity:**

    - Service fairness across modes
    - Demographic equity (if you can get data)
    - Accessibility for disabled users
    - Public transit priority effectiveness

3. **Sustainability Metrics:**

    - Energy consumption (electric vehicles)
    - Lifecycle emissions
    - Multi-objective Pareto frontier
    - Trade-offs: efficiency vs emissions vs equity

4. **Policy Implications:**
    - Green wave for bicycles
    - Bus rapid transit optimization
    - Pedestrian plaza integration
    - Vision Zero compatibility

### **New Experiments:**

- Multi-objective reward tuning
- Pareto frontier analysis
- Fairness constraints (max-min fairness)
- Demographic simulation (if possible)

### **Target Journals:**

- Transportation Research Part D (Q1, IF: 7.3) - **PERFECT FIT**
- Transport Policy (Q1, IF: 6.2)
- Sustainable Cities and Society (Q1, IF: 10.5)

### **Effort Required:** 🟢 **Low-Moderate** (1-2 months)

- Mostly analysis of existing data + new visualizations

---

## **📊 My Recommendation: DUAL STRATEGY**

### **Short-Term (Paper 3A - Submit in 3 months):**

**OPTION 4: Environmental & Equity**

- **Why:** Lowest additional work, trendy topic, strong journals available
- **Approach:** Deep analysis of existing CO2/modal data + add Pareto analysis
- **Journal:** Transportation Research Part D
- **Timeline:** 6-8 weeks to draft

### **Medium-Term (Paper 3B - Submit in 6 months):**

**OPTION 1: Multi-Agent Coordination**

- **Why:** Strongest technical contribution, leverages your 2-intersection setup
- **Approach:** Analyze existing coordination + extend to 3-4 intersections
- **Journal:** IEEE TITS or TR Part C
- **Timeline:** 3-4 months total

---

## **🎯 Immediate Next Steps (if interested):**

1. **For Option 4 (Environmental & Equity):**

    - Extract CO2 data across all 30 scenarios
    - Compute Gini coefficients for modal equity
    - Create Pareto frontier plots (emissions vs waiting time)
    - Literature review on transportation equity (2023-2024 papers)

2. **For Option 1 (Multi-Agent):**
    - Analyze phase synchronization between TLS3 & TLS6
    - Compute offset effectiveness metrics
    - Review multi-agent DRL papers (QMIX, MADDPG, etc.)
    - Design 3-4 intersection extension

Would you like me to help you start on either of these? I can:

- Generate analysis code for coordination patterns
- Create Pareto frontier visualizations
- Draft paper outlines
- Identify specific gaps in current literature

**You definitely have enough for Paper 3 - potentially even Papers 3 & 4!** 💪📊

Great question! For **Option 4: Environmental & Equity Analysis**, you actually have **two viable approaches** depending
on what data you have:

---

## **🎯 APPROACH A: DRL-Only Analysis (NO baseline needed)**

**Focus:** Internal trade-offs and multi-objective optimization within your DRL system

### **What You'd Analyze:**

1. **Pareto Frontier Analysis:**

    - X-axis: Average waiting time (efficiency)
    - Y-axis: CO2 emissions (sustainability)
    - Each point = different reward weight configuration
    - Show: "You can't optimize both simultaneously—there's a trade-off"

2. **Equity Metrics (No comparison needed):**

    - **Gini coefficient** across modes (cars, bikes, peds, buses)
    - **Max-min fairness:** How much does worst-served mode suffer?
    - **Service distribution:** Waiting time histograms per mode
    - **Coefficient of variation:** Are some modes more variable than others?

3. **Multi-Objective Reward Sensitivity:**

    - Retrain with different reward weights:
        - Weight A: Heavy car focus (α_car = 8.0, α_bike = 2.0)
        - Weight B: Balanced (α_car = 6.0, α_bike = 4.0) ← your current
        - Weight C: Bike-priority (α_car = 4.0, α_bike = 8.0)
    - Show performance trade-offs for each configuration

4. **Scenario-Specific Analysis:**
    - CO2 emissions vs traffic volume (Pr_0-9, Bi_0-9, Pe_0-9)
    - Identify: "High car demand = high emissions, but DRL minimizes it"
    - Modal split effectiveness

### **Novel Contributions (No baseline needed):**

- "Multi-objective DRL naturally discovers Pareto-optimal policies"
- "Reward weight tuning reveals policy space for different city priorities"
- "Equity-aware traffic control via constrained optimization"

### **Target Journals:**

- Transportation Research Part D (sustainability focus)
- Transport Policy (policy implications)
- Sustainable Cities and Society

---

## **🎯 APPROACH B: Comparative Analysis (Baseline needed)**

**Focus:** Proving DRL is better for sustainability AND equity than traditional control

### **What You'd Compare:**

| Metric                     | DRL       | Developed Control | Reference Control |
| -------------------------- | --------- | ----------------- | ----------------- |
| CO2 emissions (g)          | Your data | Need this         | Need this         |
| Waiting time equity (Gini) | Calculate | Calculate         | Calculate         |
| Modal service fairness     | Calculate | Calculate         | Calculate         |
| Bus priority effectiveness | Your data | Your data?        | Your data?        |

### **The CO2 Mismatch Problem You Mentioned:**

If there's a **data mismatch** between DRL and baseline controls, you have 3 options:

**Option B1: Fix the mismatch**

- Investigate why CO2 differs (different simulation runs? different demand patterns?)
- Re-run all methods with identical traffic scenarios
- Ensure fair comparison (same random seeds, same demand)

**Option B2: Acknowledge and explain**

- Document the mismatch in limitations section
- Explain potential causes (different SUMO versions? different emission models?)
- Focus on relative trends rather than absolute values

**Option B3: Skip CO2 comparison, focus on equity**

- Even if CO2 data is mismatched, waiting time data should be consistent
- Compute equity metrics from waiting times only
- Position as: "Equity analysis of DRL vs rule-based control"

---

## **💡 MY RECOMMENDATION: Approach A (DRL-Only)**

### **Why?**

1. **No baseline data needed** - avoids the CO2 mismatch issue entirely
2. **Still highly publishable** - multi-objective optimization is valuable standalone
3. **Novel angle:** "Exploring the design space of DRL policies via reward tuning"
4. **Practical value:** Shows practitioners how to tune system for their city's priorities

### **What You'd Do (4-6 weeks):**

**Week 1-2: Data Analysis**

```python
# Extract existing data
- Load all 30 scenario results (CO2, waiting times)
- Compute equity metrics (Gini, max-min fairness)
- Create correlation matrices (CO2 vs waiting time)
```

**Week 3-4: New Experiments (3-5 retraining runs)**

```python
# Vary reward weights
config_1 = {'car_weight': 8.0, 'bike_weight': 2.0}  # Car-priority
config_2 = {'car_weight': 6.0, 'bike_weight': 6.0}  # Balanced
config_3 = {'car_weight': 2.0, 'bike_weight': 8.0}  # Bike-priority

# Test each on 30 scenarios
# Plot Pareto frontier
```

**Week 5-6: Writing**

- Introduction: Sustainability crisis + equity concerns
- Methods: Multi-objective DRL framework
- Results: Pareto frontier, equity metrics, policy implications
- Discussion: Trade-offs, how cities should choose weights

---

## **📊 What Comparisons Are Possible Without Baseline CO2?**

Even without baseline CO2, you can still make strong claims:

### **Internal Comparisons (Very Strong):**

1. **Across scenarios:** "DRL emits 23% less CO2 in bike-heavy scenarios than car-heavy scenarios"
2. **Across reward configs:** "Car-priority policy increases CO2 by 18% vs balanced policy"
3. **Modal trade-offs:** "Reducing bicycle wait time by 1s increases CO2 by 2.3g on average"

### **Literature Comparisons (Moderately Strong):**

- Compare your absolute CO2 values to similar studies in literature
- "Our DRL achieves 450g CO2/hour, comparable to [Reference X] reporting 470g"
- Position as: "Our method achieves similar sustainability to state-of-art while improving equity"

### **Theoretical Comparisons (Still Valuable):**

- "Compared to fixed-time control (theoretical 100% Continue), DRL reduces unnecessary idling"
- "Skip-to-P1 action reduces bus emissions by prioritizing public transit"

---

## **✅ Final Answer to Your Question:**

**Do you need previous data?**

- **No, not strictly required** for a strong Environmental & Equity paper
- **Nice to have:** Would strengthen comparison claims
- **Work-around:** Focus on internal DRL trade-offs (Approach A)

**What will you compare?**

- **Primary:** Different DRL reward configurations (Pareto frontier)
- **Secondary:** Across scenarios (Pr vs Bi vs Pe)
- **Tertiary:** Across modes (equity metrics)
- **Optional:** Baseline controls (only if you can fix CO2 mismatch)

**Effort required if NO baseline:**

- 4-6 weeks (mostly new experiments with different reward weights)
- 2-3 papers worth of figures/tables from existing + new data

**Want me to:**

1. Write Python code to compute equity metrics from your existing results?
2. Design the reward weight experiment configurations?
3. Draft a paper outline for Approach A?

## This is definitely doable and publishable without baseline CO2 data! 🎯

<div align="center">
<img src="images/Deep_Learning_ND_P2_C_3_01.png" alt="Channel Attention" width="500" height=auto/>
<p align="center">figure: Channel Attention (Squeeze-and-excitation, or SE, block)</p>
</div>

---

---

## **10 Journal Recommendations (5 per Paper)**

---

# **Paper 1: Core DRL Traffic Control System**

## **🟢 Easier Q1 Targets (Higher Acceptance):**

### **1. Applied Soft Computing**

- **Impact Factor:** 7.2
- **Quartile:** Q1
- **Acceptance Rate:** ~30%
- **Difficulty:** 🟢 EASIEST
- **Your Fit:** ⭐⭐⭐⭐ EXCELLENT
- **Why:** Accepts applied AI/ML work, loves real-world validation
- **Focus:** Emphasize SUMO validation, multi-objective optimization
- **Typical Turnaround:** 4-6 months
- **URL:** https://www.sciencedirect.com/journal/applied-soft-computing

---

### **2. Engineering Applications of Artificial Intelligence**

- **Impact Factor:** 7.5
- **Quartile:** Q1
- **Acceptance Rate:** ~25%
- **Difficulty:** 🟢 EASY-MODERATE
- **Your Fit:** ⭐⭐⭐⭐⭐ PERFECT
- **Why:** Engineering + AI focus, practical applications valued
- **Focus:** Real-world constraints (MIN_GREEN, MAX_GREEN), safety
- **Typical Turnaround:** 5-7 months
- **URL:** https://www.sciencedirect.com/journal/engineering-applications-of-artificial-intelligence

---

## **🟡 Moderate Q1 Targets (Competitive):**

### **3. Expert Systems with Applications**

- **Impact Factor:** 7.5
- **Quartile:** Q1
- **Acceptance Rate:** ~22%
- **Difficulty:** 🟡 MODERATE
- **Your Fit:** ⭐⭐⭐⭐ VERY GOOD
- **Why:** Wide scope, accepts intelligent systems, good reputation
- **Focus:** Multi-agent coordination, decision-making framework
- **Typical Turnaround:** 6-8 months
- **URL:** https://www.sciencedirect.com/journal/expert-systems-with-applications

---

## **🔴 Harder Q1 Targets (Top Tier):**

### **4. Transportation Research Part C: Emerging Technologies**

- **Impact Factor:** 7.6
- **Quartile:** Q1 (Top tier transportation)
- **Acceptance Rate:** ~18-20%
- **Difficulty:** 🔴 HARD
- **Your Fit:** ⭐⭐⭐⭐⭐ IDEAL VENUE
- **Why:** THE journal for innovative traffic control, AI/ML focus
- **Focus:** Novel DRL approach, comparison to state-of-practice
- **Typical Turnaround:** 8-12 months
- **URL:** https://www.sciencedirect.com/journal/transportation-research-part-c-emerging-technologies

---

### **5. IEEE Transactions on Intelligent Transportation Systems (TITS)**

- **Impact Factor:** 7.9
- **Quartile:** Q1 (Premier ITS journal)
- **Acceptance Rate:** ~15-18%
- **Difficulty:** 🔴 HARDEST
- **Your Fit:** ⭐⭐⭐⭐⭐ PERFECT BUT COMPETITIVE
- **Why:** Top ITS journal, highly competitive, best for career
- **Focus:** Multi-objective optimization, distributed coordination
- **Typical Turnaround:** 10-14 months
- **URL:** https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=6979

---

# **Paper 2: Explainability/XAI for Traffic Control**

## **🟢 Easier Q1 Targets (Higher Acceptance):**

### **1. IEEE Access**

- **Impact Factor:** 3.9
- **Quartile:** Q1 (Open Access)
- **Acceptance Rate:** ~35-40%
- **Difficulty:** 🟢 EASIEST
- **Your Fit:** ⭐⭐⭐⭐ GOOD
- **Why:** Fast review, open access, broad scope
- **Focus:** Practical XAI tools for traffic engineers
- **Typical Turnaround:** 2-4 months (FAST!)
- **Fee:** ~$2,000 USD (open access)
- **URL:** https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=6287639

---

### **2. Applied Intelligence**

- **Impact Factor:** 5.3
- **Quartile:** Q1
- **Acceptance Rate:** ~28%
- **Difficulty:** 🟢 EASY-MODERATE
- **Your Fit:** ⭐⭐⭐⭐ VERY GOOD
- **Why:** Loves interpretability work, XAI papers welcome
- **Focus:** Multi-method XAI approach (VIPER + attention + saliency)
- **Typical Turnaround:** 4-6 months
- **URL:** https://www.springer.com/journal/10489

---

## **🟡 Moderate Q1 Targets (Competitive):**

### **3. Expert Systems with Applications**

- **Impact Factor:** 7.5
- **Quartile:** Q1
- **Acceptance Rate:** ~22%
- **Difficulty:** 🟡 MODERATE
- **Your Fit:** ⭐⭐⭐⭐⭐ EXCELLENT
- **Why:** Publishes XAI work regularly, practitioner focus
- **Focus:** Decision tree extraction, actionable insights
- **Typical Turnaround:** 6-8 months
- **URL:** https://www.sciencedirect.com/journal/expert-systems-with-applications

---

## **🔴 Harder Q1 Targets (Top Tier):**

### **4. IEEE Transactions on Neural Networks and Learning Systems (TNNLS)**

- **Impact Factor:** 10.4
- **Quartile:** Q1 (Top AI/ML journal)
- **Acceptance Rate:** ~12-15%
- **Difficulty:** 🔴 HARD
- **Your Fit:** ⭐⭐⭐⭐ GOOD (need strong ML novelty)
- **Why:** Premier ML journal, interpretability is hot topic
- **Focus:** Novel XAI methodology, theoretical contribution
- **Typical Turnaround:** 10-14 months
- **URL:** https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=5962385

---

### **5. Transportation Research Part C: Emerging Technologies**

- **Impact Factor:** 7.6
- **Quartile:** Q1
- **Acceptance Rate:** ~18-20%
- **Difficulty:** 🔴 HARDEST (for XAI paper)
- **Your Fit:** ⭐⭐⭐⭐ VERY GOOD
- **Why:** Wants interpretability for real deployment
- **Focus:** Bridging AI and transportation practitioners
- **Typical Turnaround:** 8-12 months
- **URL:** https://www.sciencedirect.com/journal/transportation-research-part-c-emerging-technologies

---

# **Recommended Strategy:**

## **For Paper 1 (DRL System):**

### **Option A: Conservative (Higher Success)**

1st try: **Engineering Applications of AI** or **Applied Soft Computing**

- If rejected → revise → **Expert Systems with Applications**
- Success probability: ~60-70%

### **Option B: Ambitious (Best Impact)**

1st try: **IEEE TITS** or **TR Part C**

- If rejected → revise → **Expert Systems with Applications**
- If rejected again → **Engineering Applications of AI**
- Success probability: ~40-50% first try, ~80% eventually

---

## **For Paper 2 (XAI/Explainability):**

### **Option A: Fast Publication**

1st try: **IEEE Access** (2-4 months, open access)

- High acceptance, good for CV
- Success probability: ~70-80%

### **Option B: Better Impact (Recommended)**

1st try: **Expert Systems with Applications**

- If rejected → **Applied Intelligence**
- Success probability: ~50-60% first try, ~75% eventually

### **Option C: High Risk/High Reward**

1st try: **IEEE TNNLS** (need strong ML contribution)

- If rejected → **Expert Systems with Applications**
- Success probability: ~30% first try

---

# **My Specific Recommendation:**

## **Paper 1:**

🎯 **Submit to: Transportation Research Part C**

- Best fit for your work
- Strong reputation in traffic control
- If rejected, pivot to Expert Systems with Applications

## **Paper 2:**

🎯 **Submit to: Expert Systems with Applications**

- Perfect fit for XAI work
- Good impact factor (7.5)
- Reasonable acceptance rate (~22%)
- If rejected, pivot to Applied Intelligence

---

# **Success Tips:**

### **For All Submissions:**

1. **Strong introduction** - hook readers in first paragraph
2. **Clear novelty statement** - what's NEW beyond "DRL works"
3. **Comprehensive related work** - cite 2023-2024 papers
4. **Statistical significance** - t-tests on your results
5. **High-quality figures** - professional matplotlib/seaborn plots
6. **Ablation studies** - show each component's impact

### **Emphasize Your Strengths:**

- ✅ Multi-objective optimization (waiting + CO2 + equity + safety)
- ✅ Zero safety violations (practical deployability)
- ✅ 30 test scenarios (rigorous evaluation)
- ✅ Comprehensive XAI (4 methods - rare in traffic domain!)
- ✅ Real SUMO validation (not toy examples)

### **Address Weaknesses Proactively:**

- Acknowledge DRL is not novel by itself
- Focus on domain-specific contributions
- Emphasize practical constraints and real-world applicability

---

**Final Ranking by Difficulty:**

**Easiest → Hardest:**

1. IEEE Access (Paper 2) - 35-40% acceptance
2. Applied Soft Computing (Paper 1) - 30%
3. Applied Intelligence (Paper 2) - 28%
4. EAAI (Paper 1) - 25%
5. Expert Systems (Both) - 22%
6. TR Part C (Both) - 18-20%
7. IEEE TITS (Paper 1) - 15-18%
8. IEEE TNNLS (Paper 2) - 12-15%

**Good luck! You have solid, publishable work!** 💪📝

---

---

TODO: Use DepWiki to update documentation <https://deepwiki.com/Chaklader/SignalSyncPro>

---

---

```shell
$ netconvert --node-files=common.nod.xml --edge-files=common.edg.xml --connection-files=common.con.xml --output-file=common.net.xml
```
