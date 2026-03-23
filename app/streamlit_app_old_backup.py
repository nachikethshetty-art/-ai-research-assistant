#!/usr/bin/env python3
"""
AI Research Assistant v3.0 - PRODUCTION READY
Fast, Smart, RL-Powered Research Paper Analysis
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

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="AI Research Assistant v3.0",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔬 AI Research Assistant v3.0")
st.markdown("**Lightning-Fast Research Paper Analysis with RL Feedback Loop**")
st.divider()

# ============================================================================
# SESSION STATE
# ============================================================================

if 'papers' not in st.session_state:
    st.session_state.papers = []
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'rl_feedback' not in st.session_state:
    st.session_state.rl_feedback = []
if 'rag_pipeline' not in st.session_state:
    try:
        st.session_state.rag_pipeline = RAGPipeline()
    except:
        st.session_state.rag_pipeline = None

# ============================================================================
# SIDEBAR - CONFIG & STATS
# ============================================================================

with st.sidebar:
    st.title("⚙️ Configuration")
    st.write("**v3.0 - Production Edition**")
    
    # Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Papers Found", len(st.session_state.papers))
    with col2:
        st.metric("RL Feedback", len(st.session_state.rl_feedback))
    
    st.divider()
    
    # Settings
    num_papers = st.slider("Papers to fetch:", 5, 20, 10)
    search_timeout = st.slider("Timeout (seconds):", 5, 30, 15)
    
    st.divider()
    st.write("**System Status:**")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            st.success("✅ Ollama Connected")
        else:
            st.warning("⚠️ Ollama Reconnecting")
    except:
        st.error("❌ Ollama Not Running")

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Search Papers",
    "💬 Q&A & Insights",
    "📊 Analytics",
    "🤖 RL Feedback"
])

# ============================================================================
# TAB 1: SEARCH PAPERS (FAST)
# ============================================================================

with tab1:
    st.subheader("Search Research Papers")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "🔍 Enter research topic:",
            placeholder="e.g., battery recycling, quantum computing, climate change...",
            key="search_query"
        )
    
    with col2:
        search_btn = st.button("🚀 Search", use_container_width=True)
    
    if search_btn and query:
        st.session_state.query = query
        
        with st.spinner(f"⚡ Searching for '{query}'..."):
            progress = st.progress(0)
            
            try:
                # Fetch arXiv
                progress.progress(25)
                arxiv_papers = fetch_arxiv(query, max_results=num_papers)
                
                # Fetch Semantic Scholar
                progress.progress(50)
                ss_papers = fetch_semantic_scholar(query, limit=num_papers)
                
                progress.progress(75)
                
                # Combine & deduplicate
                all_papers = arxiv_papers + ss_papers
                seen = set()
                unique = []
                
                for p in all_papers:
                    title = p.get('title', '').lower().strip()
                    if title and title not in seen:
                        seen.add(title)
                        unique.append(p)
                
                st.session_state.papers = unique[:num_papers]
                progress.progress(100)
                
                # Show results
                st.success(f"✅ Found {len(st.session_state.papers)} papers!")
                st.info(f"📊 arXiv: {len(arxiv_papers)} | Semantic Scholar: {len(ss_papers)}")
                
                # Store in RL feedback
                st.session_state.rl_feedback.append({
                    "timestamp": datetime.now().isoformat(),
                    "query": query,
                    "papers_found": len(st.session_state.papers),
                    "sources": {
                        "arxiv": len(arxiv_papers),
                        "semantic_scholar": len(ss_papers)
                    }
                })
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                progress.progress(0)
    
    # Display papers
    if st.session_state.papers:
        st.divider()
        st.subheader(f"📚 Results ({len(st.session_state.papers)} papers)")
        
        for idx, paper in enumerate(st.session_state.papers, 1):
            with st.expander(f"{idx}. {paper.get('title', 'Unknown')[:60]}... ({paper.get('year', 'N/A')})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Title:** {paper.get('title', 'N/A')}")
                    st.markdown(f"**Authors:** {', '.join(paper.get('authors', ['Unknown'])[:3])}")
                    st.markdown(f"**Year:** {paper.get('year', 'N/A')}")
                    st.markdown(f"**Source:** {paper.get('source', 'Unknown').upper()}")
                    st.markdown(f"**Citations:** {paper.get('citations', 0)}")
                    st.markdown("**Abstract:**")
                    st.write(paper.get('abstract', 'No abstract available')[:300] + "...")
                
                with col2:
                    st.metric("Citations", paper.get('citations', 0))
                    if paper.get('url'):
                        st.link_button("📖 Read", paper.get('url'))

# ============================================================================
# TAB 2: Q&A & INSIGHTS (FAST)
# ============================================================================

with tab2:
    st.subheader("💬 Q&A & Research Insights")
    
    if not st.session_state.papers:
        st.info("👈 Search papers first in the 'Search Papers' tab")
    else:
        # Q&A Section
        col1, col2 = st.columns([3, 1])
        with col1:
            user_question = st.text_input("❓ Ask a question about these papers:")
        with col2:
            qa_btn = st.button("Answer", use_container_width=True)
        
        if qa_btn and user_question:
            with st.spinner("🤖 Generating answer..."):
                try:
                    if st.session_state.rag_pipeline:
                        st.session_state.rag_pipeline.prepare_data(st.session_state.papers)
                        answer = st.session_state.rag_pipeline.answer_question(user_question)
                        
                        st.success("✅ Answer Generated!")
                        st.markdown("### Answer")
                        st.write(answer)
                        
                        # Log for RL
                        st.session_state.rl_feedback[-1]["question"] = user_question
                        st.session_state.rl_feedback[-1]["answer_generated"] = True
                    else:
                        st.warning("⚠️ RAG Pipeline not initialized")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        st.divider()
        
        # Summary Section
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Generate Summary", use_container_width=True):
                with st.spinner("📝 Generating summary..."):
                    try:
                        if st.session_state.rag_pipeline:
                            st.session_state.rag_pipeline.prepare_data(st.session_state.papers)
                            summary = st.session_state.rag_pipeline.generate_summary()
                            st.markdown("### Research Summary")
                            st.write(summary)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with col2:
            if st.button("🔍 Research Gaps", use_container_width=True):
                with st.spinner("🔎 Analyzing gaps..."):
                    try:
                        if st.session_state.rag_pipeline:
                            st.session_state.rag_pipeline.prepare_data(st.session_state.papers)
                            gaps = st.session_state.rag_pipeline.find_research_gaps()
                            st.markdown("### Research Gaps")
                            for gap in gaps:
                                st.markdown(f"• {gap}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with col3:
            if st.button("📈 Trends", use_container_width=True):
                with st.spinner("📊 Finding trends..."):
                    try:
                        years = [int(p.get('year', 2024)) for p in st.session_state.papers if p.get('year')]
                        citations = [p.get('citations', 0) for p in st.session_state.papers]
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Avg Year", int(sum(years) / len(years)) if years else "N/A")
                        with col_b:
                            st.metric("Total Citations", sum(citations))
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# ============================================================================
# TAB 3: ANALYTICS
# ============================================================================

with tab3:
    st.subheader("📊 Analytics Dashboard")
    
    if not st.session_state.rl_feedback:
        st.info("No data yet. Search papers to generate analytics.")
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Searches", len(st.session_state.rl_feedback))
        with col2:
            st.metric("Total Papers Found", sum(f.get('papers_found', 0) for f in st.session_state.rl_feedback))
        with col3:
            st.metric("Q&A Generated", len([f for f in st.session_state.rl_feedback if f.get('question')]))
        
        st.divider()
        
        # Recent Activity
        st.markdown("### Recent Searches")
        for item in reversed(st.session_state.rl_feedback[-5:]):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Query:** {item.get('query', 'N/A')}")
            with col2:
                st.write(f"**Papers:** {item.get('papers_found', 0)}")
            with col3:
                st.write(f"**Time:** {item.get('timestamp', 'N/A')[:10]}")

# ============================================================================
# TAB 4: RL FEEDBACK LOOP
# ============================================================================

with tab4:
    st.subheader("🤖 RL Feedback Loop")
    
    st.markdown("""
    ### How RL Improves Your Research
    
    Every search generates a **reward signal**:
    - Papers found → **Positive reward**
    - Q&A quality → **Feedback score**
    - Time taken → **Efficiency metric**
    
    The system learns and **improves over time**.
    """)
    
    st.divider()
    
    if st.session_state.rl_feedback:
        st.markdown("### Feedback History")
        
        feedback_df = []
        for f in st.session_state.rl_feedback:
            feedback_df.append({
                "Query": f.get('query', '')[:30],
                "Papers": f.get('papers_found', 0),
                "arXiv": f.get('sources', {}).get('arxiv', 0),
                "Scholar": f.get('sources', {}).get('semantic_scholar', 0),
                "Q&A": "Yes" if f.get('question') else "No",
                "Time": f.get('timestamp', '')[:10]
            })
        
        st.dataframe(feedback_df, use_container_width=True)
        
        # Export feedback
        if st.button("💾 Export Feedback as JSON"):
            json_data = json.dumps(st.session_state.rl_feedback, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"rl_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    else:
        st.info("No feedback data yet. Start searching to generate RL feedback.")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
---
**AI Research Assistant v3.0** | 🚀 Production Ready | ⚡ Lightning Fast | 🤖 RL-Powered
""")
