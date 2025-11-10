# GEO Expert Agent - Architecture Documentation

## System Overview

The GEO Expert Agent is a production-ready multi-agent system designed to analyze and improve brand visibility across AI-powered search platforms. It uses LangChain/LangGraph for orchestration, OpenAI for reasoning, and ChromaDB for memory.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                    (React Frontend / API)                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FastAPI Server                             │
│                   (API Routes & Middleware)                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GEO Orchestrator                              │
│              (Multi-Agent Workflow Manager)                      │
└─────┬───────────┬──────────┬──────────┬──────────┬─────────────┘
      │           │          │          │          │
      ▼           ▼          ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌────────┐ ┌───────────┐ ┌──────────────┐
│ Planner │ │Analyzer │ │Hypothe-│ │Recommender│ │ Memory Store │
│  Agent  │ │  Agent  │ │sis Gen.│ │   Agent   │ │  (ChromaDB)  │
└────┬────┘ └────┬────┘ └───┬────┘ └─────┬─────┘ └──────┬───────┘
     │           │          │            │              │
     └───────────┴──────────┴────────────┴──────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   Data Retrieval Layer   │
              ├─────────────────────────┤
              │ • OpenAI Client          │
              │ • Perplexity Client      │
              │ • Web Scraper            │
              └─────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   External AI Platforms  │
              ├─────────────────────────┤
              │ • ChatGPT API            │
              │ • Perplexity API         │
              │ • (Future: Claude, etc.) │
              └─────────────────────────┘
```

## Core Components

### 1. API Layer (`src/api/`)

**Purpose**: Expose REST API endpoints for external consumption

**Files**:
- `routes.py`: All API endpoints
- FastAPI with CORS middleware
- OpenAPI/Swagger documentation

**Endpoints**:
- `POST /api/analyze` - Run GEO analysis
- `POST /api/compare` - Compare multiple brands
- `GET /api/history` - Get historical analyses
- `GET /api/search` - Search similar analyses
- `GET /health` - Health check

### 2. Orchestrator (`src/agents/orchestrator.py`)

**Purpose**: Main workflow coordinator implementing LangGraph-style multi-agent pattern

**Workflow**:
```
1. Receive AnalysisRequest
     ↓
2. Planner Agent creates investigation plan
     ↓
3. Data Retrieval (parallel queries to AI platforms)
     ↓
4. Analyzer Agent processes patterns
     ↓
5. Hypothesis Agent explains findings (LLM reasoning)
     ↓
6. Recommender Agent creates action plan (LLM reasoning)
     ↓
7. Save to Memory Store (background)
     ↓
8. Return AnalysisResult
```

### 3. Agent System (`src/agents/`)

#### Planner Agent (`planner.py`)
- **Input**: AnalysisRequest
- **Output**: Investigation plan with query variations
- **LLM Used**: GPT-4 (temperature: 0.3)
- **Key Functions**:
  - Create analysis strategy
  - Generate query variations
  - Determine data sources

#### Analyzer Agent (`analyzer.py`)
- **Input**: List of CitationData
- **Output**: CompetitorComparison, patterns
- **LLM Used**: None (pure Python logic)
- **Key Functions**:
  - Calculate visibility scores
  - Compare brand vs competitors
  - Extract patterns (platform bias, positions, contexts)

#### Hypothesis Agent (`hypothesis.py`)
- **Input**: Query, comparison data, patterns
- **Output**: List of Hypothesis objects
- **LLM Used**: GPT-4 (temperature: 0.7)
- **Key Functions**:
  - Explain visibility patterns
  - Generate hypotheses with confidence scores
  - Provide supporting evidence

#### Recommender Agent (`recommender.py`)
- **Input**: Query, comparison, hypotheses
- **Output**: Prioritized recommendations
- **LLM Used**: GPT-4 (temperature: 0.7)
- **Key Functions**:
  - Generate actionable strategies
  - Score by impact and effort
  - Prioritize recommendations

### 4. Data Retrieval Layer (`src/data/`)

#### OpenAI Client (`openai_client.py`)
- **Purpose**: Query ChatGPT and generate embeddings
- **Functions**:
  - `search()` - Query ChatGPT
  - `analyze_with_reasoning()` - Deep analysis
  - `generate_embedding()` - Create vector embeddings
  - `extract_citations()` - Parse responses for brand mentions

#### Perplexity Client (`perplexity.py`)
- **Purpose**: Query Perplexity AI
- **Functions**:
  - `search()` - Query Perplexity API
  - `extract_citations()` - Parse citations
  - `_simulate_response()` - Demo mode (no API key)

#### Web Scraper (`scraper.py`)
- **Purpose**: Analyze domain content
- **Functions**:
  - `fetch_page()` - Get webpage content
  - `extract_text()` - Clean HTML to text
  - `extract_keywords()` - Simple keyword extraction
  - `analyze_domain()` - Full domain analysis

### 5. Memory Layer (`src/memory/store.py`)

**Purpose**: Store and retrieve historical analyses using vector embeddings

**Technology**: ChromaDB (local vector database)

**Functions**:
- `save_analysis()` - Store analysis with embeddings
- `search_similar_analyses()` - Semantic search
- `get_analysis()` - Retrieve by ID
- `get_recent_analyses()` - Get history

**Storage Format**:
- Documents: Searchable text representation
- Metadata: Structured data (brand, query, scores, etc.)
- IDs: Unique analysis identifiers

### 6. Data Models (`src/models/schemas.py`)

**Pydantic Models** for type safety and validation:

```python
AnalysisRequest
  ├─ query: str
  ├─ brand_domain: str
  ├─ competitors: List[str]
  ├─ platforms: List[Platform]
  └─ num_queries: int

AnalysisResult
  ├─ id: str
  ├─ timestamp: datetime
  ├─ request: AnalysisRequest
  ├─ citations: List[CitationData]
  ├─ visibility_scores: CompetitorComparison
  ├─ hypotheses: List[Hypothesis]
  ├─ recommendations: List[Recommendation]
  └─ summary: str
```

## Data Flow

### Analysis Request Flow

```
User Input → API Endpoint
              ↓
         Validation (Pydantic)
              ↓
         Orchestrator.run_analysis()
              ↓
    ┌─────────────────────┐
    │  1. PLANNING PHASE  │
    └─────────────────────┘
              ↓
    PlannerAgent.create_plan()
    - Generate query variations
    - Select data sources
              ↓
    ┌─────────────────────┐
    │ 2. DATA COLLECTION  │
    └─────────────────────┘
              ↓
    Parallel async queries:
    - ChatGPT queries × N
    - Perplexity queries × N
              ↓
    Extract citations & mentions
              ↓
    ┌─────────────────────┐
    │   3. ANALYSIS       │
    └─────────────────────┘
              ↓
    AnalyzerAgent.analyze_visibility()
    - Calculate mention rates
    - Compare competitors
    - Extract patterns
              ↓
    ┌─────────────────────┐
    │  4. HYPOTHESIS GEN  │
    └─────────────────────┘
              ↓
    HypothesisAgent.generate_hypotheses()
    - LLM reasoning on patterns
    - Generate explanations
    - Assign confidence scores
              ↓
    ┌─────────────────────┐
    │ 5. RECOMMENDATIONS  │
    └─────────────────────┘
              ↓
    RecommenderAgent.generate_recommendations()
    - LLM-based strategy generation
    - Impact/effort scoring
    - Prioritization
              ↓
    ┌─────────────────────┐
    │  6. PERSISTENCE     │
    └─────────────────────┘
              ↓
    MemoryStore.save_analysis()
    - Vector embeddings
    - Metadata indexing
              ↓
         Return AnalysisResult
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **LLM Orchestration**: LangChain 0.1+, LangGraph 0.0.20
- **AI/LLM**: OpenAI GPT-4, embeddings
- **Vector Database**: ChromaDB 0.4.22
- **Data Processing**: Pandas, NumPy
- **Async**: asyncio, httpx
- **Web Scraping**: BeautifulSoup4, lxml

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS 3.3
- **Charts**: Recharts 2.10
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Routing**: React Router 6

### Infrastructure
- **Web Server**: Uvicorn (ASGI)
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Environment**: Python 3.10+, Node.js 18+

## Design Decisions

### 1. Why Multi-Agent Architecture?

**Separation of Concerns**: Each agent has a specific responsibility:
- Planning vs Analysis vs Reasoning vs Recommendation
- Easier to test, debug, and improve individual components

**Flexibility**: Can replace or upgrade individual agents without affecting others

**Explainability**: Clear reasoning chain from data → analysis → hypothesis → recommendations

### 2. Why LangChain/LangGraph?

**Industry Standard**: LangChain is the de-facto standard for LLM applications

**Future-Proof**: Easy to extend with:
- Memory systems
- Tool calling
- Multi-modal inputs
- Different LLM providers

**Developer Experience**: Good abstractions, active community, extensive documentation

### 3. Why ChromaDB?

**Simplicity**: Lightweight, embedded database (no separate server)

**Performance**: Fast vector similarity search

**Development Speed**: Easy to set up and use

**Production Ready**: Can be deployed with Docker, supports persistence

### 4. Why FastAPI?

**Modern Python**: Async/await support, type hints

**Auto Documentation**: OpenAPI/Swagger built-in

**Performance**: Fast (comparable to Node.js)

**Developer Experience**: Excellent error messages, validation

### 5. Why React + Vite?

**Modern Tooling**: Fast hot reload, optimal bundling

**Developer Experience**: Great ecosystem, widely adopted

**Performance**: Vite is significantly faster than Create React App

**Production Ready**: Easy to deploy to CDN/static hosting

## Scalability Considerations

### Current Architecture (MVP)
- Single server deployment
- SQLite database
- Local ChromaDB
- Synchronous analysis requests

**Good for**: Demo, small teams, low-volume usage (<100 analyses/day)

### Production Scale (Recommended Improvements)

#### 1. Async Task Queue
```python
# Add Celery or RQ for background processing
@router.post("/api/analyze")
async def analyze(request: AnalysisRequest):
    task = analyze_task.delay(request)
    return {"task_id": task.id, "status": "processing"}
```

#### 2. Database Upgrade
- Replace SQLite with PostgreSQL
- Use connection pooling
- Add indexes on frequently queried fields

#### 3. Vector Database Scale
- Deploy ChromaDB in client-server mode
- Or migrate to Pinecone/Weaviate for cloud-native vector search

#### 4. Caching Layer
```python
# Add Redis for caching
@cache(ttl=3600)
async def get_visibility_score(domain, query):
    ...
```

#### 5. Rate Limiting
```python
# Protect API endpoints
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
@limiter.limit("5/minute")
```

#### 6. Load Balancing
- Deploy multiple FastAPI instances
- Use Nginx or AWS ALB
- Session stickiness not required (stateless API)

## Security Considerations

### Current Implementation
- API keys in environment variables
- CORS configured (needs tightening for production)
- No authentication (suitable for internal use)

### Production Additions Needed
1. **Authentication**: JWT tokens or API keys
2. **Rate Limiting**: Per-user/per-IP limits
3. **Input Validation**: Already using Pydantic, but add additional sanitization
4. **HTTPS**: Use TLS certificates
5. **Secrets Management**: Use AWS Secrets Manager / HashiCorp Vault
6. **Audit Logging**: Log all API requests

## Performance Characteristics

### Typical Analysis Timeline
```
1. Planning: ~1-2 seconds (LLM call)
2. Data Collection: ~10-30 seconds (parallel API calls)
   - 5 queries × 2 platforms = 10 API calls
   - Each call: 2-5 seconds
3. Analysis: <1 second (Python computation)
4. Hypothesis Generation: ~2-4 seconds (LLM call)
5. Recommendation Generation: ~2-4 seconds (LLM call)
6. Memory Save: <1 second (background)

Total: ~15-45 seconds per analysis
```

### Optimization Opportunities
1. **Caching**: Cache LLM responses for identical queries
2. **Batch Processing**: Run multiple analyses in parallel
3. **Streaming**: Stream results as they're generated
4. **Model Selection**: Use GPT-3.5 for faster (cheaper) analyses

## Cost Analysis

### Per Analysis Cost (Approximate)
- Planning: 1 GPT-4 call (~500 tokens) = $0.005
- Data Collection: 10 API calls (mixed) = $0.01
- Hypothesis: 1 GPT-4 call (~2000 tokens) = $0.02
- Recommendations: 1 GPT-4 call (~2000 tokens) = $0.02
- **Total: ~$0.055 per analysis**

### Monthly Cost Estimate
- 100 analyses/day × 30 days = 3,000 analyses
- 3,000 × $0.055 = **$165/month**
- Plus infrastructure: ~$50/month
- **Total: ~$215/month** for moderate usage

## Future Enhancements

### Planned Features
1. **Real-time Monitoring**: Webhook alerts for visibility changes
2. **A/B Testing**: Test content variations
3. **Multi-language**: Support for non-English queries
4. **Custom Models**: Fine-tune for specific industries
5. **Integrations**: Google Search Console, Analytics
6. **Automated Reports**: Weekly/monthly PDF reports
7. **Team Collaboration**: Multi-user support, shared workspaces

### Research Directions
1. **Predictive Analytics**: Forecast visibility trends
2. **Content Generation**: Auto-generate optimized content
3. **Competitive Intelligence**: Deep competitor analysis
4. **Platform-Specific**: Tailored strategies per AI platform



