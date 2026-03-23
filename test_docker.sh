#!/bin/bash

# Docker Test Script
# Run this to verify Docker works before deployment

echo "🐳 Docker Verification Script"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check if Docker is installed
echo "1️⃣  Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not installed. Install Docker Desktop first."
    exit 1
fi
echo "✅ Docker installed: $(docker --version)"
echo ""

# Check if Docker daemon is running
echo "2️⃣  Checking Docker daemon..."
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker daemon not running. Start Docker Desktop."
    exit 1
fi
echo "✅ Docker daemon running"
echo ""

# Verify Docker files exist
echo "3️⃣  Checking Docker files..."
if [ ! -f "server/Dockerfile" ]; then
    echo "❌ server/Dockerfile not found"
    exit 1
fi
echo "✅ server/Dockerfile exists"

if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found"
    exit 1
fi
echo "✅ docker-compose.yml exists"

if [ ! -f ".dockerignore" ]; then
    echo "❌ .dockerignore not found"
    exit 1
fi
echo "✅ .dockerignore exists"

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi
echo "✅ requirements.txt exists"
echo ""

# Build Docker image
echo "4️⃣  Building Docker image (this takes 2-3 minutes)..."
if docker build -t research-assistant:v2.0 -f server/Dockerfile . > /dev/null 2>&1; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Docker build failed"
    exit 1
fi
echo ""

# Check image size
echo "5️⃣  Docker image details..."
image_size=$(docker images research-assistant:v2.0 --format "{{.Size}}")
echo "✅ Image size: $image_size"
echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
echo "✅ ALL DOCKER CHECKS PASSED!"
echo ""
echo "Your project is ready for deployment."
echo ""
echo "Next steps:"
echo "  1. Test locally: docker run -p 8501:8501 research-assistant:v2.0"
echo "  2. Create HF Space at: https://huggingface.co/spaces"
echo "  3. Give me Space URL for cloud deployment"
echo ""
echo "═════════════════════════════════════════════════════════════════"
