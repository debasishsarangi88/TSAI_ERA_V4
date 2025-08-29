#!/bin/bash

echo "🚀 YouTube Audio Waveform Visualizer - GitHub Push Setup"
echo "========================================================"
echo ""

# Check if git is configured
if ! git config --get user.name > /dev/null 2>&1; then
    echo "❌ Git user.name not configured"
    echo "Please run: git config --global user.name 'Your Name'"
    exit 1
fi

if ! git config --get user.email > /dev/null 2>&1; then
    echo "❌ Git user.email not configured"
    echo "Please run: git config --global user.email 'your.email@example.com'"
    exit 1
fi

echo "✅ Git configuration verified"
echo ""

# Show current status
echo "📊 Current Git Status:"
echo "  Branch: $(git branch --show-current)"
echo "  Last commit: $(git log -1 --oneline)"
echo "  Files committed: $(git ls-files | wc -l | tr -d ' ')"
echo ""

echo "📋 Next Steps to Push to GitHub:"
echo "=================================="
echo ""
echo "1. 🆕 Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: youtube-waveform-visualizer"
echo "   - Description: YouTube Audio Waveform Visualizer - Flask web app"
echo "   - Make it Public or Private (your choice)"
echo "   - DO NOT initialize with README, .gitignore, or license (we already have them)"
echo "   - Click 'Create repository'"
echo ""
echo "2. 🔗 Add the remote repository (replace YOUR_USERNAME with your GitHub username):"
echo "   git remote add origin https://github.com/YOUR_USERNAME/youtube-waveform-visualizer.git"
echo ""
echo "3. 🚀 Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "4. 🌐 Verify on GitHub:"
echo "   - Visit your repository URL"
echo "   - Check that all files are uploaded"
echo "   - Verify the README.md displays correctly"
echo ""

echo "📁 Files ready to push:"
echo "========================"
git ls-files | head -20
if [ $(git ls-files | wc -l) -gt 20 ]; then
    echo "... and $(($(git ls-files | wc -l) - 20)) more files"
fi
echo ""

echo "🎯 Quick Commands (after creating GitHub repo):"
echo "==============================================="
echo "# Replace YOUR_USERNAME with your actual GitHub username"
echo "git remote add origin https://github.com/YOUR_USERNAME/youtube-waveform-visualizer.git"
echo "git push -u origin main"
echo ""

echo "✨ Your project is ready for GitHub!"
echo "   All files are committed and ready to push."
echo "   Just follow the steps above to create your repository."
