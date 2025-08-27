#!/bin/bash

# Mullet Method Demo Reset Script
# This script resets the demo to a clean state for presentations

echo "🔄 Resetting Mullet Method Demo..."

# Remove existing database
if [ -f "demo.db" ]; then
    echo "📁 Removing existing database..."
    rm demo.db
fi

# Clear Python cache
if [ -d "__pycache__" ]; then
    echo "🧹 Clearing Python cache..."
    rm -rf __pycache__
fi

# Recreate database with sample data using virtual environment Python
echo "🌱 Creating fresh database with sample data..."
.venv/bin/python seed_data.py

echo ""
echo "✅ Demo reset complete!"
echo ""
echo "🚀 Ready to start demo. Run:"
echo "   ./start_demo.sh"
echo ""
echo "Or manually:"
echo "   .venv/bin/python app.py"
echo ""
echo "📱 Demo sites will be available at:"
echo "   - Corporate: http://localhost:5000/corporate"
echo "   - Blog: http://localhost:5000/blog"
echo "   - Portfolio: http://localhost:5000/portfolio"
echo ""
echo "🎬 Ready for live demo:"
echo "   - Run './presentation_demo.sh' for guided presentation"
echo "   - Run '.venv/bin/python add_new_site.py' to add restaurant site"
echo ""
