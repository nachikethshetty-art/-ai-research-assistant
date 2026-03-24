import requests
import time

def fetch_semantic_scholar(query, limit=10):
    """
    Fetch papers from Semantic Scholar API (OPTIMIZED v2)
    - Uses multiple fallback endpoints
    - Aggressive timeout (don't wait for slow API)
    - Returns empty list if API is slow/down
    """
    if not query or not query.strip():
        return []
    
    # Endpoint 1: Try the graph v1 API with minimal fields
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        
        params = {
            "query": query,
            "limit": min(limit, 8),
            "fields": "title,abstract,year,citationCount,authors"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Research-Assistant/1.0)"
        }
        
        # Increased timeout to allow API to respond
        response = requests.get(url, params=params, headers=headers, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            papers = []
            
            for p in data.get("data", []):
                try:
                    title = p.get("title", "").strip()
                    if not title or len(title) < 5:
                        continue
                    
                    papers.append({
                        "source": "semantic_scholar",
                        "title": title,
                        "abstract": p.get("abstract", "No abstract available"),
                        "year": p.get("year"),
                        "citations": p.get("citationCount", 0),
                        "authors": [a.get("name") for a in p.get("authors", []) if a.get("name")] if p.get("authors") else [],
                        "url": f"https://semanticscholar.org/paper/{p.get('paperId', '')}" if p.get("paperId") else None
                    })
                except Exception:
                    continue
            
            if papers:
                return papers
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        print(f"Semantic Scholar API timeout: {e}, trying OpenAlex...")
    except Exception:
        pass
    
    # Endpoint 2: Try OpenAlex API (faster alternative)
    try:
        url = "https://api.openalex.org/works"
        
        params = {
            "search": query,
            "per_page": min(limit, 5),
            "sort": "cited_by_count:desc"
        }
        
        response = requests.get(url, params=params, timeout=6)
        
        if response.status_code == 200:
            data = response.json()
            papers = []
            
            for work in data.get("results", []):
                try:
                    title = work.get("title", "").strip()
                    if not title or len(title) < 5:
                        continue
                    
                    authors = []
                    for author in work.get("authorships", []):
                        author_info = author.get("author", {})
                        if author_info.get("display_name"):
                            authors.append(author_info["display_name"])
                    
                    papers.append({
                        "source": "openalex",
                        "title": title,
                        "abstract": work.get("abstract", "No abstract available"),
                        "year": work.get("publication_year"),
                        "citations": work.get("cited_by_count", 0),
                        "authors": authors[:5],
                        "url": work.get("ids", {}).get("doi", work.get("id"))
                    })
                except Exception:
                    continue
            
            if papers:
                return papers
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        print(f"OpenAlex API timeout: {e}")
    except Exception:
        pass
    
    # Return empty list if both APIs fail (don't block)
    return []