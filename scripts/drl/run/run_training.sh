#!/bin/bash

# Training script for DRL traffic signal control

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
cd "$PROJECT_ROOT"

echo "==================================="
echo "DRL Traffic Signal Control Training"
echo "==================================="

# Check SUMO installation
if [ -z "$SUMO_HOME" ]; then
    echo "Error: SUMO_HOME environment variable not set"
    echo "Please install SUMO and set SUMO_HOME"
    exit 1
fi

# No environment checks needed - script is explicitly for training

# Create necessary directories
mkdir -p logs
mkdir -p models
mkdir -p results

# Run training
echo "Starting training in background..."
echo "Logs will be written to: training.log"

nohup python run/training/train_drl.py > training.log 2>&1 &

TRAIN_PID=$!
echo "Training started with PID: $TRAIN_PID"
echo ""
echo "Monitor progress with:"
echo "  tail -100f training.log"
echo ""
echo "Check if running:"
echo "  ps -p $TRAIN_PID"
echo ""
echo "Stop training:"
echo "  kill $TRAIN_PID"
