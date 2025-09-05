#!/bin/bash

# Update EC2 instance with classification fixes
# This script will pull the latest code and restart the Flask app

echo "🚀 Updating EC2 instance with classification fixes..."
echo "================================================"

# Navigate to the project directory
cd ~/TSAI_ERA_V4

# Pull the latest changes from GitHub
echo "📥 Pulling latest changes from GitHub..."
git pull origin Session3_AI_Food_Ingredient_Scanner_Pro

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing/updating dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Stop any running Flask processes
echo "🛑 Stopping existing Flask processes..."
pkill -f "python flask_app" || true
pkill -f "gunicorn" || true

# Wait a moment for processes to stop
sleep 3

# Start the updated Flask app
echo "🚀 Starting updated Flask app with classification fixes..."
nohup python flask_app_fixed.py > flask_app.log 2>&1 &

# Wait for app to start
sleep 5

# Check if the app is running
echo "🔍 Checking if app is running..."
if curl -s http://localhost:5001/api/health > /dev/null; then
    echo "✅ Flask app is running successfully!"
    echo "🌐 App URL: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):5001"
    
    # Show health check response
    echo "📊 Health Check Response:"
    curl -s http://localhost:5001/api/health | python3 -m json.tool
    
    # Show recent logs
    echo "📝 Recent logs:"
    tail -10 flask_app.log
else
    echo "❌ Flask app failed to start. Checking logs..."
    tail -20 flask_app.log
    exit 1
fi

echo "================================================"
echo "✅ EC2 update completed successfully!"
echo "🎯 Your app now has the classification fixes:"
echo "   - Fixed banana vs orange detection (no more overlap)"
echo "   - Improved dessert detection for Rasgulla/Rosogolla"
echo "   - More sensitive white/cream color detection"
echo "   - Better fallback logic for desserts"
echo "   - Version 3.3.0 with enhanced classification"
echo "================================================"
