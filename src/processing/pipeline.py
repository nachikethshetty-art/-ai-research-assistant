#!/usr/bin/env python3
"""
Integrated Pipeline: Fetch → Chunk → Embed → Store
This script orchestrates the entire data ingestion and embedding process.
"""

import sys
import os
import json
from datetime import datetime

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ingestion'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'processing'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'embeddings'))

# Import fetcher, chunking, and vector store
import subprocess
result = subprocess.run(
    ['python3', os.path.join(os.path.dirname(__file__), '..', 'ingestion', 'main_fetcher.py')],
    capture_output=True,
    text=True
)

# For now, let's create a simpler approach by importing directly
try:
    # Import from main_fetcher
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "main_fetcher",
        os.path.join(os.path.dirname(__file__), '..', 'ingestion', 'main_fetcher.py')
    )
    main_fetcher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_fetcher)
    
    from chunking import chunk_text
    from vector_store import VectorStore
    
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

class ResearchPipeline:
    def __init__(self):
        self.papers = []
        self.chunks = []
        self.vector_store = VectorStore()
        self.metadata = []
        
    def fetch_papers(self, query, limit=20):
        """Fetch papers from Semantic Scholar and arXiv"""
        print(f"\n{'='*80}")
        print(f"🔍 PHASE 1: FETCHING PAPERS")
        print(f"{'='*80}")
        print(f"Query: {query}\n")
        
        self.papers = main_fetcher.fetch_all_papers(query)
        print(f"\n✅ Fetched {len(self.papers)} papers")
        
        return self.papers
    
    def chunk_papers(self, chunk_size=200):
        """Chunk all paper abstracts"""
        print(f"\n{'='*80}")
        print(f"✂️  PHASE 2: CHUNKING PAPERS")
        print(f"{'='*80}")
        
        chunk_id = 0
        for paper_idx, paper in enumerate(self.papers):
            abstract = paper.get('abstract', '')
            if not abstract:
                continue
                
            chunks = chunk_text(abstract, max_tokens=chunk_size)
            
            for chunk in chunks:
                self.chunks.append(chunk)
                self.metadata.append({
                    'chunk_id': chunk_id,
                    'paper_idx': paper_idx,
                    'title': paper.get('title', 'Unknown'),
                    'source': paper.get('source', 'unknown'),
                    'year': paper.get('year', 'N/A'),
                    'citations': paper.get('citations', 0)
                })
                chunk_id += 1
        
        print(f"✅ Created {len(self.chunks)} chunks from {len(self.papers)} papers")
        return self.chunks
    
    def embed_chunks(self):
        """Generate embeddings and store in FAISS"""
        print(f"\n{'='*80}")
        print(f"🧠 PHASE 3: EMBEDDING & STORING")
        print(f"{'='*80}")
        
        if not self.chunks:
            print("❌ No chunks to embed. Run chunk_papers() first.")
            return
        
        print(f"Embedding {len(self.chunks)} chunks...")
        self.vector_store.add_texts(self.chunks)
        print(f"✅ Successfully embedded and stored {len(self.chunks)} chunks in FAISS")
        
        return self.vector_store
    
    def search_similar(self, query, top_k=5):
        """Search for similar chunks using the query"""
        print(f"\n{'='*80}")
        print(f"🔎 SEARCHING FOR SIMILAR CHUNKS")
        print(f"{'='*80}")
        print(f"Query: {query}\n")
        
        distances, indices = self.vector_store.search(query, top_k=top_k)
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            chunk = self.chunks[idx] if idx < len(self.chunks) else "Unknown"
            metadata = self.metadata[idx] if idx < len(self.metadata) else {}
            
            result = {
                'rank': i + 1,
                'distance': float(distance),
                'chunk_preview': chunk[:150] + "..." if len(chunk) > 150 else chunk,
                'metadata': metadata
            }
            results.append(result)
            
            print(f"{i+1}. Distance: {distance:.4f}")
            print(f"   Paper: {metadata.get('title', 'Unknown')}")
            print(f"   Source: {metadata.get('source')}")
            print(f"   Chunk Preview: {result['chunk_preview']}\n")
        
        return results
    
    def run_full_pipeline(self, query):
        """Run the complete pipeline"""
        print(f"\n🚀 STARTING AI RESEARCH ASSISTANT PIPELINE")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Phase 1: Fetch
        self.fetch_papers(query)
        
        # Phase 2: Chunk
        self.chunk_papers()
        
        # Phase 3: Embed
        self.embed_chunks()
        
        print(f"\n{'='*80}")
        print(f"✨ PIPELINE COMPLETE - Ready for RAG Queries")
        print(f"{'='*80}\n")
        
        return self

if __name__ == "__main__":
    # Initialize pipeline
    pipeline = ResearchPipeline()
    
    # Run full pipeline
    query = "lithium-ion battery recycling sustainability"
    pipeline.run_full_pipeline(query)
    
    # Test search functionality
    test_queries = [
        "How does battery recycling work?",
        "What are the environmental impacts?",
        "Sustainability challenges in lithium extraction"
    ]
    
    print(f"\n{'='*80}")
    print(f"🧪 TESTING SEARCH FUNCTIONALITY")
    print(f"{'='*80}\n")
    
    for test_query in test_queries:
        pipeline.search_similar(test_query, top_k=3)
        print()
