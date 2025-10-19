#!/bin/bash

# Continue training from Episode 50 to Episode 100

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
cd "$PROJECT_ROOT"

echo "==================================="
echo "Continue DRL Training: Ep 51-100"
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

# Check if checkpoint exists
CHECKPOINT="models/training_20251016_200158/checkpoint_ep50.pth"
if [ ! -f "$CHECKPOINT" ]; then
    echo "Error: Checkpoint not found at $CHECKPOINT"
    exit 1
fi

echo "✓ Checkpoint found: $CHECKPOINT"
echo ""

# Create necessary directories
mkdir -p logs
mkdir -p models
mkdir -p results

# Generate initial routes
echo "Generating initial routes..."
python -c "
import sys
sys.path.append('.')
from traffic_config import get_traffic_config
from route_generator import generate_all_routes_developed
traffic_config = get_traffic_config()
generate_all_routes_developed(traffic_config)
print('✓ Routes generated')
"

echo ""

# Run training
echo "Starting continued training in background..."
echo "Logs will be written to: training.log"

nohup python training/continue_from_ep50.py > training.log 2>&1 &

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
