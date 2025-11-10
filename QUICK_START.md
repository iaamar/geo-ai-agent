# GEO Expert Agent - Quick Start Guide

Get up and running in 5 minutes! [[memory:6378194]]

---

## Step 1: Get OpenAI API Key (2 minutes)

1. Go to: https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

**Cost**: ~$0.05 per analysis (very affordable for testing)

---

## Step 2: Setup (2 minutes)

```bash
# Navigate to project
cd /Users/amarnagargoje/Documents/Projects/daydream

# Copy environment template
cp .env.example .env

# Add your API key
# Open .env in any text editor and replace:
# OPENAI_API_KEY=your-key-here
nano .env  # or use VS Code, TextEdit, etc.
```

---

## Step 3: Run (1 minute)

```bash
# Quick start script does everything
./run.sh
```

**What it does**:
- Creates virtual environment
- Installs dependencies
- Starts backend server
- Launches frontend (if Node.js available)

**Choose an option**:
1. Full stack (recommended) - Backend + Frontend
2. Backend only - API server only
3. Demo script - Quick test run

---

## You're Done! 🎉

### Access Points

**Frontend Dashboard**:
```
http://localhost:5173
```
- Beautiful web interface
- Real-time analysis
- Charts and visualizations

**API Documentation**:
```
http://localhost:8000/docs
```
- Interactive API docs
- Try endpoints directly
- See request/response schemas

**Health Check**:
```
http://localhost:8000/health
```

---

## First Analysis (30 seconds)

### Option A: Web Interface

1. Open http://localhost:5173
2. Click "Analyze"
3. Fill in:
   - Query: "best AI productivity tools"
   - Brand: "acme.com"
   - Competitors: "notion.so, asana.com"
4. Click "Run Analysis"
5. Wait ~30 seconds
6. View results!

### Option B: Python Script

```bash
python examples/simple_demo.py
```

### Option C: API Call

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best project management tools",
    "brand_domain": "myapp.io",
    "competitors": ["asana.com", "trello.com"],
    "platforms": ["chatgpt"],
    "num_queries": 3
  }'
```

---

## What You'll Get

### Visibility Analysis
- Your brand mention rate: e.g., 20%
- Competitor mention rates: e.g., Notion 80%, Asana 60%
- Platform breakdown: ChatGPT vs Perplexity

### Key Findings (AI-Generated)
- "Low Brand Visibility in AI Responses"
  - Confidence: 90%
  - Explanation: Detailed reasoning
  - Evidence: Supporting data points

### Recommendations (Prioritized)
- [HIGH] Optimize Content for AI Understanding
  - Impact: 8.5/10
  - Effort: 6.0/10
  - 4 specific action items
  - Expected outcome

---

## Common Issues

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "OpenAI API error"
- Check your API key in `.env`
- Verify credits at: https://platform.openai.com/account/billing

### "Port already in use"
```bash
lsof -ti:8000 | xargs kill -9
./run.sh
```

### Frontend won't start
- Need Node.js 18+
- Install from: https://nodejs.org
- Or use backend-only mode

---

## Example Output

```
═══════════════════════════════════════════════════
   ANALYSIS RESULTS
═══════════════════════════════════════════════════

VISIBILITY SCORES
─────────────────────────────────────────────────
Your Brand (acme.com): 15.0%
  - Total mentions: 3
  - Platforms: {'chatgpt': 2, 'perplexity': 1}

Competitors:
  - notion.so: 85.0%
  - asana.com: 70.0%

KEY FINDINGS
─────────────────────────────────────────────────
1. Low Brand Visibility in AI Responses
   Confidence: 90%
   The brand acme.com appears in only 15% of responses,
   indicating limited recognition by AI models.

2. Strong Competitor Presence
   Confidence: 85%
   notion.so has significantly higher visibility,
   suggesting better content optimization.

TOP RECOMMENDATIONS
─────────────────────────────────────────────────
1. [HIGH] Optimize Content for AI Semantic Understanding
   Impact: 8.5/10 | Effort: 6.0/10
   Improve content structure to help AI models better
   understand and cite your brand.

2. [HIGH] Build Domain Authority and Trust Signals
   Impact: 7.5/10 | Effort: 8.0/10
   Increase domain credibility through authoritative
   content and external validation.
```

---

## Next Steps

### Explore Features
- **Compare Brands**: Try the comparison tool
- **View History**: Check past analyses
- **Try API**: Use the interactive docs

### Customize
- Edit query variations in `src/agents/planner.py`
- Add new platforms in `src/data/`
- Customize recommendations logic

### Production Use
- See `ARCHITECTURE.md` for scaling info
- Read `SETUP.md` for deployment details
- Check `examples/README.md` for use cases

---

## Learn More

**Documentation**:
- `README.md` - Main documentation
- `SETUP.md` - Detailed setup
- `ARCHITECTURE.md` - Technical details
- `PROJECT_SUMMARY.md` - Complete overview

**Examples**:
- `examples/simple_demo.py` - Python usage
- `examples/api_demo.py` - API usage
- `examples/README.md` - Use cases

**Live Docs**:
- http://localhost:8000/docs - Interactive API docs

---

## Tips

1. **Start Small**: Use `num_queries=3` for faster testing
2. **Check Logs**: Backend logs show progress
3. **Use Frontend**: Easier than API for exploration
4. **Save Results**: Automatically stored in memory
5. **Compare Often**: Track improvements over time

---

## Support

Having trouble? Check:

1. **Troubleshooting**: See "Common Issues" above
2. **Documentation**: Read `SETUP.md`
3. **Examples**: Run demo scripts
4. **Logs**: Check `backend.log` if using full stack mode

---

That's it! You now have a production-ready GEO analysis system running locally.

**Happy analyzing!** 🚀



