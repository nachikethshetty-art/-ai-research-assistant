#!/usr/bin/env python3
"""
n8n Workflow Integration
Trigger n8n automation workflows for research pipelines
"""

import requests
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

class N8NWebhook:
    """n8n Webhook Integration"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        """Initialize with n8n webhook URL"""
        self.webhook_url = webhook_url or os.getenv("N8N_WEBHOOK_URL", "")
        self.enabled = bool(self.webhook_url)
        self.history = []
    
    def trigger_research_pipeline(self, query: str, papers: list) -> Dict[str, Any]:
        """Trigger n8n workflow for research analysis"""
        if not self.enabled:
            return {"success": False, "error": "n8n webhook not configured"}
        
        payload = {
            "action": "research_analysis",
            "query": query,
            "papers_count": len(papers),
            "papers": papers,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            result = {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "timestamp": datetime.now().isoformat(),
                "query": query
            }
            
            self.history.append(result)
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def trigger_analytics_update(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger n8n workflow for analytics update"""
        if not self.enabled:
            return {"success": False, "error": "n8n webhook not configured"}
        
        payload = {
            "action": "analytics_update",
            "data": analytics_data,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code
            }
        except:
            return {"success": False, "error": "Failed to trigger workflow"}
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get n8n workflow status"""
        return {
            "enabled": self.enabled,
            "webhook_configured": bool(self.webhook_url),
            "total_triggers": len(self.history),
            "last_trigger": self.history[-1]["timestamp"] if self.history else None
        }
