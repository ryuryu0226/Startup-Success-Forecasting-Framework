import logging
import time
from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional, Literal
from states.overall_state import OverallState


class ProgressUpdate(BaseModel):
    node_name: str
    status: Literal["started", "completed", "error"]
    message: str
    timestamp: float
    data: Optional[dict[str, Any]] = None


class BaseNode:
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"nodes.{name}")

    def update_progress(
        self,
        state: OverallState,
        status: Literal["started", "completed", "error"],
        message: str,
        data: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Update progress information in the state."""
        current_time = datetime.now()

        # Create progress update for messages
        progress_update = ProgressUpdate(
            node_name=self.name,
            status=status,
            message=message,
            timestamp=time.time(),
            data=data
        )

        # Update progress state
        progress = state["progress"].copy()
        progress["current_step"] = self.name
        
        if status == "started":
            if "step_times" not in progress:
                progress["step_times"] = {}
            progress["step_times"][self.name] = {"start": current_time}
            
        elif status == "completed":
            if self.name not in progress.get("completed_steps", []):
                progress["completed_steps"] = progress.get("completed_steps", []) + [self.name]
            if self.name in progress.get("step_times", {}):
                progress["step_times"][self.name]["end"] = current_time
                
        elif status == "error":
            progress["status"] = "error"
            progress["error_message"] = message
            
        # Return updates
        return {
            "messages": [progress_update.model_dump()],
            "progress": progress
        }

    def handle_error(self, state: OverallState, error: Exception) -> dict[str, Any]:
        """Handle errors in node execution."""
        error_message = f"Error in {self.name}: {str(error)}"
        self.logger.error(error_message, exc_info=True)
        return self.update_progress(state, "error", error_message)
    
    def __call__(self, state: OverallState) -> dict[str, Any]:
        """Execute the node. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement __call__ method")
