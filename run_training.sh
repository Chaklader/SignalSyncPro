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


# Run training
echo "Starting training..."

nohup python training/train_drl.py > training.log 2>&1 &

echo "Training complete!"
