from pydantic import BaseModel, Field


class IntegratedAnalysis(BaseModel):
    overall_score: float = Field(..., description="Overall score between 1 and 10")
    IntegratedAnalysis: str = Field(..., description="Comprehensive analysis from VC perspective")
    recommendation: str = Field(..., description="Brief recommendation for next steps")
    outcome: str = Field(..., description="Prediction outcome: 'Invest' or 'Hold'")


class QuantitativeDecision(BaseModel):
    outcome: str = Field(..., description="Predicted outcome: 'Successful' or 'Unsuccessful'")
    probability: float = Field(..., description="Probability of the predicted outcome")
    reasoning: str = Field(..., description="One-line reasoning for the decision")