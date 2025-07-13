"""Product analysis node for SSFF LangGraph implementation."""

from typing import Dict, Any
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nodes.base_node import BaseNode
from states.base_state import GraphState
from agents.product_agent import ProductAgent

class ProductNode(BaseNode):
    """Node for product analysis."""
    
    def __init__(self):
        super().__init__("product")
        self.product_agent = None
        
    def __call__(self, state: GraphState) -> Dict[str, Any]:
        """Perform product analysis."""
        try:
            # Update progress - starting
            updates = self.update_progress(state, "started", "プロダクト分析を実行中...")
            
            # Get configuration from state
            model = state["analysis_state"].get("model", "gpt-4o-mini")
            mode = state["analysis_state"].get("mode", "advanced")
            
            # Initialize agent if not already done
            if self.product_agent is None:
                self.product_agent = ProductAgent(model)
            
            # Get startup info
            startup_info = state["analysis_state"]["startup_info"]
            self.logger.info(f"Starting product analysis in {mode} mode")
            
            # Perform analysis
            if mode == "natural_language":
                mode = "natural_language_advanced"
            
            product_analysis = self.product_agent.analyze(startup_info, mode)
            
            # Handle different response formats
            if isinstance(product_analysis, dict) and 'analysis' in product_analysis:
                # Natural language mode returns dict with 'analysis' and 'external_report'
                updates["analysis_state"]["product_analysis"] = product_analysis
            else:
                # Advanced mode returns the analysis object directly
                updates["analysis_state"]["product_analysis"] = product_analysis.dict() if hasattr(product_analysis, 'dict') else product_analysis
            
            self.logger.info("Product analysis completed successfully")
            
            # Update progress - completed
            final_updates = self.update_progress(
                state={**state, **updates},
                status="completed",
                message="プロダクト分析が完了しました",
                data={"analysis_mode": mode}
            )
            
            # Merge updates
            updates["messages"].extend(final_updates["messages"])
            updates["analysis_state"]["progress"] = final_updates["analysis_state"]["progress"]
            
            return updates
            
        except Exception as e:
            return self.handle_error(state, e)