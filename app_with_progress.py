import streamlit as st
import time
from typing import Any
from graph import SSFFGraph


def display_progress_bar(progress_state: dict[str, Any]) -> None:
    """Display progress bar and current status."""
    
    # Define step mapping for progress calculation
    step_order = ["parse", "market", "product", "founder", "vc_scout", "integration"]
    step_names = {
        "parse": "📄 スタートアップ情報解析",
        "market": "🌍 市場分析",
        "product": "🚀 プロダクト分析", 
        "founder": "👥 創業者分析",
        "vc_scout": "💼 VC評価・ML予測",
        "integration": "🔄 統合分析"
    }
    
    current_step = progress_state.get("current_step", "")
    completed_steps = progress_state.get("completed_steps", [])
    status = progress_state.get("status", "running")
    
    # Calculate progress percentage
    if status == "completed":
        progress_pct = 1.0
    elif current_step in step_order:
        current_index = step_order.index(current_step)
        progress_pct = (current_index + 0.5) / len(step_order)
    else:
        progress_pct = len(completed_steps) / len(step_order)
    
    # Display progress bar
    st.progress(progress_pct)
    
    # Display current status
    if status == "error":
        st.error(f"❌ エラー: {progress_state.get('error_message', '不明なエラー')}")
    elif status == "completed":
        st.success("✅ 分析完了!")
    else:
        current_step_name = step_names.get(current_step, current_step)
        st.info(f"🔄 実行中: {current_step_name}")
    
    # Display step checklist
    st.write("**進捗状況:**")
    for step in step_order:
        step_name = step_names[step]
        if step in completed_steps:
            st.write(f"✅ {step_name}")
        elif step == current_step:
            st.write(f"🔄 {step_name}")
        else:
            st.write(f"⏳ {step_name}")

def display_intermediate_results(results: dict[str, Any]) -> None:
    """Display intermediate analysis results."""
    
    # Market Analysis
    if results.get("Market Analysis"):
        with st.expander("🌍 市場分析結果", expanded=False):
            market_data = results["Market Analysis"]
            if isinstance(market_data, dict) and "analysis" in market_data:
                st.write(market_data["analysis"])
                if market_data.get("external_report"):
                    st.write("**外部調査レポート:**")
                    st.write(market_data["external_report"])
            else:
                st.json(market_data)
    
    # Product Analysis
    if results.get("Product Analysis"):
        with st.expander("🚀 プロダクト分析結果", expanded=False):
            product_data = results["Product Analysis"]
            if isinstance(product_data, dict) and "analysis" in product_data:
                st.write(product_data["analysis"])
                if product_data.get("external_report"):
                    st.write("**外部調査レポート:**")
                    st.write(product_data["external_report"])
            else:
                st.json(product_data)
    
    # Founder Analysis
    if results.get("Founder Analysis"):
        with st.expander("👥 創業者分析結果", expanded=False):
            st.json(results["Founder Analysis"])
            
            col1, col2 = st.columns(2)
            with col1:
                if results.get("Founder Segmentation"):
                    st.metric("創業者セグメント", results["Founder Segmentation"])
            with col2:
                if results.get("Founder Idea Fit"):
                    st.metric("アイデア適合度", f"{results['Founder Idea Fit']:.3f}")
    
    # VC Prediction
    if results.get("Categorical Prediction"):
        with st.expander("💼 VC評価結果", expanded=False):
            prediction = results["Categorical Prediction"]
            
            if prediction == "Successful":
                st.success(f"🎯 予測結果: {prediction}")
            else:
                st.warning(f"🎯 予測結果: {prediction}")
                
            if results.get("Categorization"):
                st.json(results["Categorization"])

def run_langgraph_analysis(startup_info: str, progress_container, results_container):
    """Run analysis using LangGraph with progress updates."""
    try:
        graph = SSFFGraph()
        
        # Stream the analysis
        for step_output in graph.stream_analysis(startup_info):
            progress = step_output.get("progress", {})
            state = step_output.get("state", {})
            
            # Update progress display
            with progress_container.container():
                display_progress_bar(progress)
            
            # Update intermediate results
            with results_container.container():
                # Create results dict from state
                results = {
                    'Market Analysis': state.get("market_analysis"),
                    'Product Analysis': state.get("product_analysis"),
                    'Founder Analysis': state.get("founder_analysis"),
                    'Founder Segmentation': state.get("founder_segmentation"),
                    'Founder Idea Fit': state.get("founder_idea_fit"),
                    'Categorical Prediction': state.get("vc_prediction"),
                    'Categorization': state.get("categorization")
                }
                display_intermediate_results(results)
            
            # Small delay to make progress visible
            time.sleep(0.5)
        
        # Final results
        final_result = graph.run_analysis(startup_info)
        return final_result
        
    except Exception as e:
        st.error(f"LangGraph分析エラー: {str(e)}")
        return None


def display_final_results(result: dict[str, Any]):
    """Display final analysis results."""
    if not result:
        return
    
    st.header("📊 最終分析結果")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if result.get("Founder Segmentation"):
            st.metric("創業者セグメント", result["Founder Segmentation"])
    
    with col2:
        if result.get("Categorical Prediction"):
            prediction = result["Categorical Prediction"]
            if prediction == "Successful":
                st.metric("成功予測", prediction, delta="Good")
            else:
                st.metric("成功予測", prediction, delta="Risk")
    
    with col3:
        if result.get("Founder Idea Fit"):
            fit_score = result["Founder Idea Fit"]
            st.metric("アイデア適合度", f"{fit_score:.3f}")
    
    # Detailed analyses
    tabs = st.tabs(["📈 統合分析", "🌍 市場分析", "🚀 プロダクト分析", "👥 創業者分析", "🔢 定量的判定"])
    
    with tabs[0]:
        if result.get("Final Analysis"):
            st.json(result["Final Analysis"])
    
    with tabs[1]:
        if result.get("Market Analysis"):
            st.json(result["Market Analysis"])
    
    with tabs[2]:
        if result.get("Product Analysis"):
            st.json(result["Product Analysis"])
    
    with tabs[3]:
        if result.get("Founder Analysis"):
            st.json(result["Founder Analysis"])
    
    with tabs[4]:
        if result.get("Quantitative Decision"):
            st.json(result["Quantitative Decision"])

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="SSFF - スタートアップ成功予測",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Startup Success Forecasting Framework")
    st.subtitle("スタートアップ成功可能性分析システム")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ 設定")
        st.info("現在のバージョンではデフォルト設定（gpt-4o-mini、詳細分析モード）で動作します")
    
    # Main content
    st.header("📝 スタートアップ情報入力")
    
    # Input area
    startup_info = st.text_area(
        "スタートアップの説明を入力してください",
        placeholder="例: Turismocity is a travel search engine for Latin America that provides price comparison tools and travel deals. Eugenio Fage, the CTO and co-founder, has a background in software engineering...",
        height=150
    )
    
    # Analysis button
    if st.button("🔍 分析開始", type="primary", disabled=not startup_info.strip()):
        
        st.header("🔄 分析進捗")
        
        # Create containers for progress and intermediate results
        progress_container = st.container()
        
        st.header("📊 中間結果")
        results_container = st.container()
        
        # Run LangGraph analysis
        with st.spinner("分析を実行中..."):
            final_result = run_langgraph_analysis(
                startup_info,
                progress_container, results_container
            )
        
        if final_result:
            st.divider()
            display_final_results(final_result)
    
    # Footer
    st.divider()
    st.markdown(
        """
        **SSFF** - マルチエージェントシステムによるスタートアップ成功予測
        
        📄 [論文](https://arxiv.org/abs/2405.19456) | 
        🔧 [GitHub](https://github.com/your-repo) |
        📚 [Documentation](./CLAUDE.md)
        """
    )

if __name__ == "__main__":
    main()