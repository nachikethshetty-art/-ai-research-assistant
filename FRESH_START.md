# AI Research Assistant v2.0 - FRESH START

## 🎯 New Vision

✅ **Search ANY Topic** - Not just battery, any research area
✅ **Find 10+ Papers** - From Semantic Scholar + arXiv combined
✅ **Beautiful UI** - Simple search input, then rich results
✅ **Smart Features**:
   - Paper summaries with citations
   - Research gap detection
   - Top papers ranking
   - Plagiarism-free content generation (Abstract/Intro)
   - Q&A with Ollama LLM

✅ **Ollama Integration** - Lightweight, deployable, no GPU needed

---

## 🚀 Quick Start

### Step 1: Start Ollama (if not running)
```bash
ollama serve
```
In another terminal, pull a lightweight model:
```bash
ollama pull mistral
```

### Step 2: Run the App
```bash
cd /Users/amshumathshetty/Desktop/ai-research-assistant
source venv/bin/activate
streamlit run app/streamlit_app.py
```

**Opens at:** `http://localhost:8501`

---

## 📖 How to Use

### Tab 1: Research Search (Main Feature)

1. **Enter a topic** - Click search input, type any research topic
   - Examples: "quantum computing", "climate change", "AI ethics", "cryptocurrency"
   
2. **Search papers** - Click "🔍 Search Papers" button
   - Fetches from Semantic Scholar + arXiv
   - Shows 10+ papers with:
     - Title, Authors, Year
     - Citation count
     - Abstract preview
     - Link to full paper

3. **View summaries** - Click "Generate Summary"
   - Creates overview of research area
   - Uses Ollama + RAG pipeline

4. **Find gaps** - Click "Identify Research Gaps"
   - Shows unexplored areas
   - Highlights missing research

5. **Top papers** - See papers ranked by citations
   - Most influential research first

### Tab 2: Q&A & Content Generation

1. **Generate Abstract** - Create plagiarism-free abstract
   - Input: Research topic
   - Output: 90%+ original abstract

2. **Generate Introduction** - Create paper introduction
   - Input: Research topic
   - Output: 90%+ original intro

3. **Ask Questions** - Q&A with Ollama
   - Ask anything about research
   - Get AI-generated answers

---

## 📁 Project Structure

```
ai-research-assistant/
├── app/
│   ├── streamlit_app.py          # NEW: Main app (ANY topic search)
│   └── streamlit_app_old.py      # Backup of old version
├── src/
│   ├── ingestion/                # Data fetching
│   │   ├── semantic_scholar.py   # Semantic Scholar API
│   │   └── arxiv_fetcher.py      # arXiv API
│   ├── rag/
│   │   └── pipeline.py           # RAG + Ollama (restored)
│   ├── embeddings/
│   │   └── vector_store.py       # FAISS
│   ├── rl/
│   │   └── feedback_system.py    # Learning system
│   └── content_generator/
│       └── research_generator.py # Abstract/Intro generation
├── server/
│   └── Dockerfile                # Updated: Ollama + Streamlit
├── requirements.txt              # Cleaned: removed Groq
└── README.md                     # Updated documentation
```

---

## 🧪 Testing

### Test 1: Unit Tests
```bash
source venv/bin/activate
python3 test_app.py
```

### Test 2: Run App Locally
```bash
source venv/bin/activate
streamlit run app/streamlit_app.py
```

Then in the UI:
1. Type a topic (e.g., "machine learning")
2. Click "🔍 Search Papers"
3. See 10+ papers appear
4. Click "Generate Summary"
5. Click "Identify Research Gaps"

### Test 3: Docker Test
```bash
docker build -f server/Dockerfile -t research-assistant .
docker run -p 8501:8501 -p 11434:11434 research-assistant
```

---

## 🔑 Key Changes from v1

| Feature | v1 (Battery Only) | v2 (ANY Topic) |
|---------|-----------------|----------------|
| Topics | Only battery | Any research topic |
| Papers | Limited | 10+ from dual sources |
| Search | Simple | Rich UI with summaries |
| LLM | Groq (failed) | Ollama (lightweight) |
| Content | Q&A only | Abstract + Intro + Q&A |
| UI | 5 tabs | 2 clean tabs |

---

## ⚙️ Configuration

### API Keys
- **Semantic Scholar**: No key needed (free)
- **arXiv**: No key needed (free)
- **Ollama**: Local (no key)

### Environment Variables (optional)
Create `.env`:
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
OLLAMA_HOST=http://localhost:11434
```

---

## 📊 Expected Performance

| Operation | Time |
|-----------|------|
| Page load | 1-2 sec |
| Search papers | 5-10 sec |
| Generate summary | 10-15 sec |
| Generate abstract | 5-10 sec |
| Full Q&A | 10-20 sec |

**Note**: Ollama inference can be slow on CPU (normal!)

---

## 🆘 Troubleshooting

### "Ollama: Not running"
→ Start Ollama in another terminal: `ollama serve`

### "Papers not found"
→ Check internet connection, try different topic

### "Generation is slow"
→ Normal on CPU! Ollama is doing local inference

### "Memory issues"
→ Close other apps, use lighter Ollama model

---

## 🎯 What's Next?

1. ✅ Test locally with various topics
2. ✅ Verify papers load correctly
3. ✅ Check summary/gap detection
4. ✅ Deploy to HF Spaces or Azure
5. ✅ Share live link!

---

## 📝 Example Usage

```
User: Types "artificial intelligence"
↓
System: Searches Semantic Scholar + arXiv
↓
Result: 10-15 papers with citations, abstracts
↓
User: Clicks "Generate Summary"
↓
System: Uses Ollama + RAG to create summary
↓
Output: "AI has revolutionized... research shows that..."
↓
User: Clicks "Identify Gaps"
↓
System: Detects missing areas in research
↓
Output: "Ethics in AI", "Quantum AI", "Bio-inspired AI"
```

---

## 🚀 Deployment

### Local Testing
```bash
streamlit run app/streamlit_app.py
```

### Docker Deployment
```bash
docker build -f server/Dockerfile -t research-assistant .
docker run -p 8501:8501 -p 11434:11434 research-assistant
```

### HF Spaces Deployment
Follow the standard HF Docker deployment process

---

**You're ready to go!** Start with testing, then deploy. Good luck! 🎉
