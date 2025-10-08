#!/bin/bash

# Training script for DRL traffic signal control

echo "==================================="
echo "DRL Traffic Signal Control Training"
echo "==================================="

# Check SUMO installation
if [ -z "$SUMO_HOME" ]; then
    echo "Error: SUMO_HOME environment variable not set"
    echo "Please install SUMO and set SUMO_HOME"
    exit 1
fi

# Create necessary directories
mkdir -p logs
mkdir -p models
mkdir -p results

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies (skip if already installed)
echo "Checking dependencies..."
pip install -q -r requirements_drl.txt

# Note: Route files should already exist in infrastructure/developed/routes/
# If you need to regenerate them, run:
#   python privateCarRouteFile.py
#   python bicycleRouteFile.py
#   python pedestrianRouteFile.py

# Run training
echo "Starting training..."
python training/train_drl.py

echo "Training complete!"
