from pydantic import BaseModel, Field
from typing import Optional


class StartupInfo(BaseModel):
    name: str = Field(..., description="Official name of the startup")
    description: str = Field(..., description="Brief overview of what the startup does")
    market_size: Optional[str] = Field(None, description="Size of the market the startup is targeting")
    growth_rate: Optional[str] = Field(None, description="Growth rate of the market")
    competition: Optional[str] = Field(None, description="Key competitors in the space")
    market_trends: Optional[str] = Field(None, description="Current trends within the market")
    go_to_market_strategy: Optional[str] = Field(None, description="Plan for entering the market")
    product_details: Optional[str] = Field(None, description="Details about the startup's product or service")
    technology_stack: Optional[str] = Field(None, description="Technologies used in the product")
    scalability: Optional[str] = Field(None, description="How the product can scale")
    user_feedback: Optional[str] = Field(None, description="Feedback received from users")
    product_fit: Optional[str] = Field(None, description="How well the product fits the target market")
    founder_backgrounds: Optional[str] = Field(None, description="Background information on the founders")
    track_records: Optional[str] = Field(None, description="Track records of the founders")
    leadership_skills: Optional[str] = Field(None, description="Leadership skills of the team")
    vision_alignment: Optional[str] = Field(None, description="How the team's vision aligns with the product")
    team_dynamics: Optional[str] = Field(None, description="Dynamics within the startup team")
    web_traffic_growth: Optional[str] = Field(None, description="Growth of web traffic to the startup's site")
    social_media_presence: Optional[str] = Field(None, description="Startup's presence on social media")
    investment_rounds: Optional[str] = Field(None, description="Details of any investment rounds")
    regulatory_approvals: Optional[str] = Field(None, description="Regulatory approvals obtained")
    patents: Optional[str] = Field(None, description="Details of any patents held by the startup")


class StartupCategorization(BaseModel):
    industry_growth: str = Field(..., description="[Yes/No/N/A]")
    market_size: str = Field(..., description="[Small/Medium/Large/N/A]")
    development_pace: str = Field(..., description="[Slower/Same/Faster/N/A]")
    market_adaptability: str = Field(..., description="[Not Adaptable/Somewhat Adaptable/Very Adaptable/N/A]")
    execution_capabilities: str = Field(..., description="[Poor/Average/Excellent/N/A]")
    funding_amount: str = Field(..., description="[Below Average/Average/Above Average/N/A]")
    valuation_change: str = Field(..., description="[Decreased/Remained Stable/Increased/N/A]")
    investor_backing: str = Field(..., description="[Unknown/Recognized/Highly Regarded/N/A]")
    reviews_testimonials: str = Field(..., description="[Negative/Mixed/Positive/N/A]")
    product_market_fit: str = Field(..., description="[Weak/Moderate/Strong/N/A]")
    sentiment_analysis: str = Field(..., description="[Negative/Neutral/Positive/N/A]")
    innovation_mentions: str = Field(..., description="[Rarely/Sometimes/Often/N/A]")
    cutting_edge_technology: str = Field(..., description="[No/Mentioned/Emphasized/N/A]")
    timing: str = Field(..., description="[Too Early/Just Right/Too Late/N/A]")


class StartupEvaluation(BaseModel):
    market_opportunity: str = Field(..., description="Assessment of the market opportunity")
    product_innovation: str = Field(..., description="Evaluation of product innovation")
    founding_team: str = Field(..., description="Analysis of the founding team")
    potential_risks: str = Field(..., description="Identification of potential risks")
    overall_potential: int = Field(..., description="Overall potential score on a scale of 1 to 10")
    investment_recommendation: str = Field(..., description="Investment recommendation: 'Invest' or 'Pass'")
    confidence: float = Field(..., description="Confidence level in the recommendation (0 to 1)")
    rationale: str = Field(..., description="Brief explanation for the recommendation")