import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nodes.base_node import BaseNode
from states.product_state import ProductNodeInput, ProductNodeOutput
from agents.product_agent import ProductAgent

class ProductNode(BaseNode):
    def __init__(self):
        super().__init__("product")
        self.product_agent = None
        
    def __call__(self, input_state: ProductNodeInput) -> ProductNodeOutput:
        # Initialize typed output
        output = ProductNodeOutput(
            messages=[],
            product_analysis={},
            progress=input_state["progress"].copy()
        )
        
        try:
            # Update progress - starting
            progress_msg = self._create_progress_message("started", "Analyzing product...")
            output["messages"].append(progress_msg)
            output["progress"]["current_step"] = self.name
            
            # Initialize agent if not already done
            if self.product_agent is None:
                self.product_agent = ProductAgent("gpt-4o-mini")
            
            # Get startup info
            startup_info = input_state["startup_info"]
            
            # Perform analysis
            product_analysis = self.product_agent.analyze(startup_info, "advanced")
            
            # Convert to dict if it's a model object
            if hasattr(product_analysis, 'model_dump'):
                product_analysis_dict = product_analysis.model_dump()
            else:
                product_analysis_dict = product_analysis
            
            self.logger.info("Product analysis completed successfully")
            
            # Update output
            output["product_analysis"] = product_analysis_dict
            
            # Update progress - completed
            self._update_progress_completed(output["progress"])
            complete_msg = self._create_progress_message(
                "completed",
                "Product analysis completed",
                data={
                    "potential_score": product_analysis_dict.get("potential_score", 0),
                    "innovation_score": product_analysis_dict.get("innovation_score", 0),
                    "market_fit_score": product_analysis_dict.get("market_fit_score", 0)
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
