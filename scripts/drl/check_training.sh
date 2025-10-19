#!/bin/bash

# Check Training Status Script

echo "==================================="
echo "Training Status Check"
echo "==================================="

# Check if training is running
TRAIN_PID=$(ps aux | grep "train_drl.py" | grep -v grep | awk '{print $2}')

if [ -z "$TRAIN_PID" ]; then
    echo "❌ Training is NOT running"
else
    echo "✅ Training is running (PID: $TRAIN_PID)"
    
    # Show CPU and memory usage
    echo ""
    echo "Resource usage:"
    ps -p $TRAIN_PID -o %cpu,%mem,etime,command
fi

# Check SUMO processes
echo ""
echo "SUMO processes:"
SUMO_COUNT=$(ps aux | grep "sumo" | grep -v grep | wc -l)
if [ "$SUMO_COUNT" -eq 0 ]; then
    echo "No SUMO processes running"
else
    echo "Found $SUMO_COUNT SUMO process(es)"
fi

# Check latest log file
echo ""
echo "Latest training log:"
if [ -f "training.log" ]; then
    echo "Last 5 lines of training.log:"
    tail -5 training.log
else
    echo "No training.log found"
fi

# Check latest results
echo ""
echo "Latest training results:"
LATEST_LOG=$(ls -t logs/*/training_log.csv 2>/dev/null | head -1)
if [ -n "$LATEST_LOG" ]; then
    echo "Latest log: $LATEST_LOG"
    echo "Last episode:"
    tail -1 "$LATEST_LOG"
else
    echo "No training logs found"
fi
