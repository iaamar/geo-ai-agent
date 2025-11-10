# 🧭 GEO Expert Agent — AI-Powered Generative Engine Optimization

A production-ready AI agent system that helps brands understand and improve their visibility across AI-powered search platforms like ChatGPT, Perplexity, and Google AI Overviews.

## 🎯 What is GEO?

Generative Engine Optimization (GEO) is the next evolution of SEO. Instead of ranking on Google Search, brands need to ensure they're cited and mentioned in AI-generated answers across platforms like:

- ChatGPT (OpenAI)
- Perplexity AI
- Google AI Overviews
- Claude (Anthropic)
- Bing Chat

## 🏗️ Architecture

```
User Query → Query Parser → Planner Agent → Data Retrieval
                                ↓
                    ┌───────────┴───────────┐
                    ↓                       ↓
            Analyzer Agent          Memory/Knowledge Base
                    ↓
            Hypothesis Generator
                    ↓
            Recommendation Engine
                    ↓
            Structured Report
```

### Core Components

1. **Input Parser**: Understands natural language queries from marketing teams
2. **Planner Agent**: Orchestrates the investigation using LangGraph
3. **Data Retriever**: Fetches visibility data from AI platforms
4. **Analyzer**: Compares citation frequency, keywords, and semantic patterns
5. **Hypothesis Generator**: Explains visibility patterns using LLM reasoning
6. **Recommender**: Suggests actionable improvements
7. **Memory Layer**: Stores historical analyses using vector embeddings

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key (required)
- Perplexity API key (optional but recommended)

### Installation

1. **Clone and setup environment**:

```bash
cd /Users/amarnagargoje/Documents/Projects/daydream

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
npm install
```

2. **Configure environment variables**:

```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. **Run the backend server**:

```bash
python -m src.main
```

4. **Run the frontend** (in a new terminal):

```bash
npm run dev
```

5. **Access the application**:

- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs
- API Health: http://localhost:8000/health

## 📊 Example Use Cases

### Use Case 1: Brand Visibility Analysis

**Input**:
```
"Why isn't Acme.com showing up in ChatGPT answers for 'best productivity tools'?"
```

**Output**:
- Citation frequency: 0/10 queries
- Top competitors: Notion (8/10), Asana (6/10)
- Hypothesis: Low semantic alignment with "AI productivity" keywords
- Recommendations: Publish AI-focused content, optimize for semantic search

### Use Case 2: Competitor Comparison

**Input**:
```
"Compare our GEO visibility against HubSpot for 'CRM software'"
```

**Output**:
- Visibility score comparison
- Citation patterns analysis
- Gap analysis with recommendations

## 🛠️ API Endpoints

### POST /api/analyze
Analyze brand visibility for a specific query

```json
{
  "query": "best AI productivity tools",
  "brand_domain": "acme.com",
  "competitors": ["notion.so", "asana.com"],
  "platforms": ["chatgpt", "perplexity"]
}
```

### POST /api/compare
Compare visibility between brands

### GET /api/history
Get historical analysis results

### GET /api/recommendations/{analysis_id}
Get recommendations for a specific analysis

## 🧠 Agent Reasoning Loop

```python
def geo_agent_reasoning(question):
    # 1. Parse and understand the question
    parsed_query = parse_user_query(question)
    
    # 2. Plan investigation steps
    plan = planner_agent.create_plan(parsed_query)
    
    # 3. Collect visibility data
    data = data_retriever.fetch_from_platforms(plan)
    
    # 4. Analyze patterns
    analysis = analyzer_agent.analyze_visibility(data)
    
    # 5. Generate hypothesis
    hypothesis = hypothesis_agent.explain_patterns(analysis)
    
    # 6. Create recommendations
    recommendations = recommender_agent.suggest_actions(hypothesis)
    
    # 7. Store in memory for learning
    memory_store.save_analysis(analysis, recommendations)
    
    return format_report(analysis, hypothesis, recommendations)
```

## 📁 Project Structure

```
daydream/
├── src/
│   ├── agents/          # Multi-agent system components
│   │   ├── planner.py
│   │   ├── analyzer.py
│   │   ├── hypothesis.py
│   │   └── recommender.py
│   ├── data/            # Data retrieval modules
│   │   ├── perplexity.py
│   │   ├── openai.py
│   │   └── scraper.py
│   ├── memory/          # Vector store and knowledge base
│   │   └── store.py
│   ├── models/          # Data models
│   │   └── schemas.py
│   ├── api/             # FastAPI routes
│   │   └── routes.py
│   └── main.py          # Application entry point
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   └── index.html
├── tests/               # Test suite
├── examples/            # Example scripts
└── docs/                # Documentation
```

## 🔑 Resources Needed

### API Keys & Services

1. **OpenAI API** (Required)
   - Used for: GPT-4 reasoning, embeddings, semantic analysis
   - Cost: ~$0.01-0.03 per query
   - Get it: https://platform.openai.com/api-keys

2. **Perplexity API** (Recommended)
   - Used for: Direct visibility checks, citation analysis
   - Cost: $5/month (1000 searches)
   - Get it: https://www.perplexity.ai/settings/api

3. **Anthropic Claude API** (Optional)
   - Used for: Alternative reasoning engine
   - Cost: Pay-as-you-go
   - Get it: https://console.anthropic.com/

### System Resources

- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB for dependencies + vector database
- **Network**: Stable internet for API calls

## 🎨 Features

- Multi-agent orchestration using LangGraph
- Real-time visibility analysis across AI platforms
- Semantic similarity scoring using embeddings
- Historical tracking with vector memory
- Beautiful React dashboard with charts
- RESTful API with OpenAPI documentation
- Comprehensive reasoning with explainability
- Actionable recommendations engine

## 📈 Future Improvements

- [ ] Real-time monitoring dashboard
- [ ] Automated weekly reports
- [ ] Integration with Google Search Console
- [ ] A/B testing framework for content optimization
- [ ] Multi-language support
- [ ] Custom fine-tuned models for industry-specific GEO

## 📝 License

MIT License

## 👤 Author

Amar Nagargoje

## 🤝 Contributing

This is a demo project for the Daydream take-home assignment.



