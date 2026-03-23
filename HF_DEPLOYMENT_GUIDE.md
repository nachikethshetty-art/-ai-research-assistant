# HF Spaces Deployment Guide - Ollama + Streamlit

## Quick Setup

### Step 1: Create HF Space
1. Go: https://huggingface.co/spaces
2. **Create new Space**
   - Owner: nachikethshetty
   - Name: research-assistant
   - **Type: Docker** ← IMPORTANT!
   - Hardware: CPU (free)
   - Visibility: Public
3. Click "Create Space"

### Step 2: Deploy Code
```bash
cd /Users/amshumathshetty/Desktop/ai-research-assistant

# Add all files to git
git add .
git commit -m "Deploy Ollama + Streamlit to HF Spaces"

# Push to HF (replace username)
git remote add hf https://huggingface.co/spaces/nachikethshetty/research-assistant
git push hf main
```

### Step 3: Wait for Build
- HF will build Docker image (~5-10 minutes)
- Check status at: https://huggingface.co/spaces/nachikethshetty/research-assistant?logs=build
- Once "Building" → "Running", app is live!

### Step 4: Access App
Once built, app is live at:
**https://nachikethshetty-research-assistant.hf.space**

---

## What's Happening

The **single Dockerfile** will:
1. ✅ Start Ollama service (port 11434)
2. ✅ Auto-pull Mistral model
3. ✅ Start Streamlit dashboard (port 8501)
4. ✅ Everything runs in ONE container

---

## Performance Expectations

| Metric | Time |
|--------|------|
| First load | 2-3 min (Ollama startup) |
| Query response | 10-30 sec (CPU inference) |
| Subsequent queries | 5-15 sec |

Speed depends on Ollama model size (Mistral is ~7B, ~4GB RAM)

---

## Troubleshooting

### Build fails?
- Check: https://huggingface.co/spaces/nachikethshetty/research-assistant?logs=build
- Common issue: Ollama installation timeout
- Solution: Can increase timeout or use lighter model

### App is slow?
- Normal on free CPU
- Ollama inference takes 10-30 sec per query
- This is expected behavior

### Ollama didn't download?
- The entrypoint.sh script auto-pulls Mistral
- If fails, manually pull during runtime

---

## Local Testing (Optional)

Before deploying to HF, test locally:

```bash
# Build Docker image
docker build -f server/Dockerfile -t research-assistant .

# Run container
docker run -p 8501:8501 -p 11434:11434 research-assistant

# Open: http://localhost:8501
```

---

## That's It! 🚀

Your app is now deployed with Ollama + Streamlit in one Docker container!

Live URL: https://nachikethshetty-research-assistant.hf.space
