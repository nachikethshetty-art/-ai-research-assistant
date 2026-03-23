#!/usr/bin/env python3
"""
Reinforcement Learning Feedback Loop
Self-improving mechanism for the AI Research Assistant
Optimized for M2 MacBook Air
"""

import json
import os
from datetime import datetime
from typing import Dict, List
from pathlib import Path

class RLFeedbackSystem:
    """
    Simple RL system that learns from user feedback to improve answer quality
    Uses reward signals to adjust retrieval ranking and response preferences
    """
    
    def __init__(self, db_path="data/feedback.json"):
        self.db_path = db_path
        self.feedback_history = []
        self.model_weights = {
            'relevance': 1.0,
            'clarity': 1.0,
            'citation_quality': 1.0,
            'gap_detection': 1.0
        }
        self.query_count = 0
        self.total_reward = 0.0
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create data directory if not exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing feedback
        self._load_feedback()
    
    def _load_feedback(self):
        """Load feedback history from JSON"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    self.feedback_history = data.get('history', [])
                    self.model_weights = data.get('weights', self.model_weights)
                    self.query_count = len(self.feedback_history)
                    print(f"✅ Loaded {self.query_count} previous feedback entries")
            except Exception as e:
                print(f"⚠️  Could not load feedback: {e}")
    
    def _save_feedback(self):
        """Save feedback history to JSON"""
        try:
            data = {
                'history': self.feedback_history,
                'weights': self.model_weights,
                'total_queries': self.query_count,
                'average_reward': self.total_reward / max(1, self.query_count)
            }
            with open(self.db_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save feedback: {e}")
    
    def calculate_reward(self, feedback: Dict) -> float:
        """
        Calculate reward based on user feedback
        Reward = sum of weighted ratings
        """
        relevance_score = feedback.get('relevance', 0) / 5.0  # 0-5 scale
        clarity_score = feedback.get('clarity', 0) / 5.0
        citations_score = feedback.get('citations', 0) / 5.0
        gaps_score = feedback.get('gaps', 0) / 5.0
        
        reward = (
            relevance_score * self.model_weights['relevance'] +
            clarity_score * self.model_weights['clarity'] +
            citations_score * self.model_weights['citation_quality'] +
            gaps_score * self.model_weights['gap_detection']
        ) / 4.0
        
        return reward
    
    def update_weights(self, reward: float):
        """
        Update model weights based on reward
        High reward → increase weight importance
        Low reward → decrease weight importance
        """
        learning_rate = 0.05  # Conservative learning rate for M2
        
        if reward > 0.75:  # Excellent answer
            for key in self.model_weights:
                self.model_weights[key] *= (1 + learning_rate * 0.1)
        elif reward < 0.5:  # Poor answer
            for key in self.model_weights:
                self.model_weights[key] *= (1 - learning_rate * 0.05)
        
        # Normalize weights
        total_weight = sum(self.model_weights.values())
        for key in self.model_weights:
            self.model_weights[key] /= total_weight
    
    def record_feedback(self, query: str, answer: str, feedback: Dict) -> float:
        """
        Record user feedback and update model weights
        
        Args:
            query: User query
            answer: System answer
            feedback: Dict with ratings
                - relevance: 0-5
                - clarity: 0-5
                - citations: 0-5
                - gaps: 0-5
        
        Returns:
            reward: Calculated reward value
        """
        reward = self.calculate_reward(feedback)
        self.update_weights(reward)
        self.total_reward += reward
        self.query_count += 1
        
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'query': query,
            'answer_preview': answer[:100],
            'feedback': feedback,
            'reward': reward,
            'current_weights': dict(self.model_weights)
        }
        
        self.feedback_history.append(feedback_entry)
        self._save_feedback()
        
        return reward
    
    def get_learning_progress(self) -> Dict:
        """Get system learning progress metrics"""
        if self.query_count == 0:
            return {
                'queries_processed': 0,
                'average_reward': 0.0,
                'improvement': 0.0,
                'learning_status': 'No data yet'
            }
        
        avg_reward = self.total_reward / self.query_count
        
        # Calculate improvement trend
        if len(self.feedback_history) > 5:
            recent_avg = sum([f['reward'] for f in self.feedback_history[-5:]]) / 5
            older_avg = sum([f['reward'] for f in self.feedback_history[:5]]) / 5
            improvement = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
        else:
            improvement = 0.0
        
        # Determine learning status
        if avg_reward >= 0.8:
            status = "🟢 Excellent Learning"
        elif avg_reward >= 0.6:
            status = "🟡 Good Learning"
        elif avg_reward >= 0.4:
            status = "🟠 Moderate Learning"
        else:
            status = "🔴 Needs Improvement"
        
        return {
            'queries_processed': self.query_count,
            'average_reward': round(avg_reward, 3),
            'improvement_percent': round(improvement, 2),
            'learning_status': status,
            'model_weights': {k: round(v, 3) for k, v in self.model_weights.items()}
        }
    
    def get_recent_feedback(self, limit=5) -> List[Dict]:
        """Get recent feedback entries"""
        return self.feedback_history[-limit:]
    
    def print_learning_status(self):
        """Pretty print learning progress"""
        progress = self.get_learning_progress()
        
        print(f"\n{'='*80}")
        print(f"🤖 SYSTEM LEARNING PROGRESS")
        print(f"{'='*80}")
        print(f"Queries Processed: {progress['queries_processed']}")
        print(f"Average Reward Score: {progress['average_reward']}/1.0")
        print(f"Improvement Trend: {progress['improvement_percent']:+.2f}%")
        print(f"Status: {progress['learning_status']}")
        print(f"\nModel Weights:")
        for weight, value in progress['model_weights'].items():
            print(f"  {weight}: {value:.3f}")
        print(f"{'='*80}\n")


# Interactive Feedback Collector
def collect_user_feedback() -> Dict:
    """
    Collect feedback from user (1-5 scale)
    Optimized for quick input
    """
    print(f"\n{'='*80}")
    print(f"📝 RATE THE ANSWER (1-5 scale, where 5 is excellent)")
    print(f"{'='*80}")
    
    try:
        relevance = int(input("1. How relevant was the answer to your question? (1-5): ") or 3)
        clarity = int(input("2. How clear and understandable was the answer? (1-5): ") or 3)
        citations = int(input("3. How helpful were the citations? (1-5): ") or 3)
        gaps = int(input("4. How useful was the research gap detection? (1-5): ") or 3)
        
        # Validate inputs
        feedback = {
            'relevance': max(1, min(5, relevance)),
            'clarity': max(1, min(5, clarity)),
            'citations': max(1, min(5, citations)),
            'gaps': max(1, min(5, gaps))
        }
        
        return feedback
    
    except ValueError:
        print("⚠️  Invalid input, using default ratings")
        return {'relevance': 3, 'clarity': 3, 'citations': 3, 'gaps': 3}


if __name__ == "__main__":
    # Test the RL system
    rl_system = RLFeedbackSystem()
    
    # Simulate some feedback
    test_feedbacks = [
        {
            'query': 'What are battery recycling methods?',
            'answer': 'Battery recycling involves multiple approaches...',
            'feedback': {'relevance': 5, 'clarity': 4, 'citations': 4, 'gaps': 3}
        },
        {
            'query': 'How does sustainability affect battery production?',
            'answer': 'Sustainability in battery production encompasses...',
            'feedback': {'relevance': 4, 'clarity': 5, 'citations': 5, 'gaps': 4}
        },
        {
            'query': 'What are the economic implications?',
            'answer': 'The economics of battery recycling show...',
            'feedback': {'relevance': 3, 'clarity': 3, 'citations': 2, 'gaps': 2}
        }
    ]
    
    print("🧪 TESTING RL FEEDBACK SYSTEM\n")
    
    for test in test_feedbacks:
        reward = rl_system.record_feedback(
            test['query'],
            test['answer'],
            test['feedback']
        )
        print(f"Query: {test['query']}")
        print(f"Reward: {reward:.3f}\n")
    
    # Print learning progress
    rl_system.print_learning_status()
    
    # Print recent feedback
    print("Recent Feedback:")
    for fb in rl_system.get_recent_feedback(3):
        print(f"  Query: {fb['query']}")
        print(f"  Reward: {fb['reward']:.3f}")
        print()
