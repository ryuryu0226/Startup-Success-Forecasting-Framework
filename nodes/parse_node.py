import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nodes.base_node import BaseNode
from states.parse_state import ParseNodeInput, ParseNodeOutput
from agents.vc_scout_agent import VCScoutAgent
from schemas.vc_scout_schema import StartupInfo

class ParseNode(BaseNode):
    def __init__(self):
        super().__init__("parse")
        self.vc_scout_agent = VCScoutAgent("gpt-4o")

    def __call__(self, input_state: ParseNodeInput) -> ParseNodeOutput:
        # Initialize typed output
        output = ParseNodeOutput(
            messages=[],
            startup_info={},
            progress=input_state["progress"].copy()
        )
        
        try:
            # Update progress - starting
            progress_msg = self._create_progress_message("started", "Parsing startup information...")
            output["messages"].append(progress_msg)
            output["progress"]["current_step"] = self.name
            
            # Parse startup info
            startup_info_str = input_state["startup_info_str"]
            self.logger.info(f"Parsing startup info: {startup_info_str[:100]}...")
            
            startup_info = self.vc_scout_agent.parse_record(startup_info_str)
            
            # Convert to dict if it's a StartupInfo object
            if isinstance(startup_info, StartupInfo):
                startup_info_dict = startup_info.model_dump()
            elif not isinstance(startup_info, dict):
                raise ValueError("Failed to parse startup information")
            else:
                startup_info_dict = startup_info
            
            self.logger.info("Successfully parsed startup information")
            
            # Update output
            output["startup_info"] = startup_info_dict
            
            # Update progress - completed
            self._update_progress_completed(output["progress"])
            complete_msg = self._create_progress_message(
                "completed", 
                "Startup information parsed successfully",
                data={"parsed_fields": len(startup_info_dict)}
            )
            output["messages"].append(complete_msg)
            
        except Exception as e:
            error_msg = f"Error in {self.name}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            output["progress"]["status"] = "error"
            output["progress"]["error_message"] = error_msg
            error_progress = self._create_progress_message("error", error_msg)
            output["messages"].append(error_progress)
        
        return output
