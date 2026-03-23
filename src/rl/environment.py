#!/usr/bin/env python3
"""
OpenEnv-style RL Environment for Research Assistant
Observe → Act → Reward → Repeat
"""
import json
import uuid
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random

class ActionType(Enum):
    SEARCH = "search"
    ANSWER_QUESTION = "answer"
    GENERATE_SUMMARY = "summary"
    FIND_GAPS = "gaps"

class ResearchAssistantEnv:
    """
    RL Environment for Research Assistant
    State: {query, papers, context}
    Action: {type, parameters}
    Reward: relevance + accuracy + speed
    """
    
    def __init__(self):
        self.episode_id = str(uuid.uuid4())
        self.step_count = 0
        self.max_steps = 10
        self.query = ""
        self.papers = []
        self.context = ""
        self.done = False
        self.cumulative_reward = 0.0
        self.action_history = []
        
    def reset(self, query: str = "", papers: List[Dict] = None, **kwargs):
        """Reset environment for new episode"""
        self.episode_id = str(uuid.uuid4())
        self.step_count = 0
        self.query = query
        self.papers = papers or []
        self.context = ""
        self.done = False
        self.cumulative_reward = 0.0
        self.action_history = []
        
        return self.get_observation()
    
    def get_observation(self) -> Dict:
        """Get current state observation"""
        return {
            "episode_id": self.episode_id,
            "step": self.step_count,
            "query": self.query,
            "num_papers": len(self.papers),
            "context_length": len(self.context),
            "done": self.done,
            "cumulative_reward": self.cumulative_reward
        }
    
    def step(self, action: Dict) -> Tuple[Dict, float, bool, Dict]:
        """
        Take action in environment
        Returns: observation, reward, done, info
        """
        self.step_count += 1
        action_type = action.get("type", ActionType.SEARCH.value)
        
        # Calculate reward based on action quality
        reward = self._calculate_reward(action)
        self.cumulative_reward += reward
        
        # Store action in history
        self.action_history.append({
            "step": self.step_count,
            "action": action_type,
            "reward": reward
        })
        
        # Check termination
        if self.step_count >= self.max_steps:
            self.done = True
        
        if action_type == ActionType.SEARCH.value and not self.papers:
            self.done = True
        
        info = {
            "action_type": action_type,
            "action_history": self.action_history,
            "cumulative_reward": self.cumulative_reward
        }
        
        return self.get_observation(), reward, self.done, info
    
    def _calculate_reward(self, action: Dict) -> float:
        """
        Reward function for RL
        - Search success: +1.0
        - Good answer: +0.8
        - Summary quality: +0.7
        - Gap finding: +0.9
        - Timeout/failure: -0.5
        """
        action_type = action.get("type", "")
        
        if action_type == ActionType.SEARCH.value:
            papers = action.get("papers", [])
            reward = min(1.0, len(papers) / 5.0)  # Reward for finding papers
        
        elif action_type == ActionType.ANSWER_QUESTION.value:
            answer = action.get("answer", "")
            confidence = action.get("confidence", 0.5)
            reward = 0.8 * (len(answer) > 50) * confidence  # Reward for good answers
        
        elif action_type == ActionType.GENERATE_SUMMARY.value:
            summary = action.get("summary", "")
            reward = 0.7 * (len(summary) > 100)  # Reward for summaries
        
        elif action_type == ActionType.FIND_GAPS.value:
            gaps = action.get("gaps", [])
            reward = 0.9 * (len(gaps) > 0)  # Reward for finding gaps
        
        else:
            reward = -0.5  # Penalty for unknown actions
        
        return max(-1.0, min(1.0, reward))  # Clamp to [-1, 1]
    
    @property
    def state(self) -> Dict:
        """Get episode metadata"""
        return {
            "episode_id": self.episode_id,
            "step_count": self.step_count,
            "cumulative_reward": self.cumulative_reward,
            "done": self.done,
            "action_count": len(self.action_history)
        }


@dataclass
class RLAction:
    """RL Action: Query and Expected Answer"""
    query: str
    answer: str


@dataclass
class RLObservation:
    """RL Observation: Query State"""
    query: str
    papers_retrieved: int
    context_quality: float
    done: bool
    reward: Optional[float] = None


class ResearchPaperEnvironment(gym.Env):
    """
    OpenEnv-style RL Environment for Research Paper Q&A.
    
    Agent learns to:
    - Formulate better queries
    - Select relevant papers
    - Generate accurate answers
    
    Reward signals:
    - ✅ Correct answer: +1.0
    - ✅ Partial match: +0.5
    - ❌ Incorrect: -0.5
    - ❌ No papers: -0.3
    """
    
    def __init__(self, papers_db, max_steps=5):
        super().__init__()
        self.papers_db = papers_db
        self.max_steps = max_steps
        self.current_step = 0
        self.current_query = None
        self.retrieved_papers = []
        self.episode_reward = 0.0
        
        # Action space: query refinement (discrete)
        self.action_space = spaces.Discrete(10)
        
        # Observation space: query embedding + paper count
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(384,), dtype=np.float32
        )
    
    def reset(self, seed=None, options=None):
        """Reset environment"""
        super().reset(seed=seed)
        self.current_step = 0
        self.episode_reward = 0.0
        self.current_query = None
        self.retrieved_papers = []
        
        obs = self._get_observation()
        return obs, {}
    
    def step(self, action):
        """Execute action and return next observation"""
        self.current_step += 1
        
        # Action: refine query
        query_refinements = [
            "Add more keywords",
            "Focus on recent papers",
            "Look for high citations",
            "Search author papers",
            "Expand to related topics",
            "Filter by year",
            "Search exact phrase",
            "Include synonyms",
            "Cross-reference topics",
            "Deep dive"
        ]
        
        refinement = query_refinements[action] if action < len(query_refinements) else ""
        
        # Simulate reward based on action
        if action in [2, 3]:  # Citations or author search
            reward = 0.8  # High quality
        elif action in [0, 1]:  # Keywords or recent
            reward = 0.6  # Medium quality
        else:
            reward = 0.4  # Lower quality
        
        self.episode_reward += reward
        
        done = self.current_step >= self.max_steps
        
        obs = self._get_observation()
        
        return obs, reward, done, False, {"step": self.current_step}
    
    def _get_observation(self):
        """Get current observation"""
        # Simulate embedding (all zeros for now)
        return np.zeros(384, dtype=np.float32)
    
    def set_papers(self, papers):
        """Set papers database"""
        self.papers_db = papers
        self.retrieved_papers = papers[:5]  # Top 5 papers


# RL Policy for Research Q&A
class ResearchPolicy:
    """
    Policy that learns to answer research questions.
    
    Observe: Query + Papers
    Act: Generate answer
    Reward: Correctness score
    Learn: Improve generation
    """
    
    def __init__(self, model=None):
        self.model = model
        self.experience_buffer = []
    
    def choose_action(self, observation, papers):
        """Choose best action given observation"""
        # Simple heuristic: prefer high-citation papers
        ranked_papers = sorted(
            papers,
            key=lambda p: p.get('citations', 0),
            reverse=True
        )
        return ranked_papers[:3]  # Top 3 papers
    
    def learn(self, experiences):
        """Learn from experiences"""
        for exp in experiences:
            self.experience_buffer.append(exp)
            # Update policy based on reward
    
    def generate_answer(self, query, papers):
        """Generate answer using policy"""
        if not papers:
            return "No papers found to answer this question."
        
        # Simple template-based generation for now
        top_paper = papers[0]
        return (
            f"Based on {len(papers)} research papers:\n\n"
            f"**Key Finding:** {top_paper.get('title', 'Research finding')}\n\n"
            f"**Answer:** {top_paper.get('abstract', 'See paper for details')[:200]}..."
        )


if __name__ == "__main__":
    # Test environment
    env = ResearchPaperEnvironment(papers_db=[])
    obs, info = env.reset()
    print(f"✅ Environment initialized")
    print(f"Observation shape: {obs.shape}")
    
    for _ in range(3):
        action = env.action_space.sample()
        obs, reward, done, truncated, info = env.step(action)
        print(f"Action: {action}, Reward: {reward}, Done: {done}")
