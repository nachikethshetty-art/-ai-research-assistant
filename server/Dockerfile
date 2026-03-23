# AI Research Assistant v2.0 - Ollama + Streamlit Single Container
# Optimized for HF Spaces Free Tier

FROM python:3.11-slim

WORKDIR /app

# Install Ollama + dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl https://ollama.ai/install.sh | sh

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire application
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Expose ports
EXPOSE 8501 11434

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV OLLAMA_HOST=127.0.0.1:11434

# Start script - Run Ollama and Streamlit together
RUN echo '#!/bin/bash\n\
ollama serve &\n\
sleep 5\n\
ollama pull mistral\n\
streamlit run app/streamlit_app.py \\\n\
  --server.port=8501 \\\n\
  --server.address=0.0.0.0 \\\n\
  --logger.level=warning' > /app/entrypoint.sh && \
chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
