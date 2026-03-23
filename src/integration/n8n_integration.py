#!/usr/bin/env python3
"""
n8n Integration for Research Pipeline Automation
Connects to n8n webhooks to automate workflows
"""
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

class N8nIntegration:
    """
    Integrate with n8n for automated research workflows
    - Trigger paper fetching workflows
    - Schedule periodic analysis
    - Send results to downstream systems
    """
    
    def __init__(self, webhook_url: str = "http://localhost:5678/webhook/research"):
        self.webhook_url = webhook_url
        self.workflow_history = []
    
    def trigger_workflow(
        self,
        workflow_name: str,
        parameters: Dict,
        wait_for_response: bool = False
    ) -> Optional[Dict]:
        """
        Trigger an n8n workflow via webhook
        
        Args:
            workflow_name: Name of n8n workflow
            parameters: Input parameters for workflow
            wait_for_response: Wait for workflow completion
        
        Returns:
            Workflow result or None if async
        """
        payload = {
            "workflow_name": workflow_name,
            "timestamp": datetime.now().isoformat(),
            "parameters": parameters
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=30
            )
            
            result = response.json() if response.status_code == 200 else None
            
            self.workflow_history.append({
                "workflow": workflow_name,
                "status": "success" if response.status_code == 200 else "failed",
                "timestamp": datetime.now().isoformat()
            })
            
            return result
            
        except requests.exceptions.RequestException as e:
            self.workflow_history.append({
                "workflow": workflow_name,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return None
    
    def fetch_papers_workflow(
        self,
        query: str,
        sources: List[str] = None,
        limit: int = 10
    ) -> Optional[List[Dict]]:
        """Trigger paper fetching workflow in n8n"""
        if sources is None:
            sources = ["arxiv", "semantic_scholar"]
        
        return self.trigger_workflow(
            "fetch_research_papers",
            {
                "query": query,
                "sources": sources,
                "limit": limit
            }
        )
    
    def analyze_papers_workflow(self, papers: List[Dict]) -> Optional[Dict]:
        """Trigger paper analysis workflow in n8n"""
        return self.trigger_workflow(
            "analyze_papers",
            {"papers": papers}
        )
    
    def generate_report_workflow(
        self,
        query: str,
        papers: List[Dict],
        analysis: Dict
    ) -> Optional[str]:
        """Trigger report generation workflow in n8n"""
        return self.trigger_workflow(
            "generate_report",
            {
                "query": query,
                "papers": papers,
                "analysis": analysis
            }
        )
    
    def get_workflow_history(self) -> List[Dict]:
        """Get history of triggered workflows"""
        return self.workflow_history
    
    def health_check(self) -> bool:
        """Check if n8n is accessible"""
        try:
            response = requests.get(
                self.webhook_url.rsplit("/", 1)[0] + "/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
