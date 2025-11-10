"""
Demo script showing how to use the GEO Expert Agent via API
"""

import requests
import json
import time


API_BASE_URL = "http://localhost:8000"


def check_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        return response.status_code == 200
    except:
        return False


def run_analysis():
    """Run a GEO analysis via API"""
    
    payload = {
        "query": "best project management software",
        "brand_domain": "myapp.io",
        "competitors": ["asana.com", "monday.com", "trello.com"],
        "platforms": ["chatgpt", "perplexity"],
        "num_queries": 5
    }
    
    print("Sending analysis request...")
    print(f"Query: {payload['query']}")
    print(f"Brand: {payload['brand_domain']}")
    print()
    
    response = requests.post(
        f"{API_BASE_URL}/api/analyze",
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print("✓ Analysis complete!")
        print()
        print("RESULTS:")
        print("-" * 80)
        
        # Visibility
        brand_score = result['visibility_scores']['brand_score']
        print(f"Your visibility: {brand_score['mention_rate']*100:.1f}%")
        
        # Top competitor
        if result['visibility_scores']['competitor_scores']:
            top_comp = result['visibility_scores']['competitor_scores'][0]
            print(f"Top competitor: {top_comp['domain']} ({top_comp['mention_rate']*100:.1f}%)")
        
        print()
        print(f"Findings: {len(result['hypotheses'])}")
        print(f"Recommendations: {len(result['recommendations'])}")
        print()
        
        # Top recommendation
        if result['recommendations']:
            top_rec = result['recommendations'][0]
            print("Top Recommendation:")
            print(f"  [{top_rec['priority'].upper()}] {top_rec['title']}")
            print(f"  Impact: {top_rec['impact_score']}/10")
            print()
        
        return result
    else:
        print(f"✗ Analysis failed: {response.status_code}")
        print(response.text)
        return None


def get_history():
    """Get analysis history"""
    response = requests.get(f"{API_BASE_URL}/api/history?limit=5")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total']} historical analyses")
        
        for analysis in data['analyses']:
            print(f"  - {analysis['query']} ({analysis['brand']}): {analysis['visibility_rate']*100:.1f}%")
        
        return data
    else:
        print("Failed to get history")
        return None


def main():
    print("=" * 80)
    print("GEO EXPERT AGENT - API DEMO")
    print("=" * 80)
    print()
    
    # Check health
    print("Checking API status...")
    if not check_health():
        print("✗ API is not running!")
        print("Please start the server first: python -m src.main")
        return
    
    print("✓ API is running")
    print()
    
    # Run analysis
    result = run_analysis()
    
    if result:
        print()
        print("-" * 80)
        
        # Wait a moment for background save
        time.sleep(1)
        
        # Check history
        print()
        print("Checking history...")
        get_history()
    
    print()
    print("=" * 80)
    print("Demo complete!")
    print("View full results at: http://localhost:8000/docs")
    print("=" * 80)


if __name__ == "__main__":
    main()



