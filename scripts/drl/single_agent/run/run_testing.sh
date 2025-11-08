#!/bin/bash

# Testing script for DRL traffic signal control

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
cd "$PROJECT_ROOT"

if [ $# -eq 0 ]; then
    echo "Usage: ./run_testing.sh <path_to_model>"
    echo "Example: ./run_testing.sh models/training_20241008/final_model.pth"
    exit 1
fi

MODEL_PATH=$1

echo "==================================="
echo "DRL Traffic Signal Control Testing"
echo "==================================="
echo "Model: $MODEL_PATH"

# No environment checks needed - script is explicitly for testing

# Clean and create results directory
echo "Cleaning previous test results..."
rm -rf results/*
rm -f testing.log
mkdir -p results
echo "✓ Previous results cleaned"
echo ""

# Run testing in background with logging
echo "Starting testing in background..."
echo "Logs will be written to: testing.log"
echo ""

nohup python run/testing/test_drl.py --model "$MODEL_PATH" > testing.log 2>&1 &

TEST_PID=$!
echo "Testing started with PID: $TEST_PID"
echo ""
echo "Monitor progress with:"
echo "  tail -100f testing.log"
echo ""
echo "Check if running:"
echo "  ps -p $TEST_PID"
echo ""
echo "Stop testing:"
echo "  kill $TEST_PID"
echo ""
echo "Results will be saved to: results/drl_test_results.csv"
