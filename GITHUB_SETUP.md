# 📦 GITHUB SETUP GUIDE

## 🎯 What You Need to Do

To create a GitHub repository and push your AI Research Assistant code:

### **STEP 1: Create Repository on GitHub**

1. Go to: https://github.com/new
2. Fill in:
   - **Repository name:** `ai-research-assistant`
   - **Description:** "AI Research Assistant with Multi-Source Paper Fetching, LLM Integration (Ollama+Gemini), and RL Feedback Loop"
   - **Public/Private:** Public (for hackathon visibility)
   - **Initialize:** Leave unchecked (we have existing code)
3. Click **Create repository**
4. Copy the HTTPS URL (looks like: `https://github.com/YOUR_USERNAME/ai-research-assistant`)

### **STEP 2: Add GitHub Remote to Your Local Repo**

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
cd /Users/amshumathshetty/Desktop/ai-research-assistant

# Add GitHub as 'origin' remote
git remote add origin https://github.com/YOUR_USERNAME/ai-research-assistant

# Verify remotes are set up
git remote -v
# Should show:
# origin    https://github.com/YOUR_USERNAME/ai-research-assistant (fetch)
# origin    https://github.com/YOUR_USERNAME/ai-research-assistant (push)
# hf        https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv (fetch)
# hf        https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv (push)
```

### **STEP 3: Push to GitHub**

```bash
cd /Users/amshumathshetty/Desktop/ai-research-assistant

# Push to GitHub
git push -u origin main

# When prompted for credentials:
# Option A: Use GitHub Personal Access Token (recommended)
#   1. Create token: https://github.com/settings/tokens
#   2. Use token as password
# Option B: Use username + password (deprecated but may work)
```

### **STEP 4: Verify on GitHub**

Visit: `https://github.com/YOUR_USERNAME/ai-research-assistant`

You should see:
- ✅ All your code files
- ✅ Git history
- ✅ Branches
- ✅ README.md displayed

---

## 🔐 GitHub Authentication (Two Options)

### **Option A: Personal Access Token (Recommended)**

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"**
3. Set:
   - **Note:** "AI Research Assistant Deployment"
   - **Expiration:** 90 days (or longer)
   - **Scopes:** Check `repo` (full control)
4. Click **Generate token**
5. Copy the token (won't show again!)
6. When git asks for password, paste the token

### **Option B: SSH Key (More Secure)**

1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your-email@example.com"
   # Press Enter 3 times (no passphrase)
   ```

2. Add to GitHub:
   ```bash
   # Copy your public key
   cat ~/.ssh/id_ed25519.pub
   # Go to: https://github.com/settings/keys
   # Click "New SSH key"
   # Paste and save
   ```

3. Use SSH remote instead:
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/ai-research-assistant.git
   ```

---

## 📋 What Gets Pushed to GitHub

### **Included:**
- ✅ All source code (`src/`, `app/`)
- ✅ Docker files (`Dockerfile`, `docker-compose.yml`)
- ✅ Requirements (`requirements.txt`)
- ✅ Documentation (`README.md`, guides)
- ✅ Git history

### **Excluded (by .gitignore):**
- ❌ Virtual environment (`venv/`)
- ❌ Data files (large papers)
- ❌ `.env` with secrets
- ❌ `__pycache__/`, `.pytest_cache/`

---

## 📊 Your Repository Will Show

When someone visits your GitHub:

```
ai-research-assistant/
├── README.md (with features, quick start)
├── Dockerfile (HF Spaces optimized)
├── docker-compose.yml (local development)
├── requirements.txt (dependencies)
├── QUICK_COMMANDS.md ⭐ (deployment guide)
├── HF_SPACES_DEPLOYMENT.md (HF guide)
├── OPTIONAL_DEPLOYMENT.md (alternatives)
├── app/
│   └── streamlit_app.py (main UI)
└── src/
    ├── ingestion/
    ├── rag/
    ├── rl/
    ├── analytics/
    └── llm/
        └── backend.py (Ollama + Gemini)
```

---

## 🚀 Complete Commands (Copy & Paste)

### **Step 1: Create Repo on GitHub**
Go to: https://github.com/new
- Name: `ai-research-assistant`
- Public
- Create repository

### **Step 2: Copy Your Repo URL**
After creation, you'll see a URL like:
```
https://github.com/YOUR_USERNAME/ai-research-assistant
```

### **Step 3: Add to Local Git & Push**

```bash
cd /Users/amshumathshetty/Desktop/ai-research-assistant

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ai-research-assistant

# Push all commits to GitHub
git push -u origin main

# When prompted: use GitHub Personal Access Token
# Get token: https://github.com/settings/tokens
```

---

## ✅ After Push - Your Repo is Live!

Your GitHub will have:
- 📜 Full code history
- 📚 All documentation
- 🚀 Deploy instructions
- 💬 Issues/Pull Requests enabled
- ⭐ Ready for portfolio/hackathon

**Your GitHub URL:**
```
https://github.com/YOUR_USERNAME/ai-research-assistant
```

**Shareable Links:**
- Code: `https://github.com/YOUR_USERNAME/ai-research-assistant`
- HF Spaces: `https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv`
- Local: `http://YOUR_IP:8501`

---

## 📝 README for GitHub

Your `README.md` already includes:
- ✅ Feature overview
- ✅ Quick start guide
- ✅ Architecture diagram
- ✅ LLM options
- ✅ RL feedback loop
- ✅ Deployment instructions

---

## 🎯 Next: Tell Me Your GitHub Username

Once you:
1. Create the repo at https://github.com/new
2. Copy the HTTPS URL
3. Run the push commands above

Your code will be on GitHub! 🎉

---

## 💡 Pro Tips

1. **Add GitHub Badge to README:**
   ```markdown
   [![GitHub](https://img.shields.io/badge/GitHub-ai--research--assistant-blue?logo=github)](https://github.com/YOUR_USERNAME/ai-research-assistant)
   ```

2. **Add Topics to GitHub:**
   - Click "About" (gear icon) → Add topics:
     - `ai-research`
     - `hackathon`
     - `rag`
     - `streamlit`
     - `docker`

3. **Enable GitHub Pages:**
   - Settings → Pages → Deploy from `main` branch
   - Your README becomes a nice website!

4. **Add Collaborators:**
   - Settings → Collaborators → Invite teammates
   - Everyone can contribute

---

**Ready? Create the GitHub repo and share your username! I'll help verify the push.** ✨
