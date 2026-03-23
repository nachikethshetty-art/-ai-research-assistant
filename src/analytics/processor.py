#!/usr/bin/env python3
"""
PySpark Integration for Research Paper Analytics
Processes large-scale research data with distributed computing
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
import json


@dataclass
class PaperMetrics:
    """Metrics for a single paper"""
    title: str
    citations: int
    year: int
    keywords: List[str]
    relevance_score: float


class PaperAnalytics:
    """
    Local analytics engine (PySpark would be used for 100M+ papers)
    Implements distributed computing patterns
    """
    
    def __init__(self):
        self.papers = []
        self.metrics = {}
    
    def load_papers(self, papers: List[Dict]):
        """Load papers into analytics"""
        self.papers = papers
    
    def filter_papers(self, criteria: Dict) -> List[Dict]:
        """
        Filter papers by criteria
        Pattern: PySpark would distribute this across partitions
        """
        filtered = self.papers
        
        # Filter by year
        if 'min_year' in criteria:
            filtered = [p for p in filtered if p.get('year', 0) >= criteria['min_year']]
        
        # Filter by citations
        if 'min_citations' in criteria:
            filtered = [p for p in filtered if p.get('citations', 0) >= criteria['min_citations']]
        
        # Filter by keyword
        if 'keyword' in criteria:
            keyword = criteria['keyword'].lower()
            filtered = [
                p for p in filtered
                if keyword in p.get('title', '').lower() or
                   keyword in p.get('abstract', '').lower()
            ]
        
        return filtered
    
    def aggregate_by_year(self) -> Dict[int, int]:
        """
        Aggregate papers by year
        Pattern: PySpark would use groupBy().count()
        """
        agg = {}
        for paper in self.papers:
            year = paper.get('year', 0)
            if year:
                agg[year] = agg.get(year, 0) + 1
        return agg
    
    def aggregate_by_author(self) -> Dict[str, int]:
        """
        Aggregate papers by author
        Pattern: PySpark would use groupBy().count()
        """
        agg = {}
        for paper in self.papers:
            for author in paper.get('authors', []):
                agg[author] = agg.get(author, 0) + 1
        return dict(sorted(agg.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def top_papers_by_citations(self, n: int = 10) -> List[Dict]:
        """Get top N papers by citations"""
        return sorted(
            self.papers,
            key=lambda p: p.get('citations', 0),
            reverse=True
        )[:n]
    
    def calculate_trends(self) -> Dict:
        """Calculate research trends"""
        by_year = self.aggregate_by_year()
        
        if len(by_year) < 2:
            return {"trend": "insufficient_data"}
        
        years = sorted(by_year.keys())
        counts = [by_year[y] for y in years]
        
        # Simple trend calculation
        first_half_avg = sum(counts[:len(counts)//2]) / (len(counts)//2 or 1)
        second_half_avg = sum(counts[len(counts)//2:]) / (len(counts) - len(counts)//2 or 1)
        
        trend = "increasing" if second_half_avg > first_half_avg else "decreasing"
        growth_rate = (second_half_avg - first_half_avg) / (first_half_avg or 1) * 100
        
        return {
            "trend": trend,
            "growth_rate": growth_rate,
            "total_papers": len(self.papers),
            "year_range": f"{min(years)}-{max(years)}" if years else "N/A"
        }
    
    def extract_keywords(self) -> Dict[str, int]:
        """Extract and count keywords"""
        keywords = {}
        
        for paper in self.papers:
            title = paper.get('title', '')
            abstract = paper.get('abstract', '')
            
            # Simple keyword extraction
            common_terms = [
                'lithium', 'battery', 'recycling', 'sustainable', 'energy',
                'material', 'electrode', 'ion', 'cell', 'chemistry',
                'degradation', 'performance', 'efficiency', 'cycle', 'analysis'
            ]
            
            text = (title + " " + abstract).lower()
            for term in common_terms:
                if term in text:
                    keywords[term] = keywords.get(term, 0) + 1
        
        return dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True))
    
    def get_summary(self) -> Dict:
        """Get analytics summary"""
        return {
            "total_papers": len(self.papers),
            "by_year": self.aggregate_by_year(),
            "top_authors": self.aggregate_by_author(),
            "top_papers": [
                {"title": p.get('title'), "citations": p.get('citations')}
                for p in self.top_papers_by_citations(5)
            ],
            "trends": self.calculate_trends(),
            "keywords": self.extract_keywords()
        }


class ResearchDataProcessor:
    """
    Processes research data with distributed patterns
    In production, would use PySpark RDDs and DataFrames
    """
    
    def __init__(self):
        self.analytics = PaperAnalytics()
    
    def process_papers(self, papers: List[Dict]) -> Dict:
        """
        Process papers through analytics pipeline
        
        Pattern (PySpark):
            rdd = spark.parallelize(papers)
            filtered = rdd.filter(lambda p: p['citations'] > 10)
            grouped = filtered.groupByKey().count()
        """
        self.analytics.load_papers(papers)
        return self.analytics.get_summary()
    
    def filter_by_criteria(self, criteria: Dict) -> List[Dict]:
        """Filter papers with criteria"""
        return self.analytics.filter_papers(criteria)
    
    def export_analytics(self, filepath: str):
        """Export analytics to JSON"""
        data = self.analytics.get_summary()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    # Test analytics
    analytics = PaperAnalytics()
    
    sample_papers = [
        {"title": "Lithium Battery Recycling", "abstract": "Methods for recycling", "year": 2023, "citations": 45, "authors": ["Author A", "Author B"]},
        {"title": "Battery Chemistry", "abstract": "Advanced chemistry", "year": 2022, "citations": 30, "authors": ["Author C"]},
    ]
    
    analytics.load_papers(sample_papers)
    summary = analytics.get_summary()
    print(f"✅ Analytics summary: {json.dumps(summary, indent=2)}")
