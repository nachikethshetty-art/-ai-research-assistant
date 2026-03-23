import requests
import time
import json

def fetch_semantic_scholar(query, limit=10):
    """
    Fetch papers from Semantic Scholar API
    Note: Free API has strict rate limits. Gracefully falls back to arXiv if limited.
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": min(limit, 50),
        "fields": "title,abstract,year,citationCount,authors,paperId"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"
    }

    try:
        time.sleep(1)
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 429:
            return []  # Rate limited - fall back to arXiv
        if response.status_code == 403:
            return []  # Forbidden - API issue
        if response.status_code != 200:
            return []

        data = response.json()
        papers = []
        
        for p in data.get("data", []):
            if not p.get("abstract"):
                continue
            
            papers.append({
                "source": "semantic_scholar",
                "title": p.get("title", "Unknown"),
                "abstract": p.get("abstract", ""),
                "year": p.get("year", "Unknown"),
                "citations": p.get("citationCount", 0),
                "authors": [a.get("name", "Unknown") for a in p.get("authors", [])],
                "url": f"https://semanticscholar.org/paper/{p.get('paperId')}" if p.get('paperId') else None
            })

        return papers[:limit]
        
    except:
        return []  # Fail silently - arXiv will be used as fallback
