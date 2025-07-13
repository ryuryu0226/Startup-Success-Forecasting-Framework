from typing import TypedDict, Optional, Any
from shared.types import StartupInfo


class VCScoutNodeInput(TypedDict):
    """Input state for VC Scout node."""
    startup_info: StartupInfo


class VCScoutNodeOutput(TypedDict):
    """Output state for VC Scout node."""
    vc_prediction: str
    categorization: dict[str, Any]
    vc_evaluation: Optional[dict[str, Any]]
    prediction_confidence: Optional[float]
    evaluation_score: Optional[float]
    success: bool
    error_message: Optional[str]
