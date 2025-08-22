#!/bin/bash

# Git Helper Script for Tech Detector Chrome Extension
# Usage: ./git-helper.sh [command]

echo "🚀 Git Helper for Tech Detector Chrome Extension"
echo "================================================"

case "$1" in
    "status"|"st")
        echo "📊 Checking Git status..."
        git status
        ;;
    "add")
        echo "➕ Adding all changes..."
        git add .
        ;;
    "commit")
        echo "💾 Committing changes..."
        if [ -z "$2" ]; then
            echo "Please provide a commit message: ./git-helper.sh commit 'your message'"
            exit 1
        fi
        git commit -m "$2"
        ;;
    "push")
        echo "📤 Pushing to remote repository..."
        git push
        ;;
    "pull")
        echo "📥 Pulling from remote repository..."
        git pull
        ;;
    "branch")
        echo "🌿 Current branch:"
        git branch --show-current
        echo ""
        echo "All branches:"
        git branch -a
        ;;
    "log")
        echo "📋 Recent commits:"
        git log --oneline -10
        ;;
    "quick-push"|"qp")
        echo "⚡ Quick push - add, commit, and push all changes..."
        if [ -z "$2" ]; then
            echo "Please provide a commit message: ./git-helper.sh quick-push 'your message'"
            exit 1
        fi
        git add .
        git commit -m "$2"
        git push
        echo "✅ Quick push completed!"
        ;;
    "setup-remote")
        echo "🔗 Setting up remote repository..."
        git remote add origin https://github.com/debasishsarangi88/ERA-V4_Session1.git
        echo "✅ Remote repository configured!"
        ;;
    "create-branch")
        if [ -z "$2" ]; then
            echo "Please provide a branch name: ./git-helper.sh create-branch 'branch-name'"
            exit 1
        fi
        echo "🌿 Creating new branch: $2"
        git checkout -b "$2"
        echo "✅ Branch '$2' created and switched to!"
        ;;
    "switch-branch")
        if [ -z "$2" ]; then
            echo "Please provide a branch name: ./git-helper.sh switch-branch 'branch-name'"
            exit 1
        fi
        echo "🔄 Switching to branch: $2"
        git checkout "$2"
        echo "✅ Switched to branch '$2'!"
        ;;
    "help"|"")
        echo "Available commands:"
        echo "  status, st          - Show Git status"
        echo "  add                 - Add all changes"
        echo "  commit <message>    - Commit changes with message"
        echo "  push                - Push to remote repository"
        echo "  pull                - Pull from remote repository"
        echo "  branch              - Show current and all branches"
        echo "  log                 - Show recent commits"
        echo "  quick-push, qp <message> - Add, commit, and push all changes"
        echo "  setup-remote        - Set up remote repository"
        echo "  create-branch <name> - Create and switch to new branch"
        echo "  switch-branch <name> - Switch to existing branch"
        echo "  help                - Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./git-helper.sh quick-push 'Fix popup rendering issue'"
        echo "  ./git-helper.sh create-branch feature/new-detection"
        echo "  ./git-helper.sh switch-branch CHROME-TECH-FINDER"
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo "Use './git-helper.sh help' for available commands"
        exit 1
        ;;
esac
