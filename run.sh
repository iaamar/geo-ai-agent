#!/bin/bash

# GEO Expert Agent - Quick Start Script
# This script sets up and runs the GEO Expert Agent system

set -e  # Exit on error

echo "═══════════════════════════════════════════════════════════"
echo "   GEO Expert Agent - Quick Start"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python 3.10+ required (found $PYTHON_VERSION)"
    exit 1
fi
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo ""
    echo "Creating .env from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️  IMPORTANT: Please add your API keys to .env file"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Required:"
    echo "  • OPENAI_API_KEY - Get from https://platform.openai.com/api-keys"
    echo ""
    echo "Optional (but recommended):"
    echo "  • PERPLEXITY_API_KEY - Get from https://www.perplexity.ai/settings/api"
    echo ""
    echo "Edit the file now:"
    echo "  nano .env"
    echo ""
    read -p "Press Enter after adding your API keys..."
fi

# Check if OpenAI API key is set
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "❌ Error: OpenAI API key not configured in .env"
    echo "Please add your API key and run this script again"
    exit 1
fi
echo "✓ API keys configured"
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "Installing UV package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    echo "✓ UV installed"
fi
echo ""

# Setup virtual environment with UV
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with UV..."
    uv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi
echo ""

# Install Python dependencies with UV
echo "Installing Python dependencies with UV..."
if uv pip install -e . --quiet; then
    echo "✓ Python dependencies installed"
else
    echo "❌ Error installing dependencies"
    exit 1
fi
echo ""

# Activate virtual environment
source .venv/bin/activate

# Check if Node.js is available for frontend
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version 2>&1)
    echo "✓ Node.js $NODE_VERSION found"
    
    # Install frontend dependencies if needed
    if [ ! -d "frontend/node_modules" ]; then
        echo ""
        echo "Installing frontend dependencies..."
        cd frontend
        npm install
        cd ..
        echo "✓ Frontend dependencies installed"
    else
        echo "✓ Frontend dependencies exist"
    fi
    FRONTEND_AVAILABLE=true
else
    echo "⚠️  Node.js not found - frontend won't be available"
    echo "   Backend API will still work"
    FRONTEND_AVAILABLE=false
fi
echo ""

# Auto-start full stack
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Starting Full Stack (Backend + Frontend)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

choice=1

case $choice in
    1)
        if [ "$FRONTEND_AVAILABLE" = false ]; then
            echo "❌ Frontend not available (Node.js not installed)"
            exit 1
        fi
        
        # Kill any existing processes on ports 8000 and 5173
        echo "Checking for existing processes..."
        lsof -ti:8000 | xargs kill -9 2>/dev/null && echo "✓ Cleaned up port 8000" || true
        lsof -ti:5173 | xargs kill -9 2>/dev/null && echo "✓ Cleaned up port 5173" || true
        
        echo ""
        echo "Starting full stack..."
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Starting backend server..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Start backend in background (logs to console)
        .venv/bin/python -m src.main &
        BACKEND_PID=$!
        echo "Backend PID: $BACKEND_PID"
        echo "Backend logs will appear below..."
        echo ""
        
        # Wait for backend to start
        echo "Waiting for backend to start..."
        sleep 3
        
        # Check if backend is running
        if ! curl -s http://localhost:8000/health > /dev/null; then
            echo "⚠️  Backend taking longer to start..."
            sleep 2
            if ! curl -s http://localhost:8000/health > /dev/null; then
                echo "❌ Backend failed to start. Check backend.log for details:"
                tail -20 backend.log
                kill $BACKEND_PID 2>/dev/null || true
                exit 1
            fi
        fi
        echo "✓ Backend running at http://localhost:8000"
        echo ""
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Starting frontend..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Start frontend
        cd frontend
        npm run dev &
        FRONTEND_PID=$!
        cd ..
        
        echo ""
        echo "═══════════════════════════════════════════════════════════"
        echo "   GEO Expert Agent is running!"
        echo "═══════════════════════════════════════════════════════════"
        echo ""
        echo "🌐 Frontend:  http://localhost:5173"
        echo "🔧 API:       http://localhost:8000"
        echo "📖 API Docs:  http://localhost:8000/docs"
        echo ""
        echo "Press Ctrl+C to stop both servers"
        echo "═══════════════════════════════════════════════════════════"
        
        # Wait for Ctrl+C
        trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
        wait
        ;;
        
    2)
        echo ""
        echo "Starting backend only..."
        echo ""
        echo "═══════════════════════════════════════════════════════════"
        echo "   GEO Expert Agent Backend"
        echo "═══════════════════════════════════════════════════════════"
        echo ""
        .venv/bin/python -m src.main
        ;;
        
    3)
        echo ""
        echo "Running demo script..."
        echo ""
        .venv/bin/python examples/simple_demo.py
        ;;
        
    4)
        echo "Goodbye!"
        exit 0
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

