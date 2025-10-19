#!/bin/bash

# Run Rule-Based "Developed" Control

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "==================================="
echo "Rule-Based Developed Control"
echo "==================================="

# Check SUMO installation
if [ -z "$SUMO_HOME" ]; then
    echo "Error: SUMO_HOME environment variable not set"
    echo "Please install SUMO and set SUMO_HOME"
    exit 1
fi

echo "✓ SUMO_HOME: $SUMO_HOME"
echo ""

# Check if network exists
if [ ! -f "infrastructure/developed/common/network/test.net.xml" ]; then
    echo "Error: Network file not found"
    echo "Expected: infrastructure/developed/common/network/test.net.xml"
    exit 1
fi

echo "✓ Network file found"
echo ""

# Run the developed control
echo "Starting developed control..."
python controls/rule_based/developed/main.py

echo ""
echo "==================================="
echo "Simulation Complete!"
echo "==================================="
