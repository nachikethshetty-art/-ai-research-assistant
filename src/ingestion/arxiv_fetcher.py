import requests
import xml.etree.ElementTree as ET
import time
from datetime import datetime

def fetch_arxiv(query, max_results=10):
    """
    Fetch papers from arXiv API
    """
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={min(max_results, 200)}&sortBy=relevance&sortOrder=descending"

    try:
        time.sleep(2)
        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            return []

        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        papers = []
        for entry in root.findall('atom:entry', ns):
            try:
                title_elem = entry.find('atom:title', ns)
                summary_elem = entry.find('atom:summary', ns)
                published_elem = entry.find('atom:published', ns)
                
                title = title_elem.text.replace('\n', ' ').strip() if title_elem is not None else "Unknown"
                abstract = summary_elem.text.replace('\n', ' ').strip() if summary_elem is not None else ""
                
                # Extract year from published date
                published = published_elem.text if published_elem is not None else ""
                year = published[:4] if published else "Unknown"
                
                # Extract authors
                authors = []
                for author in entry.findall('atom:author', ns):
                    name_elem = author.find('atom:name', ns)
                    if name_elem is not None:
                        authors.append(name_elem.text)
                
                # Extract arXiv ID
                id_elem = entry.find('atom:id', ns)
                arxiv_id = ""
                if id_elem is not None:
                    arxiv_id = id_elem.text.split('/abs/')[-1] if '/abs/' in id_elem.text else id_elem.text.split('/')[-1]
                
                papers.append({
                    "source": "arxiv",
                    "title": title,
                    "abstract": abstract[:500],  # Limit abstract length
                    "year": year,
                    "citations": 0,  # arXiv doesn't provide this
                    "authors": authors,
                    "url": f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None
                })
            except Exception as e:
                continue

        return papers[:max_results]
        
    except:
        return []
