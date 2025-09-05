#!/bin/bash

# Simple Flask Deployment Script (Minimal Dependencies)
# This script sets up the Flask app with minimal system dependencies

set -e

echo "🚀 Simple Flask Deployment Script for AI Food Scanner Pro"
echo "========================================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Update system
print_status "Updating system packages..."
sudo apt-get update

# Install minimal Python dependencies
print_status "Installing Python and basic dependencies..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    curl \
    nginx

# Create application directory
APP_DIR="/opt/ai-food-scanner"
print_status "Creating application directory: $APP_DIR"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copy application files
print_status "Copying application files..."
cp -r . $APP_DIR/
cd $APP_DIR

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip

# Install packages one by one to handle any issues
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install "numpy>=1.19.3,<2.0.0"
pip install pillow==10.2.0
pip install requests==2.31.0
pip install pandas==2.3.2
pip install matplotlib==3.10.6
pip install tqdm==4.67.1
pip install python-dotenv==1.0.1
pip install gunicorn==21.2.0

# Try to install opencv-python-headless (no system dependencies)
print_status "Installing OpenCV (headless version)..."
pip install opencv-python-headless==4.9.0.80 || pip install opencv-python-headless

# Create uploads and logs directories
mkdir -p uploads logs

# Create systemd service
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/ai-food-scanner.service > /dev/null <<EOF
[Unit]
Description=AI Food Scanner Flask App
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
Environment=FLASK_ENV=production
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 flask_app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ai-food-scanner
sudo systemctl start ai-food-scanner

# Setup Nginx reverse proxy
print_status "Setting up Nginx reverse proxy..."
sudo tee /etc/nginx/sites-available/ai-food-scanner > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 86400;
    }
}
EOF

# Enable site and restart Nginx
sudo ln -sf /etc/nginx/sites-available/ai-food-scanner /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

# Setup firewall
print_status "Setting up firewall..."
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
echo "y" | sudo ufw enable

# Get public IP
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

print_status "Deployment completed successfully!"
print_status "Your app is accessible at: http://$PUBLIC_IP"
print_status "Direct Flask access: http://$PUBLIC_IP:5000"

# Show service status
echo ""
print_status "Service status:"
sudo systemctl status ai-food-scanner --no-pager -l

echo ""
print_status "Useful commands:"
print_status "  View logs: sudo journalctl -u ai-food-scanner -f"
print_status "  Restart: sudo systemctl restart ai-food-scanner"
print_status "  Stop: sudo systemctl stop ai-food-scanner"
print_status "  Status: sudo systemctl status ai-food-scanner"
