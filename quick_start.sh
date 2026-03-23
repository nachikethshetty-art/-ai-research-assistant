#!/bin/bash
# Quick Start Guide - AI Research Assistant

echo "
╔══════════════════════════════════════════════════════════════╗
║        AI RESEARCH ASSISTANT - QUICK START GUIDE            ║
╚══════════════════════════════════════════════════════════════╝
"

echo "Choose how you want to run the app:"
echo ""
echo "1️⃣  LOCAL DEVELOPMENT (Recommended for testing)"
echo "2️⃣  DOCKER (Ready for production)"
echo "3️⃣  DOCKER COMPOSE (Advanced)"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
  1)
    echo ""
    echo "📌 LOCAL DEVELOPMENT SETUP"
    echo "=========================="
    echo ""
    echo "Step 1: Open Terminal 1 and run:"
    echo "  $ ollama serve"
    echo ""
    echo "Step 2: Open Terminal 2 and run:"
    echo "  $ cd /Users/amshumathshetty/Desktop/ai-research-assistant"
    echo "  $ source venv/bin/activate"
    echo "  $ streamlit run app/streamlit_app.py"
    echo ""
    echo "Step 3: Open browser:"
    echo "  👉 http://localhost:8501"
    echo ""
    echo "✅ Ready! You should see the app in seconds"
    echo ""
    ;;
    
  2)
    echo ""
    echo "📦 DOCKER SETUP"
    echo "==============="
    echo ""
    echo "Running Docker container..."
    echo ""
    echo "Command:"
    echo "  $ docker run -p 8501:8501 -p 11434:11434 \\"
    echo "      ai-research-assistant:latest"
    echo ""
    echo "This will:"
    echo "  1. Start Ollama server"
    echo "  2. Pull Mistral model (takes 1-2 minutes first time)"
    echo "  3. Start Streamlit app"
    echo ""
    echo "Then open:"
    echo "  👉 http://localhost:8501"
    echo ""
    echo "Want to run it? (y/n)"
    read -p "> " run_docker
    if [ "$run_docker" = "y" ]; then
      docker run -p 8501:8501 -p 11434:11434 ai-research-assistant:latest
    fi
    ;;
    
  3)
    echo ""
    echo "🐳 DOCKER COMPOSE SETUP"
    echo "======================="
    echo ""
    echo "Running with docker-compose..."
    echo ""
    echo "Make sure docker-compose.yml exists with:"
    echo ""
    cat << 'DOCKER_COMPOSE'
version: '3.8'
services:
  app:
    image: ai-research-assistant:latest
    ports:
      - "8501:8501"
      - "11434:11434"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./data:/app/data
    restart: unless-stopped
DOCKER_COMPOSE
    echo ""
    echo "Then run:"
    echo "  $ docker-compose up"
    echo ""
    echo "Then open:"
    echo "  👉 http://localhost:8501"
    echo ""
    ;;
    
  *)
    echo "Invalid choice. Please run again."
    exit 1
    ;;
esac

echo ""
echo "═════════════════════════════════════════════════════════"
echo ""
echo "💡 TIPS:"
echo "  • First search takes 10-15 seconds (API calls)"
echo "  • Summary generation takes 15-30 seconds (Ollama on CPU)"
echo "  • This is normal! CPU-only machines are slower"
echo "  • Try different topics: 'machine learning', 'quantum computing', etc."
echo ""
echo "📚 DOCUMENTATION:"
echo "  • SESSION4_COMPLETE.md - Full details"
echo "  • QUICK_FIX_GUIDE.md - Troubleshooting"
echo "  • verify_fixes.sh - Verify installation"
echo ""
echo "❓ NEED HELP?"
echo "  Check the documentation or verify with: ./verify_fixes.sh"
echo ""
echo "═════════════════════════════════════════════════════════"
