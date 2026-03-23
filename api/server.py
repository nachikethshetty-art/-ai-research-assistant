#!/usr/bin/env python3
"""
Flask API Server for n8n Integration
Exposes endpoints for paper fetching, processing, and analysis
"""

from flask import Flask, request, jsonify
import sys
import os
from datetime import datetime
import json

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'ingestion'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'processing'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'embeddings'))

app = Flask(__name__)

# Store for papers (in-memory, replace with DB in production)
papers_store = []
last_fetch = None

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    """System health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0',
        'papers_count': len(papers_store)
    }), 200

# Fetch papers
@app.route('/api/fetch_papers', methods=['POST'])
def fetch_papers():
    """
    Fetch papers from Semantic Scholar
    POST data: {"query": "...", "limit": 10}
    """
    try:
        data = request.get_json() or {}
        query = data.get('query', 'lithium-ion battery recycling')
        limit = data.get('limit', 10)
        
        # Import fetcher
        from main_fetcher import fetch_semantic_scholar
        
        print(f"📚 Fetching from Semantic Scholar: {query}")
        papers = fetch_semantic_scholar(query, limit=limit)
        
        papers_store.extend(papers)
        
        return jsonify({
            'status': 'success',
            'count': len(papers),
            'papers': papers,
            'query': query,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Fetch from arXiv
@app.route('/api/fetch_arxiv', methods=['POST'])
def fetch_arxiv():
    """
    Fetch papers from arXiv
    POST data: {"query": "...", "max_results": 10}
    """
    try:
        data = request.get_json() or {}
        query = data.get('query', 'lithium-ion battery')
        max_results = data.get('max_results', 10)
        
        # Import fetcher
        from arxiv_fetcher import fetch_arxiv as fetch_arxiv_papers
        
        print(f"📚 Fetching from arXiv: {query}")
        papers = fetch_arxiv_papers(query, max_results=max_results)
        
        papers_store.extend(papers)
        
        return jsonify({
            'status': 'success',
            'count': len(papers),
            'papers': papers,
            'query': query,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Process papers
@app.route('/api/process_papers', methods=['POST'])
def process_papers():
    """
    Process papers: chunking and embedding
    POST data: {"papers": [...]}
    """
    try:
        data = request.get_json() or {}
        papers = data.get('papers', papers_store)
        
        if not papers:
            return jsonify({
                'status': 'error',
                'message': 'No papers to process'
            }), 400
        
        # Import processing modules
        from chunking import chunk_text
        
        print(f"⚙️ Processing {len(papers)} papers")
        
        chunks_created = 0
        for paper in papers:
            abstract = paper.get('abstract', '')
            if abstract:
                chunks = chunk_text(abstract, max_tokens=150)
                chunks_created += len(chunks)
        
        return jsonify({
            'status': 'success',
            'papers_processed': len(papers),
            'chunks_created': chunks_created,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Analyze papers
@app.route('/api/analyze_papers', methods=['POST'])
def analyze_papers():
    """
    Analyze papers with PySpark
    POST data: {} (uses papers_store)
    """
    try:
        papers = papers_store
        
        if not papers:
            return jsonify({
                'status': 'error',
                'message': 'No papers to analyze'
            }), 400
        
        # Try to import PySpark processor
        try:
            from src.processing.spark_processor import SparkPaperProcessor
            processor = SparkPaperProcessor()
            papers_df = processor.process_papers_batch(papers)
            processor.stop()
            
            analysis = {
                'total_papers': len(papers),
                'high_impact': len([p for p in papers if p.get('citations', 0) >= 50]),
                'recent_papers': len([p for p in papers if p.get('year', 0) >= 2024]),
                'sources': list(set([p.get('source', 'unknown') for p in papers]))
            }
        except ImportError:
            # Fallback if PySpark not available
            analysis = {
                'total_papers': len(papers),
                'high_impact': len([p for p in papers if p.get('citations', 0) >= 50]),
                'recent_papers': len([p for p in papers if p.get('year', 0) >= 2024]),
                'sources': list(set([p.get('source', 'unknown') for p in papers]))
            }
        
        return jsonify({
            'status': 'success',
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Get papers
@app.route('/api/papers', methods=['GET'])
def get_papers():
    """Get all stored papers"""
    limit = request.args.get('limit', 10, type=int)
    return jsonify({
        'status': 'success',
        'count': len(papers_store),
        'papers': papers_store[:limit],
        'timestamp': datetime.now().isoformat()
    }), 200

# Clear papers
@app.route('/api/papers/clear', methods=['DELETE'])
def clear_papers():
    """Clear all stored papers"""
    global papers_store
    count = len(papers_store)
    papers_store = []
    
    return jsonify({
        'status': 'success',
        'cleared_count': count,
        'timestamp': datetime.now().isoformat()
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AI Research Assistant API Server")
    print("="*60)
    print("\n📡 Starting Flask API Server...")
    print("   URL: http://localhost:8000")
    print("\n📚 Available Endpoints:")
    print("   GET  /api/health              - Health check")
    print("   POST /api/fetch_papers        - Fetch from Semantic Scholar")
    print("   POST /api/fetch_arxiv         - Fetch from arXiv")
    print("   POST /api/process_papers      - Process papers")
    print("   POST /api/analyze_papers      - Analyze with PySpark")
    print("   GET  /api/papers              - Get all papers")
    print("   DELETE /api/papers/clear      - Clear papers")
    print("\n" + "="*60 + "\n")
    
    app.run(host='localhost', port=8000, debug=True)
