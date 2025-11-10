"""Perplexity AI data retrieval"""

import httpx
import logging
from typing import List, Dict, Optional
from src.config import settings
from src.models.schemas import CitationData, Platform

logger = logging.getLogger(__name__)


class PerplexityClient:
    """Client for Perplexity AI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.perplexity_api_key
        self.base_url = "https://api.perplexity.ai"
        
    async def search(self, query: str) -> Dict:
        """
        Search using Perplexity AI
        
        Args:
            query: Search query
            
        Returns:
            Response with citations and sources
        """
        if not self.api_key:
            # Simulate response if no API key
            return self._simulate_response(query)
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "sonar",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful search assistant. Provide accurate information with sources."
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
        
        try:
            logger.info(f"🔍 Querying Perplexity: '{query}'")
            logger.debug(f"   Model: {payload['model']}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()
                
                # Log response
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0].get("message", {}).get("content", "")
                    logger.info("="*60)
                    logger.info(f"🔍 PERPLEXITY RESPONSE for '{query}':")
                    logger.info("-"*60)
                    logger.info(content[:500] + "..." if len(content) > 500 else content)
                    if "citations" in data:
                        logger.info(f"\n📚 Citations: {len(data.get('citations', []))}")
                        for i, cite in enumerate(data.get("citations", [])[:3], 1):
                            logger.info(f"   {i}. {cite}")
                    logger.info("="*60)
                
                return data
        except Exception as e:
            error_msg = str(e)
            error_type = type(e).__name__
            
            # Log detailed error
            logger.error(f"❌ Perplexity API error ({error_type}): {error_msg}")
            
            # Check for specific error types
            if "429" in error_msg or "rate limit" in error_msg.lower():
                logger.warning("⚠️  Rate limit reached - consider reducing concurrent requests")
            elif "timeout" in error_msg.lower():
                logger.warning("⚠️  Request timeout - try increasing timeout value")
            elif "401" in error_msg or "403" in error_msg:
                logger.error("⚠️  Authentication error - check API key")
            
            logger.info("⚠️  Using simulated response as fallback")
            return self._simulate_response(query)
    
    def extract_citations(
        self,
        response: Dict,
        query: str,
        brand_domain: str,
        competitors: List[str]
    ) -> CitationData:
        """
        Extract citation data from Perplexity response
        
        Args:
            response: API response
            query: Original query
            brand_domain: Brand domain to check
            competitors: Competitor domains
            
        Returns:
            CitationData object
        """
        try:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            citations = response.get("citations", [])
            content_lower = content.lower()
            
            logger.debug(f"Extracting citations for brand: {brand_domain}")
            logger.debug(f"Response has {len(citations)} source citations")
            
            # Check if brand is mentioned (flexible matching)
            # Match both "domain.com" and company name
            brand_name = brand_domain.split('.')[0]  # e.g., "acme" from "acme.com"
            brand_mentioned = (
                brand_domain.lower() in content_lower or
                brand_name.lower() in content_lower
            )
            
            logger.debug(f"Brand '{brand_domain}' mentioned: {brand_mentioned}")
            
            # Find position if mentioned
            citation_position = None
            if brand_mentioned:
                # Check in source citations
                for idx, citation in enumerate(citations):
                    if brand_domain.lower() in citation.lower() or brand_name.lower() in citation.lower():
                        citation_position = idx + 1
                        logger.debug(f"Found brand in citation position {citation_position}")
                        break
                
                # If not in citations, estimate position in text
                if not citation_position:
                    position_in_text = content_lower.find(brand_domain.lower())
                    if position_in_text == -1:
                        position_in_text = content_lower.find(brand_name.lower())
                    if position_in_text >= 0:
                        words_before = content_lower[:position_in_text].split()
                        citation_position = len(words_before) // 30 + 1
                        logger.debug(f"Estimated brand position from text: {citation_position}")
            
            # Check competitor mentions (flexible matching)
            competitors_mentioned = []
            for comp in competitors:
                comp_name = comp.split('.')[0]  # e.g., "hubspot" from "hubspot.com"
                if comp.lower() in content_lower or comp_name.lower() in content_lower:
                    competitors_mentioned.append(comp)
                    logger.debug(f"Found competitor: {comp}")
            
            logger.info(f"✅ Extraction complete: Brand={brand_mentioned}, Competitors={len(competitors_mentioned)}, Citations={len(citations)}")
            
            return CitationData(
                query=query,
                platform=Platform.PERPLEXITY,
                brand_mentioned=brand_mentioned,
                citation_position=citation_position,
                context=content[:500],
                competitors_mentioned=competitors_mentioned,
                raw_response=content
            )
            
        except Exception as e:
            print(f"Error extracting citations: {e}")
            return CitationData(
                query=query,
                platform=Platform.PERPLEXITY,
                brand_mentioned=False,
                raw_response=str(response)
            )
    
    def _simulate_response(self, query: str) -> Dict:
        """Simulate Perplexity response for demo purposes"""
        # This is a demo response when no API key is available
        simulated_responses = {
            "best ai productivity tools": {
                "choices": [{
                    "message": {
                        "content": "The best AI productivity tools include Notion AI for note-taking and organization, Asana for project management with AI features, and ClickUp for comprehensive task management. These tools leverage artificial intelligence to enhance workflow automation, smart scheduling, and intelligent task prioritization."
                    }
                }],
                "citations": [
                    "https://notion.so/product/ai",
                    "https://asana.com/ai",
                    "https://clickup.com/features/ai"
                ]
            },
            "best crm software": {
                "choices": [{
                    "message": {
                        "content": "Leading CRM software solutions include HubSpot CRM for its comprehensive free tier, Salesforce for enterprise-scale operations, and Pipedrive for sales-focused teams. These platforms offer contact management, pipeline tracking, and automation features."
                    }
                }],
                "citations": [
                    "https://hubspot.com/products/crm",
                    "https://salesforce.com",
                    "https://pipedrive.com"
                ]
            }
        }
        
        # Return simulated response or generic one
        return simulated_responses.get(
            query.lower(),
            {
                "choices": [{
                    "message": {
                        "content": f"Here are some options for '{query}': Various tools and platforms are available in this category, each with unique features and benefits."
                    }
                }],
                "citations": []
            }
        )


