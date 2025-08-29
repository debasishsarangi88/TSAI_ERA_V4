#!/bin/bash

# GitHub Repository Setup Script
# This script helps you set up your GitHub repository

echo "🚀 Setting up GitHub repository for YouTube Audio Waveform Visualizer"
echo "=================================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Initializing..."
    git init
fi

# Add all files
echo "📁 Adding files to git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: YouTube Audio Waveform Visualizer

- Flask web application for YouTube audio analysis
- Waveform visualization with matplotlib
- Beautiful responsive web interface
- Docker support and CI/CD pipeline
- Comprehensive testing and documentation"

echo "✅ Repository setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Add the remote origin:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo "3. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "🔧 Development commands:"
echo "   make run      # Run the application"
echo "   make test     # Run tests"
echo "   make lint     # Run linting"
echo "   make format   # Format code"
echo ""
echo "🐳 Docker commands:"
echo "   docker-compose up --build  # Run with Docker"
echo "   docker build -t youtube-waveform-visualizer .  # Build image"
echo ""
echo "🎉 Happy coding!"
