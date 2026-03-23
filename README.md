# 🔬 AI Research Assistant for Battery Innovation & Sustainability

A **self-improving AI system** that revolutionizes research discovery for lithium-ion battery innovation and sustainability. Combines **RAG (Retrieval-Augmented Generation)**, **semantic search**, **reinforcement learning**, and **interactive dashboards** for research acceleration.

---

## 🎯 What Makes This Project Win 🏆

### 1. **Domain-Specific Focus** 🎓
- Focused on **lithium-ion battery research** and **sustainability**
- Real-world problem with high impact
- Addresses critical gap in battery recycling research

### 2. **Self-Improving AI (RL Loop)** 🤖
- System **learns from user feedback**
- Adapts retrieval and ranking over time
- Tracks learning progress and improvement metrics
- **Judges love this!** Shows true innovation

### 3. **Production-Grade Architecture** ⚙️
- Dual data sources (Semantic Scholar + arXiv)
- FAISS vector database for fast retrieval
- LLM-powered answer generation (Ollama/Mistral)
- Proper citation and attribution tracking

### 4. **Research Gap Detection** 🔍 ⭐
- Identifies underexplored areas in literature
- Analyzes trends and contradictions
- Highlights missing research opportunities
- **This is your killer feature!**

### 5. **Optimized for Limited Resources** 💪
- Works flawlessly on **M2 MacBook Air (no GPU)**
- Lightweight models and efficient chunking
- Careful memory management
- Production-ready performance

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Ollama (running locally)
- macOS with M2 chip (or any modern system)

### Installation

```bash
# Clone or navigate to project
cd ai-research-assistant

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install requests pandas faiss-cpu langchain sentence-transformers streamlit

# Make startup script executable
chmod +x run.sh
```

### Start Ollama (in another terminal)
```bash
ollama serve
```

### Run the Dashboard
```bash
./run.sh
```

Or directly:
```bash
source venv/bin/activate
streamlit run app/streamlit_app.py
```

The dashboard opens at `http://localhost:8501`

---

## 📊 System Architecture

```
User Query
    ↓
┌─────────────────────────────────────┐
│ PHASE 1: DATA FETCHING              │
├─────────────────────────────────────┤
│ ├─ Semantic Scholar API             │
│ └─ arXiv API (fallback)             │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ PHASE 2: CHUNKING & EMBEDDING       │
├─────────────────────────────────────┤
│ ├─ Smart text chunking              │
│ └─ SentenceTransformers encoding    │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ PHASE 3: VECTOR STORAGE (FAISS)     │
├─────────────────────────────────────┤
│ └─ Fast similarity search            │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ PHASE 4: RAG PIPELINE               │
├─────────────────────────────────────┤
│ ├─ Retrieve top-K papers            │
│ ├─ LLM generation (Ollama/Mistral)  │
│ └─ Research gap detection           │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ PHASE 5: REINFORCEMENT LEARNING     │
├─────────────────────────────────────┤
│ ├─ Collect user feedback            │
│ ├─ Calculate rewards                │
│ ├─ Update model weights             │
│ └─ Track improvement metrics        │
└────────────┬────────────────────────┘
             ↓
        💡 Answer + Citations + Gaps
```

---

## 📁 Project Structure

```
ai-research-assistant/
│
├── src/
│   ├── ingestion/
│   │   ├── main_fetcher.py         # Dual fetcher (Semantic Scholar + arXiv)
│   │   ├── semantic_scholar.py     # Semantic Scholar API
│   │   └── arxiv_fetcher.py        # arXiv API
│   │
│   ├── processing/
│   │   ├── chunking.py             # Smart text chunking
│   │   └── pipeline.py             # Integration pipeline
│   │
│   ├── embeddings/
│   │   └── vector_store.py         # FAISS vector database
│   │
│   ├── rag/
│   │   └── pipeline.py             # RAG + LLM integration + Gap detection
│   │
│   └── rl/
│       └── feedback_system.py       # RL feedback loop
│
├── app/
│   └── streamlit_app.py            # Interactive dashboard
│
├── data/
│   └── feedback.json               # RL feedback history
│
├── run.sh                          # Startup script
├── requirements.txt                # Dependencies
└── README.md                       # This file
```

---

## 🎮 How to Use

### 1. **Web Dashboard** (Recommended)
```bash
./run.sh
```
Navigate to `http://localhost:8501` and:
- 🔍 **Query Engine**: Ask research questions
- 📥 **Data Management**: Fetch and load papers
- 📊 **Learning Analytics**: Monitor system improvement
- 📖 **Citations**: Track paper sources
- 📈 **Research Gaps**: Identify opportunities

### 2. **Direct Python Scripts**

**Fetch papers:**
```bash
python3 src/ingestion/main_fetcher.py
```

**Full pipeline (fetch → chunk → embed):**
```bash
python3 src/processing/pipeline.py
```

**RAG + Gap detection:**
```bash
python3 src/rag/pipeline.py
```

**RL feedback system:**
```bash
python3 src/rl/feedback_system.py
```

---

## 🔑 Key Features

### ✨ Smart Retrieval
- **Semantic search** using FAISS
- **Top-K ranking** by similarity
- **Context preservation** with metadata

### 🤖 LLM Integration
- **Ollama** local inference
- **Mistral** lightweight model
- **Prompt optimization** for M2

### 🎯 Research Gap Detection
Identifies:
- Underexplored topics
- Missing research areas
- Contradictions in literature
- Regional/domain gaps

### 📚 Dual Data Sources
- **Semantic Scholar**: Rich metadata, author info
- **arXiv**: Reliable fallback, preprints

### 🧠 Self-Learning System
- **Reward calculation** from user feedback
- **Weight adjustment** over time
- **Progress tracking** with metrics
- **Trend analysis** for improvement

### 📖 Citation Management
- **Automatic tracking** of sources
- **Author preservation**
- **Year and publication info**

---

## 📊 Learning System Details

### Reward Calculation
```
Reward = (Relevance_score + Clarity_score + Citation_score + Gap_score) / 4

Where each score = User_rating / 5.0
```

### Weight Updates
- **High Reward (>0.75)**: Increase model confidence
- **Low Reward (<0.50)**: Decrease weight, explore alternatives
- **Learning Rate**: 5% (conservative for M2)

### Metrics Tracked
- Total queries processed
- Average reward per query
- Improvement trend (%)
- Model weight distribution
- Feedback history

---

## 💻 Performance Optimizations for M2

1. **Lightweight Embedding Model**
   - `all-MiniLM-L6-v2` (384-dim, fast)
   - CPU-optimized inference
   - No GPU required

2. **Efficient Chunking**
   - 150-200 token chunks
   - Sentence-boundary preservation
   - Memory-friendly splitting

3. **Limited Context**
   - Top-3 papers per query
   - Short prompts for Ollama
   - 60-second timeout for inference

4. **Caching & Indexing**
   - FAISS in-memory storage
   - No external database
   - Quick JSON feedback persistence

---

## 🎬 Hackathon Demo Flow

```
1. Open dashboard (http://localhost:8501)
2. Go to "Query Engine" tab
3. Enter query: "What are the challenges in battery recycling?"
4. System retrieves papers and generates answer
5. Show retrieved papers (citations)
6. Highlight research gaps detected
7. Rate the answer (give positive feedback)
8. Go to "Learning Analytics" tab
9. Show improved learning metrics
10. Explain: "This system learns and improves over time!"
```

**Judge Impression**: 🤯 Production-ready, self-improving, domain-focused AI!

---

## 🧪 Testing

### Quick Test
```bash
source venv/bin/activate
python3 src/rag/pipeline.py
```

### Full Integration Test
```bash
python3 src/processing/pipeline.py
```

### RL Feedback Test
```bash
python3 src/rl/feedback_system.py
```

---

## ⚙️ Configuration

Edit `src/rag/pipeline.py` to adjust:
- `chunk_size`: Token size for text chunking (100-300)
- `top_k`: Number of papers to retrieve (1-10)
- `model`: LLM model name (e.g., "mistral", "llama3")
- `ollama_url`: Ollama server address

---

## 📈 Expected Results

### First Run
- ✅ Fetches 5-20 papers from dual sources
- ✅ Creates 20-50 chunks from abstracts
- ✅ Generates embeddings (~30-60 seconds on M2)
- ✅ Answers queries with citations

### After Feedback
- ✅ Records reward scores
- ✅ Adjusts model weights
- ✅ Improves retrieval ranking
- ✅ Shows learning progress

---

## 🐛 Troubleshooting

### "Ollama is not running"
```bash
# In another terminal:
ollama serve
```

### "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "FAISS error"
```bash
pip install --upgrade faiss-cpu
```

### Slow inference on M2
- Reduce `top_k` to 2-3
- Use shorter queries
- Increase Ollama timeout

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ **RAG Systems**: Retrieval-augmented generation
- ✅ **Vector Databases**: FAISS for semantic search
- ✅ **LLM Integration**: Local Ollama inference
- ✅ **Reinforcement Learning**: Feedback-based improvement
- ✅ **Web UI**: Streamlit for interactive apps
- ✅ **API Integration**: Semantic Scholar & arXiv
- ✅ **Data Processing**: Chunking, embeddings, indexing

---

## 🏆 Hackathon Winning Points

| Feature | Impact | Status |
|---------|--------|--------|
| Domain Focus (Battery) | High | ✅ |
| Dual Data Sources | High | ✅ |
| RAG System | High | ✅ |
| Self-Learning (RL) | Very High | ✅ |
| Research Gap Detection | Very High | ✅ |
| Beautiful UI | Medium | ✅ |
| M2 Optimization | Medium | ✅ |
| Citation Tracking | Medium | ✅ |

---

## 📚 References

- [Semantic Scholar API](https://api.semanticscholar.org/)
- [arXiv API](https://arxiv.org/help/api/)
- [FAISS Documentation](https://faiss.ai/)
- [SentenceTransformers](https://www.sbert.net/)
- [Ollama](https://ollama.ai/)
- [Streamlit](https://streamlit.io/)

---

## 👨‍💻 Development Team

Built for maximum impact at hackathons with:
- AI/ML expertise
- Production-grade code
- Focus on real problems
- Emphasis on learning & improvement

---

## 📝 License

MIT License - Feel free to use and modify

---

## 🚀 Future Enhancements

- [ ] Add more data sources (PubMed, IEEE, ResearchGate)
- [ ] Implement multi-language support
- [ ] Add paper summarization
- [ ] Create research trend visualization
- [ ] Add collaborative features
- [ ] Deploy to cloud (AWS, GCP)
- [ ] Mobile app version
- [ ] Advanced RL with Q-learning

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify Ollama is running
3. Check Python version (3.9+)
4. Review error messages

---

**Built with ❤️ for Battery Innovation Research** 🔋⚡

**Optimized for M2 MacBook Air** 🍎

**Ready for Hackathon Success** 🏆
