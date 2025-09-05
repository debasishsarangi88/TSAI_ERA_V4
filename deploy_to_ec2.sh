#!/bin/bash

# Deploy latest changes to EC2 instance
# This script will update the EC2 instance with the latest food detection fix

echo "🚀 Starting EC2 deployment with latest changes..."

# Check if we have the required parameters
if [ -z "$1" ]; then
    echo "❌ Error: Please provide your EC2 public IP address"
    echo "Usage: ./deploy_to_ec2.sh YOUR_EC2_PUBLIC_IP"
    echo "Example: ./deploy_to_ec2.sh 3.15.123.45"
    exit 1
fi

EC2_IP=$1
KEY_FILE="your-key.pem"  # Update this with your actual key file name

echo "📡 Connecting to EC2 instance: $EC2_IP"

# Create the deployment commands
cat > ec2_deployment_commands.sh << 'EOF'
#!/bin/bash

echo "🔧 Starting EC2 update process..."

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
pip install --upgrade pip
pip install -r requirements.txt

# Stop any running Flask processes
echo "🛑 Stopping existing Flask processes..."
pkill -f "python flask_app.py" || true
pkill -f "gunicorn" || true

# Wait a moment for processes to stop
sleep 3

# Start the Flask app
echo "🚀 Starting Flask app with latest changes..."
nohup python flask_app.py > flask_app.log 2>&1 &

# Wait for the app to start
sleep 5

# Check if the app is running
echo "🔍 Checking if Flask app is running..."
if curl -s http://localhost:5001/api/health > /dev/null; then
    echo "✅ Flask app is running successfully!"
    echo "🌐 App is available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):5001"
    echo "📊 Health check response:"
    curl -s http://localhost:5001/api/health | python3 -m json.tool
else
    echo "❌ Flask app failed to start. Checking logs..."
    echo "📋 Last 20 lines of log:"
    tail -20 flask_app.log
    echo ""
    echo "🔍 Checking for any running processes:"
    ps aux | grep python
fi

echo "🎉 EC2 update process complete!"
EOF

# Make the deployment script executable
chmod +x ec2_deployment_commands.sh

echo "📤 Uploading deployment script to EC2..."
scp -i $KEY_FILE ec2_deployment_commands.sh ubuntu@$EC2_IP:~/

echo "🚀 Executing deployment on EC2..."
ssh -i $KEY_FILE ubuntu@$EC2_IP "chmod +x ~/ec2_deployment_commands.sh && ~/ec2_deployment_commands.sh"

# Clean up local files
rm ec2_deployment_commands.sh

echo "✅ Deployment complete!"
echo "🌐 Your updated app should be available at: http://$EC2_IP:5001"
echo "🔍 Test the food detection by uploading any food image!"
