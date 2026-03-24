#!/usr/bin/env python3
import json
import requests
from typing import List, Dict
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import re
from llm.backend import LLMBackend


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
    """RAG Pipeline with Ollama + Gemini Fallback - Optimized for Speed"""
    
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.vector_store = SimpleVectorStore()
        self.papers = []
        self.chunks = []
        self.metadata = []
        self.llm_backend = LLMBackend(ollama_url=ollama_url)
        self.ollama_available = self.llm_backend.ollama_available
    
    def get_llm_status(self):
        """Get current LLM backend status"""
        return self.llm_backend.get_status()
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
                    'distance': float(distance),
                    'metadata': self.metadata[idx]
                })
        return results

    def generate_summary(self, query: str, papers: List[Dict]):
        """Generate a unified comprehensive summary for all papers combined."""
        if not papers:
            yield "No papers to summarize."
            return
        
        self.prepare_data(papers)
        
        # Create a structured context with all papers' metadata
        papers_context = "\n\n".join([
            f"Paper {i+1}: {p.get('title', 'Unknown')}\n"
            f"Year: {p.get('year', 'N/A')}\n"
            f"Citations: {p.get('citations', 0)}\n"
            f"Abstract: {p.get('abstract', '')}"
            for i, p in enumerate(papers)
        ])
        
        prompt = f"""You are a senior research analyst. Synthesize all {len(papers)} papers about '{query}' into one comprehensive summary.

REQUIREMENTS:
- Total word count: 200 words (STRICT - must be concise)
- Structure: 3-4 well-developed paragraphs
- Content: Synthesize across ALL papers - not individual summaries
- Include: Research landscape, major findings, methodologies, and current state
- Focus on: Patterns and trends across papers, not individual paper details
- Style: Academic but accessible, flowing naturally
- Do NOT: List papers individually, use bullet points, or treat papers separately

Write a unified synthesis that shows how these papers collectively advance the field:"""
        
        yield from self.llm_backend.generate_stream(prompt, max_tokens=4000)

    def detect_research_gaps(self, papers: List[Dict]):
        """
        Detects unified research gaps across all papers combined.
        """
        if not papers:
            yield "Not enough papers to analyze for research gaps."
            return

        self.prepare_data(papers)
        
        # Create a structured context with all papers' metadata
        papers_context = "\n\n".join([
            f"Paper {i+1}: {p.get('title', 'Unknown')}\n"
            f"Authors: {', '.join(p.get('authors', ['Unknown'])[:3])}\n"
            f"Year: {p.get('year', 'N/A')}\n"
            f"Citations: {p.get('citations', 0)}\n"
            f"Abstract: {p.get('abstract', '')}"
            for i, p in enumerate(papers)
        ])

        prompt = f"""You are a senior research strategist. Analyze all {len(papers)} papers collectively to identify critical research gaps.

UNIFIED GAP ANALYSIS (NOT paper-by-paper):
Focus on what is MISSING across the entire body of research:

1. **Critical Unresolved Questions**: What fundamental questions remain unanswered?
2. **Methodological Gaps**: What research approaches are underexplored?
3. **Disciplinary Gaps**: What perspectives from other fields could help?
4. **Empirical Gaps**: What real-world applications need investigation?
5. **Theoretical Gaps**: What frameworks are needed to advance the field?

REQUIREMENTS for your response:
- Identify 3-4 major research gaps (most impactful only)
- Total word count: 200 words (STRICT - must be concise)
- Each gap: 2-3 sentences, specific and actionable
- Be concise: No unnecessary elaboration
- Synthesize across papers: Show how gaps emerge from the collective analysis

Provide a concise gap analysis:"""
        
        yield from self.llm_backend.generate_stream(prompt, max_tokens=4000)

    def generate_answer(self, query: str, context: List[Dict]):
        """Generate an answer to a query based on provided context."""
        if not context:
            yield "I don't have enough information to answer that question."
            return
        
        context_str = "\n\n".join([
            f"Source: {c['metadata']['title']} ({c['metadata']['year']})\n"
            f"Content: {self.chunks[c['metadata']['chunk_id']]}"
            for c in context
        ])
        
        prompt = f"""
        You are a research assistant. Answer the following question based *only* on the provided context.
        Be concise and cite the source paper title if possible.

        Question: {query}
        """
        
        yield from self.llm_backend.generate_stream(prompt, max_tokens=500)

