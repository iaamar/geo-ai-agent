"""OpenAI API client for ChatGPT analysis"""

import logging
from openai import AsyncOpenAI
from typing import List, Dict, Optional
from src.config import settings
from src.models.schemas import CitationData, Platform

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Client for OpenAI ChatGPT API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = AsyncOpenAI(api_key=api_key or settings.openai_api_key)
        self.model = settings.default_model
        
    async def search(self, query: str, context: Optional[str] = None) -> str:
        """
        Query ChatGPT with web search capabilities
        
        Args:
            query: Search query
            context: Additional context for the query
            
        Returns:
            ChatGPT response content
        """
        system_prompt = """You are a helpful assistant that provides comprehensive answers 
        about products, tools, and services. When answering, mention specific brands, 
        websites, and tools that are relevant. Include URLs when possible."""
        
        if context:
            system_prompt += f"\n\nAdditional context: {context}"
        
        try:
            logger.info(f"💬 Querying ChatGPT: '{query}'")
            logger.debug(f"   Model: {self.model}")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            logger.info("="*60)
            logger.info(f"💬 CHATGPT RESPONSE for '{query}':")
            logger.info("-"*60)
            logger.info(content[:500] + "..." if len(content) > 500 else content)
            logger.info("="*60)
            
            return content
            
        except Exception as e:
            logger.error(f"❌ OpenAI API error: {e}")
            return ""
    
    async def analyze_with_reasoning(self, prompt: str) -> str:
        """
        Use ChatGPT for reasoning and analysis
        
        Args:
            prompt: Analysis prompt
            
        Returns:
            Reasoning output
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in digital marketing and SEO/GEO analysis."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.temperature,
                max_tokens=settings.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI reasoning error: {e}")
            return ""
    
    def extract_citations(
        self,
        response: str,
        query: str,
        brand_domain: str,
        competitors: List[str]
    ) -> CitationData:
        """
        Extract citation data from ChatGPT response
        
        Args:
            response: ChatGPT response content
            query: Original query
            brand_domain: Brand domain to check
            competitors: Competitor domains
            
        Returns:
            CitationData object
        """
        content = response.lower()
        
        # Check if brand is mentioned
        brand_mentioned = brand_domain.lower() in content
        
        # Try to find position (approximate based on text position)
        citation_position = None
        if brand_mentioned:
            position = content.find(brand_domain.lower())
            # Estimate position based on character location
            words_before = content[:position].split()
            citation_position = len(words_before) // 20 + 1  # Approximate paragraph
        
        # Check competitor mentions
        competitors_mentioned = [
            comp for comp in competitors
            if comp.lower() in content
        ]
        
        return CitationData(
            query=query,
            platform=Platform.CHATGPT,
            brand_mentioned=brand_mentioned,
            citation_position=citation_position,
            context=response[:500],
            competitors_mentioned=competitors_mentioned,
            raw_response=response
        )
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embeddings for semantic analysis
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            response = await self.client.embeddings.create(
                model=settings.embedding_model,
                input=text
            )
            return response.data[0].embedding
            
        except Exception as e:
            print(f"Embedding generation error: {e}")
            return []



