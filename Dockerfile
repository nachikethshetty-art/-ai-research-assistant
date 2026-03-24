# AI Research Assistant - HF Spaces Optimized
# Lightweight: Streamlit + Google Gemini API (no Ollama needed)
# Fast build: ~5 minutes on HF free tier

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add google-generativeai for Ollama fallback
RUN pip install --no-cache-dir google-generativeai==0.3.0

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Expose Streamlit port (HF Spaces uses 7860)
EXPOSE 7860

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_LOGGER_LEVEL=warning

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:7860/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "app/streamlit_app.py", "--logger.level=warning"]
