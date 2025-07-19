import logging
from typing import Any, Generator
from datetime import datetime
from langgraph.graph import StateGraph, START, END
from nodes import (
    ParseNode,
    MarketNode,
    ProductNode,
    FounderNode,
    VCScoutNode,
    IntegrationNode
)
from states.overall_state import OverallState
from shared.types import ProgressDict


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SSFFGraph:
    def __init__(self):
        self.graph = None
        self.node_names = ["parse", "market", "product", "founder", "vc_scout", "integration"]
        self._build_graph()
    
    def _build_graph(self):
        # Create workflow
        workflow = StateGraph(OverallState)
        
        # Add nodes
        workflow.add_node("parse", ParseNode())
        workflow.add_node("market", MarketNode())
        workflow.add_node("product", ProductNode())
        workflow.add_node("founder", FounderNode())
        workflow.add_node("vc_scout", VCScoutNode())
        workflow.add_node("integration", IntegrationNode())
        
        # Define the workflow edges - parallel execution after parse
        workflow.add_edge(START, "parse")
        
        # Parallel execution of all analysis nodes
        workflow.add_edge("parse", "market")
        workflow.add_edge("parse", "product")
        workflow.add_edge("parse", "founder")
        workflow.add_edge("parse", "vc_scout")
        
        # Integration waits for all parallel nodes to complete
        workflow.add_edge("market", "integration")
        workflow.add_edge("product", "integration")
        workflow.add_edge("founder", "integration")
        workflow.add_edge("vc_scout", "integration")
        workflow.add_edge("integration", END)
        
        # Compile the graph
        self.graph = workflow.compile()
        logger.info("SSFF LangGraph workflow compiled successfully")
    
    def create_initial_state(
        self,
        startup_info_str: str,
    ) -> OverallState:
        """Create initial state for the workflow."""
        return OverallState(
            messages=[],
            startup_info_str=startup_info_str,
            startup_info={},
            market_analysis=None,
            product_analysis=None,
            founder_analysis=None,
            vc_prediction=None,
            categorization=None,
            vc_scout_analysis=None,
            integrated_analysis=None,
            integrated_analysis_basic=None,
            quantitative_decision=None,
            progress=ProgressDict(
                current_step="",
                completed_steps=[],
                start_time=datetime.now(),
                step_times={},
                status="running",
                error_message=None
            ),
            next_step=None,
            should_continue=True
        )

    def run_analysis(self, startup_info_str: str) -> dict[str, Any]:
        """Run the complete SSFF analysis workflow."""
        if self.graph is None:
            raise RuntimeError("Graph not initialized. Please install langgraph.")
        
        # Create initial state
        initial_state = self.create_initial_state(startup_info_str)
        
        # Run the workflow
        final_state = self.graph.invoke(initial_state)
        
        # Extract and format results
        result = {
            'Final Analysis': final_state.get("integrated_analysis", {}),
            'Market Analysis': final_state.get("market_analysis", {}),
            'Product Analysis': final_state.get("product_analysis", {}),
            'Founder Analysis': final_state.get("founder_analysis", {}),
            'VC Scout Analysis': final_state.get("vc_scout_analysis", {}),
            'Categorical Prediction': final_state.get("vc_prediction", ""),
            'Categorization': final_state.get("categorization", {}),
            'Quantitative Decision': final_state.get("quantitative_decision", {}),
            'Startup Info': final_state.get("startup_info", {}),
            'Basic Analysis': final_state.get("integrated_analysis_basic", {}),
            'Progress': final_state.get("progress", {}),
            'Messages': final_state.get("messages", [])
        }
        logger.info("SSFF analysis completed successfully")
        return result

    def stream_analysis(self, startup_info_str: str) -> Generator[dict[str, Any], None, None]:
        """Stream the SSFF analysis workflow with progress updates."""
        if self.graph is None:
            raise RuntimeError("Graph not initialized. Please install langgraph.")
        
        # Create initial state
        initial_state = self.create_initial_state(startup_info_str)
        
        # Stream the workflow
        for step_output in self.graph.stream(initial_state):
            # Extract progress information
            if isinstance(step_output, dict):
                # LangGraph returns {node_name: node_output}
                for node_name, node_output in step_output.items():
                    if isinstance(node_output, dict):
                        progress = node_output.get("progress", {})
                        messages = node_output.get("messages", [])
                        
                        yield {
                            "node": node_name,
                            "progress": progress,
                            "messages": messages,
                            "state": node_output
                        }


if __name__ == "__main__":
    # Test the graph
    test_startup_info = """
    Turismocity is a travel search engine for Latin America that provides price comparison tools and travel deals. 
    Eugenio Fage, the CTO and co-founder, has a background in software engineering and extensive experience in developing travel technology solutions.
    """
    
    try:
        print("Testing SSFF LangGraph workflow...")
        graph = SSFFGraph()
        
        print("\nRunning analysis...")
        result = graph.run_analysis(test_startup_info)
        
        print("\nAnalysis completed!")
        print(f"Founder Segmentation: {result.get('Founder Segmentation', 'N/A')}")
        print(f"Prediction: {result.get('Categorical Prediction', 'N/A')}")
        print(f"Progress: {result.get('Progress', {}).get('status', 'N/A')}")
        
    except Exception as e:
        print(f"Error testing graph: {e}")
        import traceback
        traceback.print_exc()
