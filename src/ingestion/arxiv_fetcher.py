import requests
import xml.etree.ElementTree as ET

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
