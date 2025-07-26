from typing import TypedDict, Any
from typing_extensions import Annotated
import operator
from shared.types import StartupInfoDict, ProgressDict
from shared.reducers import merge_progress


class ParseNodeInput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    startup_info_str: str
    progress: Annotated[ProgressDict, merge_progress]


class ParseNodeOutput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    startup_info: StartupInfoDict
    progress: Annotated[ProgressDict, merge_progress]
