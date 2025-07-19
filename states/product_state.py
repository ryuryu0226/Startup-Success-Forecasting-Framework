from typing import TypedDict, Optional, Any
from shared.types import StartupInfoDict

class ProductNodeInput(TypedDict):
    """Input state for product analysis node."""
    startup_info: StartupInfoDict


class ProductNodeOutput(TypedDict):
    """Output state for product analysis node."""
    product_analysis: dict[str, Any]
    external_report: Optional[str]
    analysis_mode: str
    success: bool
    error_message: Optional[str]
    keywords_generated: Optional[str]
    search_results_count: Optional[int]
    innovation_score: Optional[float]
    market_fit_score: Optional[float]
