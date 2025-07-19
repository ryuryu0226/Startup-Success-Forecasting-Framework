from typing import TypedDict, Optional, Any
from shared.types import StartupInfoDict


class MarketNodeInput(TypedDict):
    """Input state for market analysis node."""
    startup_info: StartupInfoDict


class MarketNodeOutput(TypedDict):
    """Output state for market analysis node."""
    market_analysis: dict[str, Any]
    external_report: Optional[str]
    analysis_mode: str
    success: bool
    error_message: Optional[str]
    keywords_generated: Optional[str]
    search_results_count: Optional[int]
