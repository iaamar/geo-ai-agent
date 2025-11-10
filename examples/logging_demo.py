#!/usr/bin/env python3
"""
Demo script to showcase agent logging functionality
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.schemas import AnalysisRequest, AIPlatform
from src.agents.orchestrator import GEOOrchestrator


async def main():
    """Run a simple analysis to demonstrate logging"""
    
    # Create orchestrator
    orchestrator = GEOOrchestrator()
    
    # Create analysis request
    request = AnalysisRequest(
        query="best AI project management tools 2024",
        brand_domain="example.com",
        competitors=[
            "competitor1.com",
            "competitor2.com"
        ],
        platforms=[AIPlatform.CHATGPT]
    )
    
    print("\n" + "="*80)
    print("GEO EXPERT AGENT - LOGGING DEMONSTRATION")
    print("="*80)
    print("\nThis demo shows the comprehensive logging system in action.")
    print("Watch the detailed step-by-step execution logs below:\n")
    print("="*80 + "\n")
    
    # Run analysis (with full logging)
    try:
        result = await orchestrator.run_analysis(request)
        
        print("\n" + "="*80)
        print("DEMO COMPLETE")
        print("="*80)
        print(f"\nAnalysis ID: {result.id}")
        print(f"Total Citations: {len(result.citations)}")
        print(f"Hypotheses: {len(result.hypotheses)}")
        print(f"Recommendations: {len(result.recommendations)}")
        print("\nCheck 'geo_agent.log' for detailed logs including:")
        print("  • Query execution details")
        print("  • API response data")
        print("  • Performance metrics")
        print("  • Error traces (if any)")
        print("\nTo view the log file:")
        print("  tail -f geo_agent.log")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nCheck 'geo_agent.log' for full error details.")
        print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())


