# Where to See LLM-Generated Data

## ✅ Perplexity IS Working!

Test confirms:
- API responding ✅
- 15 citations returned ✅  
- Competitors detected ✅
- Flexible matching ✅

## 📺 Terminal - See ALL LLM Outputs

### When you run `./run.sh` and submit an analysis, scroll your terminal to see:

#### 1. Planner Output
```
============================================================
📋 PLANNER LLM OUTPUT:
------------------------------------------------------------
### Analysis Plan for Best CRM Software...
(Complete planning strategy from GPT-4)
============================================================
```

#### 2. ChatGPT Responses (for each query)
```
💬 Querying ChatGPT: 'best CRM software'
============================================================
💬 CHATGPT RESPONSE for 'best CRM software':
------------------------------------------------------------
Choosing the best Customer Relationship Management (CRM)...

### 1. Salesforce
- Website: https://www.salesforce.com/
- Best for: Enterprise...

### 2. HubSpot
- Website: https://www.hubspot.com/
...
============================================================
```

#### 3. Perplexity Responses (for each query)
```
🔍 Querying Perplexity: 'best CRM software'
============================================================
🔍 PERPLEXITY RESPONSE for 'best CRM software':
------------------------------------------------------------
The best CRM software in 2025 includes Salesforce Sales Cloud, 
Zoho CRM, HubSpot Sales Hub, Pipedrive, and Monday CRM...

📚 Citations: 15
   1. https://zapier.com/blog/best-crm-app/
   2. https://www.zendesk.com/sell/crm/
   3. https://monday.com/blog/crm-and-sales/crm-software/
   ...
============================================================
✅ Extraction complete: Brand=False, Competitors=3, Citations=15
```

#### 4. Hypothesis Generation
```
============================================================
💡 HYPOTHESIS LLM OUTPUT:
------------------------------------------------------------
[JSON array with generated hypotheses]
============================================================
✅ Parsed 3 hypotheses from LLM
```

#### 5. Recommendations
```
============================================================
✨ RECOMMENDER LLM OUTPUT:
------------------------------------------------------------
[JSON array with recommendations]
============================================================
✅ Parsing 6 recommendations from LLM
   1. Leverage Semantic SEO | Priority: high | Impact: 9.0/10
   2. Build Domain Authority | Priority: high | Impact: 8.0/10
```

## 🌐 Frontend - See Structured Data

### Open: http://localhost:5173

### After running analysis, you'll see:

#### At the TOP of results (NEW!)
```
┌─────────────────────────────────────────────────────────┐
│ 🤖 Multi-Agent Analysis System                         │
│ Transparent AI reasoning with parallel execution       │
├─────────────────────────────────────────────────────────┤
│ [Reasoning Trace] [System Components] [Data Flow] [Performance] │
└─────────────────────────────────────────────────────────┘
```

#### Click "Reasoning Trace" Tab
You'll see expandable cards:
```
✓ PlannerAgent | planning | 0.45s | completed
  [Click to expand]
  
✓ DataCollectorAgent | data_collection | PARALLEL | 3.21s
  Process: Parallel execution of queries across all platforms
  
  Reasoning Steps:
  1. Created 10 query tasks
  2. Executing all queries concurrently
  ...
  
  Input: { query_variations: [...], platforms: [...] }
  Output: { successful: 10, failed: 0, citations: 10 }
```

#### Click "System Components" Tab
You'll see agent details:
```
🤖 PlannerAgent
   Role: Strategic Planning
   Inputs: Query, Brand, Competitors
   Outputs: Query Variations, Platform Selection
   Execution: Sequential (first step) [Blue badge]
   
🤖 DataCollectorAgent  
   Role: Data Gathering
   Execution: Parallel (all queries concurrent) [Purple badge with ⚡]
   Concurrency: Up to 50 parallel requests
```

#### Click "Data Flow" Tab
Visual diagram showing:
```
┌──────────────┐         ┌──────────────────┐
│  User Input  │────────>│ Planning Agent   │
└──────────────┘         └─────────┬────────┘
                                   │ (4 query variations)
                         ┌─────────▼────────┐
                         │ Data Collection  │
                         └─────────┬────────┘
                                   │ (10 citations)
                         ┌─────────▼────────┐
                         │    Analysis      │
                         └──────────────────┘
```

#### Click "Performance" Tab
Timing bars and metrics:
```
[Bar chart showing each step]

Total Time: 55.2s
Agent Steps: 6
Speedup vs Sequential: ~40%
```

## Why You Might Not See Frontend Data

### Check These:

1. **Is ReasoningDisplay component showing?**
   - Look for "🤖 Multi-Agent Analysis System" header at top of results
   - Should appear BEFORE the "Analysis Summary" section

2. **Check browser console for errors:**
   - Press F12
   - Go to Console tab
   - Look for React errors

3. **Is reasoning_trace in response?**
   - Check Network tab
   - Look for `/api/analyze` request
   - Check response has `reasoning_trace` field

## Quick Test

### Terminal Test (Verify logging works):
```bash
.venv/bin/python examples/test_perplexity.py
```

**You should see:**
- 🔍 PERPLEXITY RESPONSE section
- 📚 Citations: 15
- ✅ Extraction complete

### Full App Test:
```bash
./run.sh
```

**Then:**
1. Open http://localhost:5173
2. Submit analysis
3. **Watch terminal** - scroll up to see all LLM outputs
4. **Check frontend** - look for 4 tabs at top of results

## Still Not Seeing Data?

If frontend doesn't show reasoning tabs:

1. **Check terminal for React errors**
2. **Verify reasoning_trace in API response:**
```bash
curl http://localhost:8000/health
```

3. **Check browser console** (F12)

Let me know what you see and I'll debug further!

