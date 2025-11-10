# Deploy to Railway - 2 Minutes

## Quick Deploy

### Step 1: Sign Up (30 seconds)
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign in with **GitHub**
4. Authorize Railway

### Step 2: Deploy (1 minute)
1. Click **"Deploy from GitHub repo"**
2. Select: `iaamar/geo-ai-agent`
3. Railway automatically detects:
   - ✅ Python backend (`src/main.py`)
   - ✅ React frontend (`frontend/package.json`)
   - Creates both services automatically!

### Step 3: Configure (30 seconds)

**Backend Service:**
1. Click the **Python service**
2. Go to **Variables** tab
3. Add:
   - `OPENAI_API_KEY` = your-key
   - `PERPLEXITY_API_KEY` = your-key

**Frontend Service:**
1. Click the **Node service**
2. Go to **Variables** tab
3. Get backend URL first:
   - Backend service → Settings → Networking → Generate Domain
   - Copy URL: `https://your-app.up.railway.app`
4. Add:
   - `VITE_API_URL` = `https://your-app.up.railway.app/api`

### Step 4: Test
```bash
# Backend health check
curl https://your-backend.up.railway.app/health

# Open frontend
open https://your-frontend.up.railway.app
```

## Done! ✅

Your app is live:
- **Backend:** `https://your-backend.up.railway.app`
- **Frontend:** `https://your-frontend.up.railway.app`
- **Cost:** $0/month (free $5 credit)

## Free Tier

- **$5 credit/month** (resets monthly)
- **No credit card required**
- **Enough for your app** (~$3-4/month usage)
- **Fast cold starts** (~5 seconds)

## Auto-Deploy

Every `git push` automatically deploys both services!

```bash
git push
# Railway rebuilds and deploys automatically
```

## Troubleshooting

### Build Fails
Check logs: Service → Deployments → View Logs

### Frontend Can't Reach Backend
Update CORS in `src/main.py`:
```python
allow_origins=[
    "http://localhost:5173",
    "https://*.railway.app",
    "https://*.up.railway.app"
]
```

### Out of Credit
- Credit resets monthly
- Or upgrade to Hobby plan ($5/month pay-as-you-go)

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

