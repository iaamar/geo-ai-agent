# Netlify Deployment Guide

## Current Status

**Site URL:** https://daydream-geo-agent.netlify.app/  
**Status:** ⚠️ 404 (needs configuration)

## Issue

Netlify returned 404 because it didn't know how to build the project.

## Fix Applied

Created `netlify.toml` with proper configuration:

```toml
[build]
  command = "cd frontend && npm install && npm run build"
  publish = "frontend/dist"
  base = "/"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## Deployment Steps

### 1. Commit Configuration

```bash
git add netlify.toml
git commit -m "Add Netlify configuration"
git push
```

### 2. Netlify Will Auto-Deploy

Netlify will detect the push and:
1. Install Node.js 18
2. Run `cd frontend && npm install`
3. Run `npm run build`
4. Publish from `frontend/dist/`
5. Site will be live!

### 3. Environment Variables

**Important:** The frontend needs the backend API URL.

**In Netlify Dashboard:**
1. Go to Site Settings → Environment Variables
2. Add:
   ```
   VITE_API_URL=https://your-backend-url.com
   ```

**Note:** Since you have env variables added, make sure you have:
- `VITE_API_URL` (if backend is hosted separately)
- Or remove API proxy from netlify.toml if frontend-only

## Frontend-Only Deployment

**Current issue:** Frontend expects backend at `/api/*`

**Options:**

**Option 1: Frontend-Only (Demo Mode)**
- Comment out API calls
- Show UI/UX only
- No live analysis (static demo)

**Option 2: Deploy Backend Too**
- Deploy backend to Render/Railway/Fly.io
- Update `VITE_API_URL` in Netlify
- Full functionality

**Option 3: Run Backend Locally**
- Keep backend local
- Frontend on Netlify (for portfolio/showcase)
- Run analysis locally

## Quick Fix for Frontend-Only

If you want to deploy just the UI for showcase:

**Update `frontend/src/pages/AnalysisPage.jsx`:**

```jsx
const handleSubmit = async (e) => {
  e.preventDefault()
  setLoading(true)
  
  try {
    // Check if API is available
    const apiUrl = import.meta.env.VITE_API_URL || '/api'
    
    const response = await axios.post(`${apiUrl}/analyze`, payload)
    setResult(response.data)
  } catch (err) {
    // Fallback: Show demo message
    setError('Backend not available. Run locally for full functionality.')
  } finally {
    setLoading(false)
  }
}
```

## After Configuration

Once `netlify.toml` is pushed:

1. Netlify auto-builds
2. Site becomes accessible
3. Frontend loads properly
4. (Backend needs separate deployment)

## Recommended Approach

**For portfolio/showcase:**
1. Deploy frontend to Netlify (UI/UX showcase)
2. Add note: "Run locally for full functionality"
3. Link to GitHub repo
4. Include demo video/screenshots

**For full functionality:**
1. Deploy backend to Render/Railway
2. Set `VITE_API_URL` in Netlify
3. Update CORS in backend
4. Full working app online

## Check Deployment

After pushing `netlify.toml`:

```bash
# Wait 2-3 minutes for build
# Then check:
curl -I https://daydream-geo-agent.netlify.app/

# Should return 200 OK (not 404)
```

## Current Configuration

✅ `netlify.toml` created  
✅ Build command configured  
✅ SPA routing setup  
✅ Security headers added  

**Next:** Commit and push to trigger deployment!

