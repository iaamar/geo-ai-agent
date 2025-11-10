"""Recommender agent - generates actionable recommendations"""

from typing import List, Dict, Any
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.config import settings
from src.models.schemas import Recommendation, Hypothesis, CompetitorComparison
import json

logger = logging.getLogger(__name__)


class RecommenderAgent:
    """Agent that creates actionable recommendations"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.default_model,
            temperature=0.7,
            api_key=settings.openai_api_key
        )
        
        self.recommendation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a GEO optimization strategist who creates actionable 
            recommendations to improve brand visibility in AI-generated answers.
            
            Generate 5-7 specific, actionable recommendations based on the analysis.
            
            For each recommendation:
            1. Clear, actionable title
            2. Detailed description
            3. Priority (high/medium/low)
            4. Impact score (0-10): Expected improvement in visibility
            5. Effort score (0-10): Implementation complexity
            6. 3-5 specific action items
            7. Expected outcome
            
            Focus on:
            - Content optimization
            - Semantic SEO
            - Structured data
            - Authority building
            - Platform-specific strategies
            
            Format as JSON array with keys: title, description, priority, impact_score, 
            effort_score, action_items, expected_outcome"""),
            ("user", """Based on this GEO analysis:

Query: {query}
Brand: {brand}
Current Visibility: {visibility_rate}%

Hypotheses:
{hypotheses}

Competitor Insights:
{competitor_insights}

Generate prioritized recommendations to improve GEO visibility.""")
        ])
    
    async def generate_recommendations(
        self,
        query: str,
        comparison: CompetitorComparison,
        hypotheses: List[Hypothesis],
        patterns: Dict[str, Any]
    ) -> List[Recommendation]:
        """
        Generate recommendations
        
        Args:
            query: Original query
            comparison: Competitor comparison
            hypotheses: Generated hypotheses
            patterns: Pattern analysis
            
        Returns:
            List of recommendations
        """
        # Format hypotheses
        hypotheses_str = "\n".join([
            f"- {h.title}: {h.explanation} (Confidence: {h.confidence})"
            for h in hypotheses
        ])
        
        # Format competitor insights
        competitor_insights = self._format_competitor_insights(comparison, patterns)
        
        chain = self.recommendation_prompt | self.llm
        
        try:
            response = await chain.ainvoke({
                "query": query,
                "brand": comparison.brand_score.domain,
                "visibility_rate": f"{comparison.brand_score.mention_rate * 100:.1f}",
                "hypotheses": hypotheses_str,
                "competitor_insights": competitor_insights
            })
            
            content = response.content
            
            logger.info("="*60)
            logger.info("✨ RECOMMENDER LLM OUTPUT:")
            logger.info("-"*60)
            logger.info(content[:800] + "..." if len(content) > 800 else content)
            logger.info("="*60)
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            recommendations_data = json.loads(content.strip())
            
            logger.info(f"✅ Parsing {len(recommendations_data)} recommendations from LLM")
            
            # Convert to Recommendation objects
            recommendations = [
                Recommendation(
                    title=r["title"],
                    description=r["description"],
                    priority=r["priority"].lower(),  # Ensure lowercase
                    impact_score=float(r["impact_score"]),
                    effort_score=float(r["effort_score"]),
                    action_items=r["action_items"],
                    expected_outcome=r["expected_outcome"]
                )
                for r in recommendations_data
            ]
            
            for i, rec in enumerate(recommendations, 1):
                logger.info(f"   {i}. {rec.title} | Priority: {rec.priority} | Impact: {rec.impact_score}/10")
            
            # Sort by impact/effort ratio
            recommendations.sort(
                key=lambda r: r.impact_score / max(r.effort_score, 1),
                reverse=True
            )
            
            return recommendations
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return self._generate_fallback_recommendations(comparison, hypotheses)
    
    def _format_competitor_insights(
        self,
        comparison: CompetitorComparison,
        patterns: Dict[str, Any]
    ) -> str:
        """Format competitor insights for prompt"""
        insights = []
        
        for comp in comparison.competitor_scores[:3]:
            insight = f"{comp.domain}: {comp.mention_rate*100:.1f}% visibility"
            if comp.platforms:
                platforms = ", ".join(comp.platforms.keys())
                insight += f" (Strong on: {platforms})"
            insights.append(insight)
        
        # Add pattern insights
        if patterns.get("competitor_strengths"):
            for strength in patterns["competitor_strengths"][:2]:
                insights.append(
                    f"{strength['competitor']}: {strength['mention_advantage']*100:.1f}% advantage"
                )
        
        return "\n".join(insights)
    
    def _generate_fallback_recommendations(
        self,
        comparison: CompetitorComparison,
        hypotheses: List[Hypothesis]
    ) -> List[Recommendation]:
        """Generate basic recommendations when LLM fails"""
        recommendations = []
        
        # Recommendation 1: Content optimization
        recommendations.append(Recommendation(
            title="Optimize Content for AI Semantic Understanding",
            description="Improve content structure and semantic clarity to help AI models better understand and cite your brand.",
            priority="high",
            impact_score=8.5,
            effort_score=6.0,
            action_items=[
                "Add clear, structured FAQ sections addressing common queries",
                "Use schema.org markup for better structured data",
                "Include explicit product/service descriptions with key benefits",
                "Create comprehensive comparison pages vs competitors"
            ],
            expected_outcome="20-30% improvement in AI citation rate within 2-3 months"
        ))
        
        # Recommendation 2: Authority building
        if comparison.visibility_gap > 0.3:
            recommendations.append(Recommendation(
                title="Build Domain Authority and Trust Signals",
                description="Increase domain credibility through authoritative content and external validation.",
                priority="high",
                impact_score=7.5,
                effort_score=8.0,
                action_items=[
                    "Publish thought leadership content on industry topics",
                    "Earn backlinks from authoritative sources",
                    "Get featured in industry publications",
                    "Maintain active presence on relevant platforms"
                ],
                expected_outcome="Improved trust signals leading to higher AI citation rates"
            ))
        
        # Recommendation 3: Keyword optimization
        recommendations.append(Recommendation(
            title="Enhance Semantic Keyword Targeting",
            description=f"Optimize content for variations of '{comparison.brand_score.domain}' related queries.",
            priority="medium",
            impact_score=7.0,
            effort_score=4.0,
            action_items=[
                "Research and target semantic keyword variations",
                "Create content clusters around core topics",
                "Use natural language that matches query intent",
                "Include question-answer format content"
            ],
            expected_outcome="15-25% increase in relevant query coverage"
        ))
        
        # Recommendation 4: Fresh content
        recommendations.append(Recommendation(
            title="Maintain Content Freshness",
            description="Keep content updated to ensure AI models access recent, relevant information.",
            priority="medium",
            impact_score=6.5,
            effort_score=5.0,
            action_items=[
                "Update key pages quarterly",
                "Add publication/update dates prominently",
                "Create timely, relevant content regularly",
                "Monitor and update outdated information"
            ],
            expected_outcome="Better recency signals for AI platforms"
        ))
        
        # Recommendation 5: Platform-specific optimization
        recommendations.append(Recommendation(
            title="Implement Platform-Specific Strategies",
            description="Tailor content for different AI platforms based on their preferences.",
            priority="low",
            impact_score=5.5,
            effort_score=7.0,
            action_items=[
                "Analyze top-cited sources on each platform",
                "Optimize for Perplexity's citation format",
                "Structure content for ChatGPT's context window",
                "Test content performance across platforms"
            ],
            expected_outcome="Improved platform-specific visibility"
        ))
        
        return recommendations


