"""Analyzer agent - analyzes visibility patterns"""

from typing import List, Dict, Any
from collections import defaultdict
from src.models.schemas import (
    CitationData, VisibilityScore, CompetitorComparison, Platform
)


class AnalyzerAgent:
    """Agent that analyzes visibility patterns"""
    
    def analyze_visibility(
        self,
        citations: List[CitationData],
        brand_domain: str,
        competitors: List[str]
    ) -> CompetitorComparison:
        """
        Analyze visibility from citations
        
        Args:
            citations: List of citation data
            brand_domain: Brand domain
            competitors: Competitor domains
            
        Returns:
            Competitor comparison analysis
        """
        # Calculate brand score
        brand_score = self._calculate_visibility_score(
            citations, brand_domain
        )
        
        # Calculate competitor scores
        competitor_scores = [
            self._calculate_visibility_score(citations, comp)
            for comp in competitors
        ]
        
        # Sort by mention rate
        competitor_scores.sort(key=lambda x: x.mention_rate, reverse=True)
        
        # Calculate visibility gap
        top_competitor_rate = competitor_scores[0].mention_rate if competitor_scores else 0
        visibility_gap = top_competitor_rate - brand_score.mention_rate
        
        return CompetitorComparison(
            brand_score=brand_score,
            competitor_scores=competitor_scores,
            visibility_gap=visibility_gap,
            top_competitor=competitor_scores[0].domain if competitor_scores else None
        )
    
    def _calculate_visibility_score(
        self,
        citations: List[CitationData],
        domain: str
    ) -> VisibilityScore:
        """
        Calculate visibility score for a domain
        
        Args:
            citations: List of citations
            domain: Domain to analyze
            
        Returns:
            VisibilityScore
        """
        total_citations = len(citations)
        mentions = 0
        positions = []
        platform_mentions = defaultdict(int)
        
        for citation in citations:
            # Check if this specific domain is mentioned in the response
            domain_lower = domain.lower()
            response_lower = citation.raw_response.lower() if citation.raw_response else ""
            
            is_mentioned = (
                domain_lower in response_lower or
                domain in citation.competitors_mentioned or
                (citation.brand_mentioned and domain_lower == citation.query.lower())
            )
            
            if is_mentioned:
                mentions += 1
                platform_mentions[citation.platform.value] += 1
                
                # Try to find position in response
                if domain_lower in response_lower:
                    # Calculate approximate position based on where domain appears
                    position_in_text = response_lower.find(domain_lower)
                    words_before = response_lower[:position_in_text].split()
                    estimated_position = len(words_before) // 50 + 1  # Rough estimate
                    positions.append(estimated_position)
                elif citation.citation_position:
                    positions.append(citation.citation_position)
        
        mention_rate = mentions / total_citations if total_citations > 0 else 0
        avg_position = sum(positions) / len(positions) if positions else None
        
        return VisibilityScore(
            domain=domain,
            total_mentions=mentions,
            mention_rate=mention_rate,
            avg_position=avg_position,
            platforms=dict(platform_mentions)
        )
    
    def extract_patterns(
        self,
        citations: List[CitationData],
        comparison: CompetitorComparison
    ) -> Dict[str, Any]:
        """
        Extract patterns from citations
        
        Args:
            citations: Citation data
            comparison: Competitor comparison
            
        Returns:
            Pattern analysis
        """
        patterns = {
            "platform_bias": self._analyze_platform_bias(citations),
            "position_patterns": self._analyze_positions(citations),
            "context_patterns": self._analyze_contexts(citations),
            "competitor_strengths": self._analyze_competitor_strengths(comparison)
        }
        
        return patterns
    
    def _analyze_platform_bias(self, citations: List[CitationData]) -> Dict[str, float]:
        """Analyze if certain platforms favor certain domains"""
        platform_stats = defaultdict(lambda: {"total": 0, "mentions": 0})
        
        for citation in citations:
            platform = citation.platform.value
            platform_stats[platform]["total"] += 1
            if citation.brand_mentioned:
                platform_stats[platform]["mentions"] += 1
        
        return {
            platform: stats["mentions"] / stats["total"] if stats["total"] > 0 else 0
            for platform, stats in platform_stats.items()
        }
    
    def _analyze_positions(self, citations: List[CitationData]) -> Dict[str, Any]:
        """Analyze citation positions"""
        positions = [c.citation_position for c in citations if c.citation_position]
        
        if not positions:
            return {"average": None, "best": None, "worst": None}
        
        return {
            "average": sum(positions) / len(positions),
            "best": min(positions),
            "worst": max(positions),
            "distribution": {
                "top_3": sum(1 for p in positions if p <= 3),
                "top_5": sum(1 for p in positions if p <= 5),
                "beyond_5": sum(1 for p in positions if p > 5)
            }
        }
    
    def _analyze_contexts(self, citations: List[CitationData]) -> List[str]:
        """Extract common contexts where brand appears"""
        contexts = []
        
        for citation in citations:
            if citation.brand_mentioned and citation.context:
                contexts.append(citation.context)
        
        return contexts
    
    def _analyze_competitor_strengths(
        self,
        comparison: CompetitorComparison
    ) -> List[Dict[str, Any]]:
        """Analyze what makes competitors successful"""
        strengths = []
        
        for comp_score in comparison.competitor_scores:
            if comp_score.mention_rate > comparison.brand_score.mention_rate:
                strength = {
                    "competitor": comp_score.domain,
                    "mention_advantage": comp_score.mention_rate - comparison.brand_score.mention_rate,
                    "strong_platforms": [
                        platform for platform, count in comp_score.platforms.items()
                        if count > 0
                    ]
                }
                strengths.append(strength)
        
        return strengths



