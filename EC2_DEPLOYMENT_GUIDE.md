# 🚀 **EC2 Deployment Guide - YouTube Audio Waveform Visualizer**

## 📋 **What Was Fixed**

The updated `app.py` now includes:
- ✅ **Anti-bot measures** for YouTube downloads
- ✅ **Better error handling** and logging
- ✅ **Port 5000 configuration** (instead of 8000)
- ✅ **EC2 compatibility** improvements
- ✅ **Comprehensive logging** for debugging

---

## 🔧 **Your Setup Information**

### **Key File Location:**
- **PEM File:** `~/Downloads/S2_Session_Demo.pem`
- **Working Directory:** `/Users/dragosierra/TSAI_ERAV4/Session2`
- **GitHub Branch:** `session2/Audio_wave_app`

---

## 🔄 **Method 1: Automatic Deployment (Recommended)**

### **1.1 Update the Deployment Script**
```bash
# Edit the deployment script with your EC2 IP
nano deploy_to_ec2.sh

# Update this line with your actual EC2 IP:
EC2_IP="your-actual-ec2-ip"  # e.g., "3.250.123.45"
```

### **1.2 Run the Deployment Script**
```bash
# Make script executable
chmod +x deploy_to_ec2.sh

# Run deployment
./deploy_to_ec2.sh
```

---

## 🔧 **Method 2: Manual Deployment**

### **2.1 SSH into EC2 (using your Downloads .pem file)**
```bash
# Navigate to your project directory
cd /Users/dragosierra/TSAI_ERAV4/Session2

# SSH using the .pem file from Downloads
ssh -i ~/Downloads/S2_Session_Demo.pem ubuntu@your-ec2-public-ip
```

### **2.2 Stop Current Application**
```bash
# Stop Flask app
pkill -f "python app.py"

# Verify stopped
ps aux | grep python
```

### **2.3 Update Code from GitHub**
```bash
# Navigate to app directory
cd /home/ubuntu/youtube-waveform-app

# Backup current app.py
cp app.py app.py.backup.$(date +%Y%m%d_%H%M%S)

# Pull latest changes
git pull origin session2/Audio_wave_app

# Verify changes
git status
```

### **2.4 Update Dependencies**
```bash
# Activate virtual environment
source venv/bin/activate

# Update yt-dlp (critical for anti-bot measures)
pip install --upgrade yt-dlp

# Update other packages
pip install --upgrade flask librosa numpy matplotlib scipy requests

# Verify FFmpeg
ffmpeg -version
```

### **2.5 Fix Permissions and Directories**
```bash
# Fix ownership
sudo chown -R ubuntu:ubuntu .

# Fix permissions
chmod +x app.py

# Create necessary directories
mkdir -p temp_audio logs
chmod 755 temp_audio logs
```

### **2.6 Start Updated Application**
```bash
# Start app in background
nohup python app.py > logs/app.log 2>&1 &

# Check if running
ps aux | grep python

# Check port
netstat -tlnp | grep :5000
```

---

## 🧪 **Method 3: Test the Fix**

### **3.1 Health Check**
```bash
# Test health endpoint
curl http://localhost:5000/health

# Expected: {"status": "healthy", "timestamp": "..."}
```

### **3.2 Test YouTube Download**
```bash
# Test with a simple URL
curl -X POST http://localhost:5000/analyze \
  -F "youtube_url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### **3.3 Check Logs**
```bash
# View application logs
tail -f logs/app.log

# Look for successful downloads
grep -i "successfully downloaded" logs/app.log
```

---

## 🌐 **Access Your Updated App**

### **3.1 Web Interface**
```
http://your-ec2-public-ip:5000
```

### **3.2 Test Features**
1. **Enter YouTube URL** in the input field
2. **Click "Analyze Audio & Generate Waveform"**
3. **Wait for processing** (should work without bot detection)
4. **View generated waveform** and audio information

---

## 🔍 **Troubleshooting**

### **If SSH Connection Fails**
```bash
# Check .pem file permissions
chmod 600 ~/Downloads/S2_Session_Demo.pem

# Try SSH with verbose output
ssh -v -i ~/Downloads/S2_Session_Demo.pem ubuntu@your-ec2-public-ip
```

### **If App Won't Start**
```bash
# Check logs
tail -20 logs/app.log

# Check if port 5000 is free
sudo netstat -tlnp | grep :5000

# Kill any process using port 5000
sudo fuser -k 5000/tcp
```

### **If YouTube Download Still Fails**
```bash
# Check yt-dlp version
yt-dlp --version

# Test yt-dlp directly
yt-dlp --extract-audio --audio-format m4a "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Check app logs
tail -f logs/app.log
```

### **If Port 5000 is Blocked**
```bash
# Check firewall
sudo ufw status

# Allow port 5000
sudo ufw allow 5000

# Check security group in AWS Console
# Ensure Custom TCP Port 5000 is allowed
```

---

## 📊 **Verification Checklist**

After deployment:
- [ ] **App starts:** `python app.py` runs without errors
- [ ] **Port 5000:** `netstat -tlnp | grep :5000` shows listening
- [ ] **Health check:** `curl http://localhost:5000/health` works
- [ ] **Web interface:** `http://your-ec2-ip:5000` loads
- [ ] **YouTube download:** Test with a simple URL works
- [ ] **No bot detection:** No "Sign in to confirm you're not a bot" errors
- [ ] **Logs working:** `tail -f logs/app.log` shows activity

---

## 🚀 **Quick Commands Reference**

```bash
# SSH to EC2 (from your project directory)
ssh -i ~/Downloads/S2_Session_Demo.pem ubuntu@your-ec2-public-ip

# Stop app
pkill -f "python app.py"

# Update from GitHub
git pull origin session2/Audio_wave_app

# Start app
nohup python app.py > logs/app.log 2>&1 &

# Check status
ps aux | grep python
netstat -tlnp | grep :5000

# View logs
tail -f logs/app.log

# Test health
curl http://localhost:5000/health
```

---

## 🎯 **Expected Results**

After successful deployment:
- ✅ **No more bot detection errors**
- ✅ **YouTube downloads work smoothly**
- ✅ **Waveform generation successful**
- ✅ **Better error messages and logging**
- ✅ **App accessible on port 5000**

**Your YouTube Audio Waveform Visualizer should now work perfectly on EC2!** 🎵✨
