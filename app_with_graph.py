import streamlit as st
import sys
import os
import traceback
from typing import Any, Dict, List, Tuple, Optional
import time
from dataclasses import dataclass

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from graph import SSFFGraph


@dataclass
class UIComponents:
    """Container for UI components."""
    status_container: Any
    progress_details: Any
    results_container: Any
    progress_bar: Any
    elapsed_time: Any
    status_text: Any
    progress_placeholder: Any
    node_outputs_placeholder: Any


@dataclass
class AnalysisState:
    """Container for analysis state data."""
    node_results: Dict[str, Any]
    cumulative_state: Dict[str, Any]
    all_messages: List[Dict[str, Any]]
    node_outputs: Dict[str, Dict[str, Any]]
    completed_node_list: List[str]
    start_time: float


class MessageFormatter:
    """Handles message formatting for display."""
    
    @staticmethod
    def format_message(msg: dict) -> Tuple[str, str, dict]:
        """Format a message for display."""
        status = msg.get("status", "info")
        message = msg.get("message", "")
        data = msg.get("data", {})
        node = msg.get("node_name", "")
        
        # Add node name to message if available
        if node:
            message = f"[{node}] {message}"
        
        return status, message, data


class ProgressTracker:
    """Handles progress tracking and display."""
    
    def __init__(self, ui_components: UIComponents, graph: SSFFGraph):
        self.ui = ui_components
        self.graph = graph
        self.total_nodes = len(graph.node_names)
    
    def update_progress_bar(self, completed_nodes: int) -> None:
        """Update the progress bar."""
        progress_value = completed_nodes / self.total_nodes
        self.ui.progress_bar.progress(progress_value)
    
    def update_elapsed_time(self, start_time: float) -> None:
        """Update elapsed time display."""
        elapsed = time.time() - start_time
        self.ui.elapsed_time.text(f"⏱️ {elapsed:.1f}s")
    
    def display_progress_details(self, current_step: str, completed_nodes: List[str], progress: Dict[str, Any]) -> None:
        """Display detailed progress information."""
        with self.ui.progress_placeholder.container():
            # Show current step
            if current_step:
                st.write(f"🔄 **Currently processing:** {current_step}")
            
            # Show completed nodes
            if completed_nodes:
                st.write("**Completed nodes:**")
                for completed_node in completed_nodes:
                    st.success(f"✅ {completed_node}")
            
            # Show any errors
            if progress.get("status") == "error":
                st.error(f"❌ Error: {progress.get('error_message', 'Unknown error')}")


class NodeOutputRenderer:
    """Handles rendering of node outputs."""
    
    def __init__(self, ui_components: UIComponents):
        self.ui = ui_components
        self.formatter = MessageFormatter()
    
    def render_node_outputs(self, node_outputs: Dict[str, Dict[str, Any]], current_node: str) -> None:
        """Render all node outputs."""
        with self.ui.node_outputs_placeholder.container():
            for node, output_data in node_outputs.items():
                if output_data["messages"] or output_data["data"]:
                    with st.expander(f"🔍 {node.upper()} Node", expanded=(node == current_node)):
                        self._render_node_messages(output_data["messages"])
                        self._render_node_analysis_data(node, output_data["data"])
    
    def _render_node_messages(self, messages: List[Dict[str, Any]]) -> None:
        """Render messages for a specific node."""
        if messages:
            st.write("**Messages:**")
            for msg in messages:
                status, text, msg_data = self.formatter.format_message(msg)
                
                if status == "error":
                    st.error(f"❌ {text}")
                elif status == "completed":
                    st.success(f"✅ {text}")
                else:
                    st.info(f"ℹ️ {text}")
                
                if msg_data:
                    st.json(msg_data)
    
    def _render_node_analysis_data(self, node: str, data: Dict[str, Any]) -> None:
        """Render analysis data for a specific node."""
        if not data:
            return
        
        st.write("**Analysis Results:**")
        
        if node == "market":
            self._render_market_data(data)
        elif node == "product":
            self._render_product_data(data)
        elif node == "founder":
            self._render_founder_data(data)
        elif node == "vc_scout":
            self._render_vc_scout_data(data)
    
    def _render_market_data(self, data: Dict[str, Any]) -> None:
        """Render market analysis data."""
        if data.get("viability_score"):
            st.metric("Market Viability", f"{data['viability_score']}/10")
        if data.get("market_size"):
            st.write(f"**Market Size:** {data['market_size']}")
        if data.get("competition"):
            st.write(f"**Competition:** {data['competition']}")
    
    def _render_product_data(self, data: Dict[str, Any]) -> None:
        """Render product analysis data."""
        if data.get("potential_score"):
            st.metric("Product Potential", f"{data['potential_score']}/10")
        if data.get("innovation_score"):
            st.metric("Innovation Score", f"{data['innovation_score']}/10")
    
    def _render_founder_data(self, data: Dict[str, Any]) -> None:
        """Render founder analysis data."""
        if data.get("competency_score"):
            st.metric("Founder Competency", f"{data['competency_score']}/10")
        if data.get("segmentation"):
            st.write(f"**Segmentation:** L{data['segmentation']}")
    
    def _render_vc_scout_data(self, data: Dict[str, Any]) -> None:
        """Render VC scout analysis data."""
        if data.get("vc_prediction"):
            st.metric("VC Prediction", data["vc_prediction"])
        if data.get("categorization"):
            cat = data["categorization"]
            st.write(f"**Startup Type:** {cat.get('startup_type', 'N/A')}")
            st.write(f"**Industry:** {cat.get('industry', 'N/A')}")


class ErrorHandler:
    """Handles error display and messaging."""
    
    @staticmethod
    def display_analysis_error(error: Exception) -> None:
        """Display analysis error with helpful information."""
        st.error("❌ **Analysis Failed**")
        st.error(f"**Error:** {str(error)}")
        
        # Show user-friendly error information
        with st.expander("🔧 Technical Details (for debugging)", expanded=False):
            st.write("**Error Type:**", type(error).__name__)
            st.write("**Error Message:**", str(error))
            st.code(traceback.format_exc(), language="python")
        
        # Show helpful suggestions
        st.info("💡 **Suggestions:**")
        st.write("- Check if all required API keys are set in your `.env` file")
        st.write("- Verify the startup information format")
        st.write("- Try with a shorter description if the input is very long")
        st.write("- Check the console/logs for more detailed error information")


class FinalResultsRenderer:
    """Handles rendering of final analysis results."""
    
    @staticmethod
    def render(final_state: Dict[str, Any]) -> None:
        """Render final analysis results."""
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
            
            FinalResultsRenderer._render_summary_tab(tabs[0], final_state)
            FinalResultsRenderer._render_market_tab(tabs[1], final_state)
            FinalResultsRenderer._render_product_tab(tabs[2], final_state)
            FinalResultsRenderer._render_founder_tab(tabs[3], final_state)
            FinalResultsRenderer._render_vc_scout_tab(tabs[4], final_state)
            FinalResultsRenderer._render_details_tab(tabs[5], final_state)
            
        except Exception as e:
            st.error(f"Error setting up results display: {str(e)}")
    
    @staticmethod
    def _render_summary_tab(tab, final_state: Dict[str, Any]) -> None:
        """Render summary tab."""
        with tab:
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
    
    @staticmethod
    def _render_market_tab(tab, final_state: Dict[str, Any]) -> None:
        """Render market analysis tab."""
        with tab:
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
    
    @staticmethod
    def _render_product_tab(tab, final_state: Dict[str, Any]) -> None:
        """Render product analysis tab."""
        with tab:
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
    
    @staticmethod
    def _render_founder_tab(tab, final_state: Dict[str, Any]) -> None:
        """Render founder analysis tab."""
        with tab:
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
                            FinalResultsRenderer._render_founder_idea_fit(founder)
                    
                    st.write("**Analysis:**")
                    st.write(founder.get('analysis', 'N/A'))
                else:
                    st.info("No founder analysis data available")
            except Exception as e:
                st.error(f"Error displaying Founder Analysis: {str(e)}")
                with st.expander("Debug Info", expanded=False):
                    st.write(f"founder_analysis data: {final_state.get('founder_analysis', 'Not found')}")
    
    @staticmethod
    def _render_founder_idea_fit(founder: Dict[str, Any]) -> None:
        """Render founder-idea fit metric with error handling."""
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
    
    @staticmethod
    def _render_vc_scout_tab(tab, final_state: Dict[str, Any]) -> None:
        """Render VC scout tab."""
        with tab:
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
    
    @staticmethod
    def _render_details_tab(tab, final_state: Dict[str, Any]) -> None:
        """Render details tab."""
        with tab:
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
                            st.write(f"- {step}: Completed")


class StartupAnalyzer:
    """Main analyzer class that orchestrates the analysis process."""
    
    def __init__(self, graph: SSFFGraph):
        self.graph = graph
        self.error_handler = ErrorHandler()
    
    def analyze_with_stream(self, startup_info_str: str) -> None:
        """Analyze startup using the streaming graph workflow."""
        # Create UI components
        ui_components = self._create_ui_components()
        
        # Initialize analysis state
        analysis_state = AnalysisState(
            node_results={},
            cumulative_state={},
            all_messages=[],
            node_outputs={},
            completed_node_list=[],
            start_time=time.time()
        )
        
        # Initialize helpers
        progress_tracker = ProgressTracker(ui_components, self.graph)
        node_renderer = NodeOutputRenderer(ui_components)
        formatter = MessageFormatter()
        
        try:
            # Stream the analysis
            for step_output in self.graph.stream_analysis(startup_info_str):
                self._process_step_output(
                    step_output, 
                    analysis_state, 
                    progress_tracker, 
                    node_renderer, 
                    formatter
                )
            
            # Analysis complete
            self._finalize_analysis(analysis_state, ui_components)
            
        except Exception as e:
            self.error_handler.display_analysis_error(e)
    
    def _create_ui_components(self) -> UIComponents:
        """Create and setup UI components."""
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
        
        with progress_details:
            st.write("#### Detailed Progress")
            progress_placeholder = st.empty()
            st.write("---")
            st.write("#### Node Outputs:")
            node_outputs_placeholder = st.empty()
        
        return UIComponents(
            status_container=status_container,
            progress_details=progress_details,
            results_container=results_container,
            progress_bar=progress_bar,
            elapsed_time=elapsed_time,
            status_text=status_text,
            progress_placeholder=progress_placeholder,
            node_outputs_placeholder=node_outputs_placeholder
        )
    
    def _process_step_output(
        self, 
        step_output: Dict[str, Any], 
        analysis_state: AnalysisState,
        progress_tracker: ProgressTracker,
        node_renderer: NodeOutputRenderer,
        formatter: MessageFormatter
    ) -> None:
        """Process a single step output from the graph."""
        node_name = step_output.get("node", "")
        progress = step_output.get("progress", {})
        state = step_output.get("state", {})
        messages = step_output.get("messages", [])
        
        # Update timing
        progress_tracker.update_elapsed_time(analysis_state.start_time)
        
        # Update status
        current_step = progress.get("current_step", node_name)
        
        # Update progress bar and track completed nodes
        if node_name in self.graph.node_names and node_name not in analysis_state.completed_node_list:
            analysis_state.completed_node_list.append(node_name)
            progress_tracker.update_progress_bar(len(analysis_state.completed_node_list))
        
        # Store node results and update cumulative state
        analysis_state.node_results[node_name] = state
        if isinstance(state, dict):
            analysis_state.cumulative_state.update(state)
        
        # Store intermediate outputs for display
        self._store_node_outputs(node_name, messages, state, analysis_state)
        
        # Display progress details
        progress_tracker.display_progress_details(current_step, analysis_state.completed_node_list, progress)
        
        # Update node outputs display
        if messages:
            for msg in messages:
                msg["source_node"] = node_name
            analysis_state.all_messages.extend(messages)
        
        node_renderer.render_node_outputs(analysis_state.node_outputs, node_name)
    
    def _store_node_outputs(
        self, 
        node_name: str, 
        messages: List[Dict[str, Any]], 
        state: Dict[str, Any],
        analysis_state: AnalysisState
    ) -> None:
        """Store intermediate outputs for display."""
        if node_name not in analysis_state.node_outputs:
            analysis_state.node_outputs[node_name] = {"messages": [], "data": {}}
        
        if messages:
            analysis_state.node_outputs[node_name]["messages"].extend(messages)
        
        # Extract key analysis data for intermediate display
        if isinstance(state, dict):
            if node_name == "market" and state.get("market_analysis"):
                analysis_state.node_outputs[node_name]["data"] = state["market_analysis"]
            elif node_name == "product" and state.get("product_analysis"):
                analysis_state.node_outputs[node_name]["data"] = state["product_analysis"]
            elif node_name == "founder" and state.get("founder_analysis"):
                analysis_state.node_outputs[node_name]["data"] = state["founder_analysis"]
            elif node_name == "vc_scout" and (state.get("vc_scout_analysis") or state.get("vc_prediction")):
                analysis_state.node_outputs[node_name]["data"] = {
                    "vc_prediction": state.get("vc_prediction"),
                    "vc_scout_analysis": state.get("vc_scout_analysis"),
                    "categorization": state.get("categorization")
                }
    
    def _finalize_analysis(self, analysis_state: AnalysisState, ui_components: UIComponents) -> None:
        """Finalize the analysis and display results."""
        # Analysis complete
        elapsed = time.time() - analysis_state.start_time
        ui_components.elapsed_time.text(f"✅ {elapsed:.1f}s")
        ui_components.status_text.text("✅ Analysis Complete!")
        ui_components.progress_bar.progress(1.0)
        
        # Prepare final state
        final_state = analysis_state.cumulative_state.copy()
        integration_state = analysis_state.node_results.get("integration", {})
        if integration_state and isinstance(integration_state, dict):
            final_state.update(integration_state)
        
        # Display final results
        with ui_components.results_container:
            FinalResultsRenderer.render(final_state)
        
        # Show complete message log
        self._show_complete_message_log(analysis_state.all_messages)
    
    def _show_complete_message_log(self, all_messages: List[Dict[str, Any]]) -> None:
        """Show complete message log."""
        formatter = MessageFormatter()
        with st.expander("Complete Message Log", expanded=False):
            for i, msg in enumerate(all_messages):
                status, text, data = formatter.format_message(msg)
                source_node = msg.get("source_node", "unknown")
                st.write(f"{i+1}. **[{source_node}]** [{status}] {text}")
                if data:
                    st.json(data)


class StartupAnalysisApp:
    """Main application class for Startup Success Forecasting Framework."""
    
    def __init__(self):
        self.graph = None
        self._initialize_graph()
    
    def _initialize_graph(self) -> None:
        """Initialize the SSFFGraph instance."""
        if 'graph' not in st.session_state:
            st.session_state.graph = SSFFGraph()
        self.graph = st.session_state.graph
    
    def render_header(self) -> None:
        """Render the application header."""
        st.title("Startup Success Forecasting Framework")
        st.markdown("This version uses the LangGraph workflow for analysis with enhanced progress tracking.")
    
    def render_input_section(self) -> Optional[str]:
        """Render input section and return startup info if submitted."""
        startup_info_str = st.text_area(
            "Enter Startup Information", 
            height=200,
            help="Provide a detailed description of the startup, including information about the product, market, founders, and any other relevant details."
        )
        
        if st.button("Analyze Startup"):
            if startup_info_str:
                return startup_info_str
            else:
                st.warning("Please enter startup information before analyzing.")
        return None
    
    def run(self) -> None:
        """Main application entry point."""
        self.render_header()
        startup_info = self.render_input_section()
        
        if startup_info:
            analyzer = StartupAnalyzer(self.graph)
            analyzer.analyze_with_stream(startup_info)


def main() -> None:
    """Application entry point."""
    app = StartupAnalysisApp()
    app.run()


if __name__ == "__main__":
    main()
