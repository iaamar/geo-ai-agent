#!/usr/bin/env python3
"""
Demo: GEO Analysis with Perplexity AI
Shows how to use Perplexity for brand visibility analysis
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.schemas import AnalysisRequest, AIPlatform
from src.agents.orchestrator import GEOOrchestrator


async def main():
    """Run GEO analysis with Perplexity"""
    
    print("\n" + "="*80)
    print("GEO ANALYSIS WITH PERPLEXITY AI")
    print("="*80)
    print("\nThis demo runs a complete GEO analysis using:")
    print("  • ChatGPT - For AI assistant insights")
    print("  • Perplexity - For search engine insights")
    print("\nBoth platforms will be queried to compare brand visibility")
    print("="*80 + "\n")
    
    # Create orchestrator
    orchestrator = GEOOrchestrator()
    
    # Create analysis request with both platforms
    request = AnalysisRequest(
        query="best AI project management tools 2024",
        brand_domain="example.com",
        competitors=[
            "competitor1.com",
            "competitor2.com",
            "asana.com"
        ],
        platforms=[
            AIPlatform.CHATGPT,
            AIPlatform.PERPLEXITY  # ✅ Now working!
        ]
    )
    
    print(f"📊 Analysis Configuration:")
    print(f"   Query: '{request.query}'")
    print(f"   Brand: {request.brand_domain}")
    print(f"   Competitors: {', '.join(request.competitors)}")
    print(f"   Platforms: {', '.join([p.value for p in request.platforms])}")
    print("\n" + "="*80 + "\n")
    
    try:
        # Run analysis
        result = await orchestrator.run_analysis(request)
        
        print("\n" + "="*80)
        print("ANALYSIS RESULTS")
        print("="*80)
        
        # Overall stats
        print(f"\n📈 Analysis ID: {result.id}")
        print(f"📝 Citations Collected: {len(result.citations)}")
        
        # Platform breakdown
        chatgpt_citations = [c for c in result.citations if c.platform == AIPlatform.CHATGPT]
        perplexity_citations = [c for c in result.citations if c.platform == AIPlatform.PERPLEXITY]
        
        print(f"\n🤖 ChatGPT Citations: {len(chatgpt_citations)}")
        print(f"🔍 Perplexity Citations: {len(perplexity_citations)}")
        
        # Brand visibility
        print(f"\n🎯 Brand Visibility:")
        print(f"   Overall: {result.visibility_scores.brand_score.mention_rate * 100:.1f}%")
        print(f"   Total Mentions: {result.visibility_scores.brand_score.total_mentions}")
        
        # Platform-specific visibility
        chatgpt_brand = sum(1 for c in chatgpt_citations if c.brand_mentioned)
        perplexity_brand = sum(1 for c in perplexity_citations if c.brand_mentioned)
        
        print(f"\n   ChatGPT: {chatgpt_brand}/{len(chatgpt_citations)} queries")
        print(f"   Perplexity: {perplexity_brand}/{len(perplexity_citations)} queries")
        
        # Hypotheses
        print(f"\n💡 Key Findings:")
        for i, hypothesis in enumerate(result.hypotheses[:3], 1):
            print(f"   {i}. {hypothesis.title}")
            print(f"      Confidence: {hypothesis.confidence * 100:.0f}%")
        
        # Recommendations
        print(f"\n✨ Top Recommendations:")
        for i, rec in enumerate(result.recommendations[:3], 1):
            print(f"   {i}. {rec.title}")
            print(f"      Priority: {rec.priority} | Impact: {rec.impact}")
        
        # Citation details
        print(f"\n📚 Citation Details:")
        print(f"\n   Perplexity Citations:")
        for i, citation in enumerate(perplexity_citations[:3], 1):
            print(f"   {i}. Query: {citation.query}")
            print(f"      Brand mentioned: {citation.brand_mentioned}")
            if citation.competitors_mentioned:
                print(f"      Competitors: {', '.join(citation.competitors_mentioned)}")
        
        print("\n" + "="*80)
        print("✅ ANALYSIS COMPLETE!")
        print("="*80)
        print(f"\nView complete results at: http://localhost:8000/analysis/{result.id}")
        print("(Start the server with: ./run.sh)")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nCheck the logs for details.")
        print("="*80 + "\n")
        raise


if __name__ == "__main__":
    asyncio.run(main())


