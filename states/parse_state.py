from typing import TypedDict, Optional, Any


class ParseNodeInput(TypedDict):
    """Input state for parse node."""
    startup_info_str: str


class ParseNodeOutput(TypedDict):
    """Output state for parse node."""
    startup_info: dict[str, Any]
    parse_success: bool
    error_message: Optional[str]
    parsed_fields_count: Optional[int]
