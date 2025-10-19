#!/bin/bash

# Stop DRL Testing Script

echo "==================================="
echo "Stopping DRL Testing"
echo "==================================="

# Find and kill testing process
echo "Looking for testing processes..."

# Find Python testing process
TEST_PID=$(ps aux | grep "test_drl.py" | grep -v grep | awk '{print $2}')

if [ -z "$TEST_PID" ]; then
    echo "No testing process found."
else
    echo "Found testing process with PID: $TEST_PID"
    echo "Stopping testing..."
    kill $TEST_PID
    
    # Wait a moment
    sleep 2
    
    # Check if still running
    if ps -p $TEST_PID > /dev/null 2>&1; then
        echo "Process still running, forcing stop..."
        kill -9 $TEST_PID
    fi
    
    echo "Testing stopped successfully!"
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
