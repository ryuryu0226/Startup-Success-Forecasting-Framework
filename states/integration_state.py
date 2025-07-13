from typing import TypedDict, Optional, Any


class IntegrationNodeInput(TypedDict):
    """Input state for integration node."""
    market_analysis: dict[str, Any]
    product_analysis: dict[str, Any]
    founder_analysis: dict[str, Any]
    founder_segmentation: str
    founder_idea_fit: float
    vc_prediction: str


class IntegrationNodeOutput(TypedDict):
    """Output state for integration node."""
    integrated_analysis: dict[str, Any]
    integrated_analysis_basic: dict[str, Any]
    quantitative_decision: dict[str, Any]
    final_recommendation: Optional[str]
    confidence_score: Optional[float]
    risk_assessment: Optional[str]
    success: bool
    error_message: Optional[str]
