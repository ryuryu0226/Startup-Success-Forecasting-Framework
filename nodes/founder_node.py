import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nodes.base_node import BaseNode
from states.founder_state import FounderNodeInput, FounderNodeOutput
from agents.founder_agent import FounderAgent

class FounderNode(BaseNode):
    def __init__(self):
        super().__init__("founder")
        self.founder_agent = None
        
    def __call__(self, input_state: FounderNodeInput) -> FounderNodeOutput:
        # Initialize typed output
        output = FounderNodeOutput(
            messages=[],
            founder_analysis={},
            progress=input_state["progress"].copy()
        )
        
        try:
            # Update progress - starting
            progress_msg = self._create_progress_message("started", "Analyzing founder...")
            output["messages"].append(progress_msg)
            output["progress"]["current_step"] = self.name
            
            # Initialize agent if not already done
            if self.founder_agent is None:
                self.founder_agent = FounderAgent("gpt-4o-mini")
            
            # Get startup info
            startup_info = input_state["startup_info"]
            
            # Perform founder analysis
            founder_analysis = self.founder_agent.analyze(startup_info, "advanced")
            
            # Get founder backgrounds for segmentation and idea fit
            founder_backgrounds = startup_info.get("founder_backgrounds", "")
            if not founder_backgrounds:
                # Use description if founder_backgrounds is not available
                founder_backgrounds = startup_info.get("description", "")
            
            # Perform founder segmentation
            founder_segmentation = self.founder_agent.segment_founder(founder_backgrounds)
            
            # Calculate founder-idea fit
            founder_idea_fit = self.founder_agent.calculate_idea_fit(startup_info, founder_backgrounds)
            
            # Handle founder_idea_fit if it's a list
            if isinstance(founder_idea_fit, list):
                founder_idea_fit_value = founder_idea_fit[0]
            else:
                founder_idea_fit_value = founder_idea_fit
            
            # Convert founder_analysis to dict
            if hasattr(founder_analysis, 'model_dump'):
                founder_analysis_dict = founder_analysis.model_dump()
            else:
                founder_analysis_dict = founder_analysis
            
            # Add segmentation and fit data to analysis (convert to AdvancedFounderAnalysisDict)
            founder_analysis_dict["segmentation"] = founder_segmentation
            founder_analysis_dict["idea_fit"] = (founder_idea_fit_value, 0.0)  # Convert to tuple format
            
            self.logger.info("Founder analysis completed successfully")
            
            # Update output
            output["founder_analysis"] = founder_analysis_dict
            
            # Update progress - completed
            self._update_progress_completed(output["progress"])
            complete_msg = self._create_progress_message(
                "completed",
                "Founder analysis completed",
                data={
                    "segmentation": founder_segmentation,
                    "idea_fit": founder_idea_fit_value,
                    "competency_score": founder_analysis_dict.get("competency_score", 0)
                }
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
