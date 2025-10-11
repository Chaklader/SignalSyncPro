# DRL Traffic Signal Control Implementation

This directory contains the Deep Reinforcement Learning (DRL) implementation for adaptive multimodal traffic signal
control using Deep Q-Network (DQN) with Prioritized Experience Replay (PER).

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements_drl.txt

# Make scripts executable (Linux/Mac)
chmod +x run_training.sh run_testing.sh
```

### 2. Training

```bash
# Linux/Mac
./run_training.sh

# Windows
run_training.bat
```

Training will:

- Run for 1000 episodes (configurable in `drl/config.py`)
- Save checkpoints every 50 episodes
- Generate training plots and logs
- Save final model to `models/training_TIMESTAMP/final_model.pth`

### 3. Testing

```bash
# Linux/Mac
./run_testing.sh models/training_20241008/final_model.pth

# Windows
run_testing.bat models\training_20241008\final_model.pth
```

Testing will:

- Run on all 27 scenarios (Pr_0 to Pe_9)
- Compare with Reference and Developed controls
- Generate comparison plots
- Save results to `results/drl_testing/`

## Configuration

Edit `drl/config.py` to customize:

- Network architecture
- Learning rate
- Reward weights
- Training parameters

## Architecture

### State Space (45 dimensions)

- Queue lengths (vehicles, bicycles)
- Current phase (one-hot encoded)
- Phase duration
- Detector occupancy
- Bus presence
- Pedestrian demand
- Synchronization timer
- Time of day

### Action Space (4 actions)

1. Continue current phase
2. Skip to Phase 1 (major through)
3. Progress to next phase
4. Activate pedestrian phase

### Reward Function

```
R = -α₁·waiting_time - α₂·CO₂ + α₃·sync_success + α₄·equity - α₅·safety_penalty
```

## Results

After training and testing, you'll get:

- Training curves (reward, loss, epsilon)
- Test results CSV
- Comparison plots with baselines
- Detailed performance metrics

## Troubleshooting

### SUMO not found

```bash
export SUMO_HOME="/usr/share/sumo"  # Linux
export SUMO_HOME="/opt/homebrew/share/sumo"  # Mac
set SUMO_HOME=C:\Program Files\SUMO  # Windows
```

### CUDA out of memory

Edit `drl/agent.py`:

```python
device = 'cpu'  # Instead of auto-detect
```

### Training too slow

Reduce in `drl/config.py`:

```python
NUM_EPISODES = 500  # Instead of 1000
BUFFER_SIZE = 50000  # Instead of 100000
```

## Paper Results

To reproduce paper results:

1. Train: `./run_training.sh`
2. Test: `./run_testing.sh models/training_TIMESTAMP/final_model.pth`
3. Compare: `python testing/compare_results.py --drl_results results/drl_testing/drl_test_results.csv`

## Project Structure

```
SignalSyncPro/
├── drl/                          # DRL implementation
│   ├── agent.py                  # DQN Agent with PER
│   ├── config.py                 # Configuration
│   ├── environment.py            # SUMO environment wrapper
│   ├── neural_network.py         # Q-Network architecture
│   ├── replay_buffer.py          # Prioritized replay buffer
│   └── reward.py                 # Reward calculator
├── training/
│   ├── train_drl.py              # Training script
│   └── train_config.yaml         # Training configuration
├── testing/
│   ├── test_drl.py               # Testing script
│   └── compare_results.py        # Comparison with baselines
├── models/                       # Saved models (gitignored)
├── logs/                         # Training logs (gitignored)
└── results/                      # Test results
```

## Citation

If you use this code, please cite: [Your paper citation here]
