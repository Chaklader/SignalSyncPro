# CLAUDE.md - AI Assistant Guide for SignalSyncPro

**Last Updated**: 2025-12-04
**Version**: 1.0.0

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Repository Structure](#repository-structure)
4. [Key Components](#key-components)
5. [Development Workflows](#development-workflows)
6. [Coding Conventions](#coding-conventions)
7. [Common Tasks](#common-tasks)
8. [Architecture Patterns](#architecture-patterns)
9. [Testing Strategy](#testing-strategy)
10. [Important Notes](#important-notes)

---

## Project Overview

**SignalSyncPro** is an advanced traffic signal control system using Deep Reinforcement Learning (DQN) to optimize traffic flow at intersections. The system learns to minimize vehicle waiting times while maintaining safe and efficient multi-modal traffic flow.

### Core Capabilities

- **Intelligent Control**: DQN-based agent with prioritized experience replay
- **Multi-Modal Support**: Cars, bicycles, buses, and pedestrians
- **Multi-Objective Optimization**: Balances waiting time, emissions, equity, and safety
- **Comprehensive Testing**: 30 standardized test scenarios
- **Explainable AI**: Multiple XAI techniques (VIPER, attention, saliency, counterfactuals)
- **Baseline Comparison**: Rule-based "developed" control for benchmarking

### Project Goals

1. Research-grade DRL traffic control implementation
2. Publication-ready with comprehensive evaluation
3. Interpretable decisions through XAI analysis
4. Production-ready architecture with safety guarantees

---

## Tech Stack

### Core Technologies

- **Python**: 3.10.18 (conda environment)
- **Deep Learning**: PyTorch 2.8.0
- **Traffic Simulation**: SUMO 1.24.0 (Eclipse SUMO)
- **Data Processing**: NumPy 2.2.6, Pandas 2.3.3
- **Visualization**: Matplotlib 3.10.6, Seaborn 0.13.2
- **ML Tools**: scikit-learn 1.7.2, TensorBoard 2.20.0

### Development Tools

- **Code Quality**: Black 25.9.0, Ruff 0.14.0
- **Environment**: conda (environment.yml)
- **Logging**: Built-in logging, TensorBoard
- **Version Control**: Git

### Key Dependencies

```yaml
# From environment.yml
- torch==2.8.0          # Deep learning
- sumolib==1.24.0       # SUMO Python library
- traci==1.24.0         # SUMO TraCI interface
- numpy==2.2.6          # Numerical computing
- pandas==2.3.3         # Data manipulation
- matplotlib==3.10.6    # Plotting
- seaborn==0.13.2       # Statistical visualization
- scikit-learn==1.7.2   # ML utilities
- tensorboard==2.20.0   # Training visualization
- black==25.9.0         # Code formatting
- ruff==0.14.0          # Linting
```

---

## Repository Structure

```
SignalSyncPro/
│
├── analysis/                          # XAI and analysis tools
│   └── drl/single_agent/
│       ├── attention_analysis.py      # Attention mechanism analysis
│       ├── saliency_analysis.py       # Saliency map generation
│       ├── viper_extraction.py        # Decision tree extraction
│       ├── counterfactual_generator.py # Counterfactual explanations
│       ├── bicycle_spike_analysis.py  # Specialized bicycle analysis
│       ├── safety_analysis.py         # Safety violation analysis
│       └── run_all_analyses.py        # Run all XAI analyses
│
├── common/                            # Shared utilities
│   ├── utils.py                       # General utilities
│   └── sumo_utils.py                  # SUMO environment setup
│
├── constants/                         # Configuration constants
│   ├── constants.py                   # Global constants
│   └── developed/common/
│       ├── drl_tls_constants.py       # DRL traffic light constants
│       ├── tls_constants.py           # Phase definitions
│       └── phase_transitions.py       # Phase transition rules
│
├── controls/                          # Traffic control implementations
│   ├── ml_based/drl/                  # DRL control
│   │   ├── agent.py                   # DQN Agent with PER
│   │   ├── neural_network.py          # Q-network architecture
│   │   ├── replay_buffer.py           # Prioritized replay buffer
│   │   ├── config.py                  # DRL hyperparameters
│   │   ├── reward.py                  # Reward function
│   │   └── traffic_management.py      # SUMO environment wrapper
│   └── rule_based/developed/          # Rule-based baseline
│       ├── main.py                    # Main control logic
│       ├── pedestrian_phase.py        # Pedestrian phase handling
│       └── utils.py                   # Helper functions
│
├── detectors/                         # Detector definitions
│   └── developed/
│       ├── common/detectors.py        # Common detector setup
│       └── drl/detectors.py           # DRL-specific detectors
│
├── infrastructure/                    # SUMO network files
│   └── developed/
│       ├── common/                    # Shared infrastructure
│       └── drl/
│           ├── single_agent/          # Single-agent network
│           └── multi_agent/           # Multi-agent network
│
├── route_generator/                   # Traffic generation
│   ├── traffic_config.py              # Traffic configuration
│   └── developed/common/
│       └── generate_routes.py         # Route generation logic
│
├── run/                               # Execution scripts
│   ├── training/
│   │   └── train_drl.py               # Main training script
│   └── testing/
│       ├── test_drl.py                # DRL testing
│       └── test_developed.py          # Rule-based testing
│
├── scripts/                           # Shell scripts
│   ├── drl/single_agent/
│   │   ├── run/
│   │   │   ├── run_training.sh        # Start training
│   │   │   └── run_testing.sh         # Start testing
│   │   ├── stop/
│   │   │   ├── stop_training.sh       # Stop training
│   │   │   └── stop_testing.sh        # Stop testing
│   │   ├── analyze/
│   │   │   └── run_all_analysis.sh    # Run XAI analyses
│   │   ├── tables/
│   │   │   └── create_testing_tables.sh # Generate result tables
│   │   └── qa/
│   │       └── check_training.sh      # QA checks
│   ├── rule_based/
│   │   └── run_developed_test.sh      # Test baseline
│   ├── format_and_lint.sh             # Code quality
│   └── clean_logs.sh                  # Cleanup
│
├── configurations/                    # SUMO config files
│   └── developed/
│       └── drl/single_agent/
│           ├── signal_sync.sumocfg    # SUMO configuration
│           └── signal_sync_gui_settings.cfg
│
├── logs/                              # Training/testing logs (gitignored)
├── models/                            # Saved models (gitignored)
├── results/                           # Test results (gitignored)
├── images/                            # Documentation images
├── Tables/                            # Result tables
│   ├── Table_Single_Agent.md
│   └── Table_Multi_Agent.md
│
├── .env                               # Environment variables
├── .gitignore                         # Git ignore rules
├── environment.yml                    # Conda environment
├── README.md                          # User documentation
└── CLAUDE.md                          # This file (AI assistant guide)
```

---

## Key Components

### 1. DRL Agent (`controls/ml_based/drl/agent.py`)

**Purpose**: DQN agent with advanced features

**Key Features**:
- Double DQN to reduce overestimation bias
- Prioritized Experience Replay (PER)
- Soft target network updates (τ=0.005)
- Multi-layer clipping (rewards, Q-values, loss, gradients)
- Experience replay buffer (50,000 capacity)

**State Space**: 32-dimensional
- 2 intersections (TLS3, TLS6) × 16 features each
- Features: phase one-hot, duration, detectors, bus info, sim time

**Action Space**: 3 actions
- 0: Continue (maintain current phase)
- 1: Skip2P1 (skip to Phase 1 - major arterial)
- 2: Next (advance to next phase in sequence)

**Critical Methods**:
```python
select_action(state, epsilon)  # ε-greedy action selection
update(batch_size)             # Train on batch from replay buffer
save(path)                     # Save model checkpoint
load(path)                     # Load model checkpoint
```

**Location**: `controls/ml_based/drl/agent.py:1`

### 2. Traffic Management (`controls/ml_based/drl/traffic_management.py`)

**Purpose**: SUMO environment wrapper (Gym-like interface)

**Key Responsibilities**:
- SUMO simulation lifecycle (launch, connect, close)
- State observation from TraCI
- Action execution (phase transitions)
- Reward calculation
- Safety monitoring

**Critical Methods**:
```python
reset()              # Initialize new episode
step(action)         # Execute action, return (state, reward, done, info)
close()              # Terminate SUMO
_get_state()         # Extract 32-dim state vector
_calculate_reward()  # Multi-objective reward
```

**Location**: `controls/ml_based/drl/traffic_management.py:1`

### 3. Reward Function (`controls/ml_based/drl/reward.py`)

**Purpose**: Multi-objective optimization signal

**Components** (from `config.py:30-51`):
```python
# Reward weights
ALPHA_WAIT = 2.5           # Waiting time (primary objective)
ALPHA_EMISSION = 0.05       # CO2 emissions
ALPHA_EQUITY = 0.5          # Modal equity (fairness)
ALPHA_SAFETY = 2.0          # Safety violations
ALPHA_BLOCKED = 0.1         # Blocked vehicles
ALPHA_SKIP_OVERUSE = 0.02   # Skip2P1 overuse penalty
ALPHA_STABILITY = 0.12      # Phase stability
ALPHA_NEXT_BONUS = 2.0      # Next action bonus

# Modal weights
WEIGHT_CAR = 1.3
WEIGHT_BICYCLE = 1.0
WEIGHT_PEDESTRIAN = 1.0
WEIGHT_BUS = 2.0
```

**Formula**:
```
R = -α_wait * weighted_waiting_time
    - α_emission * CO2
    + α_equity * equity_score
    - α_safety * violations
    - α_blocked * blocked_vehicles
    + α_next_bonus * next_bonus
    + α_stability * stability_bonus
    + skip2p1_effectiveness
```

**Location**: `controls/ml_based/drl/reward.py:1`

### 4. Configuration (`controls/ml_based/drl/config.py`)

**Purpose**: Central hyperparameter configuration

**Key Parameters**:
```python
# Network architecture
STATE_DIM = 32
ACTION_DIM = 3
HIDDEN_LAYERS = [256, 256, 128]

# Learning parameters
LEARNING_RATE = 0.00001
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_END = 0.05
EPSILON_DECAY = 0.98

# Replay buffer
BUFFER_SIZE = 50000
BATCH_SIZE = 64
MIN_BUFFER_SIZE = 1000

# Phase constraints
phase_min_green_time = {1: 8s, 5: 3s, 9: 5s, 13: 2s}
max_green_time = {1: 44s, 5: 15s, 9: 24s, 13: 12s}
```

**Location**: `controls/ml_based/drl/config.py:1`

### 5. Training Script (`run/training/train_drl.py`)

**Purpose**: Main training loop

**Key Features**:
- Episode-based training (100 episodes default)
- Checkpoint saving (every 10 episodes)
- Comprehensive logging
- Resume from checkpoint support
- TensorBoard integration

**Usage**:
```bash
# Start training
./scripts/drl/single_agent/run/run_training.sh

# Resume from checkpoint
./scripts/drl/single_agent/run/run_training.sh models/training_20241019/checkpoint_50.pth
```

**Location**: `run/training/train_drl.py:1`

### 6. Testing Script (`run/testing/test_drl.py`)

**Purpose**: Systematic evaluation on 30 test scenarios

**Test Scenarios**:
- **Pr_0 to Pr_9**: Varying car volumes (100-1000/hr)
- **Bi_0 to Bi_9**: Varying bicycle volumes (100-1000/hr)
- **Pe_0 to Pe_9**: Varying pedestrian volumes (100-1000/hr)

**Metrics Collected**:
- Average waiting times (car, bicycle, pedestrian, bus)
- Total CO2 emissions
- Safety violations (headway, distance, red light)
- Phase statistics
- Action distributions

**Location**: `run/testing/test_drl.py:1`

---

## Development Workflows

### 1. Training a New Model

```bash
# 1. Set up environment
export SUMO_HOME="/path/to/sumo"
conda activate sumo

# 2. Start training
./scripts/drl/single_agent/run/run_training.sh

# 3. Monitor progress
tail -100f training.log

# 4. Check if running
ps aux | grep train_drl.py

# 5. Stop if needed
./scripts/drl/single_agent/stop/stop_training.sh
```

**Output**:
- Models: `models/training_YYYYMMDD_HHMMSS/`
- Logs: `training.log`
- Checkpoints: Every 10 episodes

### 2. Testing a Trained Model

```bash
# 1. Test on all 30 scenarios
./scripts/drl/single_agent/run/run_testing.sh models/training_20241019/final_model.pth

# 2. Monitor progress
tail -100f testing.log

# 3. View results
cat results/drl_test_results.csv
```

**Output**:
- Results: `results/drl_test_results.csv`
- Logs: `testing.log`

### 3. Baseline Testing

```bash
# Test rule-based control
./scripts/rule_based/run_developed_test.sh

# Results in: results/developed_test_results.csv
```

### 4. Running XAI Analysis

```bash
# Run all XAI analyses
./scripts/drl/single_agent/analyze/run_all_analysis.sh models/training_20241019/final_model.pth

# Individual analyses
python analysis/drl/single_agent/attention_analysis.py --model <path>
python analysis/drl/single_agent/saliency_analysis.py --model <path>
python analysis/drl/single_agent/viper_extraction.py --model <path>
python analysis/drl/single_agent/counterfactual_generator.py --model <path>
```

**Output**:
- Visualizations: `images/2/`
- Reports: Various `.txt` and `.png` files

### 5. Code Quality Checks

```bash
# Format and lint code
./scripts/format_and_lint.sh

# This runs:
# - black (formatting)
# - ruff (linting)
```

### 6. Cleaning Up

```bash
# Clean logs and results
./scripts/clean_logs.sh

# This removes:
# - logs/
# - results/
# - *.log files
# - *.csv files
```

---

## Coding Conventions

### Python Style

**Follow PEP 8**:
- Snake_case for variables and functions
- PascalCase for classes
- UPPER_CASE for constants
- 4-space indentation
- Max line length: 88 characters (Black default)

**Example**:
```python
# Good
def calculate_waiting_time(vehicle_id: str) -> float:
    """Calculate waiting time for a vehicle."""
    pass

class TrafficManagement:
    """SUMO environment wrapper."""
    pass

MAX_GREEN_TIME = 44

# Bad
def CalculateWaitingTime(vehicleID):  # Wrong case
    pass
```

### Module Structure

**Standard Pattern**:
```python
"""
Module docstring explaining purpose and key functionality.
"""

# Standard library imports
import os
import sys

# Project root setup (for run/ scripts)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# SUMO environment setup
from common.sumo_utils import setup_environment
setup_environment()

# Third-party imports
import numpy as np
import torch

# Local imports
from controls.ml_based.drl.agent import DQNAgent
from constants.constants import NUM_EPISODES_TRAIN
```

### Docstrings

**Use Google-style docstrings**:
```python
def step(self, action: int) -> tuple:
    """
    Execute action and advance simulation by one step.

    Args:
        action (int): Action to take (0=Continue, 1=Skip2P1, 2=Next)

    Returns:
        tuple: (next_state, reward, done, info)
            - next_state (np.ndarray): 32-dim state vector
            - reward (float): Reward signal
            - done (bool): Episode termination flag
            - info (dict): Additional metrics

    Raises:
        RuntimeError: If SUMO connection is lost
    """
    pass
```

### Type Hints

**Use type hints for new code**:
```python
from typing import Dict, List, Tuple, Optional

def get_state(self) -> np.ndarray:
    """Get current state vector."""
    pass

def calculate_reward(self, info: Dict[str, float]) -> float:
    """Calculate reward from metrics."""
    pass

def select_action(self, state: np.ndarray, epsilon: float) -> int:
    """Select action using ε-greedy policy."""
    pass
```

### Logging

**Use consistent logging**:
```python
import logging

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Use appropriate levels
logger.debug("Detailed debug information")
logger.info("Episode 50 completed")
logger.warning("High CO2 emissions detected")
logger.error("SUMO connection failed")
```

### File Paths

**Use proper path handling**:
```python
import os

# Good - platform-independent
config_path = os.path.join("configurations", "developed", "drl", "single_agent", "signal_sync.sumocfg")
model_dir = os.path.join("models", "training_20241019")

# Bad - hardcoded separators
config_path = "configurations/developed/drl/single_agent/signal_sync.sumocfg"  # Unix only
```

### Constants

**Define constants in appropriate files**:
```python
# constants/constants.py - Global constants
NUM_EPISODES_TRAIN = 100
SIMULATION_LIMIT_TRAIN = 3600
UPDATE_FREQUENCY = 1

# constants/developed/common/drl_tls_constants.py - DRL-specific
TLS_IDS = ["3", "6"]
p1_main_green = 1
p2_main_green = 5
p3_main_green = 9
p4_main_green = 13
```

---

## Common Tasks

### Task 1: Modifying Hyperparameters

**File**: `controls/ml_based/drl/config.py`

```python
class DRLConfig:
    # Network architecture
    HIDDEN_LAYERS = [256, 256, 128]  # Change layer sizes

    # Learning rate
    LEARNING_RATE = 0.00001  # Adjust learning speed

    # Exploration
    EPSILON_START = 1.0      # Initial exploration
    EPSILON_DECAY = 0.98     # Decay rate

    # Reward weights
    ALPHA_WAIT = 2.5         # Waiting time importance
    ALPHA_EMISSION = 0.05    # CO2 importance
```

**After changing**: Retrain from scratch or document changes for paper.

### Task 2: Adding a New Test Scenario

**File**: `route_generator/traffic_config.py`

```python
def get_traffic_config(mode='training', scenario=None):
    if scenario == 'MyScenario_0':
        return {
            'privateCar': 500,
            'bicycle': 300,
            'pedestrian': 200,
            'bus': 50,
        }
```

**Then update test script**: `run/testing/test_drl.py`

### Task 3: Modifying State Space

**Files to update**:
1. `controls/ml_based/drl/traffic_management.py::_get_state()`
2. `controls/ml_based/drl/config.py::STATE_DIM`
3. Retrain all models (incompatible with old checkpoints)

**Example**:
```python
# In traffic_management.py
def _get_state(self):
    # Add new feature
    new_feature = self._get_new_metric()
    state = np.concatenate([existing_state, [new_feature]])
    return state

# In config.py
STATE_DIM = 33  # Increment
```

### Task 4: Adding a New Reward Component

**File**: `controls/ml_based/drl/reward.py`

```python
class RewardCalculator:
    def calculate(self, metrics):
        # Add new component
        new_reward = self._calculate_new_component(metrics)

        total_reward = (
            self.waiting_reward +
            self.emission_reward +
            new_reward  # Add here
        )
        return total_reward
```

**Update config**: `controls/ml_based/drl/config.py`
```python
ALPHA_NEW_COMPONENT = 0.1
```

### Task 5: Creating a New Analysis Script

**Template**: `analysis/drl/single_agent/my_analysis.py`

```python
"""
My custom analysis script
"""

import os
import sys
import argparse

# Setup paths
project_root = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from controls.ml_based.drl.agent import DQNAgent
from controls.ml_based.drl.config import DRLConfig

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='Path to model')
    args = parser.parse_args()

    # Load model
    agent = DQNAgent(DRLConfig.STATE_DIM, DRLConfig.ACTION_DIM)
    agent.load(args.model)

    # Your analysis here
    print("Running custom analysis...")

if __name__ == '__main__':
    main()
```

---

## Architecture Patterns

### 1. SUMO Integration Pattern

**All scripts follow this pattern**:

```python
# 1. Setup environment
from common.sumo_utils import setup_environment
setup_environment()

# 2. Import SUMO after setup
import traci

# 3. Launch SUMO
sumo_cmd = ["sumo", "-c", config_file, "--remote-port", "8816"]
subprocess.Popen(sumo_cmd)

# 4. Connect TraCI
traci.init(8816)

# 5. Simulation loop
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

# 6. Cleanup
traci.close()
```

**Location**: `controls/ml_based/drl/traffic_management.py:reset()` and `close()`

### 2. Episode Training Loop

```python
for episode in range(NUM_EPISODES):
    # Reset environment
    state = env.reset()
    episode_reward = 0
    done = False

    # Episode loop
    while not done:
        # Select action
        action = agent.select_action(state, epsilon)

        # Execute action
        next_state, reward, done, info = env.step(action)

        # Store transition
        agent.remember(state, action, reward, next_state, done)

        # Update agent
        if len(agent.memory) > MIN_BUFFER_SIZE:
            loss = agent.update(BATCH_SIZE)

        # Update state
        state = next_state
        episode_reward += reward

    # Decay epsilon
    epsilon *= EPSILON_DECAY

    # Save checkpoint
    if episode % SAVE_FREQUENCY == 0:
        agent.save(f'checkpoint_{episode}.pth')
```

**Location**: `run/training/train_drl.py:main()`

### 3. Testing Loop

```python
scenarios = ['Pr_0', 'Pr_1', ..., 'Pe_9']
results = []

for scenario in scenarios:
    # Generate routes
    traffic_config = get_traffic_config('test', scenario)
    generate_routes(traffic_config)

    # Reset environment
    state = env.reset()
    done = False
    metrics = defaultdict(float)

    # Test loop (no exploration)
    while not done:
        action = agent.select_action(state, epsilon=0.0)  # Greedy
        state, reward, done, info = env.step(action)

        # Accumulate metrics
        for key, value in info.items():
            metrics[key] += value

    # Save results
    results.append({
        'scenario': scenario,
        'avg_waiting_car': metrics['avg_waiting_car'],
        'co2': metrics['co2_total'],
        # ... more metrics
    })

# Export to CSV
pd.DataFrame(results).to_csv('results.csv')
```

**Location**: `run/testing/test_drl.py:main()`

### 4. Configuration Management

**Hierarchical configuration**:

```
constants/
  ├── constants.py                    # Global (training episodes, etc.)
  └── developed/common/
      ├── drl_tls_constants.py        # DRL-specific (TLS IDs, phases)
      ├── tls_constants.py            # Phase definitions
      └── phase_transitions.py        # Transition rules

controls/ml_based/drl/
  └── config.py                       # DRL hyperparameters
```

**Import pattern**:
```python
from constants.constants import NUM_EPISODES_TRAIN
from constants.developed.common.drl_tls_constants import TLS_IDS
from controls.ml_based.drl.config import DRLConfig
```

---

## Testing Strategy

### Test Scenarios (30 total)

**Structure**: `[Category]_[Level]`

**Categories**:
- **Pr**: Varying private car volumes
- **Bi**: Varying bicycle volumes
- **Pe**: Varying pedestrian volumes

**Levels** (0-9): 100/hr to 1000/hr in 100/hr increments

**Example**:
```python
'Pr_0': {car: 100, bicycle: 400, pedestrian: 400, bus: 50}
'Pr_5': {car: 600, bicycle: 400, pedestrian: 400, bus: 50}
'Bi_3': {car: 400, bicycle: 400, pedestrian: 400, bus: 50}
```

**Location**: `route_generator/traffic_config.py:get_traffic_config()`

### Evaluation Metrics

**Primary Metrics**:
- Average waiting time (car, bicycle, pedestrian, bus)
- Total CO2 emissions
- Safety violations (count)

**Secondary Metrics**:
- Action distribution (Continue, Skip2P1, Next)
- Phase durations
- Episode length

**Equity Metrics**:
- Gini coefficient across modes
- Max-min fairness
- Coefficient of variation

**Location**: Collected in `run/testing/test_drl.py`, saved to CSV

---

## Important Notes

### Critical Files - DO NOT Modify Without Understanding

1. **`common/sumo_utils.py`**: SUMO environment setup
   - Required for TraCI connection
   - Must be called before importing traci

2. **`controls/ml_based/drl/agent.py`**: Core DQN implementation
   - Changing this requires retraining all models
   - Existing checkpoints may be incompatible

3. **`infrastructure/` files**: SUMO network definitions
   - Changing network invalidates all trained models
   - Detectors are tied to specific edges

4. **Phase definitions**: `constants/developed/common/tls_constants.py`
   - Phase IDs: 1 (P1), 5 (P2), 9 (P3), 13 (P4)
   - Changing these breaks action mapping

### Common Pitfalls

1. **SUMO_HOME not set**: Always verify `export SUMO_HOME="/path/to/sumo"`

2. **Import order**: Must call `setup_environment()` before importing `traci`

3. **State dimension mismatch**: STATE_DIM must match `_get_state()` output

4. **Checkpoint incompatibility**: Changing network architecture invalidates old checkpoints

5. **Background processes**: Always check for running processes before starting new training
   ```bash
   ps aux | grep train_drl.py
   ps aux | grep test_drl.py
   ```

6. **Port conflicts**: TraCI uses port 8816. Kill existing SUMO processes if connection fails.

### Git Workflow

**Branch naming**: `claude/claude-md-<session-id>`

**Commit guidelines**:
```bash
# Good commit messages
git commit -m "Add attention analysis for bicycle phase transitions"
git commit -m "Fix reward calculation for Skip2P1 effectiveness"
git commit -m "Update DRL config: increase epsilon decay to 0.98"

# Bad commit messages
git commit -m "updates"
git commit -m "fix bug"
git commit -m "wip"
```

**Before committing**:
```bash
# Format and lint
./scripts/format_and_lint.sh

# Check status
git status

# Review changes
git diff
```

### Output Directories (Gitignored)

These are automatically created and should NOT be committed:

```
logs/           # Training/testing logs
models/         # Saved model checkpoints
results/        # Test results CSV files
output/         # Miscellaneous output
*.log           # All log files
*.csv           # All CSV files (except tables)
```

### Environment Variables

**`.env` file** (optional):
```bash
SUMO_GUI=false          # Set to 'true' for visual simulation
LOG_LEVEL=INFO          # DEBUG, INFO, WARNING, ERROR
```

**Required**: `SUMO_HOME` environment variable
```bash
export SUMO_HOME="/usr/share/sumo"  # Linux
export SUMO_HOME="/opt/homebrew/share/sumo"  # macOS (Homebrew)
```

---

## XAI (Explainable AI) Components

### 1. Attention Analysis

**File**: `analysis/drl/single_agent/attention_analysis.py`

**Purpose**: Visualize which state features the network focuses on

**Output**: Attention heatmaps in `images/2/attention/`

### 2. Saliency Maps

**File**: `analysis/drl/single_agent/saliency_analysis.py`

**Purpose**: Gradient-based feature importance

**Output**: Saliency visualizations

### 3. VIPER (Decision Tree Extraction)

**File**: `analysis/drl/single_agent/viper_extraction.py`

**Purpose**: Extract interpretable decision tree from DQN policy

**Output**: Decision tree visualization and rules

### 4. Counterfactual Explanations

**File**: `analysis/drl/single_agent/counterfactual_generator.py`

**Purpose**: "What-if" analysis - minimal changes to flip decisions

**Output**: Counterfactual scenarios and visualizations

### 5. Bicycle Spike Analysis

**File**: `analysis/drl/single_agent/bicycle_spike_analysis.py`

**Purpose**: Specialized analysis for bicycle demand handling

**Output**: Bicycle-specific metrics and visualizations

---

## Multi-Agent vs Single-Agent

### Current Status

- **Single-Agent**: Fully implemented and tested (2 intersections, centralized control)
- **Multi-Agent**: Infrastructure exists, under development

### Single-Agent Architecture

- **Intersections**: TLS3 and TLS6
- **State**: 32-dimensional (16 per intersection)
- **Agent**: One centralized DQN controlling both
- **Coordination**: Implicit through shared state and Skip2P1 action

### Multi-Agent Architecture (Future)

- **Intersections**: Scalable to N intersections
- **State**: Distributed (each agent sees local + neighbor states)
- **Agents**: Independent DQN per intersection
- **Coordination**: Communication protocol between agents

**Location**: `infrastructure/developed/drl/multi_agent/`

---

## Quick Reference

### File Naming Conventions

- **Python modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Scripts**: `descriptive_name.sh`
- **SUMO files**: `common.net.xml`, `common.det.xml`, etc.
- **Config files**: `signal_sync.sumocfg`

### Import Order

1. Standard library
2. Third-party libraries
3. Local modules (after path setup)

### Key Directories

- **Source code**: `controls/`, `analysis/`, `route_generator/`
- **Configuration**: `constants/`, `configurations/`
- **Execution**: `run/`, `scripts/`
- **Data**: `infrastructure/`, `detectors/`
- **Output**: `logs/`, `models/`, `results/` (gitignored)
- **Documentation**: `README.md`, `CLAUDE.md`, `Tables/`

### Common Commands

```bash
# Training
./scripts/drl/single_agent/run/run_training.sh
tail -100f training.log
./scripts/drl/single_agent/stop/stop_training.sh

# Testing
./scripts/drl/single_agent/run/run_testing.sh models/.../final_model.pth
tail -100f testing.log

# Analysis
./scripts/drl/single_agent/analyze/run_all_analysis.sh models/.../final_model.pth

# Code quality
./scripts/format_and_lint.sh

# Cleanup
./scripts/clean_logs.sh
```

---

## For AI Assistants: Best Practices

### When Modifying Code

1. **Read before writing**: Always read the file first to understand context
2. **Preserve style**: Match existing code style and conventions
3. **Update STATE_DIM**: If changing state space, update `config.py`
4. **Document changes**: Add comments explaining non-obvious logic
5. **Test compatibility**: Consider impact on existing checkpoints

### When Adding Features

1. **Check existing patterns**: Look for similar implementations
2. **Update config**: Add new hyperparameters to `config.py`
3. **Update docs**: Modify README.md and this file
4. **Add tests**: Create test scenarios if applicable

### When Debugging

1. **Check logs**: Look at `training.log` or `testing.log`
2. **Verify SUMO**: Ensure SUMO_HOME is set and SUMO is installed
3. **Check processes**: Look for running background processes
4. **Review state**: Print state vectors to verify dimensions

### When Analyzing Results

1. **Load results**: Use `pd.read_csv('results/drl_test_results.csv')`
2. **Compare baselines**: Cross-reference with `developed_test_results.csv`
3. **Visualize**: Use matplotlib/seaborn for plots
4. **Statistical tests**: Use scipy for significance testing

---

## Version History

- **v1.0.0** (2025-12-04): Initial comprehensive guide

---

## Additional Resources

- **README.md**: User-facing documentation
- **Multi_Agent.md**: Multi-agent architecture notes
- **Tables/**: Result tables for single and multi-agent
- **Paper notes**: Research directions and journal recommendations (in README.md)

---

**For questions or clarifications, refer to the source code documentation or commit history.**
