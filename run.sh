#!/bin/bash
# Startup script for AI Research Assistant
# Works on M2 MacBook Air

echo "🚀 AI Research Assistant Startup"
echo "================================"

# Navigate to project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check Ollama
echo ""
echo "🤖 Checking Ollama status..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama is not running. Start it with: ollama serve"
fi

# Launch Streamlit app
echo ""
echo "🎨 Starting Streamlit dashboard..."
echo "   URL: http://localhost:8501"
echo ""

streamlit run app/streamlit_app.py --logger.level=warning
