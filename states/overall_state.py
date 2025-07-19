from typing import Any, Optional, Union
from typing_extensions import Annotated, TypedDict
import operator
from shared.types import (
    ProgressDict,
    StartupInfoDict,
    MarketAnalysisDict,
    ProductAnalysisDict,
    FounderAnalysisDict,
    AdvancedFounderAnalysisDict,
    VCScoutAnalysisDict,
    IntegratedAnalysisDict,
    QuantitativeDecisionDict,
    StartupCategorizationDict,
)


class OverallState(TypedDict):
    """Overall state shared across all nodes in the SSFF workflow."""
    # LangGraph required fields
    messages: Annotated[list[dict[str, Any]], operator.add]
    
    # Input
    startup_info_str: str
    
    # Parsed data
    startup_info: StartupInfoDict
    
    # Individual analyses
    market_analysis: Optional[MarketAnalysisDict]
    product_analysis: Optional[ProductAnalysisDict]
    founder_analysis: Optional[Union[FounderAnalysisDict, AdvancedFounderAnalysisDict]]
    
    # VC Scout results
    vc_prediction: Optional[str]
    categorization: Optional[StartupCategorizationDict]
    vc_scout_analysis: Optional[VCScoutAnalysisDict]
    
    # Integrated analyses
    integrated_analysis: Optional[IntegratedAnalysisDict]
    integrated_analysis_basic: Optional[IntegratedAnalysisDict]
    quantitative_decision: Optional[QuantitativeDecisionDict]
    
    # Progress tracking
    progress: ProgressDict
    
    # Workflow control
    next_step: Optional[str]
    should_continue: bool
