# DRL Single-Agent Analysis Script

This directory contains the shell script to run all explainability and safety analyses for Paper 2.

## Usage

```bash
# From project root
./scripts/drl/single_agent/analyze/run_all_analysis.sh
```

## Configuration

The model path is configured in the shell script:

```bash
MODEL_PATH="models/training_20251103_163015/checkpoint_ep192.pth"
```

To analyze a different model, edit this line in `run_all_analysis.sh`.

## What It Does

The script runs all 5 analysis modules:
1. **Saliency Analysis** - Gradient-based feature importance
2. **Attention Analysis** - Attention weight patterns
3. **Counterfactual Generation** - Minimal state changes to flip decisions
4. **VIPER Extraction** - Decision tree extraction from DQN
5. **Safety Analysis** - Comprehensive safety evaluation

## Output

All results are saved to:
- `results/saliency/`
- `results/attention/`
- `results/counterfactuals/`
- `results/viper/`
- `results/safety/`

## Runtime

Expected total runtime: **~20 minutes**

## Requirements

- Conda environment `sumo` must be activated
- Model checkpoint must exist at the specified path
- All dependencies installed (see `environment.yml`)
