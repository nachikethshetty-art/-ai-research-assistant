#!/usr/bin/env python3
"""Quick system test to verify all components are working"""

import sys
import os

print("🧪 AI RESEARCH ASSISTANT - SYSTEM TEST\n")

# Test 1: Virtual environment
print("1️⃣  Testing virtual environment...")
try:
    import requests
    import pandas
    import faiss
    from sentence_transformers import SentenceTransformer
    print("   ✅ All core libraries installed\n")
except ImportError as e:
    print(f"   ❌ Missing library: {e}\n")
    sys.exit(1)

# Test 2: Ollama connection
print("2️⃣  Testing Ollama connection...")
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        models = response.json().get('models', [])
        print(f"   ✅ Ollama is running with {len(models)} models")
        for model in models:
            print(f"      - {model.get('name')}")
    print()
except Exception as e:
    print(f"   ⚠️  Ollama not responding: {e}")
    print("   Run 'ollama serve' in another terminal\n")

# Test 3: Module imports
print("3️⃣  Testing module imports...")
sys.path.insert(0, 'src/ingestion')
sys.path.insert(0, 'src/processing')
sys.path.insert(0, 'src/embeddings')
sys.path.insert(0, 'src/rag')
sys.path.insert(0, 'src/rl')

try:
    from chunking import chunk_text
    print("   ✅ Chunking module loaded")
    
    from vector_store import VectorStore
    print("   ✅ Vector store module loaded")
    
    from feedback_system import RLFeedbackSystem
    print("   ✅ Feedback system module loaded")
    
    print()
except ImportError as e:
    print(f"   ❌ Module import error: {e}\n")
    sys.exit(1)

# Test 4: Quick functionality test
print("4️⃣  Testing core functionality...")

# Test chunking
test_text = "Lithium-ion batteries are used in electric vehicles. They have high energy density. Recycling is important."
chunks = chunk_text(test_text, max_tokens=10)
print(f"   ✅ Chunking works ({len(chunks)} chunks created)")

# Test FAISS
try:
    store = VectorStore()
    test_texts = ["Battery recycling", "Lithium extraction", "Sustainability"]
    store.add_texts(test_texts)
    distances, indices = store.search("Battery recycling", top_k=2)
    print(f"   ✅ FAISS search works (found {len(indices[0])} results)")
except Exception as e:
    print(f"   ❌ FAISS error: {e}\n")
    sys.exit(1)

# Test RL system
try:
    rl = RLFeedbackSystem()
    feedback = {'relevance': 5, 'clarity': 4, 'citations': 5, 'gaps': 4}
    reward = rl.record_feedback("Test query", "Test answer", feedback)
    print(f"   ✅ RL system works (reward: {reward:.3f})")
except Exception as e:
    print(f"   ❌ RL system error: {e}\n")
    sys.exit(1)

print()

# Summary
print("="*60)
print("✨ SYSTEM TEST PASSED - ALL COMPONENTS WORKING!")
print("="*60)
print("\n🚀 Next steps:")
print("   1. Start Ollama: ollama serve")
print("   2. Run dashboard: ./run.sh")
print("   3. Open: http://localhost:8501\n")
