# 🔧 **EC2 Git Repository Fix Guide**

## 🚨 **Problem**
You're getting this error on EC2:
```
fatal: not a git repository (or any of the parent directories): .git
```

This means the directory `/home/ubuntu/youtube-waveform-app` on EC2 is not a git repository.

---

## 🛠️ **Solution: Manual Fix**

### **Step 1: SSH into EC2**
```bash
# From your local machine
ssh -i ~/Downloads/S2_Session_Demo.pem ubuntu@your-ec2-public-ip
```

### **Step 2: Clean up and set up fresh directory**
```bash
# Remove old directory
rm -rf /home/ubuntu/youtube-waveform-app

# Create fresh directory
mkdir -p /home/ubuntu/youtube-waveform-app
cd /home/ubuntu/youtube-waveform-app
```

### **Step 3: Initialize git repository**
```bash
# Initialize git
git init

# Add remote origin
git remote add origin https://github.com/debasishsarangi88/TSAI_ERA_V4.git

# Fetch from remote
git fetch origin

# Checkout the correct branch
git checkout -b session2/Audio_wave_app origin/session2/Audio_wave_app

# Verify setup
git status
git branch -a
```

### **Step 4: Set up Python environment**
```bash
# Check Python version
python3 --version

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install flask yt-dlp librosa numpy matplotlib scipy requests

# Verify installations
pip list | grep -E "(flask|yt-dlp|librosa)"
```

### **Step 5: Install FFmpeg**
```bash
# Update package list
sudo apt update

# Install FFmpeg
sudo apt install -y ffmpeg

# Verify installation
ffmpeg -version | head -1
```

### **Step 6: Set up directories and permissions**
```bash
# Create necessary directories
mkdir -p temp_audio logs

# Set permissions
chmod 755 temp_audio logs
chmod +x app.py

# Set ownership
sudo chown -R ubuntu:ubuntu .

# Check directory structure
ls -la
```

### **Step 7: Test and start the application**
```bash
# Activate virtual environment
source venv/bin/activate

# Test app startup
python app.py &
sleep 3
pkill -f "python app.py"

# Start app in background
nohup python app.py > logs/app.log 2>&1 &

# Check if running
ps aux | grep python

# Check port
netstat -tlnp | grep :5000

# Test health endpoint
curl http://localhost:5000/health
```

---

## 🚀 **Quick Fix Script**

If you prefer to use the automated script:

### **1. Update the script with your EC2 IP**
```bash
# Edit the script
nano fix_ec2_git.sh

# Change this line:
EC2_IP="your-actual-ec2-ip"  # Replace with your actual EC2 IP
```

### **2. Run the fix script**
```bash
chmod +x fix_ec2_git.sh
./fix_ec2_git.sh
```

---

## ✅ **Verification**

After running the fix, verify everything works:

### **1. Check git repository**
```bash
cd /home/ubuntu/youtube-waveform-app
git status
git branch
```

### **2. Check Python environment**
```bash
source venv/bin/activate
python --version
pip list | grep flask
```

### **3. Check application**
```bash
# Check if app is running
ps aux | grep python

# Check port
netstat -tlnp | grep :5000

# Test health endpoint
curl http://localhost:5000/health
```

### **4. Test web interface**
Open your browser and go to:
```
http://your-ec2-public-ip:5000
```

---

## 🔍 **Troubleshooting**

### **If git still fails:**
```bash
# Check if git is installed
git --version

# If not installed:
sudo apt update
sudo apt install -y git
```

### **If Python fails:**
```bash
# Check Python installation
python3 --version

# If not installed:
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

### **If app won't start:**
```bash
# Check logs
tail -f logs/app.log

# Check dependencies
pip list

# Try running manually
python app.py
```

---

## 🎯 **Expected Results**

After the fix:
- ✅ **Git repository working** on EC2
- ✅ **Python environment set up** with all dependencies
- ✅ **FFmpeg installed** for audio processing
- ✅ **Application running** on port 5000
- ✅ **No bot detection errors** when downloading YouTube videos
- ✅ **Web interface accessible** at `http://your-ec2-ip:5000`

**Your YouTube Audio Waveform Visualizer should now work perfectly on EC2!** 🎵✨
