# DRL Single-Agent Explainability & Safety Analysis

Analysis scripts for Paper 2 (Section 4 & 5) - Episode 192 model

## Prerequisites

```bash
conda activate sumo
```

All dependencies are in `environment.yml`

## Scripts

1. **`saliency_analysis.py`** - Gradient-based saliency maps (Section 4.4)
2. **`attention_analysis.py`** - Attention weight computation (Section 4.1)
3. **`counterfactual_generator.py`** - Counterfactual explanations (Section 4.2)
4. **`viper_extraction.py`** - Decision tree extraction (Section 4.3)
5. **`safety_analysis.py`** - Comprehensive safety evaluation (Section 5)
6. **`run_all_analyses.py`** - Master script (runs all 5)

## Quick Start

```bash
cd analysis/drl/single_agent
python run_all_analyses.py
```

Runtime: ~20 minutes total

## Model

**Episode 192:** `models/training_20251103_163015/checkpoint_ep192.pth`
- Zero safety violations across 30 test scenarios
- Excellent performance (no retraining needed)

## State Structure

**32 features** (2 intersections × 16 features each):

### Per Intersection (TLS 3 and TLS 6):
- Phase encoding (one-hot): 4 features [P1, P2, P3, P4]
- Phase duration: 1 feature (normalized)
- Vehicle queues: 4 features (binary detectors)
- Bicycle queues: 4 features (binary detectors)
- Bus present: 1 feature (binary)
- Bus wait: 1 feature (normalized)
- Simulation time: 1 feature (normalized)

See `STATE_STRUCTURE.md` for detailed feature mapping.

## Actions

- **0: Continue** - Stay in current phase
- **1: Skip2P1** - Skip to Phase 1 (major arterial)
- **2: Next** - Advance to next phase

## Results

All outputs saved to:
```
results/
├── saliency/          # Section 4.4
├── attention/         # Section 4.1
├── counterfactuals/   # Section 4.2
├── viper/            # Section 4.3
└── safety/           # Section 5
```

## No Retraining Required

All analyses use the existing trained model. No modifications to reward function or agent code.
