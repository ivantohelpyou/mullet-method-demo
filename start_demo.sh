#!/bin/bash

# Mullet Method Demo Start Script
# This script starts the Flask application for the demo

echo "🚀 Starting Mullet Method Demo..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Check if database exists
if [ ! -f "mullet_demo.db" ]; then
    echo "📁 Database not found. Creating fresh database..."
    .venv/bin/python seed_data.py
fi

echo "🐍 Starting Flask application..."
echo ""
echo "📱 Demo sites will be available at:"
echo "   - Corporate: http://localhost:5000/corporate"
echo "   - Blog: http://localhost:5000/blog"
echo "   - Portfolio: http://localhost:5000/portfolio"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
.venv/bin/python app.py
