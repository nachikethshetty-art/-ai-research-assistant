# 🔬 AI Research Assistant

> **Advanced AI-Powered Research Paper Analysis Platform**

Search any research topic • Fetch papers from 3 sources • Get unified AI summaries • Detect research gaps • Ask questions • System learns from feedback

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square)](https://docker.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud%20Ready-FF4B4B?style=flat-square)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 🎯 What It Does

1. **🔍 Multi-Source Paper Search** - Fetches from arXiv, Semantic Scholar, and OpenAlex
2. **✍️ AI-Powered Summaries** - Unified 300-400 word synthesis (not repetitive)
3. **🕵️ Research Gap Detection** - Identifies 5-6 key research gaps automatically
4. **💬 Interactive Q&A** - Ask follow-up questions about papers
5. **🧠 Reinforcement Learning Loop** - System learns from your feedback over time
6. **⚡ Real-Time Streaming** - Watch summaries generate live
7. **📊 Analytics Dashboard** - Track search history and patterns

---

## 🚀 Quick Start

### Option 1: Streamlit Cloud (Recommended)
1. Visit: https://streamlit.io/cloud
2. Connect your GitHub account
3. Deploy this repo → Select `app/streamlit_app.py`
4. Add `GOOGLE_API_KEY` to secrets
5. Done! Your app is live in 2 minutes

### Option 2: Local Docker
```bash
docker-compose up -d
# Visit http://localhost:7860
```

### Option 3: Local Python
```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

---

## 🔑 Environment Setup

Create a `.env` file (or use Streamlit secrets):
```
GOOGLE_API_KEY=your_api_key_here
```

Get a free API key:
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Add it to your `.env` or Streamlit secrets

---

## 📋 Project Structure

```
.
├── app/
│   └── streamlit_app.py       # Main web interface
├── src/
│   ├── ingestion/             # Paper fetching pipeline
│   │   ├── arxiv.py
│   │   ├── semantic_scholar.py
│   │   └── openAlex.py
│   ├── processing/            # Data processing
│   │   ├── embeddings/        # Vector embeddings
│   │   └── rag/               # RAG pipeline
│   └── llm/
│       └── backend.py         # LLM abstraction (Ollama + Gemini)
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
└── docker-compose.yml         # Local dev setup
```

---

## 🧠 How It Works

1. **Paper Fetching**: Enter a research topic → System queries 3 sources → Returns ranked results
2. **Unified Summary**: Papers are chunked → Embedded with Sentence Transformers → Searched with FAISS → Summarized with Gemini API
3. **Gap Detection**: AI identifies what's missing in current research
4. **Q&A**: Ask follow-up questions on the retrieved papers
5. **Learning**: Your feedback (ratings, corrections) trains an RL reward model

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **LLM (Primary)** | Ollama (local) |
| **LLM (Fallback)** | Google Gemini API |
| **Vector DB** | FAISS |
| **Embeddings** | Sentence Transformers |
| **Paper APIs** | arXiv, Semantic Scholar, OpenAlex |
| **RL Framework** | Custom OpenEnv-style loop |
| **Container** | Docker |
| **Deployment** | Streamlit Cloud / HF Spaces / Self-hosted |

---

## 📊 Features Breakdown

### Search Tab
- Multi-source paper search with ranking
- Configurable number of results (1-20 papers)
- Paper metadata display (title, authors, date, abstract)

### Analyze Tab
- Unified AI summary (300-400 words)
- Automatic research gap detection
- Key findings extraction
- Related topics suggestion

### Q&A Tab
- Ask follow-up questions about retrieved papers
- Context-aware answers using RAG
- Streaming responses for better UX

### Analytics Tab
- Search history visualization
- Topic frequency analysis
- API usage tracking

---

## 🚀 Deployment

### Streamlit Cloud
- Connect GitHub repo
- Select `app/streamlit_app.py`
- Add secrets: `GOOGLE_API_KEY`
- Auto-deploys on every push

### Docker (Self-hosted)
```bash
docker build -t ai-research-assistant .
docker run -p 7860:7860 -e GOOGLE_API_KEY=your_key ai-research-assistant
```

### Local Development
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

---

## 📝 Configuration

### requirements.txt
All dependencies are listed. Key packages:
- `streamlit` - Web framework
- `faiss-cpu` - Vector search
- `sentence-transformers` - Embeddings
- `google-generativeai` - Gemini API
- `requests` - HTTP client for APIs

### Dockerfile
- Optimized for Streamlit Cloud
- Port: 7860
- Health checks included
- Multi-stage build for efficiency

---

## 🤝 Contributing

Feel free to fork, modify, and deploy for your own use case!

---

## 📄 License

MIT License - Use freely for any purpose

---

## 🔧 Troubleshooting

**App won't start?**
- Check Python version: `python --version` (need 3.11+)
- Install requirements: `pip install -r requirements.txt`

**Papers not loading?**
- Check internet connection
- Try a different API (arXiv → Scholar → OpenAlex)

**Summaries taking too long?**
- First summary is slower (embedding computation)
- Subsequent summaries use cached embeddings

**Gemini API errors?**
- Verify API key is correct
- Check you have remaining free tier quota (50 req/day)
- Sign up for free at: https://makersuite.google.com/app/apikey

---

## 👨‍💻 Author

Built for research and hackathons. Star this repo if you find it useful! ⭐
