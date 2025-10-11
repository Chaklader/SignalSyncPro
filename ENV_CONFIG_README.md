# Environment Configuration Guide

This project uses environment variables for configuration, similar to `.env` files in JavaScript/TypeScript projects.

## Setup

### 1. Install Dependencies

```bash
pip install python-dotenv
# or
pip install -r requirements_drl.txt
```

### 2. Configure Environment

Edit the `.env` file in the project root:

```bash
# .env
RUN_MODE=training  # or 'test'
SUMO_GUI=false     # or 'true'
LOG_LEVEL=INFO     # DEBUG, INFO, WARNING, ERROR
```

## Usage

### In Python Code

```python
from env_config import get_run_mode, is_training_mode, is_test_mode

# Check run mode
if is_training_mode():
    print("Running in training mode")
    agent.train()
elif is_test_mode():
    print("Running in test mode")
    agent.evaluate()

# Get specific values
mode = get_run_mode()  # Returns 'training' or 'test'
gui = get_sumo_gui()   # Returns True or False
```

### Training Mode

Set `RUN_MODE=training` in `.env`:

```bash
python training/train_drl.py
```

### Test Mode

Set `RUN_MODE=test` in `.env`:

```bash
python training/test_drl.py --model models/best_model.pth --episodes 10 --gui
```

## Environment Variables

| Variable | Values | Default | Description |
|----------|--------|---------|-------------|
| `RUN_MODE` | `training`, `test` | `training` | Operating mode |
| `SUMO_GUI` | `true`, `false` | `false` | Enable SUMO visualization |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` | Logging verbosity |

## API Reference

### Functions

#### `get_run_mode()`
Returns the current run mode as a string.

```python
mode = get_run_mode()  # 'training' or 'test'
```

#### `is_training_mode()`
Returns `True` if in training mode.

```python
if is_training_mode():
    # Training-specific code
    pass
```

#### `is_test_mode()`
Returns `True` if in test mode.

```python
if is_test_mode():
    # Testing-specific code
    pass
```

#### `get_sumo_gui()`
Returns `True` if SUMO GUI should be enabled.

```python
gui_enabled = get_sumo_gui()
env = TrafficManagement(config, tls_ids, gui=gui_enabled)
```

#### `get_log_level()`
Returns the logging level as a string.

```python
level = get_log_level()  # 'INFO', 'DEBUG', etc.
```

#### `print_config()`
Prints the current environment configuration.

```python
print_config()
# Output:
# ======================================================================
# SignalSyncPro Environment Configuration
# ======================================================================
# RUN_MODE:    training
# SUMO_GUI:    False
# LOG_LEVEL:   INFO
# DOTENV:      Loaded
# ======================================================================
```

## Examples

### Example 1: Training Script

```python
from env_config import is_training_mode, print_config

def main():
    print_config()  # Show configuration
    
    if not is_training_mode():
        print("ERROR: Set RUN_MODE=training in .env")
        return
    
    # Training code here
    agent.train()
```

### Example 2: Conditional Behavior

```python
from env_config import get_run_mode

mode = get_run_mode()

if mode == 'training':
    epsilon = 0.1  # Exploration
    save_models = True
elif mode == 'test':
    epsilon = 0.0  # Greedy
    save_models = False
```

### Example 3: Dynamic GUI

```python
from env_config import get_sumo_gui

# Use environment variable to control GUI
gui = get_sumo_gui()
env = TrafficManagement("test.sumocfg", ['3', '6'], gui=gui)
```

## Switching Modes

### Switch to Training Mode

1. Edit `.env`:
   ```
   RUN_MODE=training
   ```

2. Run training:
   ```bash
   python training/train_drl.py
   ```

### Switch to Test Mode

1. Edit `.env`:
   ```
   RUN_MODE=test
   ```

2. Run testing:
   ```bash
   python training/test_drl.py --model models/best_model.pth
   ```

## Validation

The configuration is automatically validated on import. Invalid values will show a warning and fall back to defaults:

```python
# Invalid RUN_MODE in .env
RUN_MODE=invalid_mode

# Output:
# Configuration Error: Invalid RUN_MODE: 'invalid_mode'. Must be one of: ['training', 'test']
# Falling back to default: RUN_MODE='training'
```

## Best Practices

1. **Always check mode** before running training/testing code
2. **Use helper functions** (`is_training_mode()`, `is_test_mode()`) instead of string comparisons
3. **Print configuration** at the start of scripts for debugging
4. **Validate early** to catch configuration errors before long training runs

## Troubleshooting

### python-dotenv not installed

```
Warning: python-dotenv not installed. Using default values.
Install with: pip install python-dotenv
```

**Solution**: Install the package:
```bash
pip install python-dotenv
```

### .env file not found

The module will use default values if `.env` is missing. Create the file:

```bash
cp .env.example .env
```

### Wrong mode warning

```
⚠️  WARNING: RUN_MODE is set to 'test', not 'training'
```

**Solution**: Edit `.env` and set the correct mode.
