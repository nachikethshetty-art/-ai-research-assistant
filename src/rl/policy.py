#!/usr/bin/env python3
"""
RL Policy for Research Assistant
Learn which actions maximize reward
"""
import numpy as np
from typing import Dict, List
import json

class ResearchAssistantPolicy:
    """
    Epsilon-greedy policy that learns from rewards
    Explores randomly initially, exploits good actions over time
    """
    
    def __init__(self, learning_rate: float = 0.1, epsilon: float = 0.3):
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        
        # Q-values: action_type -> reward estimate
        self.q_values = {
            "search": 0.8,
            "answer": 0.7,
            "summary": 0.6,
            "gaps": 0.8
        }
        
        # Action counters
        self.action_counts = {k: 0 for k in self.q_values.keys()}
        
    def choose_action(self, observation: Dict, available_actions: List[str] = None) -> Dict:
        """
        Choose next action using epsilon-greedy strategy
        With probability epsilon: explore random action
        With probability 1-epsilon: exploit best action
        """
        if available_actions is None:
            available_actions = list(self.q_values.keys())
        
        # Epsilon-greedy exploration
        if np.random.random() < self.epsilon:
            # Explore: random action
            action_type = np.random.choice(available_actions)
        else:
            # Exploit: best action
            q_vals = {a: self.q_values.get(a, 0) for a in available_actions}
            action_type = max(q_vals, key=q_vals.get)
        
        return {"type": action_type}
    
    def update(self, action_type: str, reward: float):
        """
        Update Q-values based on received reward
        Q(a) ← Q(a) + α * (r - Q(a))
        """
        if action_type in self.q_values:
            old_q = self.q_values[action_type]
            self.q_values[action_type] += self.learning_rate * (reward - old_q)
            self.action_counts[action_type] += 1
            
            # Decay epsilon over time (explore less as we learn)
            self.epsilon = max(0.1, self.epsilon * 0.995)
    
    def get_stats(self) -> Dict:
        """Get policy statistics"""
        return {
            "q_values": self.q_values,
            "action_counts": self.action_counts,
            "epsilon": self.epsilon
        }
    
    def save(self, path: str):
        """Save policy to JSON"""
        data = {
            "q_values": self.q_values,
            "action_counts": self.action_counts,
            "epsilon": self.epsilon
        }
        with open(path, "w") as f:
            json.dump(data, f)
    
    def load(self, path: str):
        """Load policy from JSON"""
        with open(path, "r") as f:
            data = json.load(f)
        self.q_values = data.get("q_values", self.q_values)
        self.action_counts = data.get("action_counts", self.action_counts)
        self.epsilon = data.get("epsilon", self.epsilon)
