#!/bin/bash

# Update EC2 instance with latest changes
# This script will pull the latest code and restart the Flask app

echo "🚀 Updating EC2 instance with latest changes..."

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
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Stop any running Flask processes
echo "🛑 Stopping existing Flask processes..."
pkill -f "python flask_app.py" || true
pkill -f "gunicorn" || true

# Wait a moment for processes to stop
sleep 2

# Start the Flask app
echo "🚀 Starting Flask app..."
nohup python flask_app.py > flask_app.log 2>&1 &

# Wait for the app to start
sleep 3

# Check if the app is running
if curl -s http://localhost:5001/api/health > /dev/null; then
    echo "✅ Flask app is running successfully!"
    echo "🌐 App is available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):5001"
else
    echo "❌ Flask app failed to start. Check flask_app.log for details."
    echo "📋 Last 20 lines of log:"
    tail -20 flask_app.log
fi

echo "🎉 Update complete!"
