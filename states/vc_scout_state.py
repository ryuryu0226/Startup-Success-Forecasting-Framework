from typing import TypedDict, Optional, Any
from typing_extensions import Annotated
import operator
from shared.types import StartupInfoDict, VCScoutAnalysisDict, StartupCategorizationDict, ProgressDict


class VCScoutNodeInput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    startup_info: StartupInfoDict
    progress: ProgressDict


class VCScoutNodeOutput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    vc_prediction: str
    categorization: StartupCategorizationDict
    vc_scout_analysis: Optional[VCScoutAnalysisDict]
    progress: ProgressDict
