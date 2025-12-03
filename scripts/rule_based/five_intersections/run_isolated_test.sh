#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "==================================="
echo "5-TLS Isolated Control - Testing"
echo "==================================="

if [ -z "$SUMO_HOME" ]; then
    echo "Error: SUMO_HOME environment variable not set"
    exit 1
fi

echo "✓ SUMO_HOME: $SUMO_HOME"
echo ""

if [ ! -f "configurations/developed/drl/multi_agent/signal_sync.sumocfg" ]; then
    echo "Error: SUMO config file not found"
    exit 1
fi

echo "✓ SUMO config found"
echo ""

SCENARIOS="all"
if [ $# -gt 0 ]; then
    SCENARIOS="$1"
fi

echo "Starting isolated control testing (without semi-sync)..."
echo "Scenarios: $SCENARIOS"
echo ""

python -m run.testing.five_intersections.isolated_without_semi_sync.test_isolated --scenarios "$SCENARIOS"

echo ""
echo "==================================="
echo "Testing Complete!"
echo "==================================="
