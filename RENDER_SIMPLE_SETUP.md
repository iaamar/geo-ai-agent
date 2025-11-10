# Simple Render Deployment - 2 Steps

## The Issue with render.yaml

Render's Blueprint doesn't support:
- `type: static` for static sites
- Installing Node.js in Python environment
- Two different runtimes in one Blueprint

## Solution: Deploy Separately (Still Simple!)

### Step 1: Deploy Backend (3 minutes)

1. **Go to Render:** https://render.com
2. **New + → Web Service**
3. **Connect Repository:** `iaamar/geo-ai-agent`
4. **Configure:**
   - Name: `daydream-geo-backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - Plan: `Free`
5. **Environment Variables:**
   - `OPENAI_API_KEY` = your-key
   - `PERPLEXITY_API_KEY` = your-key
6. **Create Web Service**
7. **Copy URL:** `https://daydream-geo-backend.onrender.com`

### Step 2: Deploy Frontend (2 minutes)

1. **New + → Static Site**
2. **Connect Same Repository:** `iaamar/geo-ai-agent`
3. **Configure:**
   - Name: `daydream-geo-frontend`
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`
4. **Environment Variables:**
   - `VITE_API_URL` = `https://daydream-geo-backend.onrender.com/api`
     (use the URL from Step 1, add `/api`)
5. **Create Static Site**

### Done! ✅

- **Backend:** https://daydream-geo-backend.onrender.com
- **Frontend:** https://daydream-geo-frontend.onrender.com
- **Total Time:** 5 minutes
- **Cost:** $0 (both on free tier)

## Test Your Deployment

```bash
# Test backend
curl https://daydream-geo-backend.onrender.com/health
# Expected: {"status":"healthy"}

# Open frontend
open https://daydream-geo-frontend.onrender.com
# Should work with full functionality!
```

## Why This Works

- **Backend:** Python environment, perfect for FastAPI
- **Frontend:** Node environment, perfect for React/Vite
- **Separate services:** Each uses the right runtime
- **Free tier:** Both qualify for free tier
- **Auto-deploy:** Both redeploy on git push

## Auto-Deploy

Both services auto-deploy when you push to GitHub:

```bash
git push
# Render automatically:
# - Rebuilds backend
# - Rebuilds frontend
# - Deploys both
```

## Cost Breakdown

| Service | Type | Cost | Notes |
|---------|------|------|-------|
| Backend | Web Service | Free | Spins down after 15 min idle |
| Frontend | Static Site | Free | Always fast, CDN-backed |
| **Total** | | **$0/month** | |

**Upgrade Options:**
- Backend always-on: $7/month
- Keep frontend free (static sites don't spin down)

## Troubleshooting

### Backend Issues

**Build fails:**
```bash
# Check if all dependencies are in requirements.txt
pip freeze > requirements.txt
git push
```

**Import errors:**
```bash
# Verify Python version
# In Render: Environment → PYTHON_VERSION = "3.11"
```

### Frontend Issues

**Build fails:**
```bash
# Test locally first
cd frontend
npm install
npm run build
# Should create dist/ folder
```

**Can't reach backend:**
```bash
# Verify VITE_API_URL ends with /api
# Should be: https://your-backend.onrender.com/api
#           NOT: https://your-backend.onrender.com
```

**404 on routes:**
```bash
# Static sites need rewrites for SPA
# This is automatic on Render static sites
# If issues persist, check Render docs
```

### CORS Errors

If you see CORS errors in browser console:

Update `src/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://daydream-geo-frontend.onrender.com",
        "https://*.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Monitoring

### Check Service Health

**Backend:**
```bash
# Health endpoint
curl https://daydream-geo-backend.onrender.com/health

# API docs
open https://daydream-geo-backend.onrender.com/docs
```

**Frontend:**
```bash
# Load test
curl -I https://daydream-geo-frontend.onrender.com
# Should return 200 OK
```

### View Logs

**In Render Dashboard:**
1. Click service
2. Go to "Logs" tab
3. See real-time logs
4. Filter by error/warning

### Set Up Alerts

**In Render:**
1. Service → Settings → Notifications
2. Add email for:
   - Deploy failures
   - Service crashes
   - Health check failures

## Performance Tips

### Keep Backend Awake (Optional)

Free tier spins down after 15 min idle. To keep it awake:

**Use UptimeRobot (Free):**
1. Sign up at https://uptimerobot.com
2. Add monitor:
   - Type: HTTP(s)
   - URL: https://daydream-geo-backend.onrender.com/health
   - Interval: 5 minutes
3. Backend stays awake!

**Or use Cron-job.org:**
1. Sign up at https://cron-job.org
2. Create job:
   - URL: https://daydream-geo-backend.onrender.com/health
   - Schedule: Every 14 minutes
3. Done!

### Optimize Frontend

Already optimized with Vite:
- Code splitting
- Minification
- Tree shaking
- Asset optimization

Check bundle size:
```bash
cd frontend
npm run build
# Shows bundle sizes
```

## Next Steps

### Custom Domain (Optional)

**For Frontend:**
1. Render Dashboard → Frontend → Settings → Custom Domain
2. Add: `yourdomain.com`
3. Update DNS:
   ```
   Type: CNAME
   Name: @
   Value: daydream-geo-frontend.onrender.com
   ```

**For Backend API:**
1. Backend → Settings → Custom Domain
2. Add: `api.yourdomain.com`
3. Update DNS
4. Update frontend `VITE_API_URL` to use custom domain

### Production Checklist

- [ ] Backend deployed and healthy
- [ ] Frontend deployed and accessible
- [ ] Can run analysis end-to-end
- [ ] No console errors
- [ ] API keys secure (not in code)
- [ ] CORS configured correctly
- [ ] Health monitoring set up
- [ ] Deploy notifications enabled
- [ ] Custom domain (optional)
- [ ] Uptime monitoring (optional)

## Comparison: Blueprint vs Separate

| Aspect | Blueprint (render.yaml) | Separate Deployment |
|--------|-------------------------|---------------------|
| Setup Time | Would be 3 min | 5 min (2 services) |
| Works? | ❌ No (limitations) | ✅ Yes |
| Free Tier | Would be yes | ✅ Yes |
| Maintenance | Would be easy | ✅ Easy |
| Flexibility | Limited | ✅ Full control |

**Result:** Separate deployment is better and actually works!

## Summary

**What You Did:**
1. Deployed backend as Web Service (3 min)
2. Deployed frontend as Static Site (2 min)
3. Connected them via VITE_API_URL

**What You Get:**
- Full-stack app live on internet
- Both services on free tier
- Auto-deploy on git push
- Professional URLs
- HTTPS automatic
- Production-ready

**Cost:** $0/month

**Status:** 🟢 Simple and Working!

