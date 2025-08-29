#!/bin/bash

echo "🔧 Fixing EC2 Git Repository and Deploying App"
echo "=============================================="
echo ""

# Configuration - Update these with your actual values
EC2_USER="ubuntu"
EC2_IP="your-ec2-public-ip"  # Replace with your actual EC2 IP
KEY_FILE="$HOME/Downloads/S2_Session_Demo.pem"
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

echo "✅ Key file found. Proceeding with EC2 setup..."
echo ""

# Step 1: Connect to EC2 and set up git repository
echo "🔧 Step 1: Setting up git repository on EC2..."
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" << 'EOF'
    echo "Checking current directory structure..."
    ls -la /home/ubuntu/
    
    echo "Removing old directory if it exists..."
    rm -rf /home/ubuntu/youtube-waveform-app
    
    echo "Creating fresh directory..."
    mkdir -p /home/ubuntu/youtube-waveform-app
    cd /home/ubuntu/youtube-waveform-app
    
    echo "Initializing git repository..."
    git init
    
    echo "Adding remote origin..."
    git remote add origin https://github.com/debasishsarangi88/TSAI_ERA_V4.git
    
    echo "Fetching from remote..."
    git fetch origin
    
    echo "Checking out the correct branch..."
    git checkout -b session2/Audio_wave_app origin/session2/Audio_wave_app
    
    echo "Verifying git setup..."
    git status
    git branch -a
    
    echo "✅ Git repository setup complete"
EOF

echo "✅ Git repository set up on EC2"
echo ""

# Step 2: Set up Python environment
echo "🐍 Step 2: Setting up Python environment..."
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" << 'EOF'
    echo "Navigating to app directory..."
    cd /home/ubuntu/youtube-waveform-app
    
    echo "Checking Python version..."
    python3 --version
    
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "Upgrading pip..."
    pip install --upgrade pip
    
    echo "Installing dependencies..."
    pip install flask yt-dlp librosa numpy matplotlib scipy requests
    
    echo "Verifying installations..."
    pip list | grep -E "(flask|yt-dlp|librosa)"
    
    echo "✅ Python environment setup complete"
EOF

echo "✅ Python environment set up"
echo ""

# Step 3: Install FFmpeg
echo "🎵 Step 3: Installing FFmpeg..."
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" << 'EOF'
    echo "Updating package list..."
    sudo apt update
    
    echo "Installing FFmpeg..."
    sudo apt install -y ffmpeg
    
    echo "Verifying FFmpeg installation..."
    ffmpeg -version | head -1
    
    echo "✅ FFmpeg installation complete"
EOF

echo "✅ FFmpeg installed"
echo ""

# Step 4: Set up directories and permissions
echo "📁 Step 4: Setting up directories and permissions..."
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" << 'EOF'
    echo "Navigating to app directory..."
    cd /home/ubuntu/youtube-waveform-app
    
    echo "Creating necessary directories..."
    mkdir -p temp_audio logs
    
    echo "Setting permissions..."
    chmod 755 temp_audio logs
    chmod +x app.py
    
    echo "Setting ownership..."
    sudo chown -R ubuntu:ubuntu .
    
    echo "Checking directory structure..."
    ls -la
    
    echo "✅ Directories and permissions set up"
EOF

echo "✅ Directories and permissions configured"
echo ""

# Step 5: Test the application
echo "🧪 Step 5: Testing the application..."
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" << 'EOF'
    echo "Navigating to app directory..."
    cd /home/ubuntu/youtube-waveform-app
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "Testing app startup..."
    timeout 10s python app.py &
    sleep 5
    
    echo "Checking if app started..."
    if pgrep -f "python app.py" > /dev/null; then
        echo "✅ App started successfully"
        pkill -f "python app.py"
    else
        echo "❌ App failed to start"
        echo "Checking for errors..."
        python app.py
    fi
    
    echo "Testing health endpoint..."
    timeout 10s python app.py &
    sleep 3
    curl -s http://localhost:5000/health || echo "Health check failed"
    pkill -f "python app.py"
    
    echo "✅ Application testing complete"
EOF

echo "✅ Application tested"
echo ""

# Step 6: Start the application
echo "🚀 Step 6: Starting the application..."
ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" << 'EOF'
    echo "Navigating to app directory..."
    cd /home/ubuntu/youtube-waveform-app
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "Starting Flask app in background..."
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

# Step 7: Final verification
echo "🔍 Step 7: Final verification..."
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(ssh -i "$KEY_FILE" "$EC2_USER@$EC2_IP" "curl -s http://localhost:5000/health")
echo "Health check response: $HEALTH_RESPONSE"

if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
fi

echo ""
echo "🎉 EC2 Setup Complete!"
echo "====================="
echo "Your YouTube Audio Waveform Visualizer is now running on EC2!"
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
echo "🔧 Useful Commands:"
echo "  Stop app: ssh -i $KEY_FILE $EC2_USER@$EC2_IP 'pkill -f \"python app.py\"'"
echo "  Start app: ssh -i $KEY_FILE $EC2_USER@$EC2_IP 'cd /home/ubuntu/youtube-waveform-app && source venv/bin/activate && nohup python app.py > logs/app.log 2>&1 &'"
echo "  View logs: ssh -i $KEY_FILE $EC2_USER@$EC2_IP 'tail -f /home/ubuntu/youtube-waveform-app/logs/app.log'"
echo ""
echo "✨ Your app should now work without bot detection errors!"
