import streamlit as st
import sys
import os
import traceback
from typing import Any, Optional
import time

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from graph import SSFFGraph

def main() -> None:
    st.title("Startup Success Forecasting Framework (LangGraph)")
    st.markdown("This version uses the LangGraph workflow for analysis.")

    # Initialize the SSFFGraph
    if 'graph' not in st.session_state:
        st.session_state.graph = SSFFGraph()

    # Input field for startup information
    startup_info_str = st.text_area(
        "Enter Startup Information", 
        height=200,
        help="Provide a detailed description of the startup, including information about the product, market, founders, and any other relevant details."
    )

    if st.button("Analyze Startup"):
        if startup_info_str:
            analyze_startup_with_stream(st.session_state.graph, startup_info_str)
        else:
            st.warning("Please enter startup information before analyzing.")

def analyze_startup_with_stream(
    graph: SSFFGraph,
    startup_info_str: str,
) -> None:
    """Analyze startup using the streaming graph workflow."""
    
    # Create containers for dynamic updates
    status_container = st.container()
    progress_container = st.container()
    results_container = st.container()
    
    with status_container:
        st.write("### Analysis in Progress")
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    # Track nodes for progress calculation
    total_nodes = len(graph.node_names)
    completed_nodes = 0
    
    # Store results from each node
    node_results = {}
    
    try:
        # Stream the analysis
        for step_output in graph.stream_analysis(startup_info_str):
            node_name = step_output.get("node", "")
            progress = step_output.get("progress", {})
            state = step_output.get("state", {})
            
            # Update status
            current_step = progress.get("current_step", node_name)
            status_text.text(f"Current Step: {current_step}")
            
            # Update progress bar
            if node_name in graph.node_names:
                completed_nodes += 1
                progress_value = completed_nodes / total_nodes
                progress_bar.progress(progress_value)
            
            # Store node results
            node_results[node_name] = state
            
            # Display intermediate results
            with progress_container:
                if node_name == "parse":
                    st.write(" Startup information parsed")
                elif node_name == "market":
                    st.write(" Market analysis complete")
                elif node_name == "product":
                    st.write(" Product analysis complete")
                elif node_name == "founder":
                    st.write(" Founder analysis complete")
                elif node_name == "vc_scout":
                    st.write(" VC Scout evaluation complete")
                    if state.get("vc_prediction"):
                        st.write(f"Initial Prediction: {state['vc_prediction']}")
                elif node_name == "integration":
                    st.write(" Integration complete")
        
        # Analysis complete
        status_text.text("Analysis Complete!")
        progress_bar.progress(1.0)
        
        # Extract final state from integration node
        final_state = node_results.get("integration", {})
        
        # Display final results
        with results_container:
            display_final_results(final_state)
            
    except Exception as e:
        st.error(f"An error occurred during analysis: {str(e)}")
        st.write(traceback.format_exc())

def display_final_results(final_state: dict[str, Any]) -> None:
    """Display the final analysis results."""
    st.subheader("Final Analysis Results")
    
    # Display Integrated Analysis
    if final_state.get("integrated_analysis"):
        st.write("### Final Decision")
        integrated = final_state["integrated_analysis"]
        st.write(f"**Overall Score:** {integrated.get('overall_score', 'N/A')}/10")
        st.write(f"**Outcome:** {integrated.get('outcome', 'N/A')}")
        st.write(f"**Recommendation:** {integrated.get('recommendation', 'N/A')}")
        st.write("**Integrated Analysis:**")
        st.write(integrated.get('IntegratedAnalysis', 'N/A'))
    
    # Display Market Analysis
    if final_state.get("market_analysis"):
        st.write("### Market Information")
        market = final_state["market_analysis"]
        st.write(f"**Market Size:** {market.get('market_size', 'N/A')}")
        st.write(f"**Growth Rate:** {market.get('growth_rate', 'N/A')}")
        st.write(f"**Competition:** {market.get('competition', 'N/A')}")
        st.write(f"**Market Trends:** {market.get('market_trends', 'N/A')}")
        st.write(f"**Viability Score:** {market.get('viability_score', 'N/A')}/10")
    
    # Display Product Analysis
    if final_state.get("product_analysis"):
        st.write("### Product Information")
        product = final_state["product_analysis"]
        st.write(f"**Features Analysis:** {product.get('features_analysis', 'N/A')}")
        st.write(f"**Tech Stack Evaluation:** {product.get('tech_stack_evaluation', 'N/A')}")
        st.write(f"**USP Assessment:** {product.get('usp_assessment', 'N/A')}")
        st.write(f"**Potential Score:** {product.get('potential_score', 'N/A')}/10")
        st.write(f"**Innovation Score:** {product.get('innovation_score', 'N/A')}/10")
        st.write(f"**Market Fit Score:** {product.get('market_fit_score', 'N/A')}/10")
    
    # Display Founder Analysis
    if final_state.get("founder_analysis"):
        st.write("### Founder Information")
        founder = final_state["founder_analysis"]
        st.write(f"**Competency Score:** {founder.get('competency_score', 'N/A')}/10")
        st.write("**Analysis:**")
        st.write(founder.get('analysis', 'N/A'))
        
        # Advanced founder analysis if available
        if founder.get("founder_segmentation"):
            st.write(f"**Founder Segmentation:** L{founder['founder_segmentation']}")
        if founder.get("founder_idea_fit"):
            st.write(f"**Founder Idea Fit:** {founder['founder_idea_fit']:.4f}")
    
    # Display VC Scout Analysis
    if final_state.get("vc_scout_analysis"):
        st.write("### VC Scout Analysis")
        vc_scout = final_state["vc_scout_analysis"]
        st.write(f"**Investment Viability:** {vc_scout.get('investment_viability', 'N/A')}")
        st.write(f"**Risk Assessment:** {vc_scout.get('risk_assessment', 'N/A')}")
        st.write("**Key Insights:**")
        for insight in vc_scout.get('key_insights', []):
            st.write(f"- {insight}")
    
    # Display Prediction and Categorization
    if final_state.get("vc_prediction"):
        st.write("### Prediction and Categorization")
        st.write(f"**Prediction:** {final_state['vc_prediction']}")
        
        if final_state.get("categorization"):
            st.write("**Categorization:**")
            for key, value in final_state["categorization"].items():
                st.write(f"- {key}: {value}")
    
    # Display Quantitative Decision
    if final_state.get("quantitative_decision"):
        st.write("### Quantitative Decision")
        quant = final_state["quantitative_decision"]
        st.write(f"**Outcome:** {quant.get('outcome', 'N/A')}")
        st.write(f"**Probability:** {quant.get('probability', 0):.2%}")
        st.write(f"**Reasoning:** {quant.get('reasoning', 'N/A')}")
    
    # Display Progress Information
    if final_state.get("progress"):
        st.write("### Analysis Progress")
        progress = final_state["progress"]
        st.write(f"**Status:** {progress.get('status', 'N/A')}")
        st.write(f"**Completed Steps:** {', '.join(progress.get('completed_steps', []))}")
        
        # Calculate and display total time
        if progress.get("start_time") and progress.get("step_times"):
            start_time = progress["start_time"]
            step_times = progress["step_times"]
            if step_times and isinstance(step_times, dict):
                # Find the latest end time
                latest_end = None
                for step, times in step_times.items():
                    if isinstance(times, dict) and "end" in times:
                        if latest_end is None or times["end"] > latest_end:
                            latest_end = times["end"]
                
                if latest_end and start_time:
                    # Note: This is a placeholder for actual time calculation
                    st.write("**Total Analysis Time:** Calculated based on timestamps")

if __name__ == "__main__":
    main()
