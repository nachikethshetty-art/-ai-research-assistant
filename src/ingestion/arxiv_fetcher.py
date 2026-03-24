import requests
import xml.etree.ElementTree as ET
import time

def fetch_arxiv(query, max_results=10):
    """
    Fetch papers from arXiv API (OPTIMIZED - NO SLEEP)
    Note: arXiv has no strict rate limits - removed sleep delays
    """
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={min(max_results, 100)}&sortBy=relevance"

    try:
        # REMOVED TIME.SLEEP - arXiv doesn't require it for single requests
        response = requests.get(url, timeout=8)

        if response.status_code != 200:
            print(f"arXiv error: {response.status_code}")
            return []

        root = ET.fromstring(response.content)

        papers = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            try:
                title_elem = entry.find("{http://www.w3.org/2005/Atom}title")
                summary_elem = entry.find("{http://www.w3.org/2005/Atom}summary")
                published_elem = entry.find("{http://www.w3.org/2005/Atom}published")
                arxiv_id_elem = entry.find("{http://www.w3.org/2005/Atom}id")
                authors_elems = entry.findall("{http://www.w3.org/2005/Atom}author")
                
                title = title_elem.text.strip() if title_elem is not None else "Unknown"
                abstract = summary_elem.text.strip() if summary_elem is not None else ""
                year = published_elem.text[:4] if published_elem is not None else "Unknown"
                arxiv_id = arxiv_id_elem.text.split('/abs/')[-1] if arxiv_id_elem is not None else ""
                authors = [a.find("{http://www.w3.org/2005/Atom}name").text for a in authors_elems if a.find("{http://www.w3.org/2005/Atom}name") is not None]
                
                papers.append({
                    "source": "arxiv",
                    "title": title,
                    "abstract": abstract,
                    "year": year,
                    "citations": 0,  # arXiv doesn't provide citation counts
                    "authors": authors,
                    "url": f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None
                })
            except Exception as e:
                print(f"Error parsing arXiv entry: {e}")
                continue

        return papers
    except requests.exceptions.Timeout:
        print("⚠️  arXiv timeout (slow connection)")
        return []
    except Exception as e:
        print(f"arXiv fetch error: {e}")
        return []