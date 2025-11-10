"""FastAPI routes for GEO Expert Agent"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from datetime import datetime
import logging

from src.models.schemas import (
    AnalysisRequest,
    AnalysisResult,
    CompareRequest,
    HealthResponse
)
from src.agents.graph_orchestrator import graph_orchestrator
from src.memory.store import MemoryStore
from src import __version__


router = APIRouter()
# Use the new multi-agent graph orchestrator
orchestrator = graph_orchestrator
memory = MemoryStore()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.now(),
        services={
            "api": True,
            "orchestrator": True,
            "memory": True
        }
    )


@router.post("/api/analyze", response_model=AnalysisResult)
async def analyze_visibility(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Analyze brand visibility across AI platforms
    
    Args:
        request: Analysis request with query, brand, and competitors
        background_tasks: Background task handler
        
    Returns:
        Complete analysis result with hypotheses and recommendations
    """
    try:
        # Run analysis
        result = await orchestrator.run_analysis(request)
        
        # Save to memory in background
        background_tasks.add_task(memory.save_analysis, result)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/api/compare")
async def compare_brands(request: CompareRequest):
    """
    Compare visibility between multiple brands
    
    Optimized: Single analysis that treats all domains equally
    
    Args:
        request: Comparison request with multiple domains
        
    Returns:
        Comparative analysis for all brands
    """
    try:
        logger = logging.getLogger(__name__)
        logger.info(f"🔄 Starting comparison for {len(request.domains)} domains")
        
        # Pick first domain as "brand" and rest as "competitors" for ONE analysis
        # This avoids running multiple full analyses
        primary_domain = request.domains[0]
        other_domains = request.domains[1:]
        
        analysis_request = AnalysisRequest(
            query=request.query,
            brand_domain=primary_domain,
            competitors=other_domains,
            platforms=request.platforms,
            num_queries=5  # Reasonable number for comparison
        )
        
        logger.info(f"Running single optimized analysis for all domains")
        result = await orchestrator.run_analysis(analysis_request)
        
        # Extract visibility for all domains
        comparison_results = []
        
        # Add primary brand
        comparison_results.append({
            "domain": primary_domain,
            "visibility_rate": result.visibility_scores.brand_score.mention_rate,
            "mentions": result.visibility_scores.brand_score.total_mentions,
            "platforms": result.visibility_scores.brand_score.platforms
        })
        
        # Add competitors
        for comp_score in result.visibility_scores.competitor_scores:
            comparison_results.append({
                "domain": comp_score.domain,
                "visibility_rate": comp_score.mention_rate,
                "mentions": comp_score.total_mentions,
                "platforms": comp_score.platforms
            })
        
        # Sort by visibility rate
        comparison_results.sort(key=lambda x: x["visibility_rate"], reverse=True)
        
        logger.info(f"✅ Comparison complete for {len(comparison_results)} domains")
        
        return {
            "query": request.query,
            "comparison": comparison_results,
            "winner": comparison_results[0]["domain"] if comparison_results else None,
            # Include full analysis data for detailed view
            "full_analysis": {
                "citations": [c.model_dump() for c in result.citations],
                "hypotheses": [h.model_dump() for h in result.hypotheses],
                "recommendations": [r.model_dump() for r in result.recommendations],
                "summary": result.summary
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@router.get("/api/history")
async def get_history(
    brand: Optional[str] = None,
    limit: int = 10
):
    """
    Get historical analyses
    
    Args:
        brand: Optional brand filter
        limit: Number of results (max 50)
        
    Returns:
        List of historical analyses
    """
    try:
        limit = min(limit, 50)  # Cap at 50
        analyses = memory.get_recent_analyses(brand=brand, limit=limit)
        
        return {
            "total": len(analyses),
            "analyses": analyses
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")


@router.get("/api/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """
    Get specific analysis by ID
    
    Args:
        analysis_id: Analysis ID
        
    Returns:
        Analysis details
    """
    try:
        analysis = memory.get_analysis(analysis_id)
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch analysis: {str(e)}")


@router.get("/api/search")
async def search_analyses(
    query: str,
    limit: int = 5
):
    """
    Search for similar historical analyses
    
    Args:
        query: Search query
        limit: Number of results
        
    Returns:
        Similar analyses
    """
    try:
        similar = memory.search_similar_analyses(query, limit=limit)
        
        return {
            "query": query,
            "results": similar
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/api/recommendations/{analysis_id}")
async def get_recommendations(analysis_id: str):
    """
    Get recommendations for a specific analysis
    
    Args:
        analysis_id: Analysis ID
        
    Returns:
        Recommendations list
    """
    try:
        analysis = memory.get_analysis(analysis_id)
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        # In a full implementation, this would return the stored recommendations
        # For now, return metadata
        return {
            "analysis_id": analysis_id,
            "message": "Recommendations are part of the full analysis result"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recommendations: {str(e)}")


@router.delete("/api/history/clear")
async def clear_history():
    """
    Clear all historical data (admin endpoint)
    
    WARNING: This deletes all stored analyses
    """
    try:
        memory.clear_collection()
        return {"message": "History cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear history: {str(e)}")



