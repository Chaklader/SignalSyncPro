#!/bin/bash

cd "$(dirname "$0")/../../../.." || exit

echo "Starting state collection verification (running in background)..."
echo "Logs will be written to: verify.log"
echo "Monitor progress: tail -f verify.log"
echo ""

nohup python analysis/drl/single_agent/verify_state_collection.py > verify.log 2>&1 &

PID=$!
echo "Process started with PID: $PID"
echo "To check if still running: ps -p $PID"
