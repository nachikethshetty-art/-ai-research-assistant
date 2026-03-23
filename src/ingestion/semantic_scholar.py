import requests

def fetch_semantic_scholar(query, limit=10):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,year,citationCount,authors"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            print("Semantic Scholar error:", response.status_code)
            return []

        data = response.json()

        papers = []
        for p in data.get("data", []):
            papers.append({
                "source": "semantic_scholar",
                "title": p.get("title"),
                "abstract": p.get("abstract"),
                "year": p.get("year"),
                "citations": p.get("citationCount"),
                "authors": [a["name"] for a in p.get("authors", [])]
            })

        return papers
    except Exception as e:
        print(f"Semantic Scholar fetch error: {e}")
        return []
