"""Planner agent - orchestrates the analysis workflow"""

from typing import Dict, List, Any
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.config import settings
from src.models.schemas import AnalysisRequest, Platform

logger = logging.getLogger(__name__)


class PlannerAgent:
    """Agent that plans the investigation strategy"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.default_model,
            temperature=0.3,  # Lower temperature for planning
            api_key=settings.openai_api_key
        )
        
        self.planning_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a strategic planner for GEO (Generative Engine Optimization) analysis.
            Your job is to create a detailed investigation plan based on the user's query.
            
            Consider:
            1. What data sources to query (ChatGPT, Perplexity, etc.)
            2. What queries/variations to test
            3. What metrics to track
            4. What comparisons to make
            5. What hypotheses to test
            
            Be specific and actionable."""),
            ("user", "Create an analysis plan for: {query}\nBrand: {brand}\nCompetitors: {competitors}\nPlatforms: {platforms}")
        ])
    
    async def create_plan(self, request: AnalysisRequest) -> Dict[str, Any]:
        """
        Create analysis plan
        
        Args:
            request: Analysis request
            
        Returns:
            Structured plan with steps
        """
        chain = self.planning_prompt | self.llm
        
        response = await chain.ainvoke({
            "query": request.query,
            "brand": request.brand_domain,
            "competitors": ", ".join(request.competitors),
            "platforms": ", ".join([p.value for p in request.platforms])
        })
        
        logger.info("="*60)
        logger.info("📋 PLANNER LLM OUTPUT:")
        logger.info("-"*60)
        logger.info(response.content[:500] + "..." if len(response.content) > 500 else response.content)
        logger.info("="*60)
        
        # Parse response into structured plan
        plan = {
            "original_query": request.query,
            "query_variations": self._generate_query_variations(request.query),
            "platforms": request.platforms,
            "brand": request.brand_domain,
            "competitors": request.competitors,
            "num_queries": request.num_queries,
            "steps": [
                "collect_visibility_data",
                "analyze_patterns",
                "generate_hypotheses",
                "create_recommendations"
            ],
            "reasoning": response.content
        }
        
        logger.info(f"📊 Plan generated: {len(plan['query_variations'])} variations, {len(plan['platforms'])} platforms")
        
        return plan
    
    def _generate_query_variations(self, query: str) -> List[str]:
        """
        Generate variations of the query
        
        Args:
            query: Original query
            
        Returns:
            List of query variations
        """
        variations = [query]
        
        # Add "best" prefix if not present
        if not query.lower().startswith("best"):
            variations.append(f"best {query}")
        
        # Add "top" variation
        if not query.lower().startswith("top"):
            variations.append(f"top {query}")
        
        # Add comparison variation
        variations.append(f"{query} comparison")
        
        # Add "for businesses" variation
        variations.append(f"{query} for businesses")
        
        return variations[:5]  # Limit to 5 variations



