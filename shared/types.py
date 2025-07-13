from typing import TypedDict, Optional, Literal
from datetime import datetime


class Progress(TypedDict):
    """Track the progress of analysis."""
    current_step: str
    completed_steps: list[str]
    start_time: datetime
    step_times: dict[str, dict[str, datetime]]
    status: Literal["running", "completed", "error"]
    error_message: Optional[str]


class StartupInfo(TypedDict):
    """Parsed startup information."""
    name: Optional[str]
    description: Optional[str]
    founder_backgrounds: Optional[str]
    market_size: Optional[str]
    competition: Optional[str]
    growth_rate: Optional[str]
    market_trends: Optional[str]
    product_details: Optional[str]
    technology_stack: Optional[str]
    product_fit: Optional[str]
    # Additional fields from StartupInfo schema
    web_traffic_growth: Optional[str]
    social_media_presence: Optional[str]
    investment_rounds: Optional[str]
    regulatory_approvals: Optional[str]
    patents: Optional[str]
