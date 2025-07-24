from typing import TypedDict, Any
from typing_extensions import Annotated
import operator
from shared.types import StartupInfoDict, MarketAnalysisDict, ProgressDict


class MarketNodeInput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    startup_info: StartupInfoDict
    progress: ProgressDict


class MarketNodeOutput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    market_analysis: MarketAnalysisDict
    progress: ProgressDict
