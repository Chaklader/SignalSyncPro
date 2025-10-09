#!/bin/bash

# Clean Old Logs Script

echo "==================================="
echo "Clean Old Training Logs"
echo "==================================="

# Ask for confirmation
read -p "This will delete old training logs and models. Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Remove old logs
if [ -d "logs" ]; then
    echo "Removing old logs..."
    rm -rf logs/*
    echo "✅ Logs cleaned"
else
    echo "No logs directory found"
fi

# Remove old models
if [ -d "models" ]; then
    echo "Removing old models..."
    rm -rf models/*
    echo "✅ Models cleaned"
else
    echo "No models directory found"
fi

# Remove training.log
if [ -f "training.log" ]; then
    echo "Removing training.log..."
    rm training.log
    echo "✅ training.log removed"
fi

echo ""
echo "Cleanup complete!"
