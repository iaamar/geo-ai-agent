# GEO Expert Agent - Setup Guide

Complete setup instructions for the GEO Expert Agent system.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.10 or higher**
  ```bash
  python3 --version
  ```

- **Node.js 18 or higher**
  ```bash
  node --version
  ```

- **pip and npm**
  ```bash
  pip --version
  npm --version
  ```

## Step 1: Get API Keys

### Required: OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

**Note**: You'll need credits in your OpenAI account. Each analysis costs approximately $0.01-0.03.

### Optional: Perplexity API Key

1. Go to https://www.perplexity.ai/settings/api
2. Sign in or create an account
3. Generate an API key
4. Copy the key (starts with `pplx-`)

**Note**: Without this key, the system will use simulated responses for Perplexity queries.

## Step 2: Clone and Setup

```bash
# Navigate to project directory
cd /Users/amarnagargoje/Documents/Projects/daydream

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

## Step 3: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor
```

Add your API keys to `.env`:

```env
# Required
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Optional but recommended
PERPLEXITY_API_KEY=pplx-your-perplexity-api-key-here

# Server config (defaults are fine)
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Database (defaults are fine)
DATABASE_URL=sqlite:///./geo_agent.db
CHROMA_DB_PATH=./chroma_db
```

## Step 4: Test Installation

```bash
# Test backend
python -c "from src.config import settings; print(f'✓ Config loaded: {settings.openai_api_key[:10]}...')"

# Test dependencies
python -c "import langchain, openai, chromadb; print('✓ All dependencies installed')"
```

## Step 5: Run the Application

### Option A: Run Full Stack

Terminal 1 (Backend):
```bash
cd /Users/amarnagargoje/Documents/Projects/daydream
source venv/bin/activate
python -m src.main
```

Terminal 2 (Frontend):
```bash
cd /Users/amarnagargoje/Documents/Projects/daydream/frontend
npm run dev
```

Access the application:
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

### Option B: Backend Only

```bash
python -m src.main
```

Use the API directly via curl, Postman, or Python requests.

### Option C: Run Examples

```bash
# Simple Python demo
python examples/simple_demo.py

# API demo (requires server running)
python examples/api_demo.py
```

## Step 6: Verify Everything Works

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

Expected output:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-...",
  "services": {
    "api": true,
    "orchestrator": true,
    "memory": true
  }
}
```

### Test 2: Simple Analysis

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best AI tools",
    "brand_domain": "test.com",
    "competitors": ["example.com"],
    "platforms": ["chatgpt"],
    "num_queries": 2
  }'
```

This should return analysis results (may take 30-60 seconds).

### Test 3: Frontend

1. Open http://localhost:5173
2. Navigate to "Analyze"
3. Fill in the form with:
   - Query: "best AI productivity tools"
   - Brand: "acme.com"
   - Competitors: "notion.so, asana.com"
4. Click "Run Analysis"

## Troubleshooting

### Issue: "Module not found" errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: OpenAI API errors

- Check your API key is correct in `.env`
- Verify you have credits: https://platform.openai.com/account/billing
- Check rate limits: https://platform.openai.com/account/limits

### Issue: Frontend not connecting to backend

- Ensure backend is running on port 8000
- Check proxy settings in `frontend/vite.config.js`
- Try accessing API directly: http://localhost:8000/docs

### Issue: ChromaDB errors

```bash
# Clear vector database
rm -rf chroma_db/

# Restart application
python -m src.main
```

### Issue: Port already in use

```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in .env
PORT=8001
```

## Project Structure

```
daydream/
├── src/
│   ├── agents/          # Multi-agent system
│   ├── data/            # Data retrieval
│   ├── memory/          # Vector store
│   ├── models/          # Data models
│   ├── api/             # API routes
│   ├── config.py        # Configuration
│   └── main.py          # Entry point
├── frontend/            # React frontend
│   ├── src/
│   │   ├── pages/       # Page components
│   │   ├── App.jsx      # Main app
│   │   └── main.jsx     # Entry point
│   └── package.json
├── examples/            # Example scripts
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── README.md           # Main documentation
```

## Next Steps

1. **Read the Documentation**: Check `README.md` for architecture details
2. **Try Examples**: Run scripts in `examples/` directory
3. **Explore API**: Visit http://localhost:8000/docs for interactive API documentation
4. **Run Analysis**: Use the frontend to run your first GEO analysis

## Production Deployment

For production deployment:

1. **Use production-grade API keys**
2. **Set `DEBUG=false` in .env**
3. **Configure CORS properly** in `src/main.py`
4. **Use PostgreSQL** instead of SQLite for database
5. **Deploy with Docker** (see Docker section below)
6. **Add authentication** for API endpoints
7. **Set up monitoring** and logging

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
CMD ["python", "-m", "src.main"]
```

Build and run:
```bash
docker build -t geo-agent .
docker run -p 8000:8000 --env-file .env geo-agent
```

## Support

For issues or questions:
- Check troubleshooting section above
- Review API documentation: http://localhost:8000/docs
- Check example scripts in `examples/` directory

## Resources

- **OpenAI API Docs**: https://platform.openai.com/docs
- **LangChain Docs**: https://python.langchain.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev



