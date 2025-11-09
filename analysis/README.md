# Explainability and Safety Analysis for Paper 2

This directory contains all analysis scripts needed for Section 4 (Explainability) and Section 5 (Safety Analysis) of Paper 2.

## Prerequisites

```bash
pip install torch numpy matplotlib seaborn pandas scikit-learn
```

## Scripts Overview

### Section 4: Explainability Analysis

1. **`saliency_analysis.py`** - Gradient-based saliency maps
   - Computes ∇Q/∇s for each action
   - Identifies which features most influence Q-values
   - Visualizes feature importance heatmaps

2. **`attention_analysis.py`** - Attention weight computation
   - Softmax of gradient magnitudes as attention proxy
   - Groups features into semantic categories
   - Compares attention across actions

3. **`counterfactual_generator.py`** - Counterfactual explanations
   - Finds minimal state changes to flip decisions
   - Uses gradient-based optimization
   - Identifies decision boundaries

4. **`viper_extraction.py`** - Decision tree extraction
   - Implements VIPER algorithm
   - Distills DQN policy into interpretable tree
   - Extracts human-readable decision rules

### Section 5: Safety Analysis

5. **`safety_analysis.py`** - Comprehensive safety evaluation
   - Parses test results from Tables/Table_Single_Agent.md
   - Identifies edge cases and concerning behaviors
   - Analyzes decision patterns under critical conditions
   - Characterizes safe operating regions

## Quick Start

### Run All Analyses

```bash
cd analysis
python run_all_analyses.py
```

### Run Individual Analyses

```bash
# Saliency maps
python saliency_analysis.py

# Attention patterns
python attention_analysis.py

# Counterfactuals
python counterfactual_generator.py

# Decision tree extraction (takes ~10 minutes)
python viper_extraction.py

# Safety analysis (uses existing test data)
python safety_analysis.py
```

## Output Structure

```
results/
├── saliency/
│   ├── saliency_*.png          # Saliency heatmaps
│   └── ...
├── attention/
│   ├── attention_*.png         # Attention visualizations
│   └── ...
├── counterfactuals/
│   ├── cf_*.png                # Counterfactual comparisons
│   └── ...
├── viper/
│   ├── decision_tree.png       # Extracted tree visualization
│   ├── confusion_matrix.png    # Tree vs DQN accuracy
│   ├── decision_rules.txt      # Human-readable rules
│   └── extracted_tree.pkl      # Saved tree model
└── safety/
    ├── safety_summary.png      # Overall safety metrics
    ├── waiting_time_heatmap.png
    └── safety_report.txt       # Comprehensive report
```

## Model Used

All analyses use: **Episode 192** from training run `20251103_163015`
- Path: `models/training_20251103_163015/checkpoint_ep192.pth`
- Test results: Zero safety violations across 30 scenarios
- Performance: Excellent waiting times for all modes

## Expected Runtime

- Saliency analysis: ~2 minutes
- Attention analysis: ~2 minutes
- Counterfactual generation: ~5 minutes
- VIPER extraction: ~10 minutes
- Safety analysis: ~1 minute

**Total: ~20 minutes for complete analysis**

## Customization

### Change Model

Edit model path in each script:
```python
MODEL_PATH = "models/training_20251103_163015/checkpoint_ep192.pth"
```

### Adjust Parameters

**VIPER tree depth:**
```python
extractor.train_decision_tree(states, actions, max_depth=10)
```

**Counterfactual optimization:**
```python
generator.generate_counterfactual(
    state, 
    target_action,
    lambda_distance=1.0,    # L2 penalty weight
    lambda_action=10.0      # Action flip weight
)
```

**Saliency visualization:**
```python
analyzer.visualize_saliency(state, cmap='RdBu_r')
```

## For Paper 2

### Section 4 Results
- Use visualizations from `results/attention/`, `results/saliency/`, `results/counterfactuals/`, `results/viper/`
- Include decision tree rules from `results/viper/decision_rules.txt`
- Report tree accuracy from VIPER output

### Section 5 Results
- Use metrics from `results/safety/safety_report.txt`
- Include visualizations from `results/safety/`
- Reference zero safety violations finding
- Discuss edge cases and safe operating regions

## Troubleshooting

**CUDA out of memory:**
```python
self.device = torch.device("cpu")  # Force CPU
```

**Import errors:**
```bash
cd /path/to/SignalSyncPro
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Missing test data:**
Ensure `Tables/Table_Single_Agent.md` contains DRL Agent Test Results section.

## Notes

- All scripts use **Episode 192 model** (no retraining needed)
- Safety analysis uses **existing test results** from tables
- Synthetic states used for explainability (representative examples)
- All visualizations saved automatically to `results/` subdirectories
