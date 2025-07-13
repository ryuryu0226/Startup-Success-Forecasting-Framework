from typing import TypedDict, Optional, Any


class FounderNodeInput(TypedDict):
    """Input state for founder analysis node."""
    startup_info: dict[str, Any]


class FounderNodeOutput(TypedDict):
    """Output state for founder analysis node."""
    founder_analysis: dict[str, Any]
    founder_segmentation: str
    founder_idea_fit: float
    segmentation_confidence: Optional[float]
    idea_fit_reasoning: Optional[str]
    success: bool
    error_message: Optional[str]
