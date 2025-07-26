import streamlit as st
import sys
import os
import traceback
from typing import Any
import time

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from graph import SSFFGraph

def main() -> None:
    st.title("Startup Success Forecasting Framework (LangGraph)")
    st.markdown("This version uses the LangGraph workflow for analysis with enhanced progress tracking.")

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

def format_message(msg: dict) -> tuple[str, str, dict]:
    """Format a message for display."""
    status = msg.get("status", "info")
    message = msg.get("message", "")
    data = msg.get("data", {})
    node = msg.get("node_name", "")
    
    # Add node name to message if available
    if node:
        message = f"[{node}] {message}"
    
    return status, message, data

def analyze_startup_with_stream(
    graph: SSFFGraph,
    startup_info_str: str,
) -> None:
    """Analyze startup uszing the streaming graph workflow with enhanced UI."""
    
    # Create containers for dynamic updates
    status_container = st.container()
    progress_details = st.container()
    results_container = st.container()
    
    with status_container:
        st.write("### Analysis in Progress")
        col1, col2 = st.columns([3, 1])
        with col1:
            progress_bar = st.progress(0)
        with col2:
            elapsed_time = st.empty()
        status_text = st.empty()
    
    # Create containers for detailed progress
    with progress_details:
        st.write("#### Detailed Progress")
        progress_placeholder = st.empty()
        st.write("---")
        st.write("#### Node Outputs:")
        node_outputs_placeholder = st.empty()
    
    # Track timing
    start_time = time.time()
    
    # Track nodes for progress calculation
    total_nodes = len(graph.node_names)
    completed_nodes = 0
    completed_node_list = []  # Track completed nodes in order
    
    # Store results from each node and maintain cumulative state
    node_results = {}
    cumulative_state = {}
    all_messages = []
    node_outputs = {}  # Store intermediate outputs by node
    
    try:
        # Stream the analysis
        for step_output in graph.stream_analysis(startup_info_str):
            node_name = step_output.get("node", "")
            progress = step_output.get("progress", {})
            state = step_output.get("state", {})
            messages = step_output.get("messages", [])
            
            # Update elapsed time
            elapsed = time.time() - start_time
            elapsed_time.text(f"⏱️ {elapsed:.1f}s")
            
            # Update status
            current_step = progress.get("current_step", node_name)
            
            # Update progress bar and track completed nodes
            if node_name in graph.node_names and node_name not in completed_node_list:
                completed_node_list.append(node_name)
                completed_nodes = len(completed_node_list)
                progress_value = completed_nodes / total_nodes
                progress_bar.progress(progress_value)
            
            # Store node results and update cumulative state
            node_results[node_name] = state
            if isinstance(state, dict):
                cumulative_state.update(state)
            
            # Store intermediate outputs for display
            if node_name not in node_outputs:
                node_outputs[node_name] = {"messages": [], "data": {}}
            
            if messages:
                node_outputs[node_name]["messages"].extend(messages)
            
            # Extract key analysis data for intermediate display
            if isinstance(state, dict):
                if node_name == "market" and state.get("market_analysis"):
                    node_outputs[node_name]["data"] = state["market_analysis"]
                elif node_name == "product" and state.get("product_analysis"):
                    node_outputs[node_name]["data"] = state["product_analysis"]
                elif node_name == "founder" and state.get("founder_analysis"):
                    node_outputs[node_name]["data"] = state["founder_analysis"]
                elif node_name == "vc_scout" and (state.get("vc_scout_analysis") or state.get("vc_prediction")):
                    node_outputs[node_name]["data"] = {
                        "vc_prediction": state.get("vc_prediction"),
                        "vc_scout_analysis": state.get("vc_scout_analysis"),
                        "categorization": state.get("categorization")
                    }
            
            # Display progress in the placeholder (this will update the same UI element)
            with progress_placeholder.container():
                # Show current step
                if current_step:
                    st.write(f"🔄 **Currently processing:** {current_step}")
                
                # Show completed nodes
                if completed_node_list:
                    st.write("**Completed nodes:**")
                    for completed_node in completed_node_list:
                        st.success(f"✅ {completed_node}")
                
                # Show any errors
                if progress.get("status") == "error":
                    st.error(f"❌ Error: {progress.get('error_message', 'Unknown error')}")
            
            # Update node outputs display
            if messages:
                # Add node name to messages before storing
                for msg in messages:
                    msg["source_node"] = node_name
                all_messages.extend(messages)
            
            # Always update the node outputs display (whether there are new messages or not)
            with node_outputs_placeholder.container():
                # Display outputs for each completed node
                for node, output_data in node_outputs.items():
                    if output_data["messages"] or output_data["data"]:
                        with st.expander(f"🔍 {node.upper()} Node", expanded=(node == node_name)):
                            
                            # Show all messages for this node (always display)
                            if output_data["messages"]:
                                st.write("**Messages:**")
                                for i, msg in enumerate(output_data["messages"]):
                                    status, text, msg_data = format_message(msg)
                                    
                                    if status == "error":
                                        st.error(f"❌ {text}")
                                    elif status == "completed":
                                        st.success(f"✅ {text}")
                                    else:
                                        st.info(f"ℹ️ {text}")
                                    
                                    # Show message data if available
                                    if msg_data:
                                        st.json(msg_data)
                            
                            # Show key analysis data
                            if output_data["data"]:
                                st.write("**Analysis Results:**")
                                data = output_data["data"]
                                
                                if node == "market":
                                    if data.get("viability_score"):
                                        st.metric("Market Viability", f"{data['viability_score']}/10")
                                    if data.get("market_size"):
                                        st.write(f"**Market Size:** {data['market_size']}")
                                    if data.get("competition"):
                                        st.write(f"**Competition:** {data['competition']}")
                                        
                                elif node == "product":
                                    if data.get("potential_score"):
                                        st.metric("Product Potential", f"{data['potential_score']}/10")
                                    if data.get("innovation_score"):
                                        st.metric("Innovation Score", f"{data['innovation_score']}/10")
                                        
                                elif node == "founder":
                                    if data.get("competency_score"):
                                        st.metric("Founder Competency", f"{data['competency_score']}/10")
                                    if data.get("segmentation"):
                                        st.write(f"**Segmentation:** L{data['segmentation']}")
                                        
                                elif node == "vc_scout":
                                    if data.get("vc_prediction"):
                                        st.metric("VC Prediction", data["vc_prediction"])
                                    if data.get("categorization"):
                                        cat = data["categorization"]
                                        st.write(f"**Startup Type:** {cat.get('startup_type', 'N/A')}")
                                        st.write(f"**Industry:** {cat.get('industry', 'N/A')}")
            
            # Show node-specific results
            if node_name == "vc_scout" and state.get("vc_prediction"):
                with progress_placeholder.container():
                    st.write("---")
                    st.write(f"**Initial VC Prediction:** {state['vc_prediction']}")
        
        # Analysis complete
        elapsed = time.time() - start_time
        elapsed_time.text(f"✅ {elapsed:.1f}s")
        status_text.text("✅ Analysis Complete!")
        progress_bar.progress(1.0)
        
        # Use cumulative state which contains all analysis results
        final_state = cumulative_state.copy()
        
        # Ensure integration state takes precedence for any overlapping keys
        integration_state = node_results.get("integration", {})
        if integration_state and isinstance(integration_state, dict):
            final_state.update(integration_state)
        
        # Display final results
        with results_container:
            display_final_results(final_state)
        
        # Show complete message log
        with st.expander("Complete Message Log", expanded=False):
            for i, msg in enumerate(all_messages):
                status, text, data = format_message(msg)
                source_node = msg.get("source_node", "unknown")
                st.write(f"{i+1}. **[{source_node}]** [{status}] {text}")
                if data:
                    st.json(data)
            
    except Exception as e:
        st.error("❌ **Analysis Failed**")
        st.error(f"**Error:** {str(e)}")
        
        # Show user-friendly error information
        with st.expander("🔧 Technical Details (for debugging)", expanded=False):
            st.write("**Error Type:**", type(e).__name__)
            st.write("**Error Message:**", str(e))
            st.code(traceback.format_exc(), language="python")
        
        # Show helpful suggestions
        st.info("💡 **Suggestions:**")
        st.write("- Check if all required API keys are set in your `.env` file")
        st.write("- Verify the startup information format")
        st.write("- Try with a shorter description if the input is very long")
        st.write("- Check the console/logs for more detailed error information")

def display_final_results(final_state: dict[str, Any]) -> None:
    """Display the final analysis results."""
    try:
        st.subheader("Final Analysis Results")
        
        # Debug: Show what keys are available in final_state
        with st.expander("Debug: Available Keys in Final State", expanded=False):
            st.write("Keys in final_state:")
            for key, value in final_state.items():
                if isinstance(value, dict) and value:
                    st.write(f"✅ **{key}**: {type(value)} (has data)")
                elif value:
                    st.write(f"✅ **{key}**: {type(value)} = {value}")
                else:
                    st.write(f"❌ **{key}**: {type(value)} (empty/None)")
        
        # Create tabs for different sections
        tabs = st.tabs(["Summary", "Market Analysis", "Product Analysis", "Founder Analysis", "VC Scout", "Details"])
    except Exception as e:
        st.error(f"Error setting up results display: {str(e)}")
        return
    
    with tabs[0]:  # Summary
        if final_state.get("integrated_analysis"):
            integrated = final_state["integrated_analysis"]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Score", f"{integrated.get('overall_score', 'N/A')}/10")
            with col2:
                outcome = integrated.get('outcome', 'N/A')
                st.metric("Outcome", outcome, delta="Positive" if outcome == "Pass" else "Review")
            with col3:
                if final_state.get("quantitative_decision"):
                    prob = final_state["quantitative_decision"].get('probability', 0)
                    st.metric("Success Probability", f"{prob:.2%}")
            
            st.write("### Recommendation")
            st.info(integrated.get('recommendation', 'N/A'))
            
            st.write("### Integrated Analysis")
            st.write(integrated.get('IntegratedAnalysis', 'N/A'))
    
    with tabs[1]:  # Market Analysis
        if final_state.get("market_analysis"):
            market = final_state["market_analysis"]
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Market Size", market.get('market_size', 'N/A'))
                st.metric("Competition", market.get('competition', 'N/A'))
            with col2:
                st.metric("Growth Rate", market.get('growth_rate', 'N/A'))
                st.metric("Viability Score", f"{market.get('viability_score', 'N/A')}/10")
            
            st.write("**Market Trends:**")
            st.write(market.get('market_trends', 'N/A'))
    
    with tabs[2]:  # Product Analysis
        if final_state.get("product_analysis"):
            product = final_state["product_analysis"]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Potential Score", f"{product.get('potential_score', 'N/A')}/10")
            with col2:
                st.metric("Innovation Score", f"{product.get('innovation_score', 'N/A')}/10")
            with col3:
                st.metric("Market Fit Score", f"{product.get('market_fit_score', 'N/A')}/10")
            
            st.write("**Features Analysis:**")
            st.write(product.get('features_analysis', 'N/A'))
            
            st.write("**Tech Stack Evaluation:**")
            st.write(product.get('tech_stack_evaluation', 'N/A'))
            
            st.write("**USP Assessment:**")
            st.write(product.get('usp_assessment', 'N/A'))
    
    with tabs[3]:  # Founder Analysis
        try:
            if final_state.get("founder_analysis"):
                founder = final_state["founder_analysis"]
                
                st.metric("Competency Score", f"{founder.get('competency_score', 'N/A')}/10")
                
                # Check for advanced founder analysis
                if founder.get("segmentation"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Founder Segmentation", f"L{founder['segmentation']}")
                    with col2:
                        idea_fit = founder.get("idea_fit", (0.0, 0.0))
                        try:
                            if isinstance(idea_fit, tuple) and len(idea_fit) > 0:
                                # Handle nested tuples or other complex structures
                                fit_item = idea_fit[0]
                                if isinstance(fit_item, (int, float)):
                                    fit_value = float(fit_item)
                                    st.metric("Founder-Idea Fit", f"{fit_value:.4f}")
                                elif isinstance(fit_item, tuple) and len(fit_item) > 0:
                                    # Handle double-nested tuple
                                    fit_value = float(fit_item[0])
                                    st.metric("Founder-Idea Fit", f"{fit_value:.4f}")
                                else:
                                    st.write(f"**Founder-Idea Fit:** {fit_item} (type: {type(fit_item)})")
                            elif isinstance(idea_fit, (int, float)):
                                st.metric("Founder-Idea Fit", f"{float(idea_fit):.4f}")
                            else:
                                st.write(f"**Founder-Idea Fit:** {idea_fit} (type: {type(idea_fit)})")
                        except Exception as e:
                            st.error(f"Error displaying Founder-Idea Fit: {str(e)}")
                            st.write(f"**Debug - idea_fit value:** {idea_fit}")
                            st.write(f"**Debug - idea_fit type:** {type(idea_fit)}")
                
                st.write("**Analysis:**")
                st.write(founder.get('analysis', 'N/A'))
            else:
                st.info("No founder analysis data available")
        except Exception as e:
            st.error(f"Error displaying Founder Analysis: {str(e)}")
            with st.expander("Debug Info", expanded=False):
                st.write(f"founder_analysis data: {final_state.get('founder_analysis', 'Not found')}")
    
    with tabs[4]:  # VC Scout
        if final_state.get("vc_prediction"):
            st.metric("VC Prediction", final_state['vc_prediction'])
        
        if final_state.get("categorization"):
            st.write("### Startup Categorization")
            categorization = final_state["categorization"]
            
            # Display categorization in a grid
            cols = st.columns(2)
            items = list(categorization.items())
            for i, (key, value) in enumerate(items):
                with cols[i % 2]:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        if final_state.get("vc_scout_analysis"):
            st.write("### VC Scout Analysis")
            vc_scout = final_state["vc_scout_analysis"]
            st.write(f"**Investment Viability:** {vc_scout.get('investment_viability', 'N/A')}")
            st.write(f"**Risk Assessment:** {vc_scout.get('risk_assessment', 'N/A')}")
            if vc_scout.get('key_insights'):
                st.write("**Key Insights:**")
                for insight in vc_scout['key_insights']:
                    st.write(f"- {insight}")
    
    with tabs[5]:  # Details
        if final_state.get("quantitative_decision"):
            st.write("### Quantitative Decision")
            quant = final_state["quantitative_decision"]
            st.write(f"**Outcome:** {quant.get('outcome', 'N/A')}")
            st.write(f"**Probability:** {quant.get('probability', 0):.2%}")
            st.write(f"**Reasoning:** {quant.get('reasoning', 'N/A')}")
        
        if final_state.get("progress"):
            st.write("### Analysis Progress Summary")
            progress = final_state["progress"]
            st.write(f"**Status:** {progress.get('status', 'N/A')}")
            st.write(f"**Completed Steps:** {', '.join(progress.get('completed_steps', []))}")
            
            # Show step timings if available
            if progress.get("step_times"):
                step_times = progress["step_times"]
                st.write("**Step Timings:**")
                for step, times in step_times.items():
                    if isinstance(times, dict) and "start" in times and "end" in times:
                        # Note: In real implementation, you'd calculate actual time difference
                        st.write(f"- {step}: Completed")

if __name__ == "__main__":
    main()
