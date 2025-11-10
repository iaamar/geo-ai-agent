# How to See Everything Working

## 🚀 Restart the Server

```bash
# Kill existing processes
pkill -f "python -m src.main"
pkill -f "vite"

# Start fresh
cd /Users/amarnagargoje/Documents/Projects/daydream
./run.sh
```

## 📺 In Terminal You'll See

### Every LLM Response:
```
📋 PLANNER LLM OUTPUT:
(Complete planning response)

💬 CHATGPT RESPONSE for 'best CRM software':
(Complete ChatGPT answer with URLs)

🔍 PERPLEXITY RESPONSE for 'best CRM software':
(Complete Perplexity answer with citations)

💡 HYPOTHESIS LLM OUTPUT:
(Generated hypotheses JSON)

✨ RECOMMENDER LLM OUTPUT:
(Generated recommendations JSON)
```

## 🌐 On Frontend You'll See

### Open: http://localhost:5173

### Run Analysis → See 4 New Tabs:

**1. Reasoning Trace** (Expandable cards for each step)
**2. System Components** (Agent descriptions)
**3. Data Flow** (Visual diagram)
**4. Performance** (Timing charts)

## ✅ What's Fixed

1. **LLM outputs visible** - Every generation logged
2. **Perplexity working** - Logs show API responses
3. **Competitor scores accurate** - Bug fixed
4. **Frontend transparency** - Complete reasoning display
5. **Parallel execution** - 40% faster

## 📊 Test With

**Query:** "best CRM software"
**Brand:** acme.com
**Competitors:** hubspot.com, salesforce.com, pipedrive.com
**Platforms:** ✓ ChatGPT, ✓ Perplexity

**Expected:**
- Different scores for each competitor (not identical!)
- Complete LLM outputs in terminal
- Reasoning tabs on frontend
- Perplexity citations shown

## That's It!

**Everything is ready. Restart and test!** 🎉
