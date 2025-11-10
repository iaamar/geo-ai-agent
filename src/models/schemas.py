"""Pydantic models for API and data structures"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Any
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    """Supported AI platforms"""
    CHATGPT = "chatgpt"
    PERPLEXITY = "perplexity"
    CLAUDE = "claude"
    GOOGLE_AI = "google_ai"


class AnalysisRequest(BaseModel):
    """Request model for visibility analysis"""
    query: str = Field(..., description="The search query to analyze")
    brand_domain: str = Field(..., description="Your brand's domain to track")
    competitors: List[str] = Field(default_factory=list, description="Competitor domains")
    platforms: List[Platform] = Field(
        default=[Platform.CHATGPT, Platform.PERPLEXITY],
        description="Platforms to analyze"
    )
    num_queries: int = Field(default=10, description="Number of queries to test")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "best AI productivity tools",
                "brand_domain": "acme.com",
                "competitors": ["notion.so", "asana.com"],
                "platforms": ["chatgpt", "perplexity"],
                "num_queries": 10
            }
        }


class CitationData(BaseModel):
    """Citation data for a specific query"""
    query: str
    platform: Platform
    brand_mentioned: bool
    citation_position: Optional[int] = None
    context: Optional[str] = None
    competitors_mentioned: List[str] = Field(default_factory=list)
    raw_response: str


class VisibilityScore(BaseModel):
    """Visibility metrics for a domain"""
    domain: str
    total_mentions: int
    mention_rate: float
    avg_position: Optional[float] = None
    platforms: Dict[str, int]
    
    
class CompetitorComparison(BaseModel):
    """Comparison between brand and competitors"""
    brand_score: VisibilityScore
    competitor_scores: List[VisibilityScore]
    visibility_gap: float
    top_competitor: Optional[str] = None


class Hypothesis(BaseModel):
    """Hypothesis explaining visibility patterns"""
    title: str
    explanation: str
    confidence: float = Field(ge=0.0, le=1.0)
    supporting_evidence: List[str]
    

class Recommendation(BaseModel):
    """Actionable recommendation"""
    title: str
    description: str
    priority: Literal["high", "medium", "low"]
    impact_score: float = Field(ge=0.0, le=10.0)
    effort_score: float = Field(ge=0.0, le=10.0)
    action_items: List[str]
    expected_outcome: str


class AnalysisResult(BaseModel):
    """Complete analysis result with transparency data"""
    id: str
    timestamp: datetime
    request: AnalysisRequest
    citations: List[CitationData]
    visibility_scores: CompetitorComparison
    hypotheses: List[Hypothesis]
    recommendations: List[Recommendation]
    summary: str
    
    # Transparency & Reasoning Fields
    reasoning_trace: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Step-by-step reasoning process of each agent"
    )
    component_info: Dict[str, Any] = Field(
        default_factory=dict,
        description="Detailed information about system components"
    )
    data_flow: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Data flow between components"
    )
    step_timings: Dict[str, float] = Field(
        default_factory=dict,
        description="Execution time for each step"
    )
    errors: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Any errors encountered during analysis"
    )
    evaluation_metrics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Self-critique evaluation results and quality scores"
    )
    
    
class CompareRequest(BaseModel):
    """Request for comparing multiple brands"""
    query: str
    domains: List[str] = Field(..., min_length=2, max_length=5)
    platforms: List[Platform] = Field(default=[Platform.CHATGPT, Platform.PERPLEXITY])
    

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, bool]



