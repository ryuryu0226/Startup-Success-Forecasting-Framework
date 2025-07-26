"""Integration analysis node for SSFF LangGraph implementation."""

import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nodes.base_node import BaseNode
from states.integration_state import IntegrationNodeInput, IntegrationNodeOutput
from agents.integration_agent import IntegrationAgent

class IntegrationNode(BaseNode):
    def __init__(self):
        super().__init__("integration")
        self.integration_agent = None
        
    def __call__(self, input_state: IntegrationNodeInput) -> IntegrationNodeOutput:
        # Initialize typed output
        output = IntegrationNodeOutput(
            messages=[],
            integrated_analysis={},
            integrated_analysis_basic={},
            quantitative_decision={},
            progress=input_state["progress"].copy()
        )
        
        try:
            # Update progress - starting
            progress_msg = self._create_progress_message("started", "Integrating all analyses...")
            output["messages"].append(progress_msg)
            output["progress"]["current_step"] = self.name
            
            # Initialize agent if not already done
            if self.integration_agent is None:
                self.integration_agent = IntegrationAgent("gpt-4o-mini")
            
            # Get all analysis results from input state
            market_analysis = input_state.get("market_analysis", {})
            product_analysis = input_state.get("product_analysis", {})
            founder_analysis = input_state.get("founder_analysis", {})
            vc_prediction = input_state.get("vc_prediction", "")
            
            # Extract founder-specific data
            founder_segmentation = ""
            founder_idea_fit = 0.0
            if founder_analysis:
                founder_segmentation = founder_analysis.get("segmentation", "")
                # Handle idea_fit tuple format
                idea_fit_data = founder_analysis.get("idea_fit", (0.0, 0.0))
                if isinstance(idea_fit_data, tuple):
                    founder_idea_fit = idea_fit_data[0]
                else:
                    founder_idea_fit = idea_fit_data
            
            # Perform integrated analysis
            integrated_analysis = self.integration_agent.integrated_analysis_pro(
                str(market_analysis),
                str(product_analysis),
                str(founder_analysis),
                founder_idea_fit,
                founder_segmentation,
                vc_prediction
            )
            
            # Convert to dict if it's a model object
            if hasattr(integrated_analysis, 'model_dump'):
                integrated_analysis_dict = integrated_analysis.model_dump()
            else:
                integrated_analysis_dict = integrated_analysis
            
            # Perform basic integrated analysis
            integrated_analysis_basic = self.integration_agent.integrated_analysis_basic(
                str(market_analysis),
                str(product_analysis),
                str(founder_analysis)
            )
            
            # Convert to dict if it's a model object
            if hasattr(integrated_analysis_basic, 'model_dump'):
                integrated_analysis_basic_dict = integrated_analysis_basic.model_dump()
            else:
                integrated_analysis_basic_dict = integrated_analysis_basic
            
            # Get quantitative decision
            quantitative_decision = self.integration_agent.getquantDecision(
                vc_prediction,
                founder_idea_fit,
                founder_segmentation
            )
            
            # Convert to dict if it's a model object
            if hasattr(quantitative_decision, 'model_dump'):
                quantitative_decision_dict = quantitative_decision.model_dump()
            else:
                quantitative_decision_dict = quantitative_decision
            
            self.logger.info("Integration analysis completed successfully")
            
            # Update output
            output["integrated_analysis"] = integrated_analysis_dict
            output["integrated_analysis_basic"] = integrated_analysis_basic_dict
            output["quantitative_decision"] = quantitative_decision_dict
            
            # Update progress to completed - mark workflow as complete
            self._update_progress_completed(output["progress"])
            output["progress"]["status"] = "completed"
            complete_msg = self._create_progress_message(
                "completed",
                "Integration completed - Analysis finished",
                data={
                    "overall_score": integrated_analysis_dict.get("overall_score", 0),
                    "outcome": integrated_analysis_dict.get("outcome", "Unknown"),
                    "recommendation": integrated_analysis_dict.get("recommendation", "No recommendation")
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
