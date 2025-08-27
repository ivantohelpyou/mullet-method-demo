#!/bin/bash

# Simple activation script for the demo
# Usage: source activate.sh

echo "🐍 Activating Mullet Method Demo environment..."
source .venv/bin/activate

echo "✅ Virtual environment activated!"
echo "📍 Python location: $(which python)"
echo ""
echo "🚀 Ready to run:"
echo "   python seed_data.py    # Reset database"
echo "   python app.py          # Start demo"
echo "   ./reset_demo.sh        # Full reset"
echo "   ./start_demo.sh        # Start with checks"
