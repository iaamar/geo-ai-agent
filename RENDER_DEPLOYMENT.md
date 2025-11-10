# Deploy Backend to Render - 5 Minute Guide

## Step 1: Commit New Files (30 seconds)

```bash
cd /Users/amarnagargoje/Documents/Projects/daydream
git add requirements.txt render.yaml
git commit -m "Add Render deployment config"
git push
```

## Step 2: Create Render Account (1 minute)

1. Go to https://render.com
2. Sign up with GitHub (easiest)
3. Authorize Render to access your repos

## Step 3: Deploy Backend (2 minutes)

1. **Click "New +"** → **"Web Service"**

2. **Connect Repository:**
   - Find: `iaamar/geo-ai-agent` (or your repo name)
   - Click "Connect"

3. **Render Auto-Detects `render.yaml`:**
   - Service Name: `daydream-geo-backend`
   - Runtime: Python
   - All config loaded automatically ✅

4. **Add Environment Variables:**
   - Click "Environment" tab
   - Add `OPENAI_API_KEY` = `your-key-here`
   - Add `PERPLEXITY_API_KEY` = `your-key-here`

5. **Click "Create Web Service"**

Render will:
- Install dependencies
- Start your FastAPI server
- Give you a URL: `https://daydream-geo-backend.onrender.com`

## Step 4: Update Netlify (1 minute)

1. Go to **Netlify Dashboard** → Your Site
2. **Site Settings** → **Environment Variables**
3. **Add Variable:**
   - Key: `VITE_API_URL`
   - Value: `https://daydream-geo-backend.onrender.com/api`
4. **Deploys** → **Trigger Deploy** → **Clear cache and deploy**

## Step 5: Test (30 seconds)

Wait 2-3 minutes for deployments, then:

```bash
# Test backend
curl https://daydream-geo-backend.onrender.com/health
# Should return: {"status":"healthy"}

# Test frontend
open https://daydream-geo-agent.netlify.app/analyze
# Warning banner should be GONE!
# Click "Run Analysis" - should work!
```

## Done! 🎉

Your full-stack app is now live:
- **Frontend:** https://daydream-geo-agent.netlify.app
- **Backend:** https://daydream-geo-backend.onrender.com

## Free Tier Limitations

**Render Free Tier:**
- ✅ 750 hours/month (enough for 1 service)
- ✅ Automatic HTTPS
- ⚠️ Spins down after 15 min inactivity
- ⚠️ ~30 second cold start

**To keep it awake (optional):**
```bash
# Use a service like UptimeRobot or Cron-job.org to ping your backend every 14 minutes
# Ping URL: https://daydream-geo-backend.onrender.com/health
```

## Troubleshooting

### Backend won't start?
Check Render logs:
- Dashboard → Your Service → Logs
- Look for missing dependencies or import errors

### CORS errors?
Update `src/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://daydream-geo-agent.netlify.app",
        "https://*.netlify.app"  # Allow all Netlify preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then push changes:
```bash
git add src/main.py
git commit -m "Update CORS for Netlify"
git push
```

Render auto-deploys on push!

### Frontend still showing warning?
1. Verify `VITE_API_URL` is set in Netlify
2. Clear browser cache (Cmd+Shift+R or Ctrl+Shift+R)
3. Check browser console for errors (F12)

### Backend responding slowly?
This is normal for free tier after inactivity:
- First request: ~30 seconds (cold start)
- Subsequent requests: Fast (<1 second)

**Upgrade to paid ($7/month):**
- No spin down
- No cold starts
- Always fast

## Cost Comparison

| Platform | Free | Paid |
|----------|------|------|
| Netlify (Frontend) | ✅ Free forever | Free |
| Render (Backend) | ✅ 750 hrs/month | $7/month (always on) |
| **Total** | **$0/month** | **$7/month** |

## Alternative: Railway (Even Easier)

If Render doesn't work, try Railway:

1. Go to https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Select your repo
4. Railway auto-detects and deploys!
5. Add environment variables
6. Get backend URL
7. Update Netlify `VITE_API_URL`

Railway free tier: $5 credit/month (usually enough)

## Support

Need help? Common issues:

1. **"Build failed"** → Check Python version in render.yaml matches your local
2. **"Service unhealthy"** → Check if `/health` endpoint exists in your API
3. **"Import error"** → Missing dependency in requirements.txt
4. **"Port error"** → Make sure using `--port $PORT` in start command

Check logs in Render dashboard for specific errors!

