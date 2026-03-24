# 🚀 Hugging Face Spaces Deployment Guide

## Your Space URL
👉 **https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv**

---

## ✅ What's Deployed

Your AI Research Assistant is now deployed with:

### **Core Features** ✨
- 📄 Multi-source paper search (arXiv + Semantic Scholar + OpenAlex)
- 🎯 Unified 300-400 word research summaries
- 🔍 5-6 research gap detection
- 💬 Q&A with paper context
- 🤖 RL feedback loop for continuous learning
- 📊 Analytics dashboard

### **LLM Backends (Automatic Fallback)**
1. **Primary: Ollama (Mistral 7B)** - Local, private, free
2. **Fallback: Google Gemini API** - When Ollama unavailable
3. **Paper Fetching**: Always works (arXiv/Semantic Scholar)

---

## 🌐 Accessing Your App

### **Via Hugging Face Spaces** (Public, no installation needed)
- Link: `https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv`
- Click **"Running"** badge → Opens live app
- Public URL appears at top

### **Via Local Network** (Fastest, full Ollama)
```bash
cd /Users/amshumathshetty/Desktop/ai-research-assistant
docker-compose up -d

# Get your IP
ifconfig getifaddr en0

# Share: http://<YOUR_IP>:8501
```

---

## 🤖 LLM Backend Strategy

### **If Ollama Works on HF Space** ✅
- Paper search: ✅ Works
- Summaries: ✅ Works (streaming)
- Research gaps: ✅ Works
- Q&A: ✅ Works
- RL feedback: ✅ Works

### **If Ollama Unavailable** (HF Space Free Tier)
- Paper search: ✅ Works (always)
- Summaries: Uses Google Gemini API (free 50 calls/day)
- Research gaps: Uses Google Gemini API
- Q&A: Uses Google Gemini API
- RL feedback: ✅ Works (local, no LLM needed)

---

## 🔑 Enabling Google Gemini Fallback

If Ollama fails on HF Space, set this environment variable:

### **Step 1: Get Free Gemini API Key**
1. Go to [makersuite.google.com](https://makersuite.google.com)
2. Click **"Get API Key"**
3. Click **"Create API Key"**
4. Copy the key

### **Step 2: Add to HF Space**
1. Open your Space: https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv
2. Click **Settings** (gear icon, top right)
3. Go to **Repository secrets**
4. Add: `GOOGLE_API_KEY` = `your-key-here`
5. Save

✅ Now Gemini will auto-activate if Ollama is unavailable!

---

## 📋 Alternatives if Something Breaks

| Platform | Cost | Ollama | Setup Time | Notes |
|----------|------|--------|------------|-------|
| **Local LAN** | Free | ✅ Full | 2 min | Fastest, private, easiest |
| **Railway** | $5-20/mo | ✅ Full | 10 min | Reliable, auto-scales |
| **Render** | Free (slow) | ⚠️ Slow | 15 min | Works but CPU-limited |
| **AWS EC2** | $5-30/mo | ✅ Full | 20 min | Fastest, but setup complex |

---

## 🔧 Quick Troubleshooting

### **Paper search not working?**
- Check internet connection
- Semantic Scholar API might be rate-limited (7/sec max)
- Try searching for general topics first

### **Summaries/Gaps taking too long?**
- Ollama is busy (HF Space has limited CPU)
- Fallback to Gemini API (free 50/day)
- Try 3-5 papers instead of 10+

### **Getting "LLM Unavailable" message?**
- Add GOOGLE_API_KEY to Space secrets (see above)
- Or run locally with `docker-compose up -d`

---

## 📞 Support

**Having issues?** Check these files:
- `OPTIONAL_DEPLOYMENT.md` - More deployment options
- `HACKATHON_GUIDE.md` - Hackathon tips
- README.md - Feature overview

---

## 🎯 Your Shareable Links

### **Option 1: HF Spaces (Public, No Install)**
```
https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv
```
✅ Anyone can access  
✅ No installation needed  
⚠️ Ollama may be slow (free tier CPU)  

### **Option 2: Local Network (Fastest)**
```
http://<YOUR_IP>:8501
```
✅ Lightning fast  
✅ Full Ollama power  
⚠️ Only on your Wi-Fi  

### **Option 3: Railway (If needed)**
See `OPTIONAL_DEPLOYMENT.md` for Railway setup (paid, reliable).

---

**🎉 Your app is live! Share the HF Spaces link above.**
