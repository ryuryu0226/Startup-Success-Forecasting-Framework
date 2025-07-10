from pydantic import BaseModel, Field


class ProductAnalysis(BaseModel):
    features_analysis: str = Field(..., description="Analysis of product features")
    tech_stack_evaluation: str = Field(..., description="Evaluation of the technology stack")
    usp_assessment: str = Field(..., description="Assessment of the unique selling proposition")
    potential_score: int = Field(..., description="Product potential score on a scale of 1 to 10")
    innovation_score: int = Field(..., description="Innovation score on a scale of 1 to 10")
    market_fit_score: int = Field(..., description="Market fit score on a scale of 1 to 10")