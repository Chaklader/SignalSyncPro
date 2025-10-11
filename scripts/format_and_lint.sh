#!/bin/bash

# Format and Lint Python Code
# Uses Black for formatting and Ruff for linting

set -e  # Exit on error

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=================================================="
echo "Python Code Formatting & Linting"
echo "=================================================="
echo ""

# Format with Black
echo "📝 Formatting code with Black..."
black . --line-length 100 --exclude '/(\.git|\.venv|venv|build|dist|__pycache__)/'
echo "✅ Black formatting complete"
echo ""

# Lint with Ruff
echo "🔍 Linting code with Ruff..."
ruff check . --fix
echo "✅ Ruff linting complete"
echo ""

# Format with Ruff (alternative to Black, optional)
echo "🎨 Formatting with Ruff..."
ruff format .
echo "✅ Ruff formatting complete"
echo ""

echo "=================================================="
echo "✨ All done! Code is formatted and linted."
echo "=================================================="
