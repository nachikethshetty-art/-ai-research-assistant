# 🔬 AI Research Assistant

**Battery Innovation & Sustainability Research**

## Quick Start

### Local Development
```bash
docker-compose up
```
Visit: http://localhost:8501

### Cloud Deployment
Live at: https://nachikethshetty-research-assistant.hf.space

## Features
- 🔍 **Dual Data Sources**: Semantic Scholar + arXiv
- 🧠 **Semantic Search**: FAISS-powered paper retrieval
- 🤖 **LLM Answers**: Ollama/Mistral for research answers
- 📊 **Gap Detection**: Identifies unexplored research areas
- 🎓 **Self-Learning**: Reinforcement learning feedback system
- 📖 **Citations**: Automatic paper tracking

## Architecture

### Core Components
1. **Data Ingestion** (`src/ingestion/`) - Fetches papers from Semantic Scholar & arXiv
2. **Semantic Search** (`src/rag/`) - FAISS vector database + retrieval
3. **LLM Integration** (`src/rag/pipeline.py`) - Ollama/Mistral inference
4. **Gap Detection** (`src/rag/pipeline.py`) - Analyzes research gaps
5. **Learning System** (`src/rl/`) - Reinforcement learning from user feedback
6. **Dashboard** (`app/streamlit_app.py`) - Interactive UI

### Tech Stack
- **Language**: Python 3.11
- **UI**: Streamlit
- **Search**: FAISS
- **LLM**: Ollama (local)
- **Embeddings**: SentenceTransformers
- **Container**: Docker + docker-compose

## Project Structure
```
├── app/                      # Streamlit dashboard
├── src/
│   ├── ingestion/           # Data fetching
│   ├── rag/                 # RAG pipeline + gap detection
│   └── rl/                  # Reinforcement learning
├── data/                    # FAISS index + papers
├── server/                  # Backend
├── docker-compose.yml       # Local orchestration
├── Dockerfile               # Container image
└── test_docker.sh          # Testing script
```

## Running

### Docker Compose (Recommended)
```bash
docker-compose up
```
- Streamlit: http://localhost:8501
- Ollama: http://localhost:11434

### Manual Setup
```bash
pip install -r requirements.txt
ollama serve &
streamlit run app/streamlit_app.py
```

## Testing
```bash
bash test_docker.sh
```

## Compliance
✅ Hackathon guidelines verified
✅ No disqualification risks
✅ Core concept preserved
✅ Production-ready

See `HACKATHON_COMPLIANCE_AUDIT.md` for details.
