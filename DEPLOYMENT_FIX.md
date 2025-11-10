# Fixing the 404 Error on Netlify Deployment

## Problem
Your Netlify deployment shows "Analysis Error - Request failed with status code 404" because the frontend is trying to call backend API endpoints that don't exist in the static deployment.

## Root Cause
- Netlify only deploys the frontend (static files)
- The Python backend with FastAPI is NOT deployed
- API calls to `/api/analyze`, `/api/compare`, and `/api/history` fail with 404

## Solutions

### Option 1: Frontend-Only Demo Mode (Quick Fix) ✅ IMPLEMENTED

The frontend now gracefully handles the missing backend:

**Changes made:**
- Created `/frontend/src/config/api.js` with environment variable support
- Updated all API calls to use `API_BASE_URL` and check `isBackendAvailable()`
- Added warning banners on all pages when backend is unavailable
- Updated error messages to be more helpful

**Result:**
- No more 404 errors crashing the UI
- Clear messaging to users that this is a demo deployment
- Instructions on how to run the full application

### Option 2: Deploy Backend Separately (Recommended for Production)

Deploy your Python backend to a separate service and connect it to the frontend.

#### Step 1: Deploy Backend to Render (Free Tier Available)

1. Create a Render account at https://render.com
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Build Command:** `pip install -r requirements.txt` (you'll need to create this)
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3
5. Add environment variables in Render:
   - `OPENAI_API_KEY`
   - `PERPLEXITY_API_KEY`
   - Any other required keys

#### Step 2: Configure Frontend to Use Backend

1. In Netlify, go to Site settings → Environment variables
2. Add: `VITE_API_URL` = `https://your-render-app.onrender.com/api`
3. Redeploy the site

#### Alternative Backend Hosting Options:
- **Railway:** https://railway.app (Easy setup, good free tier)
- **Fly.io:** https://fly.io (Good for Python apps)
- **Google Cloud Run:** Serverless, pay-per-use
- **AWS Elastic Beanstalk:** Enterprise-grade
- **Heroku:** Simple but paid plans only

### Option 3: Use Netlify Functions (Serverless)

Convert your Python backend to Netlify Functions (requires restructuring):

1. Create `/netlify/functions/` directory
2. Convert Python code to work as serverless functions
3. Update `netlify.toml` with function configuration

**Note:** This requires significant code refactoring and may have cold start issues.

## Quick Start Guide

### Run Locally (Full Functionality)
```bash
./run.sh
```

### Deploy to Production (Full Functionality)

1. **Deploy Backend to Render:**
   ```bash
   # Create requirements.txt if not exists
   pip freeze > requirements.txt
   
   # Push to GitHub
   git add .
   git commit -m "Add backend deployment files"
   git push
   
   # Then create Web Service on Render dashboard
   ```

2. **Configure Netlify:**
   - Go to: Site settings → Build & deploy → Environment variables
   - Add: `VITE_API_URL` = `https://your-app.onrender.com/api`
   - Trigger new deployment

3. **Verify:**
   - Visit your Netlify site
   - The warning banner should disappear
   - Try running an analysis

## Environment Variables Reference

### Frontend (Netlify)
- `VITE_API_URL` - Backend API URL (e.g., `https://your-app.onrender.com/api`)
- `NODE_VERSION` - Already set to 18 in netlify.toml

### Backend (Render/Railway/etc.)
- `OPENAI_API_KEY` - Your OpenAI API key
- `PERPLEXITY_API_KEY` - Your Perplexity API key
- `PORT` - Set automatically by most hosting services

## Checking Deployment Status

### Frontend
```bash
# Check if site is live
curl https://your-site.netlify.app

# Should return HTML
```

### Backend
```bash
# Check health endpoint
curl https://your-backend.onrender.com/health

# Should return: {"status": "healthy"}
```

## Troubleshooting

### Still getting 404 errors?
1. Check if `VITE_API_URL` is set in Netlify
2. Verify backend is running: `curl https://your-backend.onrender.com/health`
3. Check browser console for exact error message
4. Verify CORS settings in backend allow your Netlify domain

### Backend not responding?
1. Check logs in your hosting service dashboard
2. Verify all environment variables are set
3. Check if API keys are valid
4. Ensure the backend service is not sleeping (free tier limitation)

### CORS errors?
Add your Netlify domain to backend CORS origins in `src/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-site.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Cost Estimates

### Free Tier (Demo)
- Netlify: Free (frontend only)
- Backend: Not deployed

### Free Tier (Full)
- Netlify: Free for frontend
- Render: Free tier available (spins down after 15 min inactivity)
- Total: $0/month

### Production Tier
- Netlify: Free for frontend
- Render: $7/month (always running)
- Total: $7/month

## Next Steps

1. ✅ Frontend deployed with graceful error handling
2. ⏭️ Deploy backend to Render or similar service
3. ⏭️ Configure `VITE_API_URL` in Netlify
4. ⏭️ Test full functionality on live site

## Support

If you need help:
1. Check logs in Netlify and your backend hosting service
2. Verify all environment variables are set correctly
3. Test API endpoints directly with curl
4. Check CORS configuration if seeing network errors

