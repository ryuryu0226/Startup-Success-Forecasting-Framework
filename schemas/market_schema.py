from pydantic import BaseModel, Field


class MarketAnalysis(BaseModel):
    market_size: str = Field(..., description="Estimated market size")
    growth_rate: str = Field(..., description="Market growth rate")
    competition: str = Field(..., description="Overview of competition")
    market_trends: str = Field(..., description="Key market trends")
    viability_score: int = Field(..., description="Market viability score on a scale of 1 to 10")