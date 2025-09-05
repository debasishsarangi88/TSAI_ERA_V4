#!/bin/bash

# Docker Deployment Script for AI Food Scanner
# This script deploys the Flask app using Docker

set -e

echo "🚀 Docker Deployment Script for AI Food Scanner Pro"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Docker and Docker Compose are installed"
}

# Install Docker (for EC2)
install_docker() {
    print_status "Installing Docker..."
    
    # Update package list
    sudo apt-get update
    
    # Install required packages
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Add Docker repository
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    # Start and enable Docker
    sudo systemctl start docker
    sudo systemctl enable docker
    
    print_status "Docker installed successfully"
}

# Install Docker Compose
install_docker_compose() {
    print_status "Installing Docker Compose..."
    
    # Download Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    
    # Make it executable
    sudo chmod +x /usr/local/bin/docker-compose
    
    print_status "Docker Compose installed successfully"
}

# Build and run the application
deploy_app() {
    print_status "Building and deploying the application..."
    
    # Stop existing containers
    docker-compose down 2>/dev/null || true
    
    # Build and start the application
    docker-compose up -d --build
    
    print_status "Application deployed successfully!"
}

# Setup firewall
setup_firewall() {
    print_status "Setting up firewall..."
    
    # Allow SSH
    sudo ufw allow ssh
    
    # Allow HTTP/HTTPS
    sudo ufw allow 80
    sudo ufw allow 443
    
    # Allow Flask port
    sudo ufw allow 5000
    
    # Enable firewall
    echo "y" | sudo ufw enable
    
    print_status "Firewall configured"
}

# Get public IP
get_public_ip() {
    if curl -s http://169.254.169.254/latest/meta-data/public-ipv4 > /dev/null 2>&1; then
        PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
        print_status "Public IP: $PUBLIC_IP"
        print_status "Your app is accessible at: http://$PUBLIC_IP:5000"
    else
        print_warning "Could not get public IP. Check your EC2 instance settings."
    fi
}

# Show status
show_status() {
    print_status "Checking application status..."
    docker-compose ps
    
    echo ""
    print_status "Useful commands:"
    print_status "  View logs: docker-compose logs -f"
    print_status "  Stop: docker-compose down"
    print_status "  Restart: docker-compose restart"
    print_status "  Update: docker-compose pull && docker-compose up -d"
}

# Main deployment function
main() {
    print_status "Starting Docker deployment process..."
    
    # Check if we're on EC2
    if curl -s http://169.254.169.254/latest/meta-data/instance-id > /dev/null 2>&1; then
        print_status "Running on EC2 instance"
        
        # Install Docker if not present
        if ! command -v docker &> /dev/null; then
            install_docker
            install_docker_compose
        else
            check_docker
        fi
        
        setup_firewall
    else
        print_warning "Not running on EC2 - assuming Docker is already installed"
        check_docker
    fi
    
    # Deploy application
    deploy_app
    
    # Get public IP and show status
    get_public_ip
    show_status
    
    print_status "Deployment completed successfully!"
}

# Run main function
main "$@"
