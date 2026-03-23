# 🚀 AI Research Assistant - Complete Setup & Demo Guide

## ⚡ Quick Start Commands

### 1. **First Time Setup**
```bash
cd /Users/amshumathshetty/Desktop/ai-research-assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install requests pandas faiss-cpu langchain sentence-transformers streamlit
```

### 2. **Start Ollama** (in a new terminal)
```bash
ollama serve
```

### 3. **Run the Dashboard**
```bash
cd /Users/amshumathshetty/Desktop/ai-research-assistant
source venv/bin/activate
./run.sh
```

Or directly:
```bash
streamlit run app/streamlit_app.py
```

**Dashboard opens at**: `http://localhost:8501`

---

## 📊 Testing Each Phase

### Phase 1: Data Fetching
```bash
cd /Users/amshumathshetty/Desktop/ai-research-assistant
source venv/bin/activate
python3 src/ingestion/main_fetcher.py
```
✅ Should fetch 10+ papers from Semantic Scholar & arXiv

### Phase 2: Chunking + FAISS
```bash
python3 src/processing/pipeline.py
```
✅ Should create 13+ chunks and test similarity search

### Phase 3: RAG Pipeline + LLM
```bash
python3 src/rag/pipeline.py
```
✅ Should generate answers with citations and research gaps

### Phase 4: RL Feedback System
```bash
python3 src/rl/feedback_system.py
```
✅ Should record feedback and show learning progress

---

## 🎬 Hackathon Demo Script

### What to Show Judges

#### **1. Dashboard Welcome (10 seconds)**
- Navigate to http://localhost:8501
- Show the beautiful Streamlit interface
- "This is an AI-powered research assistant"

#### **2. Query Engine Demo (30 seconds)**
- Go to "📖 Query Engine" tab
- Enter query: **"What are the main challenges in lithium-ion battery recycling?"**
- Click "Search & Answer"
- Show:
  - ✅ Retrieved papers with metadata
  - ✅ LLM-generated answer from Ollama
  - ✅ Citation tracking (papers, authors, years)

#### **3. Research Gap Detection (20 seconds)**
- Point to "🔍 Research Gaps" section
- Show detected gaps like:
  - "Efficiency is underexplored"
  - "Performance aspects rarely discussed"
  - "Impact on developing countries limited"
- Explain: **"Our system identifies research opportunities automatically!"**

#### **4. Learning System Demo (30 seconds)**
- Rate the answer (give 5 stars for all metrics)
- Click "Submit Feedback"
- Go to "📈 Learning Analytics" tab
- Show:
  - Total queries processed
  - Average reward score
  - Model weights
  - Recent feedback history
- Explain: **"This system learns from feedback and improves over time!"**

#### **5. Data Management (20 seconds)**
- Go to "📊 Data Management" tab
- Show paper fetching functionality
- Explain dual data sources (Semantic Scholar + arXiv)
- Show how papers get embedded in FAISS

#### **6. System Status (10 seconds)**
- Go to "ℹ️ About" tab
- Show system info and architecture
- Mention M2 optimization

### **Total Demo Time**: ~2 minutes

---

## 💡 Key Talking Points for Judges

### 🎯 Innovation
*"We built a system that not only retrieves papers but **learns over time** using reinforcement learning. Unlike static RAG systems, ours actively improves answer quality based on user feedback."*

### 🔬 Domain Expertise
*"We focused on lithium-ion battery research and sustainability - a critical gap in the market. Our system can accelerate research in this space."*

### 🧠 Technical Excellence
*"We integrated 5 cutting-edge technologies: Semantic Search (FAISS), LLM inference (Ollama), Dual APIs, and a self-learning feedback loop - all optimized for M2 with no GPU."*

### 🏆 Production-Ready
*"Our architecture mirrors enterprise research systems: dual data sources, proper citation tracking, gap detection, and extensible design."*

### 💪 Resourcefulness
*"Built on M2 MacBook Air with CPU-only execution. Shows we understand real-world constraints and built a truly portable solution."*

---

## 📈 Expected Outputs

### When running main_fetcher.py:
```
🔍 Fetching papers for: 'lithium-ion battery recycling sustainability'

📚 Fetching from Semantic Scholar...
✅ Got 10 papers from Semantic Scholar

📚 Fetching from arXiv...
✅ Got 10 papers from arXiv

🎯 Total papers collected: 20

📄 SAMPLE PAPERS (First 5):
[Papers with titles, abstracts, citations...]
```

### When running pipeline.py:
```
================================================================================
✂️  PHASE 2: CHUNKING PAPERS
================================================================================
✅ Created 13 chunks from 10 papers

================================================================================
🧠 PHASE 3: EMBEDDING & STORING
================================================================================
✅ Successfully embedded and stored 13 chunks in FAISS
```

### When running rag/pipeline.py:
```
================================================================================
✨ ANSWER
================================================================================

The main challenges in battery recycling include...
[Full answer from Ollama]

================================================================================
📖 CITATIONS
================================================================================
1. Lithium-Ion Battery Recycling...
   Authors: Smith, J., Johnson, M.
   Year: 2024 | Source: SEMANTIC_SCHOLAR

================================================================================
🔍 RESEARCH GAPS DETECTED
================================================================================
⚠️  'EFFICIENCY' is underexplored
⚠️  'SAFETY' is underexplored
⚠️  RESEARCH GAP: Impact on developing countries is limited
```

### When running feedback_system.py:
```
🧪 TESTING RL FEEDBACK SYSTEM

Query: What are battery recycling methods?
Reward: 0.800

================================================================================
🤖 SYSTEM LEARNING PROGRESS
================================================================================
Queries Processed: 3
Average Reward Score: 0.383/1.0
Improvement Trend: +0.00%
Status: 🟡 Good Learning

Model Weights:
  relevance: 0.250
  clarity: 0.250
  citation_quality: 0.250
  gap_detection: 0.250
```

---

## 🔧 Troubleshooting

### Issue: "Ollama is not running"
```bash
# Open new terminal and run:
ollama serve

# Check connection:
curl http://localhost:11434/api/tags
```

### Issue: "No module named 'requests'"
```bash
source venv/bin/activate
pip install requests pandas faiss-cpu langchain sentence-transformers
```

### Issue: Streamlit crashes on startup
```bash
# Check Python version:
python3 --version  # Should be 3.9+

# Reinstall streamlit:
pip install --upgrade streamlit
```

### Issue: Slow performance on M2
- Reduce `top_k` retrieval count (use 2 instead of 3)
- Use shorter queries
- Increase Ollama timeout (currently 60s)
- Close other apps to free up RAM

---

## 📊 Architecture at a Glance

```
┌────────────────────────────────────────────────┐
│           USER QUERY (Streamlit UI)            │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│         1. DUAL DATA FETCHING                  │
│  ├─ Semantic Scholar API                       │
│  └─ arXiv API                                  │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│         2. TEXT CHUNKING                       │
│  Split into 150-token chunks                   │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│         3. EMBEDDINGS (FAISS)                  │
│  SentenceTransformers → Vector DB              │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│         4. SEMANTIC RETRIEVAL                  │
│  Top-3 similar papers by similarity            │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│         5. LLM GENERATION (Ollama)             │
│  Mistral model generates answer with context   │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│         6. RESEARCH GAP DETECTION              │
│  Analyzes literature for gaps and trends       │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│    7. RL FEEDBACK LOOP (Self-Improvement)      │
│  Records user feedback → Updates weights       │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│  Answer + Citations + Gaps + Learning Metrics  │
└────────────────────────────────────────────────┘
```

---

## 📈 Success Metrics

✅ **Phase 1**: Data fetching from 2 sources
✅ **Phase 2**: Text chunking and FAISS embedding
✅ **Phase 3**: RAG pipeline with LLM integration
✅ **Phase 4**: Research gap detection
✅ **Phase 5**: RL feedback loop
✅ **Phase 6**: Streamlit dashboard
✅ **Phase 7**: Startup script and documentation

---

## 🎓 What Judges See

1. **Clean Code**: Well-structured, documented Python
2. **Working Demo**: Live dashboard with real data
3. **Innovation**: Self-learning system (RL)
4. **Impact**: Domain-focused on battery research
5. **Optimization**: Works on M2 without GPU
6. **Polish**: Beautiful Streamlit UI
7. **Completeness**: End-to-end pipeline

---

## 📝 File Locations

```
/Users/amshumathshetty/Desktop/ai-research-assistant/
├── src/
│   ├── ingestion/main_fetcher.py
│   ├── processing/chunking.py
│   ├── processing/pipeline.py
│   ├── embeddings/vector_store.py
│   ├── rag/pipeline.py
│   └── rl/feedback_system.py
├── app/streamlit_app.py
├── run.sh
└── README.md
```

---

## 🚀 Ready to Demo!

Everything is set up. Just:

1. **Terminal 1** (Ollama):
   ```bash
   ollama serve
   ```

2. **Terminal 2** (Dashboard):
   ```bash
   cd /Users/amshumathshetty/Desktop/ai-research-assistant
   source venv/bin/activate
   ./run.sh
   ```

3. **Open Browser**: http://localhost:8501

4. **Demo**: Follow the "Hackathon Demo Script" above

---

**Good luck! 🍀🏆**
