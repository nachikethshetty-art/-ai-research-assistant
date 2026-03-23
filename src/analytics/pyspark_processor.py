#!/usr/bin/env python3
"""
PySpark Analytics Pipeline
Distributed processing of research papers and feedback data
"""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

class PySparkAnalytics:
    """PySpark-based analytics (with graceful fallback)"""
    
    def __init__(self, use_spark: bool = True):
        """Initialize analytics engine"""
        self.use_spark = use_spark
        self.spark_available = False
        self.spark_session = None
        
        if use_spark:
            try:
                from pyspark.sql import SparkSession
                self.spark_session = SparkSession.builder \
                    .appName("ResearchAssistantAnalytics") \
                    .master("local[*]") \
                    .getOrCreate()
                self.spark_available = True
            except ImportError:
                print("⚠️ PySpark not available, using fallback analytics")
                self.spark_available = False
        
        self.data_store = []
    
    def process_papers(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process paper data and extract insights"""
        if not papers:
            return {"status": "no_data"}
        
        if self.spark_available:
            return self._spark_process(papers)
        else:
            return self._fallback_process(papers)
    
    def _spark_process(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process using PySpark"""
        try:
            # Create DataFrame
            df = self.spark_session.createDataFrame(
                [(p.get('title'), p.get('year'), p.get('citations', 0)) 
                 for p in papers],
                ["title", "year", "citations"]
            )
            
            # Analytics
            stats = {
                "total_papers": df.count(),
                "avg_citations": float(df.agg({"citations": "avg"}).collect()[0][0] or 0),
                "min_year": int(df.agg({"year": "min"}).collect()[0][0] or 0),
                "max_year": int(df.agg({"year": "max"}).collect()[0][0] or 0),
                "processing_method": "spark"
            }
            
            return stats
        except Exception as e:
            return {"error": str(e), "processing_method": "spark"}
    
    def _fallback_process(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback processing without PySpark"""
        if not papers:
            return {"total_papers": 0}
        
        citations = [p.get('citations', 0) for p in papers]
        years = [p.get('year') for p in papers if p.get('year')]
        
        stats = {
            "total_papers": len(papers),
            "avg_citations": sum(citations) / len(citations) if citations else 0,
            "min_year": min(years) if years else "N/A",
            "max_year": max(years) if years else "N/A",
            "processing_method": "fallback"
        }
        
        return stats
    
    def process_feedback(self, feedback_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process RL feedback data"""
        if not feedback_data:
            return {"status": "no_feedback"}
        
        rewards = [f.get('reward', 0) for f in feedback_data]
        actions = {}
        
        for f in feedback_data:
            action = f.get('action', 'unknown')
            actions[action] = actions.get(action, 0) + 1
        
        return {
            "total_feedback_points": len(feedback_data),
            "avg_reward": sum(rewards) / len(rewards) if rewards else 0,
            "max_reward": max(rewards) if rewards else 0,
            "actions_distribution": actions,
            "processing_method": "spark" if self.spark_available else "fallback"
        }
    
    def get_dashboard_data(self, papers: List[Dict[str, Any]], 
                          feedback: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate dashboard-ready analytics"""
        paper_stats = self.process_papers(papers)
        feedback_stats = self.process_feedback(feedback)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "papers": paper_stats,
            "feedback": feedback_stats,
            "spark_available": self.spark_available
        }
