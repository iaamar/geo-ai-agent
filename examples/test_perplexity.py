#!/usr/bin/env python3
"""
Test Perplexity API integration
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.perplexity import PerplexityClient
from src.config import settings


async def test_perplexity():
    """Test Perplexity API"""
    
    print("\n" + "="*80)
    print("PERPLEXITY API TEST")
    print("="*80)
    
    # Check API key
    if not settings.perplexity_api_key:
        print("\n❌ Error: PERPLEXITY_API_KEY not found in .env")
        print("Please add your Perplexity API key to .env file")
        return
    
    print(f"\n✅ API Key configured: {settings.perplexity_api_key[:10]}...")
    
    # Initialize client
    client = PerplexityClient()
    
    # Test query
    test_query = "What are the best AI-powered project management tools in 2024?"
    print(f"\n🔍 Testing query: '{test_query}'")
    print("\nQuerying Perplexity AI...")
    
    try:
        # Make API call
        response = await client.search(test_query)
        
        # Extract content
        if "choices" in response and len(response["choices"]) > 0:
            content = response["choices"][0].get("message", {}).get("content", "")
            citations = response.get("citations", [])
            
            print("\n✅ Query successful!")
            print("\n" + "-"*80)
            print("RESPONSE:")
            print("-"*80)
            print(content[:500] + "..." if len(content) > 500 else content)
            
            if citations:
                print("\n" + "-"*80)
                print(f"CITATIONS ({len(citations)}):")
                print("-"*80)
                for i, citation in enumerate(citations[:5], 1):
                    print(f"{i}. {citation}")
            
            # Test citation extraction
            print("\n" + "="*80)
            print("TESTING CITATION EXTRACTION")
            print("="*80)
            
            citation_data = client.extract_citations(
                response=response,
                query=test_query,
                brand_domain="example.com",
                competitors=["competitor1.com", "competitor2.com"]
            )
            
            print(f"\nPlatform: {citation_data.platform.value}")
            print(f"Brand mentioned: {citation_data.brand_mentioned}")
            print(f"Citation position: {citation_data.citation_position}")
            print(f"Competitors mentioned: {citation_data.competitors_mentioned}")
            
        else:
            print("\n⚠️  Unexpected response format")
            print(f"Response: {response}")
        
        print("\n" + "="*80)
        print("✅ PERPLEXITY API IS WORKING!")
        print("="*80)
        print("\nYou can now use Perplexity for GEO analysis.")
        print("Run the full analysis with:")
        print("  .venv/bin/python examples/simple_demo.py")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease check:")
        print("  1. API key is valid")
        print("  2. You have API credits")
        print("  3. Network connection is working")
        print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(test_perplexity())


