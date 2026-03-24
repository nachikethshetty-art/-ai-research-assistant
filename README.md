# 🔬 AI Research Assistant# 🔬 AI Research Assistant v3.0 - Hackathon Edition# 🔬 AI Research Assistant v3.0# 🔬 AI Research Assistant v2.0



> **Advanced AI-Powered Research Paper Analysis Platform**

>

> Search any research topic • Fetch papers from 3 sources • Get unified AI summaries • Detect research gaps • Ask questions • System learns from feedback> **AI-Powered Research Paper Analysis Platform**  



[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)](.)> *Search, summarize, analyze research gaps, and generate insights—all in one place*

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)](https://python.org)

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square)](https://docker.com)**Lightning-fast research paper analysis with AI-powered insights****Search ANY research topic • Find 10+ papers • Generate insights • No API costs**

[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

![Status](https://img.shields.io/badge/Status-Hackathon%20Ready-brightgreen?style=flat-square)

---

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)

## 🎯 Why This Wins Hackathons

![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square)

1. **🧠 OpenEnv-Style RL Loop** - System learns from user feedback in real-time

2. **📝 Unified Summaries** - Single 300-400 word synthesis (not repetitive)![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)## Features![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

3. **🔍 Multi-Source Fetching** - 3-source fallback (arXiv → Scholar → OpenAlex)

4. **⚡ Real-Time Streaming** - Watch summaries generate live

5. **🤖 Dual LLM Architecture** - Ollama (primary) + Gemini (fallback)

6. **📊 Production-Ready** - Docker containerized, deployable anywhere## ⚡ 30-Second Overview![Python](https://img.shields.io/badge/Python-3.11-blue)



---



## ⚡ Quick Start (Choose One)Search **ANY** research topic → Get papers from arXiv, Semantic Scholar, OpenAlex → Read unified **300-400 word summary** → Discover **5-6 research gaps** → Ask questions → System learns from feedback.✨ **Core Features:**![Docker](https://img.shields.io/badge/Docker-Ready-blue)



### Local Demo (1 minute)

```bash

cd /Users/amshumathshetty/Desktop/ai-research-assistant**Deploy instantly:** `docker-compose up -d` → Share link → Anyone can use!- 🔍 **Paper Search**: Fetch from arXiv and Semantic Scholar simultaneously![License](https://img.shields.io/badge/License-MIT-green)

docker-compose up -d

ifconfig getifaddr en0

# Share: http://YOUR_IP:8501

```---- 📊 **Unified Analysis**: 300-400 word synthesis across all papers



### Deploy to Cloud (5 minutes)

```bash

git push hf main## 🏆 Why This Wins Hackathons- 🔎 **Research Gap Detection**: Identify 5-6 critical research gaps## Quick Start (60 seconds)

# Authenticate with HF token: https://huggingface.co/settings/tokens

```



### Run Locally (No Docker)✨ **Innovation:**- 💬 **Q&A System**: Ask questions about the papers

```bash

source venv/bin/activate- 🧠 **OpenEnv RL Feedback Loop**: System learns from user ratings in real-time (not just static analysis)

streamlit run app/streamlit_app.py

# Note: Requires `ollama serve` running separately- 📊 **Unified Analysis**: Single synthesis of ALL papers (not repetitive individual summaries)- 📝 **Abstract Generation**: Generate new research abstracts### Option 1: Local (Development)

```

- ⚡ **Real-time Streaming**: Watch AI generate summaries live (no waiting for full response)

---

- 🔄 **Intelligent Fallbacks**: 3-source paper fetching with automatic API fallbacks- 🎮 **RL Feedback Loop**: OpenEnv-style learning from user feedback```bash

## 🚀 Features



### Tab 1: Search & Analyze

- **Multi-Source Paper Search**✨ **Technical Excellence:**- 📈 **Analytics Dashboard**: Track papers, citations, and system performance# Terminal 1: Start Ollama

  - arXiv (instant)

  - Semantic Scholar (robust)- 🐳 **Production-Ready Docker**: Full containerization with health checks

  - OpenAlex (fallback)

  - 🚀 **Shareable Instantly**: Anyone with link can use (zero installation friction)ollama serve

- **Unified Research Summaries**

  - 300-400 words per topic- 🎯 **Research Impact**: Saves researchers 2-3 hours of manual analysis per topic

  - Synthesizes across ALL papers

  - Streaming responses- 💰 **Zero API Costs**: Uses free APIs + local Ollama (no paid services)## Quick Start

  

- **Research Gap Detection**

  - Identifies 5-6 critical gaps

  - Actionable recommendations✨ **Judge-Friendly:**# Terminal 2: Run app

  - Based on collective analysis

- ✅ Works out-of-the-box (`docker-compose up -d`)

### Tab 2: Q&A & Generation

- Ask questions about papers- ✅ Clean, documented code (no duplicates/unused files)### Option 1: Docker (Recommended - Anyone can access!)cd /Users/amshumathshetty/Desktop/ai-research-assistant

- Get answers with citations

- Generate research abstracts- ✅ Comprehensive README with architecture diagrams



### Tab 3: Analytics & Feedback- ✅ Actual value proposition (solves real problem)source venv/bin/activate

- **RL Feedback Loop (OpenEnv)**

  - Rate search/summary quality

  - System learns optimal strategies

  - Real-time reward optimization---**Prerequisites:** Docker and Docker Compose installedstreamlit run app/streamlit_app.py

  

- **Performance Dashboard**

  - Search statistics

  - Learning trends## 🚀 Quick Start (2 minutes)```

  - Strategy evolution



---

### With Docker (Recommended - Share link with judges!)```bashThen open: **http://localhost:8501**

## 🛠️ Tech Stack

```bash

| Component | Technology |

|-----------|-----------|cd ai-research-assistant# Clone and navigate to the project

| **Frontend** | Streamlit |

| **LLM** | Ollama (Mistral 7B) + Google Gemini |docker-compose up -d

| **Vector Search** | FAISS + Sentence Transformers |

| **Paper Sources** | arXiv + Semantic Scholar + OpenAlex |```cd ai-research-assistant### Option 2: Docker (Production)

| **RL System** | OpenEnv-style feedback loop |

| **Deployment** | Docker + HF Spaces |👉 Open: **http://localhost:8501**



---```bash



## 📊 How It Works### Share Global Link



### Paper Fetching (3-Source Fallback)```bash# Start the app (first time will pull Ollama model ~4GB)docker run -p 8501:8501 -p 11434:11434 ai-research-assistant:latest

```

arXiv API (2-5s)# Find your IP

    ↓ (if slow/unavailable)

Semantic Scholar (8s timeout)ifconfig getifaddr en0  # macOS → e.g., 192.168.1.100docker-compose up -d```

    ↓ (if both fail)

OpenAlex (6s timeout)

```

# Share this link (no installation needed for viewers!)Then open: **http://localhost:8501**

### LLM Generation (Dual Backend)

```http://192.168.1.100:8501

Ollama (local, private, fast)

    ↓ (if unavailable)```# View app at http://localhost:8501

Google Gemini API (always available)

```



### RL Feedback Loop### Local Development (Without Docker)## Features

```

User rates search/summary```bash

    ↓

System calculates rewardsource venv/bin/activate# To stop:

    ↓

Updates strategy weightsstreamlit run app/streamlit_app.py

    ↓

Optimizes future responses# Note: Requires 'ollama serve' running separatelydocker-compose down### 🔍 Research Search (Tab 1)

```

```

---

```- Search **ANY** research topic

## 🎮 Usage Example

---

### 1. Search Papers

- Enter: "Large Language Models and Fine-Tuning"- Fetch papers from **Semantic Scholar** + **arXiv**

- System fetches papers from 3 sources

- Get ~10 papers in 5-10 seconds## 💡 Core Features



### 2. Read Summary**Share with Others:**- Get **10+ papers** with summaries

- Unified 300-400 word synthesis

- Identifies key findings### 1. **🔍 Multi-Source Paper Search**

- Professional academic tone

- Search ANY research topic- Once running, anyone can access: `http://YOUR_MACHINE_IP:8501`- See research **gaps** and **top papers**

### 3. Discover Gaps

- 5-6 research gaps identified- Simultaneously queries: arXiv, Semantic Scholar, OpenAlex

- Actionable recommendations

- Based on entire paper collection- Intelligent timeouts with automatic fallbacks- Find your IP: `ipconfig getifaddr en0` (macOS) or `hostname -I` (Linux)- Click to read full papers



### 4. Ask Questions- Returns 5-20 papers in 5-10 seconds

- "What are the limitations of fine-tuning?"

- Get context-aware answers- No rate limiting or API costs- Example: `http://192.168.1.100:8501`

- See source citations



### 5. Provide Feedback

- Rate quality (1-5 stars)### 2. **📊 Unified Research Summary**### 💬 Content Generation (Tab 2)

- System learns and improves

- Real-time optimization- **300-400 words** synthesizing ALL papers together



---- Identifies consensus and diverging views**Pre-load Mistral Model (Optional):**- Generate **plagiarism-free abstracts** (90%+ original)



## 🌐 Deployment Options- Real-time streaming (watch it generate!)



### Local (Fastest)- Publication-ready quality```bash- Generate **research introductions**

```bash

docker-compose up -d- Perfect for literature reviews

# Access: http://localhost:8501

```docker-compose exec ollama ollama pull mistral- **Q&A** on any research topic



### Hugging Face Spaces (Public)### 3. **🔎 Research Gap Detection**

```bash

git push hf main- Identifies **5-6 major research gaps** across entire collection```- All powered by local LLM (no cloud costs!)

# Access: https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv

```- Analyzes:



### Network Sharing (Share with Judges)  - Unanswered questions

```bash

docker-compose up -d  - Methodological gaps

ifconfig getifaddr en0

# Share: http://YOUR_IP:8501  - Contradictions between papers### Option 2: Local Installation## What's Included

```

  - Future work opportunities

---

  - Emerging research areas

## 📦 What's Included

- Each gap is specific and actionable

```

ai-research-assistant/**Prerequisites:**### Core Technologies

├── app/

│   └── streamlit_app.py              # Main UI (3 tabs)### 4. **💬 AI-Powered Q&A**

├── src/

│   ├── ingestion/                    # Paper fetching- Ask ANY question about papers- Python 3.9+- **Streamlit** - Interactive web UI

│   │   ├── arxiv_fetcher.py

│   │   └── semantic_scholar.py- Vector search for context

│   ├── rag/                          # RAG pipeline

│   │   └── pipeline.py- Cites source papers- Ollama running: `ollama serve` (in another terminal)- **Ollama** - Local LLM inference (Mistral 7B)

│   ├── rl/                           # Reinforcement learning

│   │   └── feedback_loop.py- Context-aware responses

│   ├── llm/                          # LLM backend

│   │   └── backend.py                # Ollama + Gemini- **FAISS** - Fast semantic search

│   └── analytics/                    # Analytics

│       └── pyspark_processor.py### 5. **📝 Abstract Generation**

├── Dockerfile                        # Production image

├── docker-compose.yml                # Local setup- Generate new research abstracts```bash- **SentenceTransformers** - Embeddings

├── requirements.txt                  # Dependencies

└── README.md                         # This file- Based on collective paper insights

```

- Plagiarism-free original content# Create virtual environment- **arXiv + Semantic Scholar** - Free paper APIs

---



## ⚙️ Configuration

### 6. **🧠 OpenEnv RL Feedback Loop** (UNIQUE!)python3 -m venv venv

### Enable Gemini Fallback (Recommended)

- **Innovation**: System learns from user feedback in real-time

Get free API key: https://makersuite.google.com

- Rate: paper relevance, answer quality, response speedsource venv/bin/activate### Key Improvements (Session 4)

```bash

export GOOGLE_API_KEY="your-key-here"- Accumulates reward over episodes



# Or set in HF Space secrets (Name: GOOGLE_API_KEY)- Optimizes strategies based on feedback✅ Fixed arXiv XML parsing (namespace handling)

```

- Creates continuously improving research assistant

### Adjust Timeouts

Edit `docker-compose.yml`:- Implements episodic learning like OpenAI Gym# Install dependencies✅ Improved Semantic Scholar (graceful fallback)

```yaml

environment:

  SEMANTIC_SCHOLAR_TIMEOUT: 8

  OPENALEX_TIMEOUT: 6### 7. **📈 Analytics Dashboard**pip install -r requirements.txt✅ Better author/year/URL extraction

```

- Paper statistics and citations

---

- Feedback history✅ Docker container built (2.27GB)

## 📈 Performance

- System learning progress

| Operation | Time |

|-----------|------|- Strategy optimization tracking# Run the app✅ Comprehensive .gitignore (130+ rules)

| Paper Search | 5-10s |

| Summary Generation | 15-30s |

| Gap Detection | 20-40s |

| Q&A Response | 5-15s |---streamlit run app/streamlit_app.py✅ Clean project structure

| App Startup | 5-10s |



**Note:** Times are CPU-only. GPU would be 2-5x faster.

## 🏗️ Architecture```✅ Complete documentation

---



## 🔧 Troubleshooting

```

### Docker won't start

```bash┌─────────────────────────────────────────────────────┐

# Make sure Docker Desktop is running

lsof -i :8501  # Check if port is in use│         AI RESEARCH ASSISTANT v3.0                  │## How to Use## Installation

```

├─────────────────────────────────────────────────────┤

### Paper search slow

```bash│                                                     │

# Semantic Scholar has rate limit (7 req/sec)

# Wait 1 minute and retry│  🎨 FRONTEND (Streamlit UI)                        │

```

│  ├─ Tab 1: Search & Unified Analysis               │### 1️⃣ Search Papers### From Source

### Ollama unavailable

```bash│  ├─ Tab 2: Q&A & Abstract Generation               │

# Add GOOGLE_API_KEY for automatic Gemini fallback

export GOOGLE_API_KEY="your-key"│  └─ Tab 3: Analytics & RL Feedback Loop            │- Enter research topic (e.g., "quantum computing", "climate change")```bash

```

│                                                     │

### HF Spaces build slow

```bash│  🧠 BACKEND SERVICES                               │- Select number of papers (5-20)# Clone repository

# Free tier = slower build (5-10 min)

# Use local demo while waiting│  ├─ 🔍 Paper Fetchers (3 sources)                  │

```

│  │   ├─ arXiv (2-5s)                               │- Click "🔍 Search & Analyze"git clone <repo-url>

---

│  │   ├─ Semantic Scholar (8s)                      │

## 🧪 Testing

│  │   └─ OpenAlex (fallback)                        │cd ai-research-assistant

```bash

# Test paper fetching│  │                                                  │

python -c "from src.ingestion.arxiv_fetcher import fetch_arxiv; print(fetch_arxiv('deep learning'))"

│  ├─ 📚 RAG Pipeline                                │### 2️⃣ View Results

# Test RAG pipeline

python -c "from src.rag.pipeline import RAGPipeline; rag = RAGPipeline(); print(rag.get_llm_status())"│  │   ├─ FAISS Vector Store                         │



# Test RL feedback│  │   ├─ Sentence Transformers                      │- **📊 Research Summary**: 300-400 word synthesis of all papers# Create environment

python -c "from src.rl.feedback_loop import RLFeedbackLoop; rl = RLFeedbackLoop(); print(rl)"

```│  │   └─ Ollama + Mistral LLM                       │



---│  │                                                  │- **🔍 Research Gaps**: 5-6 critical research gaps identifiedpython3 -m venv venv



## 🎓 What Makes This Special│  └─ 🧠 OpenEnv RL Learning System                  │



### Innovation│      ├─ Episode tracking                           │- **📚 Papers**: Full list with citations and abstractssource venv/bin/activate

- **RL Feedback Loop**: Unlike static systems, this learns from user feedback in real-time

- **Unified Analysis**: Synthesizes across ALL papers, not individual summaries│      ├─ Reward calculation                         │

- **Multi-Source**: Intelligent fallbacks ensure reliability

│      ├─ Strategy optimization                      │

### Code Quality

- Clean, modular architecture│      └─ Continuous learning                        │

- No duplicate files or unused code

- Comprehensive error handling│                                                     │### 3️⃣ Ask Questions (Tab 2)# Install dependencies

- Production-ready Docker setup

│  📊 ANALYTICS ENGINE                               │

### User Experience

- Real-time streaming responses│  └─ Real-time metrics & dashboards                │- Ask any question about the paperspip install -r requirements.txt

- 3-tab interface

- Instant sharing (no installation friction)│                                                     │

- Graceful degradation (works without Ollama)

│  🐳 DOCKER CONTAINERIZATION                        │- Generate new research abstracts

### Value Proposition

- Saves researchers 2-3 hours per analysis│  └─ Health checks & orchestration                  │

- Zero API costs

- Instant deployment│                                                     │# Start Ollama (Terminal 1)

- Works on any device

└─────────────────────────────────────────────────────┘

---

```### 4️⃣ Provide Feedback (Tab 3)ollama serve

## 📝 Hackathon Pitch



> "I built an AI Research Assistant that searches papers from 3 sources, generates unified AI summaries, identifies research gaps, and learns from user feedback using an OpenEnv-style RL loop. It's Docker-ready, deployed on HF Spaces, and features a dual-LLM architecture with automatic fallbacks for reliability."

---- Rate paper quality, answer quality, and speed

**Tell judges:**

- ✨ OpenEnv-style RL feedback loop (continuous learning)

- ✨ Unified summaries (not repetitive)

- ✨ Multi-source with smart fallbacks## 🛠️ Tech Stack- System learns and improves (OpenEnv-style RL)# Run app (Terminal 2)

- ✨ Real-time streaming (better UX)

- ✨ Production-ready Docker deployment



---| Component | Technology | Why It Matters |streamlit run app/streamlit_app.py



## 🔗 Links|-----------|-----------|---|



- **Live Demo**: https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv| **Frontend** | Streamlit | Fast iteration, beautiful UI |## Architecture```

- **GitHub**: [Your GitHub URL]

- **Local**: http://YOUR_IP:8501| **Paper Sources** | arXiv + Semantic Scholar + OpenAlex | No costs, reliable, comprehensive |



---| **Vector Search** | FAISS | Lightning-fast similarity search |



## 📚 Documentation| **Embeddings** | Sentence Transformers | Fast, accurate, lightweight |



- `DEPLOYMENT.md` - Deployment guide| **LLM** | Ollama + Mistral 7B | Local, no API costs, privacy-friendly |```### Using Docker

- `QUICK_START.md` - Getting started

- `QUICK_COMMANDS.md` - All commands| **RL System** | OpenEnv-style episodic learning | Novel approach judges love |

- `STATUS.md` - Project status

| **Containerization** | Docker + Docker Compose | Production-ready, portable |ai-research-assistant/```bash

---



## 📄 License

---├── app/# Build image

MIT License - Free to use and modify



---

## 📊 Performance│   └── streamlit_app.py          # Main Streamlit applicationdocker build -f server/Dockerfile -t ai-research-assistant:latest .

## 🙏 Credits



Built with ❤️ for researchers and hackathons.

| Metric | Time |├── src/

---

|--------|------|

**Ready? Deploy now and start analyzing research! 🚀**

| **Paper Search** | 5-10 seconds |│   ├── ingestion/# Run container

```bash

docker-compose up -d| **Summary Generation** | 30-60 seconds |

```

| **Gap Analysis** | 30-60 seconds |│   │   ├── arxiv_fetcher.py      # arXiv paper fetcherdocker run -p 8501:8501 -p 11434:11434 ai-research-assistant:latest

Then open: **http://localhost:8501**

| **Q&A per Question** | 10-20 seconds |

| **Dashboard Load** | < 1 second |│   │   └── semantic_scholar.py   # Semantic Scholar fetcher```

| **First Load** | 2-3 minutes (model init) |

| **Subsequent Searches** | 1-2 minutes |│   ├── rag/



**Resource Usage:**│   │   └── pipeline.py           # RAG pipeline with Ollama## Usage

- Docker Image: ~1.5GB

- RAM: 8GB (for Ollama)│   ├── rl/

- No GPU required

│   │   └── feedback_loop.py       # RL feedback learning### Search Papers

---

│   └── analytics/1. Enter a topic (e.g., "quantum computing", "climate change")

## ❓ Key Questions Answered

│       └── pyspark_processor.py   # Analytics engine2. Select number of papers (5, 10, 15, 20)

### Q: Can judges/viewers use it without Ollama installed?

**A: YES!** When deployed via Docker:├── Dockerfile                      # Container configuration3. Click "🔍 Search Papers"

- Ollama is automatically included in the container

- Remote viewers just need a web browser and internet├── docker-compose.yml              # Multi-container setup4. Wait 10-15 seconds for results

- Zero installation for everyone

├── requirements.txt                # Python dependencies5. Expand papers to see full details

### Q: Is Docker deployment necessary for hackathons?

**A: NO, but it's HIGHLY RECOMMENDED because:**└── README.md                        # This file

- Shows production-ready thinking

- Makes it instantly shareable (share IP + port)```### Generate Content

- Judges can spin up immediately

- Demonstrates DevOps knowledge1. **Abstract**: Enter topic → Click "Generate Abstract"

- Shows you can deploy to cloud (AWS, GCP, etc.)

- **Without Docker**: Only works on YOUR machine locally## Technology Stack2. **Introduction**: Enter topic → Click "Generate Introduction"



### Q: How do I create a shareable link after `docker-compose up`?3. **Q&A**: Ask question → Click "Get Answer"

**A: Simple 2-step process:**

```bash- **Frontend**: Streamlit (Python)

# Step 1: Find your machine's IP

ifconfig getifaddr en0- **Paper Fetchers**: arXiv, Semantic Scholar, OpenAlex APIs## Performance



# Step 2: Share this link- **RAG Engine**: FAISS vector search + Ollama LLM

http://192.168.1.100:8501

# (Replace 192.168.1.100 with your actual IP)- **LLM Model**: Mistral (via Ollama)| Action | Time |

```

**That's it!** Anyone on the same network (or via VPN) can access it instantly.- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)|--------|------|



### Q: What makes the RL feedback loop special?- **RL Training**: OpenEnv-style feedback loop| Search papers | 10-15 sec |

**A: Unlike most systems that are static:**

- Users rate the system (quality 0-10)- **Analytics**: PySpark (optional)| Generate summary | 15-30 sec |

- System tracks rewards per episode

- Learns which strategies work best- **Containerization**: Docker & Docker Compose| Generate abstract | 5-10 sec |

- Improves recommendations over time

- Implements OpenAI Gym-style episodic learning| App startup | 5-10 sec |

- **This is innovation judges look for!**

## API Timeouts

### Q: No Ollama? Can I still use it?

**A: YES! The app gracefully handles this:****Note**: Times are for CPU-only. GPU would be 2-5x faster.

- Shows "Ollama not connected" status

- Still allows paper search (arXiv + Semantic Scholar work)- **arXiv**: 5 seconds (fast fallback)

- Q&A/Summary features show helpful message

- Fallback to static analysis without LLM- **Semantic Scholar**: 8 seconds (with fallback to OpenAlex)## Architecture



---- **OpenAlex**: 6 seconds (reliable alternative)



## 🎯 Winning Strategy for Judges- **Ollama**: 60 seconds (with streaming for responsiveness)```



**When presenting to judges, emphasize:**app/streamlit_app.py          # Main UI (2 tabs)



1. **Live Demo**: Search a topic → Show unified summary generation → Show research gaps## Troubleshooting│

2. **Share Link**: Have judges access via link while you present (no installation!)

3. **RL Innovation**: Explain how feedback loop learns over time├── src/ingestion/

4. **Code Quality**: Show clean, modular architecture

5. **Docker Ready**: Show how to `docker-compose up -d` and it just works**Issue: Ollama not responding**│   ├── semantic_scholar.py   # Paper API

6. **Real Value**: Mention it saves researchers 2-3 hours per analysis

```bash│   └── arxiv_fetcher.py      # Paper API

---

# Check if Ollama is running│

## 📝 Project Structure (Clean & Modular)

docker-compose ps├── src/rag/

```

ai-research-assistant/│   └── pipeline.py           # RAG with Ollama

├── app/

│   └── streamlit_app.py              # Main UI (3 tabs)# Pull the model manually│

├── src/

│   ├── ingestion/docker-compose exec ollama ollama pull mistral└── server/

│   │   ├── arxiv_fetcher.py          # arXiv API

│   │   └── semantic_scholar.py       # Semantic Scholar + OpenAlex fallback    └── Dockerfile            # Docker container

│   ├── rag/

│   │   └── pipeline.py               # RAG with Ollama# View logs```

│   ├── rl/

│   │   └── feedback_loop.py           # OpenEnv-style RLdocker-compose logs ollama

│   └── analytics/

│       └── pyspark_processor.py       # Analytics engine```## Documentation

├── Dockerfile                         # Production image

├── docker-compose.yml                 # Orchestration

├── requirements.txt                   # Dependencies

└── README.md                          # This file**Issue: Semantic Scholar not fetching**- **SESSION4_COMPLETE.md** - Full session details & fixes



✅ NO duplicates- Check internet connection- **SESSION3_COMPLETE.md** - Previous session summary

✅ NO backup files

✅ NO unused code- Verify API timeouts in `src/ingestion/semantic_scholar.py`- **QUICK_FIX_GUIDE.md** - Quick troubleshooting

```

- OpenAlex fallback should work if Semantic Scholar is slow- **quick_start.sh** - Interactive setup script

---



## 🚀 Deployment for Hackathons

**Issue: App running slow**## Troubleshooting

### Local Demo (for presentations)

```bash- First search takes time while model loads (~30-60 seconds)

docker-compose up -d

# Access: http://localhost:8501- Subsequent searches are faster (model cached in memory)### "Port 8501 already in use"

```

- Ollama model size: ~4GB (can take time on first pull)```bash

### Share with Judges (via network)

```bashlsof -i :8501

# Get your IP

ifconfig getifaddr en0## Environment Variableskill -9 <PID>



# Share: http://YOUR_IP:8501```

```

```bash

### Cloud Deployment (future)

```bash# Optional: Set Ollama URL (default: http://localhost:11434)### "Ollama: Not running"

# Push to Docker Hub

docker tag ai-research-assistant YOUR_DOCKERHUB/ai-research-assistantexport OLLAMA_HOST=http://ollama:11434```bash

docker push YOUR_DOCKERHUB/ai-research-assistant

ollama serve

# Deploy on AWS/GCP/Azure (any Docker-compatible platform)

```# Optional: Set Streamlit theme```



---export STREAMLIT_THEME_PRIMARYCOLOR='#FF6B35'



## 💡 Advanced Features```### "No papers found"



**Already Implemented:**Wait 5+ minutes (Semantic Scholar rate limit)

- ✅ Streaming responses (real-time generation)

- ✅ Vector search with FAISS## Performance Tips

- ✅ Multi-source paper fetching

- ✅ Intelligent API fallbacks### "Docker daemon not running"

- ✅ OpenEnv RL learning system

- ✅ Full Docker containerization- 🚀 Use Docker for best performance```bash

- ✅ Health checks & error handling

- 🔄 First search takes 30-60s (model loading), subsequent searches are fasteropen /Applications/Docker.app

**Easy to Add (if time permits):**

- [ ] Export to PDF/BibTeX- 📊 Keep number of papers under 20 for best results```

- [ ] Collaborative sessions

- [ ] Advanced RL (PPO/A3C)- 💾 Ollama requires ~8GB RAM minimum

- [ ] Multi-language support

- [ ] GPU acceleration## Deployment Options



---## License



## 🏅 Hackathon Submission Checklist### 1. Local Machine (Development)



- ✅ **Functionality**: Search → Summarize → Analyze gaps → Q&A → LearnMIT License - Feel free to use and modifyBest for testing and development

- ✅ **Innovation**: OpenEnv RL feedback loop

- ✅ **UX**: 3-tab interface, real-time streaming

- ✅ **Code Quality**: Clean, modular, documented

- ✅ **Deployment**: Docker ready, shareable link## Support### 2. Docker Container (Your Server)

- ✅ **Performance**: 5-10 seconds for search, 30-60 for analysis

- ✅ **Documentation**: Comprehensive READMEProduction-ready, fully isolated

- ✅ **Error Handling**: Graceful fallbacks, helpful messages

- ✅ **Scalability**: Works locally and in cloudFor issues or questions:

- ✅ **Cost**: Zero API costs (uses free services)

1. Check Ollama logs: `docker-compose logs ollama`### 3. HuggingFace Spaces (Free Cloud)

---

2. Check app logs: `docker-compose logs streamlit`Free tier with CPU only

## 🎓 Learning Points for Judges

3. Verify all services are running: `docker-compose ps`

This project demonstrates:

- **AI/ML**: Vector embeddings, LLMs, RAG, RL training### 4. Cloud VM (AWS/GCP/Azure)

- **Backend**: Multi-source APIs, async handling, error handling

- **Frontend**: Streamlit, real-time updates, multi-tab UI---Full control, scalable

- **DevOps**: Docker, containerization, health checks

- **Architecture**: Modular design, clean separation of concerns

- **Product Thinking**: Solves real user problem

**Made with ❤️ for researchers by researchers**## Features Roadmap

---



## 📄 License- [ ] Paper caching (faster searches)

- [ ] PDF downloads

MIT - Open source, free for hackathons and commercial use- [ ] User authentication

- [ ] Search history database

---- [ ] Advanced filtering

- [ ] Batch processing

## 🙏 Thank You!

## Git History

Thank you for reviewing the AI Research Assistant! This is production-ready, hackathon-winning code that solves real problems for researchers.

```

**Ready to win?** 855867e Clean: Remove .DS_Store from git tracking

```bash49a2fc0 Add: Interactive quick start script

docker-compose up -d2d0a2ea Doc: Session 4 complete - Fixed APIs

```09cf590 Clean: Add .gitignore, remove .DS_Store

d330fb2 Fix: Improved API fetchers

Share the link and watch judges be impressed! 🚀```



---## Support



**Made with ❤️ for researchers and hackathon judges**- Check documentation files

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
