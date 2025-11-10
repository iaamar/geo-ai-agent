# Deploy for FREE - Railway.app

## Why Railway Instead of Render?

**Render "free" tier problems:**
- ❌ 30-50 second cold starts
- ❌ Spins down after 15 min
- ❌ Unusable in practice
- ❌ Basically forces you to pay $7/month

**Railway free tier:**
- ✅ $5 credit/month (resets monthly)
- ✅ No credit card required
- ✅ Fast cold starts (~5 seconds)
- ✅ Actually usable
- ✅ Enough for small projects

---

## Deploy to Railway (2 Minutes) - TRULY FREE

### Step 1: Sign Up
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign in with GitHub
4. Authorize Railway

### Step 2: Deploy
1. **"Deploy from GitHub repo"**
2. Select: `iaamar/geo-ai-agent`
3. **Railway automatically:**
   - Detects Python backend
   - Detects React frontend
   - Creates both services
   - Deploys everything

### Step 3: Configure
1. Click **backend service**
2. **Variables tab:**
   - Add `OPENAI_API_KEY`
   - Add `PERPLEXITY_API_KEY`

3. Click **frontend service**
4. **Variables tab:**
   - Add `VITE_API_URL` = (get backend URL first)

### Step 4: Get URLs
1. Backend service → Settings → Generate Domain
2. Copy URL: `https://your-app.up.railway.app`
3. Go to frontend → Variables
4. Update `VITE_API_URL` = `https://your-app.up.railway.app/api`

### Done! ✅

**Your app is live:**
- Backend: `https://your-backend.up.railway.app`
- Frontend: `https://your-frontend.up.railway.app`
- **Cost: $0/month**

---

## Free Tier Details

### What You Get
- **$5 credit/month** (renews every month)
- **Usage:** ~$3-4/month for your app
- **Enough for:** 
  - ~100 hours runtime
  - ~500MB bandwidth
  - Testing and small projects

### When Credit Runs Out
- Railway pauses services
- Next month credit resets
- Services resume automatically

### To Stretch Your Credit
```bash
# Option 1: Sleep services when not using
# Railway dashboard → Service → Settings → Sleep

# Option 2: Deploy only when needed
# Deploy for demos, pause when done

# Option 3: Upgrade to Hobby ($5/month pay-as-you-go)
# Only pay for what you use
```

---

## Alternative: Fly.io (Also Free)

### Fly.io Free Tier
- **3 shared VMs** free forever
- **3GB storage** persistent
- **160GB bandwidth/month**
- Enough for your full app!

### Deploy to Fly.io

1. **Install flyctl:**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Sign up:**
```bash
flyctl auth signup
```

3. **Deploy:**
```bash
cd /Users/amarnagargoje/Documents/Projects/daydream
flyctl launch
# Follow prompts - it detects Dockerfile
```

4. **Add secrets:**
```bash
flyctl secrets set OPENAI_API_KEY=your-key
flyctl secrets set PERPLEXITY_API_KEY=your-key
```

5. **Deploy frontend separately or use included Dockerfile**

**Your app is live at:** `https://your-app.fly.dev`

---

## Comparison: What's ACTUALLY Free?

### ✅ Railway
- **Free:** $5 credit/month
- **Good for:** Small projects, demos
- **Setup:** 2 minutes (easiest!)
- **Limitations:** Credit renews monthly

### ✅ Fly.io
- **Free:** 3 VMs forever
- **Good for:** Personal projects
- **Setup:** 5 minutes (requires Docker)
- **Limitations:** 3GB storage

### ⚠️ Render
- **Free:** Yes, but unusable (50s cold starts)
- **Paid:** $7/month (actually usable)
- **Good for:** When you want to pay
- **Limitations:** Free tier is frustrating

### ✅ Vercel (Frontend only)
- **Free:** Unlimited
- **Good for:** Frontend hosting
- **Setup:** 1 minute
- **Limitations:** Backend needs separate service

### ✅ Netlify (Frontend only)
- **Free:** Unlimited
- **Good for:** Frontend hosting
- **Setup:** 1 minute
- **Limitations:** Backend needs separate service

---

## Recommended Free Stack

### Option 1: All-in-One (Easiest)
**Railway for everything:**
- Backend: Railway ($5 credit)
- Frontend: Railway ($5 credit)
- **Total: $0/month** (within credit)

### Option 2: Split (Most Free)
**Vercel + Railway:**
- Frontend: Vercel (unlimited free)
- Backend: Railway ($5 credit)
- **Total: $0/month**
- More free resources!

### Option 3: Maximum Free
**Netlify + Fly.io:**
- Frontend: Netlify (unlimited free)
- Backend: Fly.io (3 VMs free)
- **Total: $0/month forever**

---

## Step-by-Step: Railway Deployment

I'll walk you through Railway since it's easiest:

### 1. Go to Railway
https://railway.app

### 2. New Project
Click "Deploy from GitHub repo"

### 3. Authorize GitHub
Allow Railway to access your repos

### 4. Select Repository
Choose: `iaamar/geo-ai-agent`

### 5. Railway Magic ✨
Railway detects:
- `src/main.py` → Creates Python service
- `frontend/package.json` → Creates Node service

Both services automatically configured!

### 6. Add Environment Variables

**Backend service:**
```
OPENAI_API_KEY=sk-...
PERPLEXITY_API_KEY=pplx-...
```

**Frontend service:**
```
VITE_API_URL=https://[backend-url].up.railway.app/api
```

### 7. Generate Domains
- Backend → Settings → Networking → Generate Domain
- Frontend → Settings → Networking → Generate Domain

### 8. Test
```bash
# Backend
curl https://[backend-url].up.railway.app/health

# Frontend
open https://[frontend-url].up.railway.app
```

---

## Troubleshooting

### "Out of credit"
**Monthly limit reached:**
- Wait until next month (credit resets)
- Or upgrade to Hobby plan ($5/month pay-as-you-go)

### "Build failed"
**Check logs:**
- Railway dashboard → Service → Deployments
- Click failed deployment
- Read error message

**Common fixes:**
```bash
# Missing dependencies
pip freeze > requirements.txt
git push

# Node version
# Set NODE_VERSION=18 in environment variables
```

### Frontend can't reach backend
**CORS issue:**

Update `src/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://*.railway.app",
        "https://*.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Summary

### Render = Not Really Free
- Free tier exists but unusable
- Need to pay $7/month for decent experience

### Railway = Actually Free
- $5 credit/month (sufficient for small apps)
- Fast, easy, works great
- **Recommended!**

### Fly.io = Forever Free
- 3 VMs free permanently
- More setup required (Docker)
- Great if you want no time limits

---

## Quick Deploy Commands

### Railway (Recommended)
```bash
# Just use the web dashboard
# https://railway.app
# Connect GitHub → Deploy → Done!
```

### Fly.io (Alternative)
```bash
# Install CLI
curl -L https://fly.io/install.sh | sh

# Deploy
flyctl auth signup
flyctl launch
flyctl secrets set OPENAI_API_KEY=your-key
flyctl secrets set PERPLEXITY_API_KEY=your-key
```

---

## Cost Breakdown

| Platform | Monthly Cost | Annual Cost |
|----------|--------------|-------------|
| **Railway** (free tier) | $0 | $0 |
| **Fly.io** (free tier) | $0 | $0 |
| **Render** (paid) | $7 | $84 |
| **Railway** (hobby) | ~$5 | ~$60 |
| **Vercel + Railway** | $0 | $0 |

**Best value: Railway free tier** ⭐

---

## Next Steps

1. **Choose platform:** Railway (recommended)
2. **Go to:** https://railway.app
3. **Deploy:** 2 minutes
4. **Enjoy:** Actually free hosting!

**No credit card required. No hidden costs. Actually free.** 🎉

