# AI Research Assistant v3.0 - Groq Cloud Integration
# Simple, fast, cloud-native deployment

FROM python:3.11-slim

WORKDIR /app

# Install minimal dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire application
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Expose port for Streamlit
EXPOSE 8501

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run Streamlit app
CMD ["streamlit", "run", "app/streamlit_app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--logger.level=warning"]
