#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ET

# Semantic Scholar Fetcher
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

# arXiv Fetcher
def fetch_arxiv(query, max_results=10):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print("arXiv error:", response.status_code)
            return []

        root = ET.fromstring(response.content)

        papers = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text

            papers.append({
                "source": "arxiv",
                "title": title.strip(),
                "abstract": summary.strip()
            })

        return papers
    except Exception as e:
        print(f"arXiv fetch error: {e}")
        return []

# Main fetcher
def fetch_all_papers(query):
    print(f"\n🔍 Fetching papers for: '{query}'\n")
    
    print("📚 Fetching from Semantic Scholar...")
    ss_papers = fetch_semantic_scholar(query)
    print(f"✅ Got {len(ss_papers)} papers from Semantic Scholar")

    print("\n📚 Fetching from arXiv...")
    arxiv_papers = fetch_arxiv(query)
    print(f"✅ Got {len(arxiv_papers)} papers from arXiv")

    all_papers = ss_papers + arxiv_papers

    print(f"\n🎯 Total papers collected: {len(all_papers)}\n")

    return all_papers


if __name__ == "__main__":
    query = "lithium-ion battery recycling sustainability"
    papers = fetch_all_papers(query)

    print("=" * 80)
    print("📄 SAMPLE PAPERS (First 5):")
    print("=" * 80)
    
    for i, p in enumerate(papers[:5], 1):
        print(f"\n{i}. {p.get('title', 'No title')}")
        print(f"   Source: {p.get('source')}")
        if p.get('abstract'):
            abstract_preview = p.get('abstract')[:200] + "..." if len(p.get('abstract', '')) > 200 else p.get('abstract')
            print(f"   Abstract: {abstract_preview}")
        if p.get('year'):
            print(f"   Year: {p.get('year')}")
        if p.get('citations'):
            print(f"   Citations: {p.get('citations')}")
    
    print("\n" + "=" * 80)
