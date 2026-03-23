#!/usr/bin/env python3
import json
import requests
from typing import List, Dict
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import re


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
    """RAG Pipeline with Ollama Integration - Optimized for Speed"""
    
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.vector_store = SimpleVectorStore()
        self.papers = []
        self.chunks = []
        self.metadata = []
        self.model = "mistral"
        self.ollama_available = self._check_ollama()
    
    def _check_ollama(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                return True
        except Exception:
            pass
        return False
    
    def prepare_data(self, papers):
        """Fast data preparation for RAG"""
        self.papers = papers
        self.chunks = []
        self.metadata = []
        
        # Use paper titles + abstracts as chunks (faster than word splitting)
        for paper_idx, paper in enumerate(papers):
            title = paper.get('title', 'Unknown')
            abstract = paper.get('abstract', '')
            
            # Use whole abstract as chunk (skip slow chunking)
            if abstract.strip():
                self.chunks.append(f"{title}: {abstract}")
                self.metadata.append({
                    'chunk_id': paper_idx,
                    'paper_idx': paper_idx,
                    'title': title,
                    'source': paper.get('source', 'unknown'),
                    'year': paper.get('year', 'N/A'),
                    'citations': paper.get('citations', 0),
                    'authors': paper.get('authors', []),
                    'url': paper.get('url', '')
                })
        
        if self.chunks:
            self.vector_store.add_texts(self.chunks)
    
    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict]:
        """Fast context retrieval"""
        if not self.chunks:
            return []
        
        distances, indices = self.vector_store.search(query, top_k=min(top_k, len(self.chunks)))
        
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
        """Generate answer using Ollama with proper context"""
        if context_chunks is None:
            context_chunks = []
        
        # Build context from chunks
        context_text = ""
        if context_chunks:
            context_text = "\n".join([
                f"Paper: {c['metadata']['title']}\nContent: {c['chunk'][:300]}"
                for c in context_chunks[:3]
            ])
        
        # Smart prompt based on query type
        if any(word in query.lower() for word in ['summary', 'overview', 'what is']):
            prompt = f"""Answer this research question concisely (2-3 sentences):
{query}

Research context:
{context_text if context_text else 'No specific context available'}

Provide a clear, academic answer."""
        
        elif any(word in query.lower() for word in ['how', 'explain', 'why']):
            prompt = f"""Explain this research topic clearly:
{query}

Context:
{context_text if context_text else 'General knowledge response'}

Provide a detailed but concise explanation."""
        
        else:
            prompt = f"""Answer this research question:
{query}

Relevant papers and findings:
{context_text if context_text else 'No specific papers available'}

Provide an accurate, research-backed answer."""
        
        # Try to get answer from Ollama
        if not self.ollama_available:
            return self._generate_default_answer(query)
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.6,
                    "top_p": 0.9,
                    "num_predict": 150
                },
                timeout=30
            )
            
            if response.status_code == 200:
                answer = response.json().get('response', '').strip()
                if answer and len(answer) > 10:
                    return answer
        except requests.exceptions.Timeout:
            pass
        except Exception:
            pass
        
        return self._generate_default_answer(query)
    
    def _generate_default_answer(self, query: str) -> str:
        """Fallback answer generation when Ollama is unavailable"""
        # Extract key terms and generate a reasonable response
        keywords = query.lower().split()
        
        responses = {
            'summary': "Based on recent research in this field, key findings show significant progress in understanding and practical applications.",
            'gap': "Future research should focus on scalability, real-world validation, and integration with existing systems.",
            'challenge': "Major challenges include computational complexity, data availability, and practical implementation constraints.",
            'trend': "Recent trends show increased adoption of AI-driven approaches, cloud-based solutions, and collaborative research methodologies."
        }
        
        for key, response in responses.items():
            if key in query.lower():
                return response
        
        return "Research in this area is actively advancing. Key areas of focus include novel methodologies, practical applications, and theoretical foundations."
    
    def detect_research_gaps(self, papers: List[Dict]) -> List[str]:
        """Detect and describe research gaps"""
        if not papers:
            return ["Insufficient papers to analyze"]
        
        all_text = " ".join([
            paper.get('title', '') + " " + paper.get('abstract', '')
            for paper in papers
        ]).lower()
        
        gaps = []
        
        # Check for future work mentions
        if any(phrase in all_text for phrase in ['future work', 'future research', 'future studies', 'further investigation']):
            gaps.append("🔮 Future Work: Papers identify several areas for extended research and new methodologies")
        
        # Check for limitations
        if any(phrase in all_text for phrase in ['limitation', 'limited', 'challenging', 'challenge']):
            gaps.append("⚠️ Limitations & Challenges: Current approaches face scalability, efficiency, or accuracy limitations")
        
        # Check for emerging areas
        if any(phrase in all_text for phrase in ['novel', 'new approach', 'emerging', 'breakthrough']):
            gaps.append("✨ Emerging Frontiers: Novel techniques and breakthrough approaches are being developed")
        
        # Check for application gaps
        if any(phrase in all_text for phrase in ['application', 'practical', 'implementation', 'real-world']):
            gaps.append("🛠️ Real-World Applications: Need for practical implementations and deployment strategies")
        
        # Check for theoretical gaps
        if any(phrase in all_text for phrase in ['theoretical', 'foundation', 'framework', 'model']):
            gaps.append("🧪 Theoretical Advancement: Opportunities to strengthen theoretical understanding and frameworks")
        
        # Default gaps if none found
        if not gaps:
            gaps = [
                "🔍 Interdisciplinary Research: Integration with other fields could yield new insights",
                "📊 Empirical Validation: More comprehensive experimental studies needed",
                "🌐 Scalability: Solutions need optimization for larger datasets and real-world scenarios"
            ]
        
        return gaps[:5]  # Return top 5 gaps
    
    def generate_summary(self, query: str, papers: List[Dict]) -> str:
        """Generate comprehensive research summary"""
        if not papers:
            return "No papers available for summary"
        
        self.prepare_data(papers)
        
        # Build context from papers
        paper_info = "\n".join([
            f"- {p.get('title', 'Unknown')} ({p.get('year', 'N/A')}) - {len(p.get('abstract', ''))} chars"
            for p in papers[:10]
        ])
        
        prompt = f"""Write a comprehensive research summary about: {query}

Based on {len(papers)} papers:
{paper_info}

Create a 5-7 sentence summary covering:
1. Key research area overview
2. Main findings and contributions
3. Current state of the field
4. Emerging trends
5. Future directions

Make it academic but accessible."""
        
        if not self.ollama_available:
            return f"Summary: Recent research on '{query}' shows significant progress with {len(papers)} relevant papers found. Key themes include novel methodologies, practical applications, and theoretical advances. The field continues to evolve with emerging interdisciplinary approaches."
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                    "num_predict": 250
                },
                timeout=45
            )
            
            if response.status_code == 200:
                summary = response.json().get('response', '').strip()
                if summary and len(summary) > 20:
                    return summary
        except:
            pass
        
        return f"Summary: Recent research on '{query}' shows significant progress with {len(papers)} relevant papers found. Key themes include novel methodologies, practical applications, and theoretical advances. The field continues to evolve with emerging interdisciplinary approaches."
