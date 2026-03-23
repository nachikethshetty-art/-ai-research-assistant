#!/usr/bin/env python3
"""
Analytics & Metrics Tracker
Track queries, answers, rewards, performance
"""
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class AnalyticsTracker:
    """Track all system interactions and metrics"""
    
    def __init__(self, log_dir: str = "data/analytics"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.queries = []
        self.answers = []
        self.actions = []
        self.rewards = []
        
    def log_query(self, query: str, num_papers: int = 0, time_taken: float = 0.0):
        """Log a search query"""
        self.queries.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "num_papers": num_papers,
            "time_taken": time_taken
        })
    
    def log_answer(self, query: str, answer: str, confidence: float = 0.0):
        """Log a generated answer"""
        self.answers.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "answer_length": len(answer),
            "confidence": confidence
        })
    
    def log_action(self, action_type: str, reward: float, metadata: Dict = None):
        """Log RL action"""
        self.actions.append({
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "reward": reward,
            "metadata": metadata or {}
        })
        self.rewards.append(reward)
    
    def get_stats(self) -> Dict:
        """Get current statistics"""
        avg_papers = sum(q.get("num_papers", 0) for q in self.queries) / max(1, len(self.queries))
        avg_search_time = sum(q.get("time_taken", 0) for q in self.queries) / max(1, len(self.queries))
        avg_answer_length = sum(a.get("answer_length", 0) for a in self.answers) / max(1, len(self.answers))
        avg_reward = sum(self.rewards) / max(1, len(self.rewards)) if self.rewards else 0.0
        
        return {
            "total_queries": len(self.queries),
            "total_answers": len(self.answers),
            "total_actions": len(self.actions),
            "avg_papers_per_query": round(avg_papers, 2),
            "avg_search_time": round(avg_search_time, 2),
            "avg_answer_length": round(avg_answer_length, 0),
            "avg_reward": round(avg_reward, 3),
            "total_reward": round(sum(self.rewards), 2)
        }
    
    def save(self):
        """Save analytics to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with open(self.log_dir / f"queries_{timestamp}.json", "w") as f:
            json.dump(self.queries, f, indent=2)
        
        with open(self.log_dir / f"answers_{timestamp}.json", "w") as f:
            json.dump(self.answers, f, indent=2)
        
        with open(self.log_dir / f"actions_{timestamp}.json", "w") as f:
            json.dump(self.actions, f, indent=2)
        
        with open(self.log_dir / f"stats_{timestamp}.json", "w") as f:
            json.dump(self.get_stats(), f, indent=2)
    
    def clear(self):
        """Clear all logs"""
        self.queries.clear()
        self.answers.clear()
        self.actions.clear()
        self.rewards.clear()
