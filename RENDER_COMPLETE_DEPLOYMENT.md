# Complete Render Deployment - Backend + Frontend

## Overview
Deploy both frontend and backend to Render using `render.yaml` configuration.

## Step 1: Commit Changes (30 seconds)

```bash
cd /Users/amarnagargoje/Documents/Projects/daydream

# Verify files are ready
ls -la render.yaml requirements.txt

# Commit
git add -A
git commit -m "Switch to Render: Remove Netlify, add full-stack config"
git push
```

## Step 2: Create Render Account (1 minute)

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your repositories

## Step 3: Deploy with Blueprint (3 minutes)

### Option A: Deploy from Dashboard (Easier)

1. **Click "New +"** → **"Blueprint"**

2. **Connect Repository:**
   - Find: `iaamar/geo-ai-agent` (your repo)
   - Click "Connect"

3. **Render reads `render.yaml`:**
   - Detects 2 services:
     - ✅ Backend: `daydream-geo-backend`
     - ✅ Frontend: `daydream-geo-frontend`
   - Shows preview of what will be created

4. **Give Blueprint a Name:**
   - Name: `daydream-full-stack`
   - Click "Apply"

5. **Add Environment Variables:**
   - Backend service → Environment tab
   - Click "Add Environment Variable"
   - Add:
     - `OPENAI_API_KEY` = `your-openai-key-here`
     - `PERPLEXITY_API_KEY` = `your-perplexity-key-here`

6. **Wait for Deployment:**
   - Backend builds first (~2-3 min)
   - Frontend builds after (~1-2 min)
   - Watch logs in real-time

7. **Get Backend URL:**
   - Click backend service
   - Copy URL: `https://daydream-geo-backend.onrender.com`

8. **Update Frontend Environment Variable:**
   - Click frontend service
   - Environment tab
   - Find `VITE_API_URL`
   - Update to: `https://daydream-geo-backend.onrender.com/api`
   - Click "Save Changes"

9. **Trigger Frontend Redeploy:**
   - Frontend service → Manual Deploy → "Clear build cache & deploy"

### Option B: Deploy from Terminal (Advanced)

```bash
# Install Render CLI
brew install render  # macOS
# or
npm install -g @render/cli  # npm

# Login
render login

# Deploy blueprint
render blueprint launch
```

## Step 4: Test Your Deployment (1 minute)

### Test Backend
```bash
# Health check
curl https://daydream-geo-backend.onrender.com/health
# Expected: {"status":"healthy"}

# Test API docs
open https://daydream-geo-backend.onrender.com/docs
```

### Test Frontend
```bash
# Open your app
open https://daydream-geo-frontend.onrender.com

# Should see:
# - No warning banner about missing backend
# - Can run analysis successfully
# - All features working
```

### End-to-End Test
1. Go to frontend URL
2. Click "Analyze" page
3. Use one of the example queries
4. Click "Run Analysis"
5. Should see real-time progress
6. Results should appear (may take 30-60 seconds)

## Step 5: Configure Custom Domain (Optional)

### For Frontend
1. Frontend service → Settings → Custom Domain
2. Add domain: `yourdomain.com`
3. Update DNS records:
   ```
   Type: CNAME
   Name: @
   Value: daydream-geo-frontend.onrender.com
   ```

### For Backend (if needed)
1. Backend service → Settings → Custom Domain
2. Add domain: `api.yourdomain.com`
3. Update DNS records

## Your Live URLs

After deployment:
- **Frontend:** https://daydream-geo-frontend.onrender.com
- **Backend:** https://daydream-geo-backend.onrender.com
- **API Docs:** https://daydream-geo-backend.onrender.com/docs
- **Health Check:** https://daydream-geo-backend.onrender.com/health

## What Render Deploys

### Backend Service
- **Runtime:** Python 3.11
- **Build:** Installs from `requirements.txt`
- **Start:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
- **Health Check:** `/health` endpoint
- **Auto-deploy:** On every git push to main

### Frontend Service
- **Runtime:** Node.js 18
- **Build:** `cd frontend && npm install && npm run build`
- **Serve:** Static files from `frontend/dist`
- **Connects to:** Backend API via `VITE_API_URL`
- **Auto-deploy:** On every git push to main

## Free Tier Details

**Per Service:**
- 750 hours/month (enough for 1 service 24/7)
- 512MB RAM
- Automatic SSL/HTTPS
- Spins down after 15 min inactivity
- ~30 second cold start

**Both Services Together:**
- Works on free tier!
- Backend spins down when idle
- Frontend is static (always fast)
- First request after idle: ~30 seconds
- Then fast until idle again

## Cost Breakdown

| Tier | Backend | Frontend | Total | Features |
|------|---------|----------|-------|----------|
| Free | $0 | $0 | **$0/month** | Spins down after 15 min |
| Starter | $7 | $0 | **$7/month** | Backend always on |
| Professional | $25 | $0 | **$25/month** | More RAM, faster |

**Recommendation:**
- Start with free tier
- Upgrade backend to $7 if you need it always available

## Auto-Deploy Setup

Render automatically deploys on every push to `main` branch.

```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Render automatically:
# 1. Detects push
# 2. Runs build
# 3. Deploys if successful
# 4. Sends notification
```

**Configure notifications:**
- Dashboard → Account Settings → Notifications
- Enable email/Slack for deploy events

## Environment Variables Reference

### Backend Required
- `OPENAI_API_KEY` - Your OpenAI API key
- `PERPLEXITY_API_KEY` - Your Perplexity API key
- `PORT` - Auto-set by Render
- `PYTHON_VERSION` - Set to "3.11"

### Frontend Required
- `VITE_API_URL` - Backend URL + `/api` suffix
- `NODE_VERSION` - Set to "18"

## Monitoring & Logs

### View Logs
```bash
# In Render dashboard:
# Service → Logs (live streaming)

# Or filter:
# Service → Logs → Search for "error" or specific terms
```

### Metrics
```bash
# Service → Metrics shows:
# - CPU usage
# - Memory usage
# - Request rate
# - Response times
```

### Health Checks
Backend has automatic health monitoring:
- Endpoint: `/health`
- Interval: Every 30 seconds
- Unhealthy after: 3 failed checks
- Auto-restarts if unhealthy

## Troubleshooting

### Backend Build Failed
**Check logs:**
```bash
Dashboard → Backend service → Events → Click failed build
```

**Common issues:**
```bash
# Missing dependencies
pip freeze > requirements.txt
git add requirements.txt && git commit -m "Update deps" && git push

# Wrong Python version
# Update render.yaml → PYTHON_VERSION → "3.11"

# Import errors
# Check if all files are committed
git status
```

### Frontend Build Failed
**Check Node version:**
```bash
# Update render.yaml → NODE_VERSION → "18"
```

**Check build command:**
```bash
# Test locally first
cd frontend
npm install
npm run build
# Should create dist/ folder
```

### 404 Errors on Frontend
Frontend is SPA - needs redirects:

Add to `render.yaml` under frontend service:
```yaml
routes:
  - type: rewrite
    source: /*
    destination: /index.html
```

Already configured in your setup!

### CORS Errors

Update `src/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://daydream-geo-frontend.onrender.com",
        "https://*.onrender.com",  # Allow all Render domains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then push:
```bash
git add src/main.py
git commit -m "Update CORS for Render frontend"
git push
```

### Slow First Request (Cold Start)

**This is normal on free tier:**
- Service spins down after 15 min idle
- First request wakes it up (~30 seconds)
- Subsequent requests are fast

**Solutions:**
1. **Upgrade to paid tier** ($7/month - always on)
2. **Use cron job to ping periodically:**
   ```bash
   # Use cron-job.org or UptimeRobot
   # Ping every 14 minutes:
   # URL: https://daydream-geo-backend.onrender.com/health
   ```

### Backend Not Responding
```bash
# Check if service is live
curl https://daydream-geo-backend.onrender.com/health

# If timeout or 404:
# 1. Check Render dashboard - is service running?
# 2. Check logs for errors
# 3. Verify environment variables are set
# 4. Try manual redeploy
```

### Frontend Can't Reach Backend
```bash
# Verify VITE_API_URL is correct
# Should end with /api
# Example: https://daydream-geo-backend.onrender.com/api

# Check browser console (F12)
# Look for CORS errors or 404s

# Test backend directly
curl https://daydream-geo-backend.onrender.com/api/health
```

## Performance Tips

### Optimize Backend
```python
# Add caching in src/main.py
from functools import lru_cache

@lru_cache(maxsize=128)
def get_llm_response(query: str):
    # Your LLM call here
    pass
```

### Optimize Frontend
```bash
# Already optimized with Vite
# Build creates minified production bundle
npm run build
# Check dist/ folder size
```

### Database (if needed later)
Render offers PostgreSQL:
```bash
# Dashboard → New → PostgreSQL
# Free tier: 256MB storage
# Connect via DATABASE_URL env var
```

## Security Checklist

- [x] HTTPS enabled (automatic on Render)
- [x] Environment variables for secrets
- [ ] Add CORS restrictions (update allow_origins)
- [ ] Add rate limiting (optional)
- [ ] Add authentication (if needed)
- [ ] Enable DDoS protection (paid tiers)

## Backup & Recovery

### Backup Code
```bash
# Code is in GitHub - already backed up
git remote -v
```

### Backup Environment Variables
```bash
# Export from Render dashboard:
# Service → Environment → Copy all variables
# Save to secure password manager
```

### Disaster Recovery
```bash
# If service deleted:
# 1. New Blueprint deploy
# 2. Restore environment variables
# 3. Redeploy
# Total time: ~10 minutes
```

## Next Steps

After successful deployment:

1. **Test thoroughly:**
   - [ ] All pages load
   - [ ] Analysis works end-to-end
   - [ ] Compare feature works
   - [ ] History persists

2. **Share your app:**
   - [ ] Add URL to README
   - [ ] Share on social media
   - [ ] Add to portfolio

3. **Monitor:**
   - [ ] Set up uptime monitoring
   - [ ] Configure email alerts
   - [ ] Check logs regularly

4. **Optimize:**
   - [ ] Add caching
   - [ ] Optimize bundle size
   - [ ] Add analytics

5. **Scale (if needed):**
   - [ ] Upgrade to paid tier for always-on
   - [ ] Add custom domain
   - [ ] Set up staging environment

## Support Resources

**Render Documentation:**
- https://render.com/docs

**Render Community:**
- https://community.render.com

**Your App Docs:**
- See README.md for local development
- See QUICK_START.md for features

## Success! 🎉

Once everything is deployed:

```bash
# Your live app:
echo "Frontend: https://daydream-geo-frontend.onrender.com"
echo "Backend: https://daydream-geo-backend.onrender.com"
echo "Status: Both running on Render free tier"
```

You now have a fully functional, production-ready GEO analysis platform deployed to the cloud!

