"""Main orchestrator using LangGraph for multi-agent coordination"""

from typing import Dict, Any, List
from datetime import datetime
import uuid
import asyncio
import logging
import time

from src.models.schemas import (
    AnalysisRequest, AnalysisResult, CitationData
)
from src.agents.planner import PlannerAgent
from src.agents.analyzer import AnalyzerAgent
from src.agents.hypothesis import HypothesisAgent
from src.agents.recommender import RecommenderAgent
from src.data.openai_client import OpenAIClient
from src.data.perplexity import PerplexityClient

logger = logging.getLogger(__name__)


class GEOOrchestrator:
    """
    Main orchestrator for GEO analysis workflow
    
    This implements a LangGraph-style multi-agent system:
    1. Planner creates investigation strategy
    2. Data collectors fetch visibility data
    3. Analyzer processes patterns
    4. Hypothesis generator explains findings
    5. Recommender creates action plan
    """
    
    def __init__(self):
        self.planner = PlannerAgent()
        self.analyzer = AnalyzerAgent()
        self.hypothesis_agent = HypothesisAgent()
        self.recommender = RecommenderAgent()
        self.openai_client = OpenAIClient()
        self.perplexity_client = PerplexityClient()
    
    async def run_analysis(self, request: AnalysisRequest) -> AnalysisResult:
        """
        Run complete GEO analysis workflow
        
        Args:
            request: Analysis request
            
        Returns:
            Complete analysis result
        """
        analysis_id = str(uuid.uuid4())
        start_time = time.time()
        
        logger.info("="*80)
        logger.info(f"STARTING GEO ANALYSIS | ID: {analysis_id}")
        logger.info(f"Query: '{request.query}'")
        logger.info(f"Brand: {request.brand_domain}")
        logger.info(f"Competitors: {', '.join(request.competitors)}")
        logger.info(f"Platforms: {', '.join([p.value for p in request.platforms])}")
        logger.info("="*80)
        
        # Step 1: Planning
        step_start = time.time()
        logger.info(f"[{analysis_id}] STEP 1/6: Creating analysis plan...")
        plan = await self.planner.create_plan(request)
        logger.info(f"[{analysis_id}] ✓ Plan created in {time.time() - step_start:.2f}s")
        logger.debug(f"[{analysis_id}] Plan details: {plan}")
        
        # Step 2: Data Collection
        step_start = time.time()
        logger.info(f"[{analysis_id}] STEP 2/6: Collecting visibility data...")
        logger.info(f"[{analysis_id}] - Testing {len(plan['query_variations'])} query variations")
        logger.info(f"[{analysis_id}] - Querying {len(plan['platforms'])} platforms")
        citations = await self._collect_visibility_data(plan)
        logger.info(f"[{analysis_id}] ✓ Collected {len(citations)} citations in {time.time() - step_start:.2f}s")
        
        # Step 3: Analysis
        step_start = time.time()
        logger.info(f"[{analysis_id}] STEP 3/6: Analyzing visibility patterns...")
        comparison = self.analyzer.analyze_visibility(
            citations,
            request.brand_domain,
            request.competitors
        )
        patterns = self.analyzer.extract_patterns(citations, comparison)
        logger.info(f"[{analysis_id}] ✓ Analysis complete in {time.time() - step_start:.2f}s")
        logger.info(f"[{analysis_id}] - Brand visibility: {comparison.brand_score.mention_rate*100:.1f}%")
        logger.info(f"[{analysis_id}] - Patterns identified: {len(patterns)}")
        
        # Step 4: Hypothesis Generation
        step_start = time.time()
        logger.info(f"[{analysis_id}] STEP 4/6: Generating hypotheses...")
        hypotheses = await self.hypothesis_agent.generate_hypotheses(
            request.query,
            comparison,
            patterns
        )
        logger.info(f"[{analysis_id}] ✓ Generated {len(hypotheses)} hypotheses in {time.time() - step_start:.2f}s")
        for i, h in enumerate(hypotheses[:3], 1):
            logger.info(f"[{analysis_id}]   {i}. {h.title} (confidence: {h.confidence*100:.0f}%)")
        
        # Step 5: Recommendations
        step_start = time.time()
        logger.info(f"[{analysis_id}] STEP 5/6: Creating recommendations...")
        recommendations = await self.recommender.generate_recommendations(
            request.query,
            comparison,
            hypotheses,
            patterns
        )
        logger.info(f"[{analysis_id}] ✓ Generated {len(recommendations)} recommendations in {time.time() - step_start:.2f}s")
        for i, rec in enumerate(recommendations[:3], 1):
            logger.info(f"[{analysis_id}]   {i}. {rec.title} (priority: {rec.priority}, impact: {rec.impact_score:.1f}/10)")
        
        # Step 6: Generate Summary
        step_start = time.time()
        logger.info(f"[{analysis_id}] STEP 6/6: Generating executive summary...")
        summary = self._generate_summary(request, comparison, hypotheses)
        logger.info(f"[{analysis_id}] ✓ Summary generated in {time.time() - step_start:.2f}s")
        
        total_time = time.time() - start_time
        logger.info("="*80)
        logger.info(f"ANALYSIS COMPLETE | ID: {analysis_id}")
        logger.info(f"Total execution time: {total_time:.2f}s")
        logger.info(f"Citations collected: {len(citations)}")
        logger.info(f"Hypotheses generated: {len(hypotheses)}")
        logger.info(f"Recommendations created: {len(recommendations)}")
        logger.info("="*80)
        
        return AnalysisResult(
            id=analysis_id,
            timestamp=datetime.now(),
            request=request,
            citations=citations,
            visibility_scores=comparison,
            hypotheses=hypotheses,
            recommendations=recommendations,
            summary=summary
        )
    
    async def _collect_visibility_data(self, plan: Dict[str, Any]) -> List[CitationData]:
        """
        Collect visibility data from AI platforms
        
        Args:
            plan: Analysis plan
            
        Returns:
            List of citation data
        """
        citations = []
        
        queries_to_test = plan["query_variations"][:plan["num_queries"]]
        
        logger.debug(f"Collecting data for {len(queries_to_test)} queries across {len(plan['platforms'])} platforms")
        
        # Collect data from each platform
        tasks = []
        
        for query in queries_to_test:
            for platform in plan["platforms"]:
                if platform.value == "chatgpt":
                    logger.debug(f"Queuing ChatGPT query: '{query}'")
                    tasks.append(self._query_chatgpt(
                        query,
                        plan["brand"],
                        plan["competitors"]
                    ))
                elif platform.value == "perplexity":
                    logger.debug(f"Queuing Perplexity query: '{query}'")
                    tasks.append(self._query_perplexity(
                        query,
                        plan["brand"],
                        plan["competitors"]
                    ))
        
        logger.info(f"Executing {len(tasks)} concurrent queries...")
        
        # Execute all queries concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log errors
        successful = 0
        failed = 0
        for r in results:
            if isinstance(r, CitationData):
                citations.append(r)
                successful += 1
            else:
                failed += 1
                if isinstance(r, Exception):
                    logger.warning(f"Query failed: {str(r)}")
        
        logger.info(f"Query results: {successful} successful, {failed} failed")
        
        return citations
    
    async def _query_chatgpt(
        self,
        query: str,
        brand: str,
        competitors: List[str]
    ) -> CitationData:
        """Query ChatGPT and extract citations"""
        logger.debug(f"Querying ChatGPT: '{query}'")
        start = time.time()
        try:
            response = await self.openai_client.search(query)
            citation_data = self.openai_client.extract_citations(
                response,
                query,
                brand,
                competitors
            )
            logger.debug(f"ChatGPT query completed in {time.time()-start:.2f}s")
            return citation_data
        except Exception as e:
            logger.error(f"ChatGPT query failed for '{query}': {str(e)}")
            raise
    
    async def _query_perplexity(
        self,
        query: str,
        brand: str,
        competitors: List[str]
    ) -> CitationData:
        """Query Perplexity and extract citations"""
        logger.debug(f"Querying Perplexity: '{query}'")
        start = time.time()
        try:
            response = await self.perplexity_client.search(query)
            citation_data = self.perplexity_client.extract_citations(
                response,
                query,
                brand,
                competitors
            )
            logger.debug(f"Perplexity query completed in {time.time()-start:.2f}s")
            return citation_data
        except Exception as e:
            logger.error(f"Perplexity query failed for '{query}': {str(e)}")
            raise
    
    def _generate_summary(
        self,
        request: AnalysisRequest,
        comparison,
        hypotheses
    ) -> str:
        """Generate executive summary"""
        brand_rate = comparison.brand_score.mention_rate * 100
        
        top_comp = "N/A"
        top_comp_rate = 0
        if comparison.competitor_scores:
            top_comp = comparison.competitor_scores[0].domain
            top_comp_rate = comparison.competitor_scores[0].mention_rate * 100
        
        summary = f"""
GEO Analysis Summary for "{request.query}"

Brand Performance:
- {request.brand_domain}: {brand_rate:.1f}% visibility rate
- Mentioned in {comparison.brand_score.total_mentions} out of {len(request.platforms)} platform queries

Competitive Landscape:
- Top competitor: {top_comp} ({top_comp_rate:.1f}% visibility)
- Visibility gap: {comparison.visibility_gap * 100:.1f} percentage points

Key Findings:
{self._format_hypotheses_summary(hypotheses)}

Recommended Actions:
Focus on high-impact, low-effort improvements first. Top priority items have been 
identified to maximize visibility improvements with efficient resource allocation.
        """.strip()
        
        return summary
    
    def _format_hypotheses_summary(self, hypotheses) -> str:
        """Format hypotheses for summary"""
        if not hypotheses:
            return "- No significant patterns identified"
        
        return "\n".join([
            f"- {h.title} (Confidence: {h.confidence*100:.0f}%)"
            for h in hypotheses[:3]
        ])


