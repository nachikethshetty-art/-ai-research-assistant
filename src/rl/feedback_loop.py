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
    def __init__(self):
        self.episode_id = ""
        self.step_count = 0
        self.total_reward = 0.0
        self.history = []
        self.current_query = ""
        self.papers_found = 0
    
    def reset(self, query: str = "") -> StepResult:
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
            info={"episode_id": self.episode_id}
        )
    
    def step(self, action: Action, papers_found: int = 0, answer_quality: float = 0.5) -> StepResult:
        self.step_count += 1
        self.papers_found = papers_found
        
        papers_reward = min(papers_found / 10.0, 1.0)
        quality_reward = answer_quality
        combined_reward = (papers_reward + quality_reward) / 2.0
        
        self.total_reward += combined_reward
        
        self.history.append({
            "step": self.step_count,
            "action": action.action_type,
            "papers": papers_found,
            "quality": answer_quality,
            "reward": combined_reward,
            "timestamp": datetime.now().isoformat()
        })
        
        done = self.step_count >= 5 or combined_reward >= 0.95
        
        observation = Observation(
            query=action.query,
            papers_found=papers_found,
            query_confidence=min(0.5 + (self.step_count * 0.1), 1.0),
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
                "history": self.history
            }
        )
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "step_count": self.step_count,
            "total_reward": self.total_reward,
            "papers_found": self.papers_found,
            "history": self.history
        }
