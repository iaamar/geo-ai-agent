# 🔧 Why Your AWS Instance App Goes Down (And How to Fix It)

## ❌ The Problem

Your app is **dying when you disconnect from SSH** because:

1. **Processes are attached to your terminal session**
   - When SSH disconnects, the shell sends SIGHUP to all child processes
   - Background processes (`&`) still die when the parent shell exits
   - No process manager to keep them alive

2. **The `run.sh` script runs in foreground**
   - Line 192-193: Uses `trap` and `wait` which keeps the script running
   - When you close SSH, the script exits → all processes die

3. **No auto-restart mechanism**
   - If the app crashes, it doesn't restart
   - If the server reboots, the app doesn't start automatically

---

## ✅ Solutions (Choose One)

### **Option 1: systemd Service (RECOMMENDED for Production)** ⭐

**Best for:** Production servers, auto-restart, logging, monitoring

**Setup:**

```bash
# On your AWS Ubuntu server:

# 1. Copy service files
cd ~/geo-ai-agent
sudo cp deploy/geo-agent.service /etc/systemd/system/
sudo cp deploy/geo-agent-frontend.service /etc/systemd/system/

# 2. Update paths in service files (if needed)
sudo nano /etc/systemd/system/geo-agent.service
# Verify: WorkingDirectory, ExecStart paths match your setup

# 3. Reload systemd
sudo systemctl daemon-reload

# 4. Enable services (start on boot)
sudo systemctl enable geo-agent.service
sudo systemctl enable geo-agent-frontend.service

# 5. Start services
sudo systemctl start geo-agent.service
sudo systemctl start geo-agent-frontend.service

# 6. Check status
sudo systemctl status geo-agent.service
sudo systemctl status geo-agent-frontend.service

# 7. View logs
sudo journalctl -u geo-agent.service -f
sudo journalctl -u geo-agent-frontend.service -f
```

**Benefits:**
- ✅ Auto-starts on server reboot
- ✅ Auto-restarts if app crashes
- ✅ Proper logging via journalctl
- ✅ Can stop/start/restart easily
- ✅ Survives SSH disconnects

**Commands:**
```bash
# Stop
sudo systemctl stop geo-agent.service

# Start
sudo systemctl start geo-agent.service

# Restart
sudo systemctl restart geo-agent.service

# Check status
sudo systemctl status geo-agent.service

# View logs
sudo journalctl -u geo-agent.service -n 100
```

---

### **Option 2: nohup (Quick Fix)**

**Best for:** Quick testing, temporary setup

```bash
# On your AWS server:

# Stop current processes
pkill -f "python -m src.main"
pkill -f "npm run dev"

# Start with nohup (detached from terminal)
cd ~/geo-ai-agent
source .venv/bin/activate
nohup .venv/bin/python -m src.main > backend.log 2>&1 &

cd frontend
nohup npm run dev > ../frontend.log 2>&1 &

# Check they're running
ps aux | grep "python -m src.main"
ps aux | grep "npm run dev"

# View logs
tail -f ~/geo-ai-agent/backend.log
tail -f ~/geo-ai-agent/frontend.log
```

**Benefits:**
- ✅ Quick setup (2 commands)
- ✅ Survives SSH disconnect
- ✅ Logs to files

**Drawbacks:**
- ❌ No auto-restart on crash
- ❌ No auto-start on reboot
- ❌ Manual log management

---

### **Option 3: screen or tmux (Development)**

**Best for:** Development, debugging, interactive sessions

```bash
# Install screen
sudo apt install screen -y

# Start a screen session
screen -S geo-agent

# Inside screen, run your app
cd ~/geo-ai-agent
./run.sh

# Detach: Press Ctrl+A, then D
# Reattach: screen -r geo-agent
```

**Benefits:**
- ✅ Keep terminal session alive
- ✅ Can reattach later
- ✅ See live logs

**Drawbacks:**
- ❌ Still dies if server reboots
- ❌ Manual restart needed

---

### **Option 4: PM2 (Node.js Process Manager)**

**Best for:** Node.js apps, easy process management

```bash
# Install PM2
sudo npm install -g pm2

# Start backend with PM2
cd ~/geo-ai-agent
source .venv/bin/activate
pm2 start .venv/bin/python --name "geo-backend" -- -m src.main

# Start frontend with PM2
cd frontend
pm2 start npm --name "geo-frontend" -- run dev

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup
# Follow the command it prints

# Check status
pm2 status
pm2 logs
```

**Benefits:**
- ✅ Auto-restart on crash
- ✅ Auto-start on reboot
- ✅ Easy monitoring dashboard
- ✅ Log management

---

## 🔍 Check Why It's Going Down

### 1. **Is the EC2 instance stopping?**

```bash
# Check instance status in AWS Console
# EC2 → Instances → Check "Instance State"

# Check system logs
sudo journalctl -b -1  # Previous boot logs
sudo dmesg | tail -50  # Recent kernel messages
```

**Common causes:**
- Spot instance termination
- Auto-shutdown script
- Out of memory (OOM killer)
- Instance limit reached

### 2. **Is the app crashing?**

```bash
# Check if processes are running
ps aux | grep "python -m src.main"
ps aux | grep "npm run dev"

# Check system logs
sudo journalctl -xe | tail -50

# Check for OOM (Out of Memory)
dmesg | grep -i "killed process"
free -h  # Check memory usage
```

### 3. **Is SSH disconnecting?**

```bash
# Check SSH session timeout
sudo nano /etc/ssh/sshd_config
# Look for: ClientAliveInterval, ClientAliveCountMax

# Increase timeout (optional)
# ClientAliveInterval 60
# ClientAliveCountMax 3
```

---

## 🎯 Recommended Setup for AWS

**For Production:**
1. ✅ Use **systemd services** (Option 1)
2. ✅ Enable auto-start on boot
3. ✅ Monitor with `systemctl status`
4. ✅ Check logs with `journalctl`

**Quick Commands:**
```bash
# Setup (one time)
sudo cp deploy/geo-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable geo-agent.service geo-agent-frontend.service
sudo systemctl start geo-agent.service geo-agent-frontend.service

# Daily use
sudo systemctl status geo-agent.service  # Check if running
sudo journalctl -u geo-agent.service -f  # Watch logs
```

---

## 📊 Verify It's Working

```bash
# 1. Check services are running
sudo systemctl status geo-agent.service

# 2. Check ports are listening
sudo netstat -tlnp | grep -E "8000|5173"

# 3. Test endpoints
curl http://localhost:8000/health
curl http://localhost:5173

# 4. Disconnect SSH and reconnect
# App should still be running!
```

---

## 🚨 Troubleshooting

**Service won't start:**
```bash
# Check service file syntax
sudo systemctl status geo-agent.service

# Check logs
sudo journalctl -u geo-agent.service -n 50

# Verify paths in service file
sudo cat /etc/systemd/system/geo-agent.service
```

**Port already in use:**
```bash
# Find what's using the port
sudo lsof -i :8000
sudo lsof -i :5173

# Kill it
sudo kill -9 <PID>
```

**Permission denied:**
```bash
# Ensure service file has correct user
sudo nano /etc/systemd/system/geo-agent.service
# User=ubuntu (or your username)
```

---

## ✅ Summary

**The root cause:** Processes die when SSH disconnects because they're attached to the terminal session.

**The fix:** Use systemd services to run processes as daemons that survive SSH disconnects and auto-restart.

**Quick fix:** Use `nohup` for immediate relief, but systemd is better for production.

**Your app will now stay running even after you disconnect!** 🚀

