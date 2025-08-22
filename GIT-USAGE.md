# Git Usage Guide for Tech Detector Chrome Extension

## 🚀 Quick Start

Git is now configured and ready to use! Here's how to make pushing code easier:

## 📋 Git Configuration

Your Git is configured with:
- **User**: Debasish Sarangi
- **Email**: debasishsarangi88@gmail.com
- **Default Branch**: main
- **Editor**: VS Code

## 🛠️ Git Helper Script

Use the included `git-helper.sh` script for easier Git operations:

### Quick Commands

```bash
# Check status
./git-helper.sh status

# Quick push (add, commit, push all changes)
./git-helper.sh quick-push "Your commit message"

# Create new branch
./git-helper.sh create-branch feature-name

# Switch branches
./git-helper.sh switch-branch CHROME-TECH-FINDER

# View recent commits
./git-helper.sh log
```

### Examples

```bash
# Fix a bug and push quickly
./git-helper.sh quick-push "Fix popup rendering issue"

# Create a new feature branch
./git-helper.sh create-branch feature/new-detection

# Switch to main branch
./git-helper.sh switch-branch main
```

## 🔄 Standard Git Workflow

### 1. Check Status
```bash
git status
# or
./git-helper.sh status
```

### 2. Add Changes
```bash
git add .
# or
./git-helper.sh add
```

### 3. Commit Changes
```bash
git commit -m "Your commit message"
# or
./git-helper.sh commit "Your commit message"
```

### 4. Push to Repository
```bash
git push
# or
./git-helper.sh push
```

## 🌿 Branch Management

### Current Branches
- `main` - Original arXiv Enhancer extension
- `CHROME-TECH-FINDER` - Tech Detector Chrome extension

### Switch Between Branches
```bash
# Switch to Tech Detector branch
git checkout CHROME-TECH-FINDER
# or
./git-helper.sh switch-branch CHROME-TECH-FINDER

# Switch to main branch
git checkout main
# or
./git-helper.sh switch-branch main
```

### Create New Branch
```bash
git checkout -b feature-name
# or
./git-helper.sh create-branch feature-name
```

## 📤 Quick Push Workflow

For daily development, use the quick push command:

```bash
# Make your changes to files
# Then push everything with one command:
./git-helper.sh quick-push "Description of your changes"
```

This will:
1. Add all changes
2. Commit with your message
3. Push to the remote repository

## 🔗 Repository Information

- **Repository**: https://github.com/debasishsarangi88/ERA-V4_Session1
- **Tech Detector Branch**: https://github.com/debasishsarangi88/ERA-V4_Session1/tree/CHROME-TECH-FINDER
- **Main Branch**: https://github.com/debasishsarangi88/ERA-V4_Session1/tree/main

## 🆘 Common Commands

### View Help
```bash
./git-helper.sh help
```

### View Recent Commits
```bash
./git-helper.sh log
```

### Pull Latest Changes
```bash
./git-helper.sh pull
```

### View All Branches
```bash
./git-helper.sh branch
```

## 💡 Tips

1. **Always check status** before committing: `./git-helper.sh status`
2. **Use descriptive commit messages** that explain what you changed
3. **Use the quick-push command** for daily development
4. **Create feature branches** for major changes
5. **Pull before pushing** to avoid conflicts

## 🎯 Example Workflow

```bash
# 1. Start working on a new feature
./git-helper.sh create-branch feature/new-detection

# 2. Make your changes to files
# Edit content.js, popup.js, etc.

# 3. Check what changed
./git-helper.sh status

# 4. Push your changes
./git-helper.sh quick-push "Add new technology detection patterns"

# 5. Switch back to main branch
./git-helper.sh switch-branch main
```

Now you can easily push code changes with simple commands! 🚀
