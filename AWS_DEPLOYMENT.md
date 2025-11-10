# AWS EC2 Deployment - Auto-Detection

## ✅ Smart Configuration Applied

The frontend now **automatically detects** the environment and connects to the right backend:

**On localhost:**
```
Frontend: http://localhost:5173
Backend: http://localhost:8000 (via proxy)
Mode: Local development
```

**On AWS EC2:**
```
Frontend: http://3.12.198.127:5173
Backend: http://3.12.198.127:8000 (auto-detected)
Mode: AWS deployment
```

**On Netlify (if redeployed):**
```
Frontend: https://your-site.netlify.app
Backend: Set via VITE_API_URL env var
Mode: Production
```

---

## How It Works

**New config file:** `frontend/src/config.js`

**Auto-detection logic:**
```javascript
1. Check VITE_API_URL env var (production)
2. If localhost → use proxy (same origin)
3. If AWS/remote → use same hostname with :8000
```

**Result:** No manual configuration needed! ✅

---

## Deployment on AWS

### Step 1: Commit Changes

```bash
cd ~/geo-ai-agent

git add frontend/vite.config.js frontend/src/config.js frontend/src/pages/
git commit -m "Add smart API URL auto-detection for localhost and AWS"
git push
```

### Step 2: Pull on AWS Server

```bash
# On your Ubuntu server
cd ~/geo-ai-agent
git pull
```

### Step 3: Restart Frontend

```bash
cd ~/geo-ai-agent/frontend
pkill -f vite
npm run dev -- --host 0.0.0.0
```

### Step 4: Open AWS Security Ports

**In EC2 Security Group, add inbound rules:**

**Port 8000** (Backend):
- Type: Custom TCP
- Port: 8000
- Source: 0.0.0.0/0

**Port 5173** (Frontend):
- Type: Custom TCP
- Port: 5173
- Source: 0.0.0.0/0

---

## Access Your App

**After ports are open:**

**Frontend:**
```
http://3.12.198.127:5173
```

**The app will automatically connect to:**
```
http://3.12.198.127:8000
```

**No manual configuration needed!** The frontend detects it's on AWS and uses the same IP with port 8000.

---

## Test It

**On AWS server:**
```bash
# Start backend (if not running)
cd ~/geo-ai-agent
.venv/bin/python -m src.main &

# Start frontend
cd ~/geo-ai-agent/frontend
npm run dev -- --host 0.0.0.0
```

**Open browser:**
```
http://3.12.198.127:5173
```

**Click "Run Analysis"** → Should work! ✅

---

## For Production (Keep Running)

```bash
# Use PM2 to manage both processes
sudo npm install -g pm2

# Start backend
cd ~/geo-ai-agent
pm2 start ".venv/bin/python -m src.main" --name geo-backend

# Start frontend  
cd ~/geo-ai-agent/frontend
pm2 start "npm run dev -- --host 0.0.0.0" --name geo-frontend

# Check status
pm2 list

# Save to restart on reboot
pm2 save
pm2 startup
```

---

## Summary

**Changes made:**
- ✅ `frontend/src/config.js` - Smart API URL detection
- ✅ `frontend/vite.config.js` - Proxy for localhost
- ✅ `AnalysisPage.jsx` - Uses auto-detected URL
- ✅ `ComparePage.jsx` - Uses auto-detected URL

**Result:**
- Works on localhost automatically
- Works on AWS automatically
- Works on Netlify with env var

**Commit, push, pull on AWS, restart frontend - it will work!** 🚀
