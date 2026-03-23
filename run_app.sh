#!/bin/bash
# Run the AI Research Assistant

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please create it first with: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "🚀 Starting AI Research Assistant v3.0..."
echo ""
echo "📝 Make sure Ollama is running in another terminal:"
echo "   ollama serve"
echo ""
echo "Opening http://localhost:8501..."
echo ""

# Run Streamlit
python -m streamlit run app/streamlit_app.py
