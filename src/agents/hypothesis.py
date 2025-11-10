"""Hypothesis generator agent - explains visibility patterns"""

from typing import List, Dict, Any
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.config import settings
from src.models.schemas import Hypothesis, CompetitorComparison
import json

logger = logging.getLogger(__name__)


class HypothesisAgent:
    """Agent that generates hypotheses explaining visibility patterns"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.default_model,
            temperature=0.7,
            api_key=settings.openai_api_key
        )
        
        self.hypothesis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert GEO analyst who explains why brands 
            appear or don't appear in AI-generated answers.
            
            Generate 3-5 clear hypotheses explaining the visibility patterns.
            Consider:
            - Content quality and relevance
            - Semantic alignment with query intent
            - Domain authority and trust signals
            - Freshness and recency of content
            - Keyword optimization
            - Structured data and citations
            
            For each hypothesis:
            1. Provide a clear title
            2. Explain the reasoning
            3. Estimate confidence (0-1)
            4. List supporting evidence
            
            Format as JSON array of objects with keys: title, explanation, confidence, supporting_evidence"""),
            ("user", """Analyze this GEO visibility data:
            
Query: {query}
Brand: {brand} (Mention Rate: {brand_rate}%)
Top Competitor: {top_competitor} (Mention Rate: {competitor_rate}%)
Visibility Gap: {gap}%

Platform Performance:
{platform_data}

Patterns Observed:
{patterns}

Generate hypotheses explaining these patterns.""")
        ])
    
    async def generate_hypotheses(
        self,
        query: str,
        comparison: CompetitorComparison,
        patterns: Dict[str, Any]
    ) -> List[Hypothesis]:
        """
        Generate hypotheses explaining visibility patterns
        
        Args:
            query: Original query
            comparison: Competitor comparison data
            patterns: Pattern analysis
            
        Returns:
            List of hypotheses
        """
        brand_rate = comparison.brand_score.mention_rate * 100
        
        top_comp_rate = 0
        top_comp_name = "N/A"
        if comparison.competitor_scores:
            top_comp_rate = comparison.competitor_scores[0].mention_rate * 100
            top_comp_name = comparison.competitor_scores[0].domain
        
        gap = comparison.visibility_gap * 100
        
        # Format platform data
        platform_data = json.dumps(comparison.brand_score.platforms, indent=2)
        patterns_str = json.dumps(patterns, indent=2, default=str)
        
        chain = self.hypothesis_prompt | self.llm
        
        try:
            response = await chain.ainvoke({
                "query": query,
                "brand": comparison.brand_score.domain,
                "brand_rate": f"{brand_rate:.1f}",
                "top_competitor": top_comp_name,
                "competitor_rate": f"{top_comp_rate:.1f}",
                "gap": f"{gap:.1f}",
                "platform_data": platform_data,
                "patterns": patterns_str
            })
            
            # Parse JSON response
            content = response.content
            
            logger.info("="*60)
            logger.info("💡 HYPOTHESIS LLM OUTPUT:")
            logger.info("-"*60)
            logger.info(content[:800] + "..." if len(content) > 800 else content)
            logger.info("="*60)
            
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            hypotheses_data = json.loads(content.strip())
            
            # Convert to Hypothesis objects
            hypotheses = [
                Hypothesis(
                    title=h["title"],
                    explanation=h["explanation"],
                    confidence=h["confidence"],
                    supporting_evidence=h["supporting_evidence"]
                )
                for h in hypotheses_data
            ]
            
            logger.info(f"✅ Parsed {len(hypotheses)} hypotheses from LLM")
            
            return hypotheses
            
        except Exception as e:
            print(f"Error generating hypotheses: {e}")
            # Return fallback hypotheses
            return self._generate_fallback_hypotheses(comparison, patterns)
    
    def _generate_fallback_hypotheses(
        self,
        comparison: CompetitorComparison,
        patterns: Dict[str, Any]
    ) -> List[Hypothesis]:
        """Generate basic hypotheses when LLM fails"""
        hypotheses = []
        
        # Hypothesis 1: Low visibility
        if comparison.brand_score.mention_rate < 0.3:
            hypotheses.append(Hypothesis(
                title="Low Brand Visibility in AI Responses",
                explanation=f"The brand {comparison.brand_score.domain} appears in only {comparison.brand_score.mention_rate*100:.0f}% of responses, indicating limited recognition by AI models.",
                confidence=0.9,
                supporting_evidence=[
                    f"Mention rate: {comparison.brand_score.mention_rate*100:.0f}%",
                    f"Visibility gap vs top competitor: {comparison.visibility_gap*100:.0f}%"
                ]
            ))
        
        # Hypothesis 2: Competitor advantage
        if comparison.competitor_scores and comparison.visibility_gap > 0.2:
            top_comp = comparison.competitor_scores[0]
            hypotheses.append(Hypothesis(
                title="Strong Competitor Presence",
                explanation=f"{top_comp.domain} has significantly higher visibility, suggesting better content optimization or domain authority.",
                confidence=0.85,
                supporting_evidence=[
                    f"{top_comp.domain} mention rate: {top_comp.mention_rate*100:.0f}%",
                    f"Appears on {len(top_comp.platforms)} platforms"
                ]
            ))
        
        # Hypothesis 3: Platform-specific issues
        platform_bias = patterns.get("platform_bias", {})
        if platform_bias:
            hypotheses.append(Hypothesis(
                title="Platform-Specific Performance Variation",
                explanation="Visibility varies significantly across different AI platforms, suggesting platform-specific optimization opportunities.",
                confidence=0.75,
                supporting_evidence=[
                    f"Platform performance: {platform_bias}"
                ]
            ))
        
        return hypotheses if hypotheses else [
            Hypothesis(
                title="Insufficient Data",
                explanation="Unable to generate detailed hypotheses with current data.",
                confidence=0.5,
                supporting_evidence=["Limited citation data available"]
            )
        ]



