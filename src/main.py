"""Main application entry point"""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from src.api.routes import router
from src.config import settings
from src import __version__


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    # Startup
    print(f"🚀 Starting GEO Expert Agent v{__version__}")
    print(f"📊 Server: http://{settings.host}:{settings.port}")
    print(f"📖 API Docs: http://{settings.host}:{settings.port}/docs")
    
    yield
    
    # Shutdown
    print("👋 Shutting down GEO Expert Agent")


# Create FastAPI app
app = FastAPI(
    title="GEO Expert Agent API",
    description="AI-Powered Generative Engine Optimization Analysis System",
    version=__version__,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Serve static files (frontend) if they exist
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    # Mount static assets (js, css, images)
    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")
    
    # Serve index.html for all non-API routes (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve frontend SPA for all non-API routes"""
        # If it's an API route, let it be handled by the router
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("health"):
            return {"error": "Not found"}
        
        # For root path, serve index.html
        if full_path == "" or full_path == "/":
            return FileResponse(frontend_dist / "index.html")
        
        # Check if file exists in dist folder
        file_path = frontend_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        
        # For all other routes (SPA routing), serve index.html
        return FileResponse(frontend_dist / "index.html")
else:
    @app.get("/")
    async def root():
        """Root endpoint when frontend is not built"""
        return {
            "name": "GEO Expert Agent API",
            "version": __version__,
            "status": "running",
            "docs": "/docs",
            "health": "/health",
            "note": "Frontend not built. Run 'cd frontend && npm run build' to build frontend."
        }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )



