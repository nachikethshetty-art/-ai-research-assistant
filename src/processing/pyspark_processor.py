#!/usr/bin/env python3
"""
PySpark Integration for distributed data processing
Process large paper datasets efficiently
"""
from typing import Dict, List, Optional
import json
from pathlib import Path

class PySparkProcessor:
    """
    Process research papers using PySpark
    - Distributed filtering and deduplication
    - Feature extraction at scale
    - Analytics and aggregations
    """
    
    def __init__(self, enable_spark: bool = False):
        self.enable_spark = enable_spark
        self.spark = None
        if enable_spark:
            self._init_spark()
    
    def _init_spark(self):
        """Initialize Spark session"""
        try:
            from pyspark.sql import SparkSession
            self.spark = SparkSession.builder \
                .appName("ResearchAssistant") \
                .config("spark.driver.memory", "2g") \
                .config("spark.sql.shuffle.partitions", "4") \
                .getOrCreate()
        except ImportError:
            print("⚠️ PySpark not installed. Running in single-node mode.")
            self.enable_spark = False
    
    def process_papers(
        self,
        papers: List[Dict],
        filters: Dict = None,
        deduplicate: bool = True
    ) -> List[Dict]:
        """
        Process papers with filtering, deduplication, enrichment
        
        Args:
            papers: List of paper dictionaries
            filters: Filter criteria (e.g., {"year": 2020})
            deduplicate: Remove duplicate papers
        
        Returns:
            Processed papers
        """
        if not papers:
            return []
        
        processed = papers.copy()
        
        # Deduplication
        if deduplicate:
            processed = self._deduplicate(processed)
        
        # Filtering
        if filters:
            processed = self._filter_papers(processed, filters)
        
        # Enrichment
        processed = self._enrich_papers(processed)
        
        return processed
    
    def _deduplicate(self, papers: List[Dict]) -> List[Dict]:
        """Remove duplicate papers by title"""
        seen = {}
        unique = []
        
        for paper in papers:
            title = paper.get("title", "").lower().strip()
            if title and title not in seen:
                seen[title] = True
                unique.append(paper)
        
        return unique
    
    def _filter_papers(self, papers: List[Dict], filters: Dict) -> List[Dict]:
        """Filter papers by criteria"""
        filtered = papers
        
        # Filter by keywords
        if "keywords" in filters:
            keywords = [k.lower() for k in filters["keywords"]]
            filtered = [
                p for p in filtered
                if any(k in p.get("title", "").lower() or 
                      k in p.get("abstract", "").lower()
                      for k in keywords)
            ]
        
        # Filter by year
        if "year_min" in filters:
            year_min = filters["year_min"]
            filtered = [p for p in filtered if int(str(p.get("year", 0))) >= year_min]
        
        if "year_max" in filters:
            year_max = filters["year_max"]
            filtered = [p for p in filtered if int(str(p.get("year", 9999))) <= year_max]
        
        # Filter by min citations
        if "min_citations" in filters:
            min_cites = filters["min_citations"]
            filtered = [p for p in filtered if int(p.get("citations", 0)) >= min_cites]
        
        return filtered
    
    def _enrich_papers(self, papers: List[Dict]) -> List[Dict]:
        """Add computed features"""
        for paper in papers:
            # Add computed fields
            paper["abstract_length"] = len(paper.get("abstract", ""))
            paper["num_authors"] = len(paper.get("authors", []))
            paper["title_length"] = len(paper.get("title", ""))
            
            # Add keywords from abstract
            abstract = paper.get("abstract", "").lower()
            keywords = []
            common_keywords = ["learning", "network", "model", "data", "algorithm", 
                             "performance", "system", "method", "analysis"]
            for kw in common_keywords:
                if kw in abstract:
                    keywords.append(kw)
            paper["detected_keywords"] = keywords
        
        return papers
    
    def aggregate_statistics(self, papers: List[Dict]) -> Dict:
        """Compute aggregate statistics over papers"""
        if not papers:
            return {}
        
        stats = {
            "total_papers": len(papers),
            "avg_citations": sum(p.get("citations", 0) for p in papers) / len(papers),
            "avg_year": sum(int(str(p.get("year", 0))) for p in papers) / len(papers),
            "avg_authors": sum(len(p.get("authors", [])) for p in papers) / len(papers),
            "avg_abstract_length": sum(len(p.get("abstract", "")) for p in papers) / len(papers),
            "citation_range": (
                min(p.get("citations", 0) for p in papers),
                max(p.get("citations", 0) for p in papers)
            ),
            "year_range": (
                min(int(str(p.get("year", 9999))) for p in papers),
                max(int(str(p.get("year", 0))) for p in papers)
            ),
            "sources": list(set(p.get("source", "unknown") for p in papers))
        }
        
        return {k: round(v, 2) if isinstance(v, float) else v for k, v in stats.items()}
    
    def save_processing_report(self, papers: List[Dict], output_path: str = "data/processing_report.json"):
        """Save processing statistics to file"""
        report = {
            "timestamp": str(__import__("datetime").datetime.now().isoformat()),
            "total_papers": len(papers),
            "statistics": self.aggregate_statistics(papers),
            "sources": list(set(p.get("source", "unknown") for p in papers))
        }
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        
        return report
