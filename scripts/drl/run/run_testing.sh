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

# Create results directory
mkdir -p results/drl_testing

# Run testing
python run/testing/test_drl.py --model "$MODEL_PATH"

echo "Testing complete! Results saved in results/drl_testing"
