from typing import TypedDict, Any
from typing_extensions import Annotated
import operator
from shared.types import StartupInfoDict, ProductAnalysisDict, ProgressDict
from shared.reducers import merge_progress


class ProductNodeInput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    startup_info: StartupInfoDict
    progress: Annotated[ProgressDict, merge_progress]


class ProductNodeOutput(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]
    product_analysis: ProductAnalysisDict
    progress: Annotated[ProgressDict, merge_progress]
