"""VC Scout node for SSFF LangGraph implementation."""

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

class VCScoutNode(BaseNode):
    """Node for VC Scout evaluation and ML prediction."""
    
    def __init__(self):
        super().__init__("vc_scout")
        self.vc_scout_agent = None
        
    def __call__(self, state: GraphState) -> Dict[str, Any]:
        """Perform VC Scout evaluation and ML prediction."""
        try:
            # Update progress - starting
            updates = self.update_progress(state, "started", "VC評価と機械学習予測を実行中...")
            
            # Get configuration from state
            model = state["analysis_state"].get("model", "gpt-4o-mini")
            
            # Initialize agent if not already done
            if self.vc_scout_agent is None:
                self.vc_scout_agent = VCScoutAgent(model)
            
            # Get startup info
            startup_info = state["analysis_state"]["startup_info"]
            self.logger.info("Starting VC Scout evaluation")
            
            # Convert to StartupInfo object if needed
            if isinstance(startup_info, dict):
                startup_info_obj = StartupInfo(**startup_info)
            else:
                startup_info_obj = startup_info
            
            # Perform VC evaluation
            vc_evaluation = self.vc_scout_agent.evaluate(startup_info_obj, "advanced")
            
            # Perform side evaluation (categorization and ML prediction)
            prediction, categorization = self.vc_scout_agent.side_evaluate(startup_info_obj)
            
            # Update state with results
            updates["analysis_state"]["vc_prediction"] = prediction
            updates["analysis_state"]["categorization"] = categorization.dict() if hasattr(categorization, 'dict') else categorization
            
            self.logger.info(f"VC Scout evaluation completed - Prediction: {prediction}")
            
            # Update progress - completed
            final_updates = self.update_progress(
                state={**state, **updates},
                status="completed",
                message="VC評価と機械学習予測が完了しました",
                data={
                    "prediction": prediction,
                    "evaluation_score": vc_evaluation.dict().get("overall_potential_score", "N/A") if hasattr(vc_evaluation, 'dict') else "N/A"
                }
            )
            
            # Merge updates
            updates["messages"].extend(final_updates["messages"])
            updates["analysis_state"]["progress"] = final_updates["analysis_state"]["progress"]
            
            return updates
            
        except Exception as e:
            return self.handle_error(state, e)