"""Parse node for SSFF LangGraph implementation."""

from typing import Dict, Any
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nodes.base_node import BaseNode
from states.base_state import GraphState
from agents.vc_scout_agent import VCScoutAgent
from schemas.vc_scout_schema import StartupInfo

class ParseNode(BaseNode):
    """Node for parsing startup information."""
    
    def __init__(self):
        super().__init__("parse")
        self.vc_scout_agent = None
        
    def __call__(self, state: GraphState) -> Dict[str, Any]:
        """Parse startup information string into structured data."""
        try:
            # Update progress - starting
            updates = self.update_progress(state, "started", "スタートアップ情報を解析中...")
            
            # Get model from state
            model = state["analysis_state"].get("model", "gpt-4o-mini")
            
            # Initialize agent if not already done
            if self.vc_scout_agent is None:
                self.vc_scout_agent = VCScoutAgent(model)
            
            # Parse startup info
            startup_info_str = state["analysis_state"]["startup_info_str"]
            self.logger.info(f"Parsing startup info: {startup_info_str[:100]}...")
            
            startup_info = self.vc_scout_agent.parse_record(startup_info_str)
            
            # Convert to dict if it's a StartupInfo object
            if isinstance(startup_info, StartupInfo):
                startup_info = startup_info.dict()
            elif not isinstance(startup_info, dict):
                # Failed to parse
                raise ValueError("Failed to parse startup information")
            
            self.logger.info("Successfully parsed startup information")
            
            # Update state with parsed info
            updates["analysis_state"]["startup_info"] = startup_info
            
            # Update progress - completed
            final_updates = self.update_progress(
                state={**state, **updates}, 
                status="completed", 
                message="スタートアップ情報の解析が完了しました",
                data={"parsed_fields": len(startup_info)}
            )
            
            # Merge updates
            updates["messages"].extend(final_updates["messages"])
            updates["analysis_state"]["progress"] = final_updates["analysis_state"]["progress"]
            
            return updates
            
        except Exception as e:
            return self.handle_error(state, e)