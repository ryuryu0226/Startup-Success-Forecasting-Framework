from typing import TypedDict, Union, Any
from typing_extensions import Annotated
import operator
from shared.types import StartupInfoDict, FounderAnalysisDict, AdvancedFounderAnalysisDict, ProgressDict


class FounderNodeInput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    startup_info: StartupInfoDict
    progress: ProgressDict


class FounderNodeOutput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    founder_analysis: Union[FounderAnalysisDict, AdvancedFounderAnalysisDict]
    progress: ProgressDict