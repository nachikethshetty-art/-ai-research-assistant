# AI Research Assistant v2.0 - Lightweight with Ollama
# Search ANY topic • Find 10+ papers • Generate insights

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Ollama
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl https://ollama.ai/install.sh | sh

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .
RUN mkdir -p /app/data

# Expose ports
EXPOSE 8501 11434

# Start Ollama and Streamlit
RUN echo '#!/bin/bash\n\
ollama serve &\n\
sleep 5\n\
ollama pull mistral\n\
streamlit run app/streamlit_app.py \\\n\
  --server.port=8501 \\\n\
  --server.address=0.0.0.0 \\\n\
  --logger.level=warning' > /start.sh && chmod +x /start.sh

CMD ["/start.sh"]
