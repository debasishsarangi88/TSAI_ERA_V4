#!/bin/bash

echo "🚀 Deploying YouTube Audio Waveform Visualizer to EC2"
echo "====================================================="
echo ""

# Configuration - Update these with your actual values
EC2_USER="ubuntu"
EC2_IP="your-ec2-public-ip"  # Replace with your actual EC2 IP
KEY_FILE="$HOME/Downloads/S2_Session_Demo.pem"  # Your .pem file from Downloads
APP_DIR="/home/ubuntu/youtube-waveform-app"

echo "📋 Configuration:"
echo "  EC2 User: $EC2_USER"
echo "  EC2 IP: $EC2_IP"
echo "  Key File: $KEY_FILE"
echo "  App Directory: $APP_DIR"
echo ""

# Check if key file exists
if [ ! -f "$KEY_FILE" ]; then
    echo "❌ Key file not found: $KEY_FILE"
    echo "Please check if your .pem file is in Downloads folder"
    exit 1
fi

# Check key file permissions
if [ "$(stat -f %Lp "$KEY_FILE")" != "600" ]; then
    echo "🔧 Fixing key file permissions..."
    chmod 600 "$KEY_FILE"
fi

echo "✅ Key file found and permissions set correctly"
echo ""

# Step 1: Stop the current application
echo "🛑 Step 1: Stopping current application..."
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" << 'EOF'
    echo "Stopping Flask app..."
    pkill -f "python app.py"
    sleep 3
    
    # Check if stopped
    if pgrep -f "python app.py" > /dev/null; then
        echo "Force killing remaining processes..."
        pkill -9 -f "python app.py"
    fi
    
    echo "Checking if app is stopped..."
    ps aux | grep python | grep -v grep || echo "✅ No Python processes found"
EOF

echo "✅ Application stopped"
echo ""

# Step 2: Update code from GitHub
echo "📥 Step 2: Updating code from GitHub..."
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" << 'EOF'
    echo "Navigating to app directory..."
    cd /home/ubuntu/youtube-waveform-app
    
    echo "Backing up current app.py..."
    cp app.py app.py.backup.$(date +%Y%m%d_%H%M%S)
    
    echo "Pulling latest changes from GitHub..."
    git pull origin session2/Audio_wave_app
    
    echo "Checking if app.py was updated..."
    if git status --porcelain | grep app.py; then
        echo "✅ app.py updated successfully"
    else
        echo "⚠️  No changes detected in app.py"
    fi
    
    echo "Current git status:"
    git status --porcelain
EOF

echo "✅ Code updated from GitHub"
echo ""

# Step 3: Update dependencies
echo "📦 Step 3: Updating dependencies..."
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" << 'EOF'
    echo "Activating virtual environment..."
    cd /home/ubuntu/youtube-waveform-app
    source venv/bin/activate
    
    echo "Updating yt-dlp to latest version..."
    pip install --upgrade yt-dlp
    
    echo "Installing/updating other dependencies..."
    pip install --upgrade flask librosa numpy matplotlib scipy requests
    
    echo "Checking FFmpeg installation..."
    if command -v ffmpeg >/dev/null 2>&1; then
        echo "✅ FFmpeg is installed"
        ffmpeg -version | head -1
    else
        echo "Installing FFmpeg..."
        sudo apt update && sudo apt install -y ffmpeg
    fi
    
    echo "Verifying yt-dlp version..."
    yt-dlp --version
EOF

echo "✅ Dependencies updated"
echo ""

# Step 4: Fix permissions and create directories
echo "🔧 Step 4: Fixing permissions and creating directories..."
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" << 'EOF'
    echo "Fixing file permissions..."
    cd /home/ubuntu/youtube-waveform-app
    sudo chown -R ubuntu:ubuntu .
    chmod +x app.py
    
    echo "Creating necessary directories..."
    mkdir -p temp_audio logs
    chmod 755 temp_audio logs
    
    echo "Checking directory structure..."
    ls -la
EOF

echo "✅ Permissions and directories fixed"
echo ""

# Step 5: Start the updated application
echo "🚀 Step 5: Starting updated application..."
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" << 'EOF'
    echo "Starting Flask app..."
    cd /home/ubuntu/youtube-waveform-app
    source venv/bin/activate
    
    # Start app in background
    nohup python app.py > logs/app.log 2>&1 &
    
    echo "Waiting for app to start..."
    sleep 5
    
    echo "Checking if app is running..."
    if pgrep -f "python app.py" > /dev/null; then
        echo "✅ Flask app is running"
        ps aux | grep "python app.py" | grep -v grep
    else
        echo "❌ Flask app failed to start"
        echo "Checking logs..."
        tail -20 logs/app.log
        exit 1
    fi
    
    echo "Checking if port 5000 is listening..."
    if netstat -tlnp | grep :5000; then
        echo "✅ Port 5000 is listening"
    else
        echo "❌ Port 5000 is not listening"
    fi
EOF

echo "✅ Application started"
echo ""

# Step 6: Test the application
echo "🧪 Step 6: Testing the application..."
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" "curl -s http://localhost:5000/health")
echo "Health check response: $HEALTH_RESPONSE"

if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
fi

echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo "Your updated app is now running on EC2!"
echo ""
echo "🌐 Access URLs:"
echo "  Local: http://localhost:5000"
echo "  External: http://$EC2_IP:5000"
echo ""
echo "📋 Next Steps:"
echo "1. Test the web interface: http://$EC2_IP:5000"
echo "2. Try downloading a YouTube video"
echo "3. Check logs if issues occur: ssh -i $KEY_FILE $EC2_USER@$EC2_IP 'tail -f /home/ubuntu/youtube-waveform-app/logs/app.log'"
echo ""
echo "🔧 If you need to restart the app:"
echo "  ssh -i $KEY_FILE $EC2_USER@$EC2_IP 'cd /home/ubuntu/youtube-waveform-app && pkill -f \"python app.py\" && source venv/bin/activate && nohup python app.py > logs/app.log 2>&1 &'"
echo ""
echo "✨ Happy waveform generating!"
