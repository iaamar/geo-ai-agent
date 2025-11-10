# Contributing to GEO Expert Agent

## Development Setup

```bash
# Clone repository
git clone <your-repo-url>
cd daydream

# Run setup script
./run.sh
```

The script will:
- Install UV package manager
- Create virtual environment
- Install dependencies
- Start backend + frontend

## Project Structure

```
daydream/
├── deliverables/     ← Submission materials
├── src/              ← Backend (Python/FastAPI)
├── frontend/         ← Frontend (React)
├── examples/         ← Demo scripts
└── archive/          ← Working documents
```

## Running Tests

```bash
# Run prototype demo
.venv/bin/python deliverables/prototype/demo_notebook.py

# Run example
.venv/bin/python examples/simple_demo.py
```

## Key Files

**Backend:**
- `src/agents/graph_orchestrator.py` - Multi-agent system
- `src/agents/evaluator.py` - Reflexion implementation
- `src/api/routes.py` - API endpoints

**Frontend:**
- `frontend/src/pages/AnalysisPage.jsx` - Main analysis UI
- `frontend/src/components/RealTimeProgress.jsx` - Live progress
- `frontend/src/components/EvaluationDisplay.jsx` - Quality display

**Documentation:**
- `deliverables/FINAL_AGENT_DESIGN_DOCUMENT.md` - Complete spec
- `README.md` - This file
- `QUICK_START.md` - Setup guide

## Making Changes

1. Backend changes: Modify files in `src/`
2. Frontend changes: Modify files in `frontend/src/`
3. Test locally with `./run.sh`
4. Update documentation as needed

## Questions?

See `deliverables/` folder for complete documentation.
