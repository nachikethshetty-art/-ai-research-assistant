#!/usr/bin/env python3
"""
RAG Pipeline with Groq API Integration + Research Gap Detection
Cloud-native deployment with fast inference
"""

import sys
import os
import json
from typing import List, Dict, Tuple
from groq import Groq

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ingestion'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'processing'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'embeddings'))

from chunking import chunk_text
from vector_store import VectorStore

class RAGPipeline:
    def __init__(self, groq_api_key=None):
        """
        Initialize RAG Pipeline with Groq API integration
        """
        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found. Set it as an environment variable.")
        
        self.client = Groq(api_key=self.groq_api_key)
        self.vector_store = VectorStore()
        self.papers = []
        self.chunks = []
        self.metadata = []
        self.model = "mixtral-8x7b-32768"  # Fast Groq model
        
        # Check if Groq API is accessible
        self._check_groq()
    
    def _check_groq(self):
        """Check if Groq API is accessible"""
        try:
            # Simple test call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            print("✅ Groq API is connected and working")
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            print("   Make sure GROQ_API_KEY is set correctly")
    
    def load_papers_from_json(self, json_file):
        """Load papers from a JSON file (for testing/demo)"""
        try:
            with open(json_file, 'r') as f:
                self.papers = json.load(f)
            print(f"✅ Loaded {len(self.papers)} papers from {json_file}")
        except FileNotFoundError:
            print(f"❌ File not found: {json_file}")
    
    def prepare_data(self, papers):
        """Prepare papers for RAG: chunk and embed"""
        self.papers = papers
        
        print(f"\n{'='*80}")
        print(f"📊 PREPARING DATA FOR RAG")
        print(f"{'='*80}\n")
        
        # Chunk papers
        chunk_id = 0
        for paper_idx, paper in enumerate(self.papers):
            abstract = paper.get('abstract', '')
            if not abstract:
                continue
            
            chunks = chunk_text(abstract, max_tokens=150)  # Smaller chunks for M2
            
            for chunk in chunks:
                self.chunks.append(chunk)
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
        
        print(f"✅ Created {len(self.chunks)} chunks")
        
        # Embed chunks
        print(f"🧠 Embedding chunks (this may take a moment on M2)...")
        self.vector_store.add_texts(self.chunks)
        print(f"✅ Embeddings stored in FAISS\n")
    
    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve top-k relevant chunks for a query
        Optimized to limit context for M2 performance
        """
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
    
    def generate_answer(self, query: str, context_chunks: List[Dict]) -> str:
        """
        Generate answer using Groq API with retrieved context
        Fast cloud-native inference
        """
        # Prepare context
        context = "\n".join([
            f"Paper: {c['metadata']['title']}\n"
            f"Content: {c['chunk'][:200]}..."
            for c in context_chunks
        ])
        
        # Create prompt for Groq
        prompt = f"""Based on the following research papers, answer the question concisely and accurately.

Papers:
{context}

Question: {query}

Answer:"""
        
        try:
            print(f"🤖 Generating answer with Groq (mixtral-8x7b)...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7,
                top_p=0.9
            )
            
            answer = response.choices[0].message.content.strip()
            return answer
        
        except Exception as e:
            return f"❌ Error generating answer: {str(e)}"
    
    def detect_research_gaps(self, papers: List[Dict] = None) -> List[str]:
        """
        Detect research gaps by analyzing paper abstracts
        Simple heuristic approach suitable for M2
        """
        if papers is None:
            papers = self.papers
        
        print(f"\n{'='*80}")
        print(f"🔍 DETECTING RESEARCH GAPS")
        print(f"{'='*80}\n")
        
        # Extract keywords from all abstracts
        all_text = " ".join([p.get('abstract', '').lower() for p in papers])
        
        # Define research gap indicators
        gap_indicators = {
            'limited': 'Limited research exists',
            'few studies': 'Few studies have explored',
            'unexplored': 'Underexplored areas remain',
            'challenges': 'Key challenges persist',
            'future work': 'Future research is needed',
            'scalability': 'Scalability remains a concern',
            'environmental': 'Environmental impacts need more study',
            'economics': 'Economic viability is unclear'
        }
        
        detected_gaps = []
        
        # Count keyword frequency to identify focus areas
        keyword_counts = {}
        keywords = ['efficiency', 'sustainability', 'recycling', 'scalability', 
                   'environmental', 'cost', 'performance', 'safety']
        
        for keyword in keywords:
            count = all_text.count(keyword)
            keyword_counts[keyword] = count
        
        # Identify underexplored topics
        avg_count = sum(keyword_counts.values()) / len(keyword_counts)
        
        for keyword, count in keyword_counts.items():
            if count < avg_count * 0.5:
                detected_gaps.append(f"⚠️  '{keyword.upper()}' is underexplored (mentioned {count} times vs average {avg_count:.0f})")
        
        # Add domain-specific gaps
        if 'recycling' in all_text and 'scalability' not in all_text:
            detected_gaps.append("⚠️  RESEARCH GAP: Scalability of recycling processes is rarely discussed")
        
        if 'lithium' in all_text and 'developing countries' not in all_text:
            detected_gaps.append("⚠️  RESEARCH GAP: Impact on developing countries is limited in literature")
        
        if 'environmental' in all_text and 'economics' not in all_text.lower():
            detected_gaps.append("⚠️  RESEARCH GAP: Economic analysis of sustainable practices is sparse")
        
        if not detected_gaps:
            detected_gaps.append("✅ Current research appears well-balanced across key topics")
        
        for gap in detected_gaps:
            print(gap)
        
        return detected_gaps
    
    def answer_query(self, query: str) -> Dict:
        """
        Complete RAG pipeline: Retrieve → Detect Gaps → Generate Answer
        """
        print(f"\n{'='*80}")
        print(f"🔎 ANSWERING QUERY")
        print(f"{'='*80}")
        print(f"Question: {query}\n")
        
        # Retrieve relevant context
        print("📚 Retrieving relevant papers...")
        context_chunks = self.retrieve_context(query, top_k=3)
        
        print(f"✅ Found {len(context_chunks)} relevant chunks\n")
        
        # Display retrieved papers
        print("📄 Retrieved Papers:")
        for i, chunk in enumerate(context_chunks, 1):
            print(f"  {i}. {chunk['metadata']['title']}")
            print(f"     Source: {chunk['metadata']['source']} | Year: {chunk['metadata']['year']}")
            print(f"     Similarity Score: {1 - chunk['distance']:.3f}")
        
        # Generate answer
        answer = self.generate_answer(query, context_chunks)
        
        # Detect research gaps in retrieved context
        retrieved_papers = [
            next((p for p in self.papers if p.get('title') == chunk['metadata']['title']), None)
            for chunk in context_chunks
        ]
        retrieved_papers = [p for p in retrieved_papers if p is not None]
        
        gaps = self.detect_research_gaps(retrieved_papers) if retrieved_papers else []
        
        # Compile result
        result = {
            'query': query,
            'answer': answer,
            'citations': [
                {
                    'title': chunk['metadata']['title'],
                    'source': chunk['metadata']['source'],
                    'year': chunk['metadata']['year'],
                    'authors': chunk['metadata'].get('authors', [])
                }
                for chunk in context_chunks
            ],
            'research_gaps': gaps
        }
        
        return result
    
    def print_result(self, result: Dict):
        """Pretty print the RAG result"""
        print(f"\n{'='*80}")
        print(f"✨ ANSWER")
        print(f"{'='*80}")
        print(f"\n{result['answer']}\n")
        
        print(f"{'='*80}")
        print(f"📖 CITATIONS")
        print(f"{'='*80}")
        for i, citation in enumerate(result['citations'], 1):
            print(f"{i}. {citation['title']}")
            print(f"   Authors: {', '.join(citation['authors'][:3]) if citation['authors'] else 'Unknown'}")
            print(f"   Year: {citation['year']} | Source: {citation['source']}\n")
        
        print(f"{'='*80}")
        print(f"🔍 RESEARCH GAPS DETECTED")
        print(f"{'='*80}")
        for gap in result['research_gaps']:
            print(gap)
        
        print(f"\n{'='*80}\n")


if __name__ == "__main__":
    # Initialize RAG pipeline
    rag = RAGPipeline()
    
    # Test with sample papers (from previous pipeline run)
    # In production, these would come from the fetcher
    sample_papers = [
        {
            'title': 'Lithium-Ion Battery Recycling: Technologies and Sustainability',
            'abstract': 'Lithium-ion batteries are increasingly used in electric vehicles and renewable energy storage. However, their recycling remains a significant challenge. This study explores advanced recycling technologies including hydrometallurgical, pyrometallurgical, and direct recycling methods. We discuss sustainability aspects and environmental impacts. Future work should focus on improving scalability and reducing costs.',
            'source': 'semantic_scholar',
            'year': 2024,
            'citations': 150,
            'authors': ['Smith, J.', 'Johnson, M.', 'Williams, R.']
        },
        {
            'title': 'Environmental Impact of Battery Manufacturing',
            'abstract': 'Battery manufacturing consumes significant energy and water resources. Our analysis shows that environmental costs are highest during cathode material production. We examine supply chain impacts and propose sustainable manufacturing practices. Environmental regulations are critical for reducing impact.',
            'source': 'arxiv',
            'year': 2025,
            'citations': 89,
            'authors': ['Brown, A.', 'Davis, C.']
        },
        {
            'title': 'Economic Viability of Battery Recycling Programs',
            'abstract': 'This paper evaluates the economics of large-scale battery recycling. We analyze cost structures and revenue potential. Economic models suggest recycling can be profitable with proper policy support. However, economics vary significantly by region.',
            'source': 'arxiv',
            'year': 2023,
            'citations': 45,
            'authors': ['Taylor, K.', 'Anderson, P.', 'Martin, L.']
        }
    ]
    
    # Prepare data
    rag.prepare_data(sample_papers)
    
    # Test queries
    test_queries = [
        "What are the main challenges in battery recycling?",
        "How can we make battery recycling more sustainable?",
        "What are the economic aspects of battery recycling?"
    ]
    
    print(f"\n🚀 RAG PIPELINE READY - Testing with sample queries\n")
    
    for query in test_queries:
        result = rag.answer_query(query)
        rag.print_result(result)
        print("\n")
