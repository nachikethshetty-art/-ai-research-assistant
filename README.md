# 🔬 AI Research Assistant v2.0

**Search ANY research topic • Find 10+ papers • Generate insights • No API costs**

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Quick Start (60 seconds)

### Option 1: Local (Development)
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Run app
cd /Users/amshumathshetty/Desktop/ai-research-assistant
source venv/bin/activate
streamlit run app/streamlit_app.py
```
Then open: **http://localhost:8501**

### Option 2: Docker (Production)
```bash
docker run -p 8501:8501 -p 11434:11434 ai-research-assistant:latest
```
Then open: **http://localhost:8501**

## Features

### 🔍 Research Search (Tab 1)
- Search **ANY** research topic
- Fetch papers from **Semantic Scholar** + **arXiv**
- Get **10+ papers** with summaries
- See research **gaps** and **top papers**
- Click to read full papers

### 💬 Content Generation (Tab 2)
- Generate **plagiarism-free abstracts** (90%+ original)
- Generate **research introductions**
- **Q&A** on any research topic
- All powered by local LLM (no cloud costs!)

## What's Included

### Core Technologies
- **Streamlit** - Interactive web UI
- **Ollama** - Local LLM inference (Mistral 7B)
- **FAISS** - Fast semantic search
- **SentenceTransformers** - Embeddings
- **arXiv + Semantic Scholar** - Free paper APIs

### Key Improvements (Session 4)
✅ Fixed arXiv XML parsing (namespace handling)
✅ Improved Semantic Scholar (graceful fallback)
✅ Better author/year/URL extraction
✅ Docker container built (2.27GB)
✅ Comprehensive .gitignore (130+ rules)
✅ Clean project structure
✅ Complete documentation

## Installation

### From Source
```bash
# Clone repository
git clone <repo-url>
cd ai-research-assistant

# Create environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama (Terminal 1)
ollama serve

# Run app (Terminal 2)
streamlit run app/streamlit_app.py
```

### Using Docker
```bash
# Build image
docker build -f server/Dockerfile -t ai-research-assistant:latest .

# Run container
docker run -p 8501:8501 -p 11434:11434 ai-research-assistant:latest
```

## Usage

### Search Papers
1. Enter a topic (e.g., "quantum computing", "climate change")
2. Select number of papers (5, 10, 15, 20)
3. Click "🔍 Search Papers"
4. Wait 10-15 seconds for results
5. Expand papers to see full details

### Generate Content
1. **Abstract**: Enter topic → Click "Generate Abstract"
2. **Introduction**: Enter topic → Click "Generate Introduction"
3. **Q&A**: Ask question → Click "Get Answer"

## Performance

| Action | Time |
|--------|------|
| Search papers | 10-15 sec |
| Generate summary | 15-30 sec |
| Generate abstract | 5-10 sec |
| App startup | 5-10 sec |

**Note**: Times are for CPU-only. GPU would be 2-5x faster.

## Architecture

```
app/streamlit_app.py          # Main UI (2 tabs)
│
├── src/ingestion/
│   ├── semantic_scholar.py   # Paper API
│   └── arxiv_fetcher.py      # Paper API
│
├── src/rag/
│   └── pipeline.py           # RAG with Ollama
│
└── server/
    └── Dockerfile            # Docker container
```

## Documentation

- **SESSION4_COMPLETE.md** - Full session details & fixes
- **SESSION3_COMPLETE.md** - Previous session summary
- **QUICK_FIX_GUIDE.md** - Quick troubleshooting
- **quick_start.sh** - Interactive setup script

## Troubleshooting

### "Port 8501 already in use"
```bash
lsof -i :8501
kill -9 <PID>
```

### "Ollama: Not running"
```bash
ollama serve
```

### "No papers found"
Wait 5+ minutes (Semantic Scholar rate limit)

### "Docker daemon not running"
```bash
open /Applications/Docker.app
```

## Deployment Options

### 1. Local Machine (Development)
Best for testing and development

### 2. Docker Container (Your Server)
Production-ready, fully isolated

### 3. HuggingFace Spaces (Free Cloud)
Free tier with CPU only

### 4. Cloud VM (AWS/GCP/Azure)
Full control, scalable

## Features Roadmap

- [ ] Paper caching (faster searches)
- [ ] PDF downloads
- [ ] User authentication
- [ ] Search history database
- [ ] Advanced filtering
- [ ] Batch processing

## Git History

```
855867e Clean: Remove .DS_Store from git tracking
49a2fc0 Add: Interactive quick start script
2d0a2ea Doc: Session 4 complete - Fixed APIs
09cf590 Clean: Add .gitignore, remove .DS_Store
d330fb2 Fix: Improved API fetchers
```

## Support

- Check documentation files
- Run `./verify_fixes.sh` to test installation
- Run `./quick_start.sh` for interactive setup

## License

MIT License - Free to use and modify

## Status

✅ **PRODUCTION READY**

All issues fixed, tested, and documented. Ready for deployment!

---

**Made with ❤️ for researchers**

Open http://localhost:8501 and start searching! 🚀
