from typing import TypedDict, Any
from typing_extensions import Annotated
import operator
from shared.types import StartupInfoDict, ProgressDict


class ParseNodeInput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    startup_info_str: str
    progress: ProgressDict


class ParseNodeOutput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    startup_info: StartupInfoDict
    progress: ProgressDict
