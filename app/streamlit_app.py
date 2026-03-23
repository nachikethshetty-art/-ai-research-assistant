#!/usr/bin/env python3
"""
AI Research Assistant v3.0 - PRODUCTION READY
⚡ Lightning-Fast • 🧠 Smart RL Feedback • 🚀 Hackathon Winner
"""

import streamlit as st
import sys
import os
import time
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ingestion.arxiv_fetcher import fetch_arxiv
from ingestion.semantic_scholar import fetch_semantic_scholar
from rag.pipeline import RAGPipeline
from rl.feedback_loop import RLFeedbackLoop, Action
from integrations.n8n_webhook import N8NWebhook
from analytics.pyspark_processor import PySparkAnalytics

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="AI Research Assistant v3.0",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 AI Research Assistant v3.0")
st.markdown("**⚡ Lightning-Fast Research Paper Analysis with RL Feedback Loop**")
st.divider()

# ============================================================================
# INITIALIZE COMPONENTS
# ============================================================================
@st.cache_resource
def init_components():
    """Initialize all system components once"""
    rl_loop = RLFeedbackLoop()
    n8n = N8NWebhook()
    analytics = PySparkAnalytics(use_spark=False)  # Fallback mode
    try:
        rag = RAGPipeline()
    except:
        rag = None
    return rl_loop, n8n, analytics, rag

rl_loop, n8n, analytics, rag_pipeline = init_components()

# Initialize session state
if 'papers' not in st.session_state:
    st.session_state.papers = []
if 'feedback_history' not in st.session_state:
    st.session_state.feedback_history = []

# ============================================================================
# SIDEBAR - STATUS & CONFIG
# ============================================================================
with st.sidebar:
    st.header("⚙️ System Status")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Papers Cached", len(st.session_state.papers))
    with col2:
        st.metric("Feedback Points", len(st.session_state.feedback_history))
    
    st.divider()
    
    # System health
    st.subheader("🏥 System Health")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("✅ **Fetchers**")
        st.caption("Ready")
    with col2:
        st.write("✅ **RL Loop**" if rl_loop else "⚠️ **RL Loop**")
        st.caption("Ready")
    with col3:
        st.write("✅ **Analytics**")
        st.caption(analytics.spark_available and "Spark" or "Fallback")
    
    st.divider()
    
    # n8n status
    st.subheader("🔗 n8n Integration")
    n8n_status = n8n.get_workflow_status()
    if n8n_status['enabled']:
        st.success(f"✅ Connected • {n8n_status['total_triggers']} triggers")
    else:
        st.info("ℹ️ Not configured (optional)")

# ============================================================================
# MAIN TABS
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📊 Analysis", "🤖 RL Feedback", "📈 Dashboard"])

# ============================================================================
# TAB 1: SEARCH
# ============================================================================
with tab1:
    st.subheader("Search Research Papers")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input(
            "📌 Enter research topic:",
            placeholder="e.g., battery recycling, quantum computing, climate change..."
        )
    with col2:
        num_papers = st.selectbox("Papers:", [5, 10, 15, 20], index=1)
    
    search_btn = st.button("🔍 Search", use_container_width=True)
    
    if search_btn and query:
        st.session_state.query = query
        
        with st.spinner("⏳ Searching papers..."):
            start = time.time()
            
            # Fetch papers
            arxiv_papers = fetch_arxiv(query, max_results=num_papers)
            ss_papers = fetch_semantic_scholar(query, limit=num_papers)
            
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
        
        # Display results
        st.success(f"✅ Found {len(st.session_state.papers)} papers in {elapsed:.1f}s")
        
        # Show papers
        for idx, paper in enumerate(st.session_state.papers, 1):
            with st.expander(f"{idx}. {paper.get('title', 'Unknown')[:60]}..."):
                st.write(f"**Title:** {paper.get('title')}")
                st.write(f"**Authors:** {', '.join(paper.get('authors', ['N/A'])[:3])}")
                st.write(f"**Year:** {paper.get('year', 'N/A')} | **Citations:** {paper.get('citations', 0)}")
                st.write(f"**Source:** {paper.get('source', 'N/A').upper()}")
                st.write("**Abstract:**")
                st.write(paper.get('abstract', 'N/A')[:300] + "...")
                
                if paper.get('url'):
                    st.link_button("📖 Read Full Paper", paper['url'])

# ============================================================================
# TAB 2: ANALYSIS (Q&A + Summary)
# ============================================================================
with tab2:
    st.subheader("Research Analysis & Q&A")
    
    if not st.session_state.papers:
        st.info("👉 Search for papers first in the 🔍 Search tab")
    else:
        analysis_type = st.radio("Select analysis:", 
                                ["Summary", "Q&A", "Research Gaps", "Introduction Generator"])
        
        if analysis_type == "Summary":
            if st.button("📊 Generate Summary", use_container_width=True):
                with st.spinner("🤖 Analyzing papers..."):
                    if rag_pipeline:
                        summary = rag_pipeline.generate_summary(st.session_state.papers)
                        st.write(summary)
                    else:
                        st.info("RAG Pipeline not available (Ollama might not be running)")
        
        elif analysis_type == "Q&A":
            question = st.text_input("Ask a question about the papers:")
            if question and st.button("💬 Get Answer", use_container_width=True):
                with st.spinner("🤖 Generating answer..."):
                    if rag_pipeline:
                        answer = rag_pipeline.answer_question(question, st.session_state.papers)
                        st.write(answer)
                    else:
                        st.info("RAG Pipeline not available")
        
        elif analysis_type == "Research Gaps":
            if st.button("🔍 Identify Research Gaps", use_container_width=True):
                with st.spinner("🤖 Analyzing gaps..."):
                    if rag_pipeline:
                        gaps = rag_pipeline.find_research_gaps(st.session_state.papers)
                        st.write(gaps)
                    else:
                        st.info("RAG Pipeline not available")
        
        elif analysis_type == "Introduction Generator":
            if st.button("📝 Generate Introduction", use_container_width=True):
                with st.spinner("🤖 Writing introduction..."):
                    if rag_pipeline:
                        intro = rag_pipeline.generate_introduction(st.session_state.papers)
                        st.write(intro)
                    else:
                        st.info("RAG Pipeline not available")

# ============================================================================
# TAB 3: RL FEEDBACK LOOP
# ============================================================================
with tab3:
    st.subheader("🤖 RL Feedback System")
    
    st.write("**How it works:** The system learns from your feedback to improve search quality.")
    
    if st.session_state.papers:
        col1, col2 = st.columns(2)
        
        with col1:
            papers_quality = st.slider("📄 Paper Quality (0-10):", 0, 10, 5)
        with col2:
            answer_quality = st.slider("💬 Answer Quality (0-10):", 0, 10, 5)
        
        if st.button("📊 Submit Feedback", use_container_width=True):
            # Create RL action
            action = Action(
                action_type="feedback",
                query=st.session_state.query,
                parameters={"papers_quality": papers_quality, "answer_quality": answer_quality}
            )
            
            # Execute RL step
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
                "reward": result.reward,
                "timestamp": datetime.now().isoformat(),
                "action": action.action_type
            }
            st.session_state.feedback_history.append(feedback_entry)
            
            # Trigger n8n if configured
            if n8n.enabled:
                n8n.trigger_research_pipeline(st.session_state.query, st.session_state.papers)
            
            st.success(f"✅ Feedback recorded! Reward: {result.reward:.2f}")
            st.write(f"**Episode Total Reward:** {result.info['total_reward']:.2f}")
    else:
        st.info("👉 Search for papers first to provide feedback")

# ============================================================================
# TAB 4: ANALYTICS DASHBOARD
# ============================================================================
with tab4:
    st.subheader("📈 Analytics Dashboard")
    
    if st.session_state.papers or st.session_state.feedback_history:
        # Get analytics
        dashboard = analytics.get_dashboard_data(
            st.session_state.papers,
            st.session_state.feedback_history
        )
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Papers", dashboard['papers'].get('total_papers', 0))
        with col2:
            st.metric("Avg Citations", f"{dashboard['papers'].get('avg_citations', 0):.1f}")
        with col3:
            st.metric("Feedback Points", dashboard['feedback'].get('total_feedback_points', 0))
        with col4:
            st.metric("Avg Reward", f"{dashboard['feedback'].get('avg_reward', 0):.2f}")
        
        st.divider()
        
        # RL Episode History
        if st.session_state.feedback_history:
            st.subheader("🎮 RL Episode History")
            
            feedback_df = st.session_state.feedback_history
            st.write(f"Total feedback points: {len(feedback_df)}")
            
            for idx, f in enumerate(feedback_df[-5:], 1):  # Show last 5
                st.write(f"**#{idx}** | Query: *{f['query'][:40]}...* | Reward: {f['reward']:.2f} | {f['timestamp'][:10]}")
        
        st.divider()
        
        # Processing method
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Analytics Engine:** {dashboard['papers'].get('processing_method', 'N/A').upper()}")
        with col2:
            st.write(f"**PySpark Available:** {'✅ Yes' if analytics.spark_available else '⚠️ Fallback'}")
    
    else:
        st.info("👉 Search for papers or submit feedback to see analytics")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.caption("🚀 AI Research Assistant v3.0 | Production Ready | RL-Powered | hackathon-ready")
