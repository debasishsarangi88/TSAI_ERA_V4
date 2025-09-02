#!/bin/bash

echo "🍽️ Starting AI Food Ingredient Scanner Pro..."
echo "=============================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "ai_food_scanner.py" ]; then
    echo "❌ Please run this script from the Session3 directory"
    exit 1
fi

# Start the Streamlit app
echo "🚀 Launching Streamlit app..."
echo "📱 The app will open in your browser at: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the app"
echo ""

# Run the app using uv
uv run streamlit run ai_food_scanner.py --server.port 8501
