from typing import TypedDict, Any, Optional
from typing_extensions import Annotated
import operator
from shared.types import Progress, StartupInfo


class OverallState(TypedDict):
    """Overall state shared across all nodes in the SSFF workflow."""
    # LangGraph required fields
    messages: Annotated[list[dict[str, Any]], operator.add]
    
    # Input
    startup_info_str: str
    
    # Parsed data
    startup_info: StartupInfo
    
    # Individual analyses
    market_analysis: Optional[dict[str, Any]]
    product_analysis: Optional[dict[str, Any]]
    founder_analysis: Optional[dict[str, Any]]
    
    # Founder specific metrics
    founder_segmentation: Optional[str]
    founder_idea_fit: Optional[float]
    
    # VC Scout results
    vc_prediction: Optional[str]
    categorization: Optional[dict[str, Any]]
    
    # Integrated analyses
    integrated_analysis: Optional[dict[str, Any]]
    integrated_analysis_basic: Optional[dict[str, Any]]
    quantitative_decision: Optional[dict[str, Any]]
    
    # Progress tracking
    progress: Progress
    
    # Workflow control
    next_step: Optional[str]
    should_continue: bool
