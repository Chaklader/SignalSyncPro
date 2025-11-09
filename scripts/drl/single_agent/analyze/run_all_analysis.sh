#!/bin/bash

set -e

MODEL_PATH="models/training_20251103_163015/checkpoint_ep192.pth"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

echo "=================================================="
echo "DRL Single-Agent Explainability & Safety Analysis"
echo "=================================================="
echo ""
echo "Model: $MODEL_PATH"
echo "Project Root: $PROJECT_ROOT"
echo ""

cd "$PROJECT_ROOT"

if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Error: Model not found at $MODEL_PATH"
    echo "Please update MODEL_PATH in this script to point to your trained model."
    exit 1
fi

echo "Starting analysis..."
echo ""

python analysis/drl/single_agent/run_all_analyses.py "$MODEL_PATH"

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✅ Analysis completed successfully!"
    echo "=================================================="
else
    echo ""
    echo "=================================================="
    echo "❌ Analysis failed with exit code $exit_code"
    echo "=================================================="
fi

exit $exit_code
