#!/usr/bin/env python3
"""
AI Research Assistant v3.0 - MINIMAL WORKING VERSION
Testing basic functionality without heavy dependencies
"""

import streamlit as st
import sys
import os
import time
from datetime import datetime

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

# ============================================================================
# IMPORT MODULES SAFELY
# ============================================================================
import_errors = []

try:
    from ingestion.arxiv_fetcher import fetch_arxiv
except Exception as e:
    import_errors.append(f"arxiv_fetcher: {e}")
    fetch_arxiv = None

try:
    from ingestion.semantic_scholar import fetch_semantic_scholar
except Exception as e:
    import_errors.append(f"semantic_scholar: {e}")
    fetch_semantic_scholar = None

try:
    from rag.pipeline import RAGPipeline
    rag_pipeline = RAGPipeline()
except Exception as e:
    import_errors.append(f"RAG Pipeline: {e}")
    rag_pipeline = None

try:
    from rl.feedback_loop import RLFeedbackLoop, Action
    rl_loop = RLFeedbackLoop()
except Exception as e:
    import_errors.append(f"RL Feedback Loop: {e}")
    rl_loop = None

try:
    from integrations.n8n_webhook import N8NWebhook
    n8n = N8NWebhook()
except Exception as e:
    import_errors.append(f"n8n Webhook: {e}")
    n8n = None

try:
    from analytics.pyspark_processor import PySparkAnalytics
    analytics = PySparkAnalytics(use_spark=False)
except Exception as e:
    import_errors.append(f"Analytics: {e}")
    analytics = None

# ============================================================================
# PAGE HEADER
# ============================================================================
st.title("🔬 AI Research Assistant v3.0")
st.markdown("**⚡ Lightning-Fast Research Paper Analysis**")
st.divider()

# Show import errors if any
if import_errors:
    with st.expander("⚠️ Import Warnings", expanded=True):
        for error in import_errors:
            st.warning(error)

# ============================================================================
# SESSION STATE
# ============================================================================
def init_session_state():
    """Initialize session state"""
    if 'papers' not in st.session_state:
        st.session_state.papers = []
    if 'summary' not in st.session_state:
        st.session_state.summary = ""
    if 'research_gaps' not in st.session_state:
        st.session_state.research_gaps = []
    if 'feedback_history' not in st.session_state:
        st.session_state.feedback_history = []
    if 'query' not in st.session_state:
        st.session_state.query = ""

init_session_state()

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.header("⚙️ System Status")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Papers Found", len(st.session_state.papers))
    with col2:
        st.metric("Feedback Points", len(st.session_state.feedback_history))
    
    st.divider()
    
    st.subheader("🏥 System Components")
    
    st.write("**Fetchers:** ✅ Ready")
    st.write("**RAG Pipeline:** " + ("✅ Ready" if rag_pipeline else "❌ Error"))
    st.write("**RL Loop:** " + ("✅ Ready" if rl_loop else "❌ Error"))
    st.write("**n8n Webhook:** " + ("✅ Ready" if n8n else "❌ Error"))
    st.write("**Analytics:** " + ("✅ Ready" if analytics else "❌ Error"))

# ============================================================================
# MAIN TABS
# ============================================================================
tab1, tab2, tab3 = st.tabs(["📰 Papers & Summary", "💬 Q&A & Generation", "📊 Analytics"])

# ============================================================================
# TAB 1: PAPERS + AUTO SUMMARY
# ============================================================================
with tab1:
    st.subheader("🔍 Search Research Papers")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input(
            "📌 Enter research topic:",
            placeholder="e.g., battery recycling, quantum computing..."
        )
    with col2:
        num_papers = st.selectbox("Papers:", [5, 10, 15, 20], index=1)
    
    if st.button("🔍 Search & Analyze", use_container_width=True) and query:
        st.session_state.query = query
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("⏳ Searching papers...")
            progress_bar.progress(20)
            
            # Fetch from arXiv
            arxiv_papers = []
            if fetch_arxiv:
                try:
                    arxiv_papers = fetch_arxiv(query, max_results=num_papers)
                    progress_bar.progress(40)
                except Exception as e:
                    st.warning(f"arXiv fetch error: {e}")
            
            # Fetch from Semantic Scholar
            ss_papers = []
            if fetch_semantic_scholar:
                try:
                    ss_papers = fetch_semantic_scholar(query, limit=num_papers)
                    progress_bar.progress(60)
                except Exception as e:
                    st.warning(f"Semantic Scholar error: {e}")
            
            # Combine papers
            all_papers = arxiv_papers + ss_papers
            seen = set()
            unique_papers = []
            for p in all_papers:
                title_key = p.get('title', '').lower()
                if title_key not in seen:
                    seen.add(title_key)
                    unique_papers.append(p)
            
            st.session_state.papers = unique_papers[:num_papers]
            progress_bar.progress(80)
            
            # Generate summary if RAG available
            if st.session_state.papers and rag_pipeline:
                status_text.text("📊 Generating summary...")
                try:
                    summary = rag_pipeline.generate_summary(query, st.session_state.papers)
                    st.session_state.summary = summary
                except Exception as e:
                    st.session_state.summary = f"Summary error: {e}"
            
            # Generate gaps if RAG available
            if st.session_state.papers and rag_pipeline:
                status_text.text("🔍 Detecting research gaps...")
                try:
                    gaps = rag_pipeline.detect_research_gaps(st.session_state.papers)
                    st.session_state.research_gaps = gaps
                except Exception as e:
                    st.session_state.research_gaps = ["Error detecting gaps"]
            
            progress_bar.progress(100)
            status_text.empty()
            st.success(f"✅ Found {len(st.session_state.papers)} papers!")
            
        except Exception as e:
            st.error(f"❌ Search failed: {e}")
            progress_bar.empty()
            status_text.empty()
    
    # Display summary
    if st.session_state.summary:
        st.divider()
        st.subheader("📊 Research Summary")
        st.write(st.session_state.summary)
    
    # Display gaps
    if st.session_state.research_gaps:
        st.divider()
        st.subheader("🔍 Research Gaps & Opportunities")
        for gap in st.session_state.research_gaps:
            st.write(f"• {gap}")
    
    # Display papers
    if st.session_state.papers:
        st.divider()
        st.subheader(f"📚 Papers ({len(st.session_state.papers)} total)")
        
        for idx, paper in enumerate(st.session_state.papers, 1):
            with st.expander(f"{idx}. {paper.get('title', 'Unknown')[:70]}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Title:** {paper.get('title', 'N/A')}")
                    st.write(f"**Authors:** {', '.join(paper.get('authors', ['N/A'])[:3])}")
                    st.write(f"**Year:** {paper.get('year', 'N/A')} | **Citations:** {paper.get('citations', 0)}")
                    st.write(f"**Source:** {paper.get('source', 'N/A').upper()}")
                    if paper.get('abstract'):
                        st.write("**Abstract:**")
                        st.write(paper['abstract'][:500] + "...")
                
                with col2:
                    st.metric("Citations", paper.get('citations', 0))
                    if paper.get('url'):
                        st.link_button("📖 Read", paper['url'], use_container_width=True)

# ============================================================================
# TAB 2: Q&A
# ============================================================================
with tab2:
    st.subheader("💬 Q&A & Generation")
    
    if not st.session_state.papers:
        st.info("👉 Search for papers first in the 📰 tab")
    else:
        st.subheader("🤖 Ask Questions About Papers")
        question = st.text_input("Your question:")
        
        if question and st.button("💬 Get Answer", use_container_width=True):
            if rag_pipeline:
                with st.spinner("🤖 Thinking..."):
                    try:
                        context = rag_pipeline.retrieve_context(question, top_k=3)
                        answer = rag_pipeline.generate_answer(question, context)
                        st.success("✅ Answer Generated")
                        st.write(answer)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.error("RAG Pipeline not available")
        
        st.divider()
        
        st.subheader("📝 Generate Abstract")
        if st.button("✍️ Generate Abstract", use_container_width=True):
            if rag_pipeline:
                with st.spinner("📝 Writing..."):
                    try:
                        prompt = f"Write a concise research abstract about {st.session_state.query}"
                        context = rag_pipeline.retrieve_context(st.session_state.query, top_k=3)
                        abstract = rag_pipeline.generate_answer(prompt, context)
                        st.success("✅ Abstract Generated")
                        st.write(abstract)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.error("RAG Pipeline not available")

# ============================================================================
# TAB 3: ANALYTICS
# ============================================================================
with tab3:
    st.subheader("📈 Analytics & Feedback")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Papers", len(st.session_state.papers))
    with col2:
        if st.session_state.papers:
            avg_cites = sum([p.get('citations', 0) for p in st.session_state.papers]) / len(st.session_state.papers)
            st.metric("Avg Citations", f"{avg_cites:.1f}")
        else:
            st.metric("Avg Citations", "0")
    with col3:
        st.metric("Feedback", len(st.session_state.feedback_history))
    with col4:
        st.metric("n8n Status", "✅ Ready" if n8n else "❌ Error")
    
    st.divider()
    
    st.subheader("🎮 RL Feedback")
    if st.session_state.papers:
        col1, col2 = st.columns(2)
        with col1:
            papers_quality = st.slider("Paper Quality:", 0, 10, 5)
        with col2:
            answer_quality = st.slider("Answer Quality:", 0, 10, 5)
        
        if st.button("📊 Submit Feedback", use_container_width=True):
            if rl_loop:
                try:
                    action = Action(
                        action_type="feedback",
                        query=st.session_state.query,
                        parameters={"papers": papers_quality, "answer": answer_quality}
                    )
                    
                    result = rl_loop.step(
                        action=action,
                        papers_found=len(st.session_state.papers),
                        answer_quality=answer_quality / 10.0
                    )
                    
                    feedback_entry = {
                        "query": st.session_state.query,
                        "papers_quality": papers_quality,
                        "answer_quality": answer_quality,
                        "reward": result.reward,
                        "timestamp": datetime.now().isoformat()
                    }
                    st.session_state.feedback_history.append(feedback_entry)
                    
                    st.success(f"✅ Feedback saved! Reward: {result.reward:.2f}")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("RL Loop not available")
    else:
        st.info("👉 Search for papers first")
    
    st.divider()
    
    st.subheader("📊 Dashboard")
    if st.session_state.papers or st.session_state.feedback_history:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Papers:** {len(st.session_state.papers)}")
            if st.session_state.papers:
                years = [p.get('year', 0) for p in st.session_state.papers]
                st.write(f"**Year Range:** {min(years)}-{max(years)}")
        with col2:
            st.write(f"**Feedback Points:** {len(st.session_state.feedback_history)}")
            if st.session_state.feedback_history:
                rewards = [f['reward'] for f in st.session_state.feedback_history]
                st.write(f"**Avg Reward:** {sum(rewards)/len(rewards):.2f}")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.caption("🚀 AI Research Assistant v3.0 | Production Ready")
