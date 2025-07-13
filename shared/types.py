"""Type definitions for the SSFF framework using TypedDict."""
from typing import TypedDict, Optional, Literal
from datetime import datetime


class ProgressDict(TypedDict):
    """Track the progress of analysis."""
    current_step: str
    completed_steps: list[str]
    start_time: datetime
    step_times: dict[str, dict[str, datetime]]
    status: Literal["running", "completed", "error"]
    error_message: Optional[str]


class StartupInfo(TypedDict):
    """Parsed startup information."""
    name: str
    description: str
    market_size: Optional[str]
    growth_rate: Optional[str]
    competition: Optional[str]
    market_trends: Optional[str]
    go_to_market_strategy: Optional[str]
    product_details: Optional[str]
    technology_stack: Optional[str]
    scalability: Optional[str]
    user_feedback: Optional[str]
    product_fit: Optional[str]
    founder_backgrounds: Optional[str]
    track_records: Optional[str]
    leadership_skills: Optional[str]
    vision_alignment: Optional[str]
    team_dynamics: Optional[str]
    web_traffic_growth: Optional[str]
    social_media_presence: Optional[str]
    investment_rounds: Optional[str]
    regulatory_approvals: Optional[str]
    patents: Optional[str]


class StartupCategorizationDict(TypedDict):
    """Startup categorization results."""
    industry_growth: str
    market_size: str
    development_pace: str
    market_adaptability: str
    execution_capabilities: str
    funding_amount: str
    valuation_change: str
    investor_backing: str
    reviews_testimonials: str
    product_market_fit: str
    sentiment_analysis: str
    innovation_mentions: str
    cutting_edge_technology: str
    timing: str


class StartupEvaluationDict(TypedDict):
    """VC Scout evaluation results."""
    market_opportunity: str
    product_innovation: str
    founding_team: str
    potential_risks: str
    overall_potential: int
    investment_recommendation: str
    confidence: float
    rationale: str


class VCScoutAnalysisDict(TypedDict):
    """Complete VC Scout analysis results."""
    startup_info: StartupInfo
    categorization: StartupCategorizationDict
    evaluation: StartupEvaluationDict


class MarketAnalysisDict(TypedDict):
    """Market analysis results."""
    market_size: str
    growth_rate: str
    competition: str
    market_trends: str
    viability_score: int


class ProductAnalysisDict(TypedDict):
    """Product analysis results."""
    features_analysis: str
    tech_stack_evaluation: str
    usp_assessment: str
    potential_score: int
    innovation_score: int
    market_fit_score: int


class FounderAnalysisDict(TypedDict):
    """Founder analysis results."""
    competency_score: int
    analysis: str


class AdvancedFounderAnalysisDict(FounderAnalysisDict):
    """Advanced founder analysis with segmentation."""
    segmentation: int
    cosine_similarity: float
    idea_fit: float


class IntegratedAnalysisDict(TypedDict):
    """Integrated analysis results."""
    overall_score: float
    IntegratedAnalysis: str
    recommendation: str
    outcome: str


class QuantitativeDecisionDict(TypedDict):
    """Quantitative decision results."""
    outcome: str
    probability: float
    reasoning: str
