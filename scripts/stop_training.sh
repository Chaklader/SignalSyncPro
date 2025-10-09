#!/bin/bash

# Stop DRL Training Script

echo "==================================="
echo "Stopping DRL Training"
echo "==================================="

# Find and kill training process
echo "Looking for training processes..."

# Find Python training process
TRAIN_PID=$(ps aux | grep "train_drl.py" | grep -v grep | awk '{print $2}')

if [ -z "$TRAIN_PID" ]; then
    echo "No training process found."
else
    echo "Found training process with PID: $TRAIN_PID"
    echo "Stopping training..."
    kill $TRAIN_PID
    
    # Wait a moment
    sleep 2
    
    # Check if still running
    if ps -p $TRAIN_PID > /dev/null 2>&1; then
        echo "Process still running, forcing stop..."
        kill -9 $TRAIN_PID
    fi
    
    echo "Training stopped successfully!"
fi

# Find and kill any SUMO processes
echo ""
echo "Checking for SUMO processes..."
SUMO_PIDS=$(ps aux | grep "sumo" | grep -v grep | awk '{print $2}')

if [ -z "$SUMO_PIDS" ]; then
    echo "No SUMO processes found."
else
    echo "Found SUMO processes, stopping..."
    echo "$SUMO_PIDS" | xargs kill 2>/dev/null
    echo "SUMO processes stopped."
fi

echo ""
echo "All processes stopped!"
