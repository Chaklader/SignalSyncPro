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
