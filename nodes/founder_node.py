"""Founder analysis node for SSFF LangGraph implementation."""

from typing import Dict, Any
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nodes.base_node import BaseNode
from states.base_state import GraphState
from agents.founder_agent import FounderAgent

class FounderNode(BaseNode):
    """Node for founder analysis."""
    
    def __init__(self):
        super().__init__("founder")
        self.founder_agent = None
        
    def __call__(self, state: GraphState) -> Dict[str, Any]:
        """Perform founder analysis."""
        try:
            # Update progress - starting
            updates = self.update_progress(state, "started", "創業者分析を実行中...")
            
            # Get configuration from state
            model = state["analysis_state"].get("model", "gpt-4o-mini")
            mode = state["analysis_state"].get("mode", "advanced")
            
            # Initialize agent if not already done
            if self.founder_agent is None:
                self.founder_agent = FounderAgent(model)
            
            # Get startup info
            startup_info = state["analysis_state"]["startup_info"]
            self.logger.info(f"Starting founder analysis in {mode} mode")
            
            # Perform founder analysis
            founder_analysis = self.founder_agent.analyze(startup_info, mode)
            
            # Get founder backgrounds for segmentation and idea fit
            founder_backgrounds = startup_info.get("founder_backgrounds", "")
            if not founder_backgrounds:
                # Use description if founder_backgrounds is not available
                founder_backgrounds = startup_info.get("description", "")
            
            # Perform founder segmentation
            founder_segmentation = self.founder_agent.segment_founder(founder_backgrounds)
            
            # Calculate founder-idea fit
            founder_idea_fit = self.founder_agent.calculate_idea_fit(startup_info, founder_backgrounds)
            
            # Update state with all founder-related results
            updates["analysis_state"]["founder_analysis"] = founder_analysis.dict() if hasattr(founder_analysis, 'dict') else founder_analysis
            updates["analysis_state"]["founder_segmentation"] = founder_segmentation
            updates["analysis_state"]["founder_idea_fit"] = founder_idea_fit[0] if isinstance(founder_idea_fit, list) else founder_idea_fit
            
            self.logger.info(f"Founder analysis completed - Segmentation: {founder_segmentation}, Idea Fit: {founder_idea_fit}")
            
            # Update progress - completed
            final_updates = self.update_progress(
                state={**state, **updates},
                status="completed",
                message="創業者分析が完了しました",
                data={
                    "segmentation": founder_segmentation,
                    "idea_fit": founder_idea_fit[0] if isinstance(founder_idea_fit, list) else founder_idea_fit
                }
            )
            
            # Merge updates
            updates["messages"].extend(final_updates["messages"])
            updates["analysis_state"]["progress"] = final_updates["analysis_state"]["progress"]
            
            return updates
            
        except Exception as e:
            return self.handle_error(state, e)