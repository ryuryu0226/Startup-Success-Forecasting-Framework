import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nodes.base_node import BaseNode
from states.market_state import MarketNodeInput, MarketNodeOutput
from agents.market_agent import MarketAgent

class MarketNode(BaseNode):
    def __init__(self):
        super().__init__("market")
        self.market_agent = MarketAgent("gpt-4o")
    
    def __call__(self, input_state: MarketNodeInput) -> MarketNodeOutput:
        # Initialize typed output
        output = MarketNodeOutput(
            messages=[],
            market_analysis={},
            progress=input_state["progress"].copy()
        )
        
        try:
            # Update progress - starting
            progress_msg = self._create_progress_message("started", "Analyzing market...")
            output["messages"].append(progress_msg)
            output["progress"]["current_step"] = self.name
            
            # Get startup info
            startup_info = input_state["startup_info"]
            
            # Perform analysis
            market_analysis = self.market_agent.analyze(startup_info, "advanced")
            market_analysis_dict = market_analysis.model_dump()
            
            self.logger.info("Market analysis completed successfully")
            
            # Update output
            output["market_analysis"] = market_analysis_dict
            
            # Update progress - completed
            self._update_progress_completed(output["progress"])
            complete_msg = self._create_progress_message(
                "completed", 
                "Market analysis completed",
                data={"viability_score": market_analysis_dict.get("viability_score", 0)}
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
