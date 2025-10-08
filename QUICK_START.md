# DRL Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Verify Setup
```bash
python verify_drl_setup.py
```

This will check:
- ✓ Python packages installed
- ✓ SUMO configured
- ✓ DRL modules working
- ✓ Infrastructure files present

### Step 2: Install Dependencies (if needed)
```bash
pip install -r requirements_drl.txt
```

### Step 3: Generate Route Files
```bash
python privateCarRouteFile.py
python bicycleRouteFile.py
python pedestrianRouteFile.py
```

### Step 4: Start Training
```bash
./run_training.sh
```

**Training will:**
- Run 1000 episodes (~2-4 days)
- Save checkpoints every 50 episodes
- Create logs in `logs/training_TIMESTAMP/`
- Save final model to `models/training_TIMESTAMP/final_model.pth`

### Step 5: Test Trained Model
```bash
./run_testing.sh models/training_TIMESTAMP/final_model.pth
```

**Testing will:**
- Run 27 scenarios (~2-4 hours)
- Save results to `results/drl_testing/`
- Print performance summary

---

## 📊 Monitor Training Progress

### View Training Logs
```bash
# Real-time monitoring
tail -f logs/training_TIMESTAMP/training_log.csv

# View plots
open logs/training_TIMESTAMP/training_progress.png
```

### Check Episode Progress
```bash
# Count completed episodes
wc -l logs/training_TIMESTAMP/training_log.csv
```

---

## 🎯 Quick Test (10 Episodes)

For a quick test before full training:

1. Edit `drl/config.py`:
```python
NUM_EPISODES = 10  # Instead of 1000
```

2. Run training:
```bash
python training/train_drl.py
```

3. Check results in `logs/` directory

---

## 🔧 Common Issues

### Issue: "SUMO_HOME not set"
```bash
# Linux/Mac
export SUMO_HOME="/usr/share/sumo"

# Add to ~/.bashrc or ~/.zshrc for permanent
echo 'export SUMO_HOME="/usr/share/sumo"' >> ~/.bashrc
```

### Issue: "CUDA out of memory"
Edit `drl/agent.py` line 19:
```python
device = 'cpu'  # Force CPU usage
```

### Issue: "Route files not found"
Generate them first:
```bash
python privateCarRouteFile.py
python bicycleRouteFile.py
python pedestrianRouteFile.py
```

---

## 📈 Expected Training Progress

### Episode 1-100: Exploration Phase
- Reward: -150 to -80
- Epsilon: 1.0 → 0.6
- Agent learning basic patterns

### Episode 100-300: Learning Phase
- Reward: -80 to -30
- Epsilon: 0.6 → 0.2
- Agent discovering good strategies

### Episode 300-600: Optimization Phase
- Reward: -30 to +20
- Epsilon: 0.2 → 0.05
- Agent fine-tuning policies

### Episode 600-1000: Convergence Phase
- Reward: +20 to +50
- Epsilon: 0.05 → 0.01
- Agent mastering rare events

---

## 🎓 Understanding the Output

### Training Logs
```csv
episode,reward,loss,length,epsilon
0,-145.2,0.8234,3600,1.0
1,-142.8,0.7891,3600,0.995
...
```

### Test Results
```csv
scenario,car_wait_time,bike_wait_time,ped_wait_time,bus_wait_time,sync_success_rate,co2_emission
Pr_0,29.3,35.2,18.4,22.1,0.82,145.3
Pr_1,31.5,38.1,19.2,23.4,0.79,152.8
...
```

---

## 💡 Tips for Better Results

### 1. Longer Training
```python
NUM_EPISODES = 1500  # More episodes = better performance
```

### 2. Adjust Reward Weights
```python
# Prioritize synchronization
ALPHA_SYNC = 10.0  # Instead of 5.0

# Prioritize vulnerable modes
WEIGHT_BICYCLE = 2.0  # Instead of 1.5
WEIGHT_PEDESTRIAN = 3.0  # Instead of 2.0
```

### 3. Larger Network
```python
HIDDEN_LAYERS = [512, 512, 256]  # Instead of [256, 256, 128]
```

### 4. More Exploration
```python
EPSILON_DECAY = 0.998  # Instead of 0.995 (slower decay)
```

---

## 📞 Need Help?

1. **Check verification**: `python verify_drl_setup.py`
2. **Read full docs**: `DRL_README.md`
3. **View implementation**: `DRL_IMPLEMENTATION_SUMMARY.md`
4. **Check paper**: `PAPER.md`

---

## ✅ Checklist

Before starting training:
- [ ] Python 3.8+ installed
- [ ] SUMO installed and SUMO_HOME set
- [ ] Dependencies installed (`pip install -r requirements_drl.txt`)
- [ ] Verification passed (`python verify_drl_setup.py`)
- [ ] Route files generated
- [ ] Sufficient disk space (~5GB for logs/models)
- [ ] GPU available (optional, but recommended)

Ready to train? Run: `./run_training.sh` 🚀
