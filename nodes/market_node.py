"""Market analysis node for SSFF LangGraph implementation."""

from typing import Dict, Any
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nodes.base_node import BaseNode
from states.base_state import GraphState
from agents.market_agent import MarketAgent

class MarketNode(BaseNode):
    """Node for market analysis."""
    
    def __init__(self):
        super().__init__("market")
        self.market_agent = None
        
    def __call__(self, state: GraphState) -> Dict[str, Any]:
        """Perform market analysis."""
        try:
            # Update progress - starting
            updates = self.update_progress(state, "started", "市場分析を実行中...")
            
            # Get configuration from state
            model = state["analysis_state"].get("model", "gpt-4o-mini")
            mode = state["analysis_state"].get("mode", "advanced")
            
            # Initialize agent if not already done
            if self.market_agent is None:
                self.market_agent = MarketAgent(model)
            
            # Get startup info
            startup_info = state["analysis_state"]["startup_info"]
            self.logger.info(f"Starting market analysis in {mode} mode")
            
            # Perform analysis
            if mode == "natural_language":
                mode = "natural_language_advanced"
            
            market_analysis = self.market_agent.analyze(startup_info, mode)
            
            # Handle different response formats
            if isinstance(market_analysis, dict) and 'analysis' in market_analysis:
                # Natural language mode returns dict with 'analysis' and 'external_report'
                updates["analysis_state"]["market_analysis"] = market_analysis
            else:
                # Advanced mode returns the analysis object directly
                updates["analysis_state"]["market_analysis"] = market_analysis.dict() if hasattr(market_analysis, 'dict') else market_analysis
            
            self.logger.info("Market analysis completed successfully")
            
            # Update progress - completed
            final_updates = self.update_progress(
                state={**state, **updates},
                status="completed",
                message="市場分析が完了しました",
                data={"analysis_mode": mode}
            )
            
            # Merge updates
            updates["messages"].extend(final_updates["messages"])
            updates["analysis_state"]["progress"] = final_updates["analysis_state"]["progress"]
            
            return updates
            
        except Exception as e:
            return self.handle_error(state, e)