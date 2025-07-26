import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nodes.base_node import BaseNode
from states.vc_scout_state import VCScoutNodeInput, VCScoutNodeOutput
from agents.vc_scout_agent import VCScoutAgent
from schemas.vc_scout_schema import StartupInfo

class VCScoutNode(BaseNode):
    def __init__(self):
        super().__init__("vc_scout")
        self.vc_scout_agent = None
        
    def __call__(self, input_state: VCScoutNodeInput) -> VCScoutNodeOutput:
        # Initialize typed output
        output = VCScoutNodeOutput(
            messages=[],
            vc_prediction="",
            categorization={},
            vc_scout_analysis=None,
            progress=input_state["progress"].copy()
        )
        
        try:
            # Update progress - starting
            progress_msg = self._create_progress_message("started", "Performing VC Scout evaluation...")
            output["messages"].append(progress_msg)
            output["progress"]["current_step"] = self.name
            
            # Initialize agent if not already done
            if self.vc_scout_agent is None:
                self.vc_scout_agent = VCScoutAgent("gpt-4o-mini")
            
            # Get startup info
            startup_info = input_state["startup_info"]
            
            # Convert to StartupInfo object if needed
            if isinstance(startup_info, dict):
                startup_info_obj = StartupInfo(**startup_info)
            else:
                startup_info_obj = startup_info
            
            # Perform VC Scout evaluation
            prediction, categorization = self.vc_scout_agent.side_evaluate(startup_info_obj)
            
            # Perform additional VC Scout analysis if available
            vc_scout_analysis = None
            try:
                # Try to get more detailed VC analysis if method exists
                if hasattr(self.vc_scout_agent, 'detailed_analysis'):
                    vc_scout_analysis = self.vc_scout_agent.detailed_analysis(startup_info_obj)
                    if hasattr(vc_scout_analysis, 'model_dump'):
                        vc_scout_analysis = vc_scout_analysis.model_dump()
            except Exception as e:
                self.logger.warning(f"Detailed VC analysis not available: {e}")
            
            # Convert categorization to dict
            if hasattr(categorization, 'model_dump'):
                categorization_dict = categorization.model_dump()
            else:
                categorization_dict = categorization
            
            self.logger.info(f"VC Scout evaluation completed: {prediction}")
            
            # Update output
            output["vc_prediction"] = prediction
            output["categorization"] = categorization_dict
            output["vc_scout_analysis"] = vc_scout_analysis
            
            # Update progress - completed
            self._update_progress_completed(output["progress"])
            complete_msg = self._create_progress_message(
                "completed",
                "VC Scout evaluation completed",
                data={"prediction": prediction}
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
