#!/bin/bash

# Test Rule-Based "Developed" Control across 30 scenarios

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "==================================="
echo "Rule-Based Developed Control - Testing"
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

# Parse command line arguments
SCENARIOS="all"
if [ $# -gt 0 ]; then
    SCENARIOS="$1"
fi

# Run the developed control test
echo "Starting developed control testing..."
echo "Scenarios: $SCENARIOS"
echo ""

python testing/test_developed.py --scenarios "$SCENARIOS"

echo ""
echo "==================================="
echo "Testing Complete!"
echo "==================================="
