# GEO Expert Agent - Examples

This directory contains example scripts demonstrating how to use the GEO Expert Agent.

## Examples

### 1. Simple Demo (Direct Python)

Run a GEO analysis directly using Python:

```bash
python examples/simple_demo.py
```

This demonstrates:
- Creating an analysis request
- Running the multi-agent orchestrator
- Displaying results (visibility scores, hypotheses, recommendations)

### 2. API Demo

Use the GEO Expert Agent via REST API:

```bash
# First, start the server
python -m src.main

# In another terminal, run the demo
python examples/api_demo.py
```

This demonstrates:
- Checking API health
- Submitting analysis via POST request
- Retrieving historical analyses

## Use Cases

### Use Case 1: Brand Visibility Check

**Scenario**: A marketing team wants to understand why their SaaS product isn't showing up in ChatGPT recommendations.

```python
from src.models.schemas import AnalysisRequest, Platform
from src.agents.orchestrator import GEOOrchestrator

request = AnalysisRequest(
    query="best customer support software",
    brand_domain="yourproduct.com",
    competitors=["zendesk.com", "intercom.com", "freshdesk.com"],
    platforms=[Platform.CHATGPT, Platform.PERPLEXITY],
    num_queries=10
)

orchestrator = GEOOrchestrator()
result = await orchestrator.run_analysis(request)

# Access results
print(f"Visibility: {result.visibility_scores.brand_score.mention_rate * 100}%")
for hypothesis in result.hypotheses:
    print(f"- {hypothesis.title}: {hypothesis.explanation}")
```

### Use Case 2: Competitor Analysis

**Scenario**: Compare your brand against multiple competitors to identify gaps.

```bash
curl -X POST http://localhost:8000/api/compare \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best CRM tools",
    "domains": ["yourcrm.com", "salesforce.com", "hubspot.com"],
    "platforms": ["chatgpt", "perplexity"]
  }'
```

### Use Case 3: Historical Tracking

**Scenario**: Track visibility improvements over time.

```python
# Run analysis weekly
import schedule

def weekly_analysis():
    request = AnalysisRequest(
        query="best project management tools",
        brand_domain="yourtool.com",
        competitors=["asana.com", "monday.com"],
        platforms=[Platform.CHATGPT, Platform.PERPLEXITY]
    )
    
    orchestrator = GEOOrchestrator()
    result = await orchestrator.run_analysis(request)
    
    # Results automatically saved to memory
    print(f"Week {week}: {result.visibility_scores.brand_score.mention_rate * 100}%")

schedule.every().monday.at("09:00").do(weekly_analysis)
```

## Production Use Cases

### 1. Automated Monitoring Dashboard

Create a monitoring system that tracks GEO visibility daily:

```python
# monitor.py
from src.agents.orchestrator import GEOOrchestrator
from src.memory.store import MemoryStore

async def daily_monitoring(brands, queries):
    orchestrator = GEOOrchestrator()
    memory = MemoryStore()
    
    for brand in brands:
        for query in queries:
            result = await orchestrator.run_analysis(
                AnalysisRequest(query=query, brand_domain=brand, ...)
            )
            
            # Check for significant changes
            similar = memory.search_similar_analyses(query, limit=1)
            if similar:
                prev_rate = similar[0]['visibility_rate']
                curr_rate = result.visibility_scores.brand_score.mention_rate
                
                if abs(curr_rate - prev_rate) > 0.1:  # 10% change
                    send_alert(brand, query, prev_rate, curr_rate)
```

### 2. Content Optimization Pipeline

Use recommendations to guide content strategy:

```python
async def optimize_content(topic):
    # Run analysis
    result = await orchestrator.run_analysis(
        AnalysisRequest(query=f"best {topic} tools", ...)
    )
    
    # Extract high-priority recommendations
    high_priority = [
        r for r in result.recommendations
        if r.priority == "high"
    ]
    
    # Generate content brief
    brief = {
        "topic": topic,
        "target_visibility": result.visibility_scores.brand_score.mention_rate + 0.2,
        "action_items": [
            item
            for rec in high_priority
            for item in rec.action_items
        ],
        "competitor_keywords": extract_keywords(result.citations)
    }
    
    return brief
```

### 3. Multi-Brand Portfolio Management

Manage GEO for multiple brands:

```python
async def portfolio_analysis(portfolio):
    results = []
    
    for brand in portfolio:
        for query in brand['target_queries']:
            result = await orchestrator.run_analysis(
                AnalysisRequest(
                    query=query,
                    brand_domain=brand['domain'],
                    competitors=brand['competitors']
                )
            )
            results.append(result)
    
    # Generate portfolio report
    report = {
        "total_brands": len(portfolio),
        "avg_visibility": np.mean([r.visibility_scores.brand_score.mention_rate for r in results]),
        "top_performer": max(results, key=lambda r: r.visibility_scores.brand_score.mention_rate),
        "needs_attention": [r for r in results if r.visibility_scores.brand_score.mention_rate < 0.2]
    }
    
    return report
```

## Advanced Examples

### Custom Agent Workflow

Extend the orchestrator with custom logic:

```python
from src.agents.orchestrator import GEOOrchestrator

class CustomOrchestrator(GEOOrchestrator):
    async def run_analysis(self, request):
        # Pre-processing
        request = self.enhance_query(request)
        
        # Run standard analysis
        result = await super().run_analysis(request)
        
        # Post-processing
        result = self.add_custom_insights(result)
        
        return result
    
    def enhance_query(self, request):
        # Add semantic variations
        request.query = f"{request.query} {current_year}"
        return request
```

## Running Examples

Make sure you have:
1. Set up `.env` with API keys
2. Installed dependencies: `pip install -r requirements.txt`
3. Activated virtual environment: `source venv/bin/activate`

Then run any example:
```bash
python examples/simple_demo.py
python examples/api_demo.py
```



