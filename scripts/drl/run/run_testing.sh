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

# Check if .env exists and has correct mode
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Please create .env file with RUN_MODE=test"
    exit 1
fi

# Check if RUN_MODE is set to test
if ! grep -q "RUN_MODE=test" .env; then
    echo "Warning: RUN_MODE is not set to 'test' in .env"
    echo "Current .env content:"
    cat .env
    echo ""
    echo "Please set RUN_MODE=test in .env file"
    exit 1
fi

echo "✓ RUN_MODE=test confirmed in .env"
echo ""

# Create results directory
mkdir -p results/drl_testing

# Run testing
python testing/test_drl.py --model "$MODEL_PATH"

echo "Testing complete! Results saved in results/drl_testing"
