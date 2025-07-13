"""Integration node for SSFF LangGraph implementation."""

from typing import Dict, Any
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nodes.base_node import BaseNode
from states.base_state import GraphState
from agents.integration_agent import IntegrationAgent

class IntegrationNode(BaseNode):
    """Node for integrating all analyses."""
    
    def __init__(self):
        super().__init__("integration")
        self.integration_agent = None
        
    def __call__(self, state: GraphState) -> Dict[str, Any]:
        """Integrate all analyses into final results."""
        try:
            # Update progress - starting
            updates = self.update_progress(state, "started", "統合分析を実行中...")
            
            # Get configuration from state
            model = state["analysis_state"].get("model", "gpt-4o-mini")
            
            # Initialize agent if not already done
            if self.integration_agent is None:
                self.integration_agent = IntegrationAgent(model)
            
            # Get all analysis results
            analysis_state = state["analysis_state"]
            market_analysis = analysis_state.get("market_analysis", {})
            product_analysis = analysis_state.get("product_analysis", {})
            founder_analysis = analysis_state.get("founder_analysis", {})
            founder_segmentation = analysis_state.get("founder_segmentation", "")
            founder_idea_fit = analysis_state.get("founder_idea_fit", 0.0)
            vc_prediction = analysis_state.get("vc_prediction", "")
            
            self.logger.info("Starting integration analysis")
            
            # Perform integrated analysis (advanced)
            integrated_analysis = self.integration_agent.integrated_analysis_pro(
                market_info=market_analysis,
                product_info=product_analysis,
                founder_info=founder_analysis,
                founder_idea_fit=founder_idea_fit,
                founder_segmentation=founder_segmentation,
                rf_prediction=vc_prediction,
            )
            
            # Perform basic integrated analysis
            integrated_analysis_basic = self.integration_agent.integrated_analysis_basic(
                market_info=market_analysis,
                product_info=product_analysis,
                founder_info=founder_analysis,
            )
            
            # Get quantitative decision
            quantitative_decision = self.integration_agent.getquantDecision(
                vc_prediction,
                founder_idea_fit,
                founder_segmentation,
            )
            
            # Update state with integrated results
            updates["analysis_state"]["integrated_analysis"] = integrated_analysis.dict() if hasattr(integrated_analysis, 'dict') else integrated_analysis
            updates["analysis_state"]["integrated_analysis_basic"] = integrated_analysis_basic.dict() if hasattr(integrated_analysis_basic, 'dict') else integrated_analysis_basic
            updates["analysis_state"]["quantitative_decision"] = quantitative_decision.dict() if hasattr(quantitative_decision, 'dict') else quantitative_decision
            
            self.logger.info("Integration analysis completed successfully")
            
            # Update progress - completed
            final_updates = self.update_progress(
                state={**state, **updates},
                status="completed",
                message="統合分析が完了しました - 全ての分析が完了",
                data={
                    "final_prediction": vc_prediction,
                    "founder_segment": founder_segmentation,
                    "total_steps_completed": len(analysis_state.get("progress", {}).get("completed_steps", [])) + 1
                }
            )
            
            # Mark workflow as completed
            final_updates["analysis_state"]["progress"]["status"] = "completed"
            
            # Merge updates
            updates["messages"].extend(final_updates["messages"])
            updates["analysis_state"]["progress"] = final_updates["analysis_state"]["progress"]
            
            return updates
            
        except Exception as e:
            return self.handle_error(state, e)