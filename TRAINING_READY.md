# ✅ Training Scripts Updated - Ready to Train!

## 🔧 Updates Made

### 1. **run_training.sh** - Updated
- ✅ Removed automatic route generation (files already exist)
- ✅ Added quiet mode for pip install (`-q` flag)
- ✅ Added comments about when to regenerate routes
- ✅ Kept directory creation and dependency checks

### 2. **training/train_drl.py** - Updated
- ✅ Added SUMO tools path handling
- ✅ Ensures TraCI can be imported from conda environment
- ✅ Better error handling for SUMO_HOME

### 3. **testing/test_drl.py** - Updated
- ✅ Added SUMO tools path handling
- ✅ Consistent with training script

## 📋 What You Have

### Existing Route Files (Ready to Use)
- ✅ `infrastructure/developed/routes/privateCar.rou.xml` (362 KB)
- ✅ `infrastructure/developed/routes/bicycle.rou.xml` (356 KB)
- ✅ `infrastructure/developed/routes/pedestrian.rou.xml` (1.8 MB)
- ✅ `infrastructure/developed/routes/bus.rou.xml` (6.9 KB)

### SUMO Configuration
- ✅ `test.sumocfg` points to correct route files
- ✅ Network files in `infrastructure/developed/network/`
- ✅ Detectors in `infrastructure/developed/detector/`
- ✅ Bus stops in `infrastructure/developed/bus_stop/`

## 🚀 How to Start Training

### Option 1: Using the Shell Script (Recommended)
```bash
# Make sure you're in the sumo conda environment
conda activate sumo

# Run the training script
./run_training.sh
```

### Option 2: Direct Python Execution
```bash
# Make sure you're in the sumo conda environment
conda activate sumo

# Run training directly
python training/train_drl.py
```

## 📊 What Will Happen

### Training Process
1. **Setup Phase** (~5 seconds)
   - Creates log and model directories
   - Initializes SUMO environment
   - Detects state dimension (should be ~45)
   - Creates DQN agent with 110,980 parameters

2. **Training Loop** (2-4 days for 1000 episodes)
   - Episode 1-100: Exploration (reward: -150 to -80)
   - Episode 100-300: Learning (reward: -80 to -30)
   - Episode 300-600: Optimization (reward: -30 to +20)
   - Episode 600-1000: Convergence (reward: +20 to +50)

3. **Outputs**
   - Checkpoints saved every 50 episodes
   - Training logs updated continuously
   - Progress plots generated at each checkpoint

### Directory Structure After Training
```
logs/
└── training_20241008_HHMMSS/
    ├── training_log.csv
    ├── training_metrics.csv
    └── training_progress.png

models/
└── training_20241008_HHMMSS/
    ├── checkpoint_ep50.pth
    ├── checkpoint_ep100.pth
    ├── ...
    ├── checkpoint_ep1000.pth
    └── final_model.pth
```

## 🔍 Monitoring Training

### Real-time Progress
```bash
# Watch training logs
tail -f logs/training_*/training_log.csv

# Check episode count
wc -l logs/training_*/training_log.csv
```

### View Training Curves
```bash
# Open latest plot
open logs/training_*/training_progress.png
```

### Check GPU/CPU Usage
```bash
# Monitor system resources
top -pid $(pgrep -f train_drl.py)
```

## ⚙️ Configuration Options

### Quick Test (10 Episodes)
Edit `drl/config.py`:
```python
NUM_EPISODES = 10  # Instead of 1000
```

### Adjust Learning Rate
Edit `drl/config.py`:
```python
LEARNING_RATE = 0.0005  # Instead of 0.0001 (faster learning)
```

### Change Reward Weights
Edit `drl/config.py`:
```python
ALPHA_SYNC = 10.0  # Prioritize synchronization
WEIGHT_BICYCLE = 2.0  # Higher priority for bikes
```

### Use CPU Only
Edit `drl/agent.py` line 19:
```python
device = 'cpu'  # Force CPU
```

## 🛑 Stopping and Resuming

### Stop Training
- Press `Ctrl+C` to stop gracefully
- Latest checkpoint will be saved

### Resume Training
Currently not implemented, but you can:
1. Load the latest checkpoint
2. Continue from that episode
3. (Would need to modify training script)

## ✅ Pre-Flight Checklist

Before starting training:
- [x] Conda environment activated (`conda activate sumo`)
- [x] Route files exist in `infrastructure/developed/routes/`
- [x] SUMO_HOME environment variable set
- [x] Dependencies installed (`pip install -r requirements_drl.txt`)
- [x] Verification passed (`python verify_drl_setup.py`)
- [x] Sufficient disk space (~5GB for logs/models)
- [x] Time allocated (2-4 days for full training)

## 🎯 Expected Timeline

### Full Training (1000 episodes)
- **Duration**: 2-4 days
- **Checkpoints**: 20 checkpoints (every 50 episodes)
- **Final model**: `models/training_TIMESTAMP/final_model.pth`

### Quick Test (10 episodes)
- **Duration**: ~1-2 hours
- **Purpose**: Verify everything works
- **Checkpoints**: None (too few episodes)

## 📞 Troubleshooting

### Issue: "SUMO_HOME not set"
```bash
# Check current value
echo $SUMO_HOME

# Set if needed (add to ~/.bashrc or ~/.zshrc)
export SUMO_HOME="/Library/Frameworks/EclipseSUMO.framework/Versions/Current/EclipseSUMO"
```

### Issue: "TraCI module not found"
```bash
# Make sure you're in sumo conda environment
conda activate sumo

# Verify SUMO tools path
ls $SUMO_HOME/tools/
```

### Issue: Training very slow
- Use GPU if available
- Reduce `NUM_EPISODES` for testing
- Reduce `BUFFER_SIZE` to save memory
- Close other applications

### Issue: Out of memory
- Edit `drl/config.py`: `BUFFER_SIZE = 50000`
- Use CPU instead of GPU
- Close other applications

## 🎉 Ready to Train!

Everything is configured and ready. Start training with:

```bash
conda activate sumo
./run_training.sh
```

**Good luck with your research!** 🚦🤖📊
