#!/usr/bin/env python3
"""RL Feedback Loop - OpenEnv Style"""

import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Observation:
    query: str
    papers_found: int
    query_confidence: float
    timestamp: str

@dataclass
class Action:
    action_type: str
    query: str
    parameters: Dict[str, Any]

@dataclass
class StepResult:
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]

class RLFeedbackLoop:
    """RL Feedback Loop - OpenEnv Style with Advanced Learning"""
    
    def __init__(self):
        self.episode_id = ""
        self.step_count = 0
        self.total_reward = 0.0
        self.history = []
        self.current_query = ""
        self.papers_found = 0
        self.learning_rate = 0.1
        self.query_performance = {}  # Track performance per query
        self.strategy_metrics = {  # Track effectiveness of strategies
            "arXiv": {"calls": 0, "success": 0, "avg_reward": 0},
            "semantic_scholar": {"calls": 0, "success": 0, "avg_reward": 0},
            "multi_source": {"calls": 0, "success": 0, "avg_reward": 0}
        }
    
    def reset(self, query: str = "") -> StepResult:
        """Reset episode with new query (OpenEnv reset)"""
        self.episode_id = f"episode_{int(time.time())}"
        self.step_count = 0
        self.total_reward = 0.0
        self.history = []
        self.current_query = query
        self.papers_found = 0
        
        observation = Observation(
            query=query,
            papers_found=0,
            query_confidence=0.5,
            timestamp=datetime.now().isoformat()
        )
        
        return StepResult(
            observation=observation,
            reward=0.0,
            done=False,
            info={
                "episode_id": self.episode_id,
                "query": query,
                "strategy": "initialized"
            }
        )
    
    def step(self, action: Action, papers_found: int = 0, answer_quality: float = 0.5) -> StepResult:
        """Execute action and calculate reward (OpenEnv step)"""
        self.step_count += 1
        self.papers_found = papers_found
        
        # Calculate multi-component reward
        papers_reward = min(papers_found / 5.0, 1.0)  # Normalize to 5 papers
        quality_reward = answer_quality
        speed_bonus = min(1.0 / max(self.step_count, 1), 0.3)  # Reward faster responses
        
        combined_reward = (papers_reward * 0.4 + quality_reward * 0.5 + speed_bonus * 0.1)
        combined_reward = min(combined_reward, 1.0)
        
        self.total_reward += combined_reward
        
        # Update strategy metrics
        strategy = action.parameters.get("strategy", "unknown")
        if strategy in self.strategy_metrics:
            self.strategy_metrics[strategy]["calls"] += 1
            if papers_found > 0:
                self.strategy_metrics[strategy]["success"] += 1
            self.strategy_metrics[strategy]["avg_reward"] = (
                (self.strategy_metrics[strategy]["avg_reward"] * 
                 (self.strategy_metrics[strategy]["calls"] - 1) + combined_reward) / 
                self.strategy_metrics[strategy]["calls"]
            )
        
        # Track query performance
        if action.query not in self.query_performance:
            self.query_performance[action.query] = []
        self.query_performance[action.query].append({
            "step": self.step_count,
            "reward": combined_reward,
            "papers": papers_found,
            "timestamp": datetime.now().isoformat()
        })
        
        # Store history entry
        self.history.append({
            "step": self.step_count,
            "action": action.action_type,
            "strategy": strategy,
            "papers": papers_found,
            "quality": answer_quality,
            "reward": combined_reward,
            "total_reward": self.total_reward,
            "timestamp": datetime.now().isoformat()
        })
        
        # Episode ends after 5 steps or perfect quality
        done = self.step_count >= 5 or combined_reward >= 0.95
        
        # Update observation with learned confidence
        confidence = min(0.5 + (self.step_count * 0.15), 1.0)
        
        observation = Observation(
            query=action.query,
            papers_found=papers_found,
            query_confidence=confidence,
            timestamp=datetime.now().isoformat()
        )
        
        return StepResult(
            observation=observation,
            reward=combined_reward,
            done=done,
            info={
                "episode_id": self.episode_id,
                "step": self.step_count,
                "total_reward": self.total_reward,
                "papers_reward": papers_reward,
                "quality_reward": quality_reward,
                "speed_bonus": speed_bonus,
                "strategy": strategy,
                "history": self.history
            }
        )
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state (OpenEnv observation)"""
        return {
            "episode_id": self.episode_id,
            "step_count": self.step_count,
            "total_reward": self.total_reward,
            "papers_found": self.papers_found,
            "history": self.history,
            "strategy_metrics": self.strategy_metrics,
            "query_performance": self.query_performance
        }
    
    def get_best_strategy(self) -> str:
        """Return the best performing strategy based on learning"""
        best_strategy = max(
            self.strategy_metrics.items(),
            key=lambda x: x[1]["avg_reward"] if x[1]["calls"] > 0 else 0
        )
        return best_strategy[0]
    
    def save_episode(self, filename: str = None) -> str:
        """Save episode data for analysis"""
        if not filename:
            filename = f"episode_{self.episode_id}.json"
        
        episode_data = {
            "episode_id": self.episode_id,
            "duration_steps": self.step_count,
            "total_reward": self.total_reward,
            "history": self.history,
            "strategy_metrics": self.strategy_metrics,
            "query_performance": self.query_performance,
            "best_strategy": self.get_best_strategy()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(episode_data, f, indent=2)
            return filename
        except Exception:
            return None
