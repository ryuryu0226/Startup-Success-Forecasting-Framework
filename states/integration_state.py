from typing import TypedDict, Optional, Union, Any
from typing_extensions import Annotated
import operator
from shared.types import (
    MarketAnalysisDict, 
    ProductAnalysisDict, 
    FounderAnalysisDict, 
    AdvancedFounderAnalysisDict,
    StartupCategorizationDict,
    VCScoutAnalysisDict,
    IntegratedAnalysisDict,
    QuantitativeDecisionDict,
    ProgressDict
)


class IntegrationNodeInput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    market_analysis: Optional[MarketAnalysisDict]
    product_analysis: Optional[ProductAnalysisDict]
    founder_analysis: Optional[Union[FounderAnalysisDict, AdvancedFounderAnalysisDict]]
    vc_prediction: Optional[str]
    categorization: Optional[StartupCategorizationDict]
    vc_scout_analysis: Optional[VCScoutAnalysisDict]
    progress: ProgressDict


class IntegrationNodeOutput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    integrated_analysis: IntegratedAnalysisDict
    integrated_analysis_basic: IntegratedAnalysisDict
    quantitative_decision: QuantitativeDecisionDict
    progress: ProgressDict
