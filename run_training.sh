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

# Check if .env exists and has correct mode
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Please create .env file with RUN_MODE=training"
    exit 1
fi

# Check if RUN_MODE is set to training
if ! grep -q "RUN_MODE=training" .env; then
    echo "Warning: RUN_MODE is not set to 'training' in .env"
    echo "Current .env content:"
    cat .env
    echo ""
    echo "Please set RUN_MODE=training in .env file"
    exit 1
fi

echo "✓ RUN_MODE=training confirmed in .env"
echo ""

# Create necessary directories
mkdir -p logs
mkdir -p models
mkdir -p results

# Run training
echo "Starting training in background..."
echo "Logs will be written to: training.log"

nohup python training/train_drl.py > training.log 2>&1 &

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
