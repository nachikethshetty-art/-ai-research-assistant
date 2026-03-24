#!/usr/bin/env python3
"""
AI Research Assistant v3.0 - PRODUCTION READY
⚡ Auto-generate summary + research gaps on search
🎯 Q&A and Abstract Generation in Tab 2
"""

import streamlit as st
import sys
import os
import time
import json
import concurrent.futures
from datetime import datetime
import re

# ============================================================================
# PAGE CONFIG (MUST BE FIRST)
# ============================================================================
st.set_page_config(
    page_title="AI Research Assistant v3.0",
    page_icon="🔬",
    layout="wide"
)

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import after path setup
try:
    from ingestion.arxiv_fetcher import fetch_arxiv
    from ingestion.semantic_scholar import fetch_semantic_scholar
    from rag.pipeline import RAGPipeline
    from rl.feedback_loop import RLFeedbackLoop, Action
    from analytics.pyspark_processor import PySparkAnalytics
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.stop()

# ============================================================================
# PAGE TITLE & HEADER
# ============================================================================
st.title("🔬 AI Research Assistant v3.0")
st.markdown("**⚡ Lightning-Fast Research Paper Analysis**")
st.divider()

# ============================================================================
# INITIALIZE COMPONENTS (CACHED)
# ============================================================================
@st.cache_resource
def init_components():
    """Initialize all system components once"""
    try:
        rl_loop = RLFeedbackLoop()
        analytics = PySparkAnalytics(use_spark=False)
        rag = RAGPipeline()
        return rl_loop, analytics, rag, None
    except Exception as e:
        error_msg = f"Component initialization error: {e}"
        print(error_msg)
        return None, None, None, error_msg

rl_loop, analytics, rag_pipeline, init_error = init_components()

if init_error:
    st.error(f"❌ Initialization Error: {init_error}")
    st.info("Some features may be unavailable, but basic search should work.")

# Initialize session state - ALWAYS run this
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'papers': [],
        'summary': "",
        'research_gaps': [],
        'feedback_history': [],
        'query': ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================================
# SIDEBAR - STATUS & CONFIG
# ============================================================================
with st.sidebar:
    st.header("⚙️ System Status")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Papers Found", len(st.session_state.papers))
    with col2:
        st.metric("Feedback Points", len(st.session_state.feedback_history))
    
    st.divider()
    
    # System health
    st.subheader("🏥 System Components")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("✅ **Fetchers**")
        st.caption("Ready")
    with col2:
        st.write("✅ **RAG**")
        st.caption("Ready" if rag_pipeline else "Error")
    with col3:
        st.write("✅ **Analytics**")
        st.caption("Ready" if analytics else "Error")
    
    st.divider()
    
    # Ollama status
    st.subheader("🧠 Ollama Status")
    if rag_pipeline and rag_pipeline.ollama_available:
        st.success("✅ **CONNECTED**")
    else:
        st.error("❌ **NOT CONNECTED**")
        st.warning("Please start Ollama to enable Q&A and generation.")

# ============================================================================
# MAIN TABS
# ============================================================================
tab1, tab2, tab3, tab_debug = st.tabs(["📰 Papers & Summary", "💬 Q&A & Generation", "📊 Analytics", "🔧 Debug"])

# ============================================================================
# TAB 1: PAPERS + AUTO SUMMARY + RESEARCH GAPS
# ============================================================================
with tab1:
    st.subheader("🔍 Search Research Papers")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input(
            "📌 Enter research topic:",
            placeholder="e.g., battery recycling, quantum computing, climate change..."
        )
    with col2:
        num_papers = st.selectbox("Papers:", [5, 10, 15, 20], index=1)
    
    search_btn = st.button("🔍 Search & Analyze", use_container_width=True)
    
    if search_btn and query:
        st.session_state.query = query
        
        status_placeholder = st.empty()
        
        try:
            start = time.time()
            
            status_placeholder.info("⏳ Fetching from arXiv and Semantic Scholar...")
            
            # Fetch papers in parallel (fast-fail approach)
            import concurrent.futures
            papers_list = []
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                arxiv_future = executor.submit(lambda: fetch_arxiv(query, max_results=num_papers) if fetch_arxiv else [])
                ss_future = executor.submit(lambda: fetch_semantic_scholar(query, limit=num_papers) if fetch_semantic_scholar else [])
                
                # Get results with timeout
                try:
                    arxiv_papers = arxiv_future.result(timeout=5)
                except:
                    arxiv_papers = []
                
                try:
                    ss_papers = ss_future.result(timeout=3)
                except:
                    ss_papers = []
            
            # Combine and deduplicate
            all_papers = arxiv_papers + ss_papers
            seen = set()
            unique_papers = []
            for p in all_papers:
                title_key = p.get('title', '').lower()
                if title_key not in seen:
                    seen.add(title_key)
                    unique_papers.append(p)
            
            st.session_state.papers = unique_papers[:num_papers]
            elapsed = time.time() - start
            
            status_placeholder.success(f"✅ Found {len(st.session_state.papers)} papers in {elapsed:.1f}s")
        except Exception as e:
                st.error(f"❌ Search error: {e}")
                st.session_state.papers = []
        
        # AUTO-GENERATE SUMMARY
        if st.session_state.papers and rag_pipeline:
            st.session_state.summary = ""
            st.session_state.research_gaps = []
            
            st.divider()
            st.subheader("📊 Research Summary")
            summary_placeholder = st.empty()

            try:
                full_summary = ""
                for chunk in rag_pipeline.generate_summary(query, st.session_state.papers):
                    full_summary += chunk
                    summary_placeholder.write(full_summary)
                st.session_state.summary = full_summary

            except Exception as e:
                st.error(f"Summary generation error: {e}")
                st.session_state.summary = f"Error: {e}"
            
            # AUTO-GENERATE RESEARCH GAPS
            st.divider()
            st.subheader("🔍 Research Gaps & Opportunities")
            gaps_placeholder = st.empty()

            try:
                full_gaps = ""
                for chunk in rag_pipeline.detect_research_gaps(st.session_state.papers):
                    full_gaps += chunk
                    gaps_placeholder.write(full_gaps)
                st.session_state.research_gaps = full_gaps

            except Exception as e:
                st.error(f"Research gaps analysis error: {e}")
                st.session_state.research_gaps = f"Error: {e}"

    # Display Papers (with details)
    if st.session_state.papers:
        st.divider()
        st.subheader(f"📚 Papers ({len(st.session_state.papers)} total)")
        
        for idx, paper in enumerate(st.session_state.papers, 1):
            with st.expander(f"{idx}. {paper.get('title', 'Unknown')[:70]}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Title:** {paper.get('title', 'N/A')}")
                    st.write(f"**Authors:** {', '.join(paper.get('authors', ['N/A'])[:5])}")
                    st.write(f"**Year:** {paper.get('year', 'N/A')} | **Citations:** {paper.get('citations', 0)}")
                    st.write(f"**Source:** {paper.get('source', 'N/A').upper()}")
                    st.write("**Abstract:**")
                    st.write(paper.get('abstract', 'N/A')[:500] + "...")
                
                with col2:
                    st.metric("Citations", paper.get('citations', 0))
                    if paper.get('url'):
                        st.link_button("📖 Read Paper", paper['url'], use_container_width=True)

# ============================================================================
# TAB 2: Q&A + ABSTRACT GENERATION
# ============================================================================
with tab2:
    st.subheader("💬 AI-Powered Q&A & Content Generation")
    
    if not st.session_state.papers:
        st.info("👉 Search for papers first in the 📰 Papers & Summary tab")
    else:
        # Q&A Section
        st.subheader("🤖 Ask Questions About Papers")
        question = st.text_input(
            "Ask any question about the papers:",
            placeholder="e.g., What are the main findings? What are the challenges?"
        )
        
        if question and st.button("💬 Get Answer", use_container_width=True):
            with st.spinner("🤖 Generating answer..."):
                try:
                    if rag_pipeline:
                        # Retrieve context
                        context = rag_pipeline.retrieve_context(question, top_k=3)
                        answer = rag_pipeline.generate_answer(question, context)
                        st.success("✅ Answer Generated")
                        st.write(answer)
                    else:
                        st.error("RAG Pipeline not available")
                except Exception as e:
                    st.error(f"Error generating answer: {e}")
        
        st.divider()
        
        # Abstract Generation Section
        st.subheader("📝 Generate New Abstract")
        st.write("Generate a new, original abstract for your research topic:")
        
        if st.button("✍️ Generate Abstract", use_container_width=True):
            with st.spinner("📝 Writing abstract..."):
                try:
                    if rag_pipeline:
                        abstract_prompt = f"Write a concise research abstract about {st.session_state.query} based on recent papers."
                        abstract = rag_pipeline.generate_answer(abstract_prompt, rag_pipeline.retrieve_context(st.session_state.query, top_k=3))
                        st.success("✅ Abstract Generated")
                        st.write(abstract)
                    else:
                        st.error("RAG Pipeline not available")
                except Exception as e:
                    st.error(f"Error generating abstract: {e}")

# ============================================================================
# TAB 3: ANALYTICS & RL FEEDBACK
# ============================================================================
with tab3:
    st.subheader("📈 Analytics & RL Feedback Loop")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Papers", len(st.session_state.papers))
    with col2:
        avg_citations = sum([p.get('citations', 0) for p in st.session_state.papers]) / max(len(st.session_state.papers), 1)
        st.metric("Avg Citations", f"{avg_citations:.1f}")
    with col3:
        st.metric("Feedback Points", len(st.session_state.feedback_history))
    
    st.divider()
    
    # RL Feedback Section
    st.subheader("🎮 RL Feedback Loop (OpenEnv-Style Learning)")
    st.write("Your feedback trains the system to improve. Rate papers and answers:")
    
    if st.session_state.papers:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            papers_quality = st.slider("📄 Paper Relevance (0-10):", 0, 10, 5)
        with col2:
            answer_quality = st.slider("💬 Answer Quality (0-10):", 0, 10, 5)
        with col3:
            speed_rating = st.slider("⚡ Speed (0-10):", 0, 10, 5)
        
        if st.button("📊 Submit Feedback & Train", use_container_width=True):
            # Create RL action with strategy
            action = Action(
                action_type="feedback",
                query=st.session_state.query,
                parameters={
                    "papers_quality": papers_quality,
                    "answer_quality": answer_quality,
                    "speed": speed_rating,
                    "strategy": "multi_source"  # Which strategy was used
                }
            )
            
            # Execute RL step (OpenEnv step method)
            result = rl_loop.step(
                action=action,
                papers_found=len(st.session_state.papers),
                answer_quality=answer_quality / 10.0
            )
            
            # Store feedback
            feedback_entry = {
                "query": st.session_state.query,
                "papers_quality": papers_quality,
                "answer_quality": answer_quality,
                "speed": speed_rating,
                "reward": result.reward,
                "timestamp": datetime.now().isoformat(),
                "action": action.action_type
            }
            st.session_state.feedback_history.append(feedback_entry)
            
            # Show learning results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.success(f"✅ Reward: {result.reward:.3f}")
            with col2:
                st.info(f"📈 Step: {result.info['step']}/5")
            with col3:
                st.metric("Episode Total", f"{result.info['total_reward']:.2f}")
            
            # Show reward breakdown
            with st.expander("📊 Reward Breakdown"):
                st.write(f"- Papers Reward: {result.info['papers_reward']:.3f}")
                st.write(f"- Quality Reward: {result.info['quality_reward']:.3f}")
                st.write(f"- Speed Bonus: {result.info['speed_bonus']:.3f}")
                st.write(f"- Strategy: {result.info['strategy']}")
            
            # Show learning state
            state = rl_loop.get_state()
            with st.expander("🧠 System Learning State"):
                st.write(f"**Episode ID:** {state['episode_id']}")
                st.write(f"**Total Steps:** {state['step_count']}")
                st.write(f"**Total Reward:** {state['total_reward']:.2f}")
                st.write(f"**Best Strategy:** {rl_loop.get_best_strategy()}")
    else:
        st.info("👉 Search for papers first to provide feedback and train the system")
    
    st.divider()
    
    # Analytics Dashboard
    st.subheader("📊 System Analytics")
    
    if st.session_state.papers or st.session_state.feedback_history:
        dashboard = analytics.get_dashboard_data(
            st.session_state.papers,
            st.session_state.feedback_history
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Paper Statistics:**")
            st.write(f"- Total: {dashboard['papers'].get('total_papers', 0)}")
            st.write(f"- Avg Citations: {dashboard['papers'].get('avg_citations', 0):.1f}")
            st.write(f"- Year Range: {dashboard['papers'].get('min_year', 'N/A')}-{dashboard['papers'].get('max_year', 'N/A')}")
        
        with col2:
            st.write("**Feedback Statistics:**")
            st.write(f"- Total Points: {dashboard['feedback'].get('total_feedback_points', 0)}")
            st.write(f"- Avg Reward: {dashboard['feedback'].get('avg_reward', 0):.2f}")
            st.write(f"- Max Reward: {dashboard['feedback'].get('max_reward', 0):.2f}")
        
        st.write(f"**Engine:** {dashboard['papers'].get('processing_method', 'N/A').upper()}")
        st.write(f"**PySpark Available:** {'✅ Yes' if analytics.spark_available else '⚠️ Fallback'}")
    else:
        st.info("👉 Search for papers or submit feedback to see analytics")
    
    st.divider()
    
    # Hackathon Enhancement: Export Feature
    st.subheader("📥 Export Analysis")
    
    if st.session_state.papers and st.session_state.summary:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Download Report (TXT)", use_container_width=True):
                report_text = f"""
═══════════════════════════════════════════════════════════════════════
              AI RESEARCH ASSISTANT - ANALYSIS REPORT
═══════════════════════════════════════════════════════════════════════

📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 RESEARCH QUERY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: {st.session_state.query}
Papers Found: {len(st.session_state.papers)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 RESEARCH SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{st.session_state.summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔎 RESEARCH GAPS & OPPORTUNITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{st.session_state.research_gaps}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 PAPERS ANALYZED ({len(st.session_state.papers)} total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
                
                for idx, paper in enumerate(st.session_state.papers, 1):
                    report_text += f"""
{idx}. {paper.get('title', 'Unknown')}
   Authors: {', '.join(paper.get('authors', ['N/A'])[:3])}
   Year: {paper.get('year', 'N/A')} | Citations: {paper.get('citations', 0)}
   Source: {paper.get('source', 'unknown').upper()}
   URL: {paper.get('url', 'N/A')}
"""
                
                report_text += f"""
═══════════════════════════════════════════════════════════════════════
Generated by: AI Research Assistant v3.0
System Performance: {len(st.session_state.feedback_history)} feedback entries tracked
═══════════════════════════════════════════════════════════════════════
"""
                
                st.download_button(
                    label="📥 Download",
                    data=report_text,
                    file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("📊 Download as JSON", use_container_width=True):
                json_data = {
                    "query": st.session_state.query,
                    "timestamp": datetime.now().isoformat(),
                    "papers_count": len(st.session_state.papers),
                    "summary": st.session_state.summary,
                    "research_gaps": st.session_state.research_gaps,
                    "papers": st.session_state.papers,
                    "feedback_entries": len(st.session_state.feedback_history)
                }
                
                st.download_button(
                    label="📥 Download",
                    data=json.dumps(json_data, indent=2),
                    file_name=f"research_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    else:
        st.info("👉 Complete a search first to export the analysis")

# ============================================================================
# TAB 4: DEBUG
# ============================================================================
with tab_debug:
    st.subheader("🔧 Debug & System Status")
    
    # Check LLM backend
    try:
        from llm.backend import LLMBackend
        llm = LLMBackend()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status = llm.get_status()
            st.metric("Ollama Available", "✅" if status["ollama"] else "❌")
        
        with col2:
            st.metric("Gemini Available", "✅" if status["gemini"] else "❌")
        
        with col3:
            st.metric("Active Backend", status["active_backend"])
        
        st.divider()
        
        # List available models
        st.subheader("📋 Available Gemini Models")
        if st.button("🔄 List Models"):
            models = llm.list_available_models()
            if models:
                st.success(f"Found {len(models)} models:")
                for model in models:
                    st.code(model)
            else:
                st.error("No models found or API key not working")
        
        st.divider()
        
        # API Key status
        st.subheader("🔑 API Key Status")
        api_key = os.getenv("GOOGLE_API_KEY", "NOT SET")
        if api_key == "NOT SET":
            st.error("⚠️ GOOGLE_API_KEY environment variable not set")
        else:
            masked_key = api_key[:20] + "..." + api_key[-4:] if len(api_key) > 24 else "***"
            st.success(f"✅ API Key configured: {masked_key}")
    
    except Exception as e:
        st.error(f"❌ Error loading debug info: {e}")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.caption("🚀 AI Research Assistant v3.0 | Production Ready | Hackathon Winner")
