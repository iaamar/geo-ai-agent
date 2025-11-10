"""
Simple demo script showing how to use the GEO Expert Agent
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.schemas import AnalysisRequest, Platform
from src.agents.orchestrator import GEOOrchestrator


async def main():
    """Run a simple GEO analysis"""
    
    print("=" * 80)
    print("GEO EXPERT AGENT - SIMPLE DEMO")
    print("=" * 80)
    print()
    
    # Create analysis request
    request = AnalysisRequest(
        query="best AI productivity tools",
        brand_domain="acme.com",
        competitors=["notion.so", "asana.com", "clickup.com"],
        platforms=[Platform.CHATGPT, Platform.PERPLEXITY],
        num_queries=3  # Reduced for demo
    )
    
    print(f"Query: {request.query}")
    print(f"Brand: {request.brand_domain}")
    print(f"Competitors: {', '.join(request.competitors)}")
    print(f"Platforms: {', '.join([p.value for p in request.platforms])}")
    print()
    print("Starting analysis...")
    print("-" * 80)
    print()
    
    # Run analysis
    orchestrator = GEOOrchestrator()
    result = await orchestrator.run_analysis(request)
    
    # Display results
    print()
    print("=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)
    print()
    
    # Visibility scores
    print("VISIBILITY SCORES")
    print("-" * 80)
    brand_score = result.visibility_scores.brand_score
    print(f"Your Brand ({brand_score.domain}): {brand_score.mention_rate*100:.1f}%")
    print(f"  - Total mentions: {brand_score.total_mentions}")
    print(f"  - Platforms: {brand_score.platforms}")
    print()
    
    print("Competitors:")
    for comp in result.visibility_scores.competitor_scores:
        print(f"  - {comp.domain}: {comp.mention_rate*100:.1f}%")
    print()
    
    # Hypotheses
    print("KEY FINDINGS")
    print("-" * 80)
    for i, hypothesis in enumerate(result.hypotheses, 1):
        print(f"{i}. {hypothesis.title}")
        print(f"   Confidence: {hypothesis.confidence*100:.0f}%")
        print(f"   {hypothesis.explanation}")
        print()
    
    # Top recommendations
    print("TOP RECOMMENDATIONS")
    print("-" * 80)
    for i, rec in enumerate(result.recommendations[:3], 1):
        print(f"{i}. [{rec.priority.upper()}] {rec.title}")
        print(f"   Impact: {rec.impact_score}/10 | Effort: {rec.effort_score}/10")
        print(f"   {rec.description}")
        print()
    
    # Summary
    print("SUMMARY")
    print("-" * 80)
    print(result.summary)
    print()
    
    print("=" * 80)
    print(f"Analysis ID: {result.id}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())



