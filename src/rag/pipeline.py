#!/usr/bin/env python3
import json
import requests
from typing import List, Dict
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class SimpleVectorStore:
    """Minimal Vector Store using FAISS"""
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.embeddings = None
        self.texts = []
        self.index = None
    
    def add_texts(self, texts: List[str]):
        """Add texts and create FAISS index"""
        self.texts = texts
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        embeddings = embeddings.astype('float32')
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
    
    def search(self, query: str, top_k: int = 3):
        """Search for similar texts"""
        if self.index is None or len(self.texts) == 0:
            return np.array([[0.0] * top_k]), np.array([[0] * top_k])
        
        query_embedding = self.model.encode([query], convert_to_numpy=True).astype('float32')
        distances, indices = self.index.search(query_embedding, min(top_k, len(self.texts)))
        return distances, indices


class RAGPipeline:
    """RAG Pipeline with Ollama Integration"""
    
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.vector_store = SimpleVectorStore()
        self.papers = []
        self.chunks = []
        self.metadata = []
        self.model = "mistral"
        self._check_ollama()
    
    def _check_ollama(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                print(f"✅ Ollama ready ({len(models)} models)")
        except Exception:
            pass
    
    def prepare_data(self, papers):
        """Prepare papers for RAG"""
        self.papers = papers
        self.chunks = []
        self.metadata = []
        
        chunk_id = 0
        for paper_idx, paper in enumerate(papers):
            abstract = paper.get('abstract', '')
            if not abstract:
                continue
            
            # Simple chunking
            words = abstract.split()
            current_chunk = []
            for word in words:
                current_chunk.append(word)
                if len(current_chunk) >= 30:
                    chunk_text = " ".join(current_chunk)
                    self.chunks.append(chunk_text)
                    self.metadata.append({
                        'chunk_id': chunk_id,
                        'paper_idx': paper_idx,
                        'title': paper.get('title', 'Unknown'),
                        'source': paper.get('source', 'unknown'),
                        'year': paper.get('year', 'N/A'),
                        'citations': paper.get('citations', 0),
                        'authors': paper.get('authors', [])
                    })
                    chunk_id += 1
                    current_chunk = []
            
            if current_chunk:
                chunk_text = " ".join(current_chunk)
                self.chunks.append(chunk_text)
                self.metadata.append({
                    'chunk_id': chunk_id,
                    'paper_idx': paper_idx,
                    'title': paper.get('title', 'Unknown'),
                    'source': paper.get('source', 'unknown'),
                    'year': paper.get('year', 'N/A'),
                    'citations': paper.get('citations', 0),
                    'authors': paper.get('authors', [])
                })
                chunk_id += 1
        
        if self.chunks:
            self.vector_store.add_texts(self.chunks)
    
    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant context"""
        if not self.chunks:
            return []
        
        distances, indices = self.vector_store.search(query, top_k=top_k)
        
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx < len(self.chunks):
                results.append({
                    'chunk': self.chunks[idx],
                    'metadata': self.metadata[idx],
                    'distance': float(distance)
                })
        
        return results
    
    def generate_answer(self, query: str, context_chunks: List[Dict] = None) -> str:
        """Generate answer using Ollama"""
        if context_chunks is None:
            context_chunks = []
        
        context = "\n".join([
            f"- {c['metadata']['title']}: {c['chunk'][:150]}..."
            for c in context_chunks[:3]
        ])
        
        prompt = f"""Answer briefly: {query}

Context: {context if context else "No context"}"""
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
        except Exception:
            pass
        
        return "Ollama not available"
    
    def detect_research_gaps(self, papers) -> Dict:
        """Detect research gaps"""
        if not papers:
            return {}
        
        all_text = " ".join([
            paper.get('title', '') + " " + paper.get('abstract', '')
            for paper in papers
        ]).lower()
        
        gaps = {}
        if any(w in all_text for w in ['future', 'further', 'next']):
            gaps['future_work'] = True
        if any(w in all_text for w in ['challenge', 'limitation', 'difficult']):
            gaps['challenges'] = True
        
        return gaps
    
    def generate_summary(self, query: str, papers: List[Dict]) -> str:
        """Generate research summary"""
        self.prepare_data(papers)
        
        prompt = f"Summarize {len(papers)} papers on '{query}' in 50 words."
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
        except Exception:
            pass
        
        return "Summary generation unavailable"
