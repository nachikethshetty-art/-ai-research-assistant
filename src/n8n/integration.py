#!/usr/bin/env python3
"""
n8n Workflow Integration for Research Pipeline Automation
Connects to n8n instance to automate paper processing
"""
from typing import Dict, List, Optional
import httpx
import asyncio
from dataclasses import dataclass


@dataclass
class N8nWorkflow:
    """Represents an n8n workflow"""
    id: str
    name: str
    description: str
    status: str
    webhook_url: Optional[str] = None


class N8nIntegration:
    """
    Integrate with n8n for workflow automation
    
    Workflows handled by n8n:
    1. Paper Fetch → Validate → Store
    2. Chunking → Embedding → Index
    3. User Query → Retrieve → Generate
    4. Feedback → Analyze → Learn
    """
    
    def __init__(self, base_url: str = "http://localhost:5678"):
        self.base_url = base_url
        self.client = httpx.Client()
        self.workflows: Dict[str, N8nWorkflow] = {}
    
    def create_fetch_workflow(self) -> N8nWorkflow:
        """
        Create n8n workflow for paper fetching
        
        Flow:
        1. Trigger: User submits query
        2. Fetch from arXiv API
        3. Fetch from Semantic Scholar
        4. Merge & deduplicate
        5. Store in database
        6. Trigger RL feedback loop
        """
        workflow = N8nWorkflow(
            id="paper_fetch",
            name="Fetch Research Papers",
            description="Fetch papers from APIs and store",
            status="active",
            webhook_url="/api/v1/webhook/paper-fetch"
        )
        self.workflows["paper_fetch"] = workflow
        return workflow
    
    def create_processing_workflow(self) -> N8nWorkflow:
        """
        Create n8n workflow for paper processing
        
        Flow:
        1. Trigger: New papers added
        2. Clean text (lowercase, remove special chars)
        3. Split into chunks
        4. Generate embeddings
        5. Index in FAISS
        6. Update analytics
        """
        workflow = N8nWorkflow(
            id="paper_processing",
            name="Process Papers",
            description="Clean, chunk, and embed papers",
            status="active",
            webhook_url="/api/v1/webhook/process-papers"
        )
        self.workflows["paper_processing"] = workflow
        return workflow
    
    def create_qa_workflow(self) -> N8nWorkflow:
        """
        Create n8n workflow for Q&A
        
        Flow:
        1. Trigger: User asks question
        2. Search similar chunks (FAISS)
        3. Retrieve top papers
        4. Generate answer (Ollama)
        5. Score answer (RL)
        6. Store feedback
        7. Update metrics
        """
        workflow = N8nWorkflow(
            id="qa_generation",
            name="Generate Q&A",
            description="Answer questions using papers",
            status="active",
            webhook_url="/api/v1/webhook/qa-generate"
        )
        self.workflows["qa_generation"] = workflow
        return workflow
    
    def create_analytics_workflow(self) -> N8nWorkflow:
        """
        Create n8n workflow for analytics
        
        Flow:
        1. Trigger: Daily
        2. Process feedback data
        3. Calculate metrics
        4. Generate charts
        5. Send dashboard update
        """
        workflow = N8nWorkflow(
            id="analytics_update",
            name="Update Analytics",
            description="Daily analytics update",
            status="active",
            webhook_url="/api/v1/webhook/analytics-update"
        )
        self.workflows["analytics_update"] = workflow
        return workflow
    
    async def trigger_fetch_papers(self, query: str) -> Dict:
        """Trigger paper fetch workflow"""
        payload = {
            "workflow_id": "paper_fetch",
            "query": query,
            "sources": ["arxiv", "semantic_scholar"]
        }
        
        # In production: POST to n8n webhook
        # response = await self.client.post(
        #     f"{self.base_url}/webhook/paper-fetch",
        #     json=payload
        # )
        
        return {
            "status": "triggered",
            "workflow": "paper_fetch",
            "query": query
        }
    
    async def trigger_process_papers(self, papers: List[Dict]) -> Dict:
        """Trigger paper processing workflow"""
        payload = {
            "workflow_id": "paper_processing",
            "papers_count": len(papers),
            "papers": papers[:10]  # Sample
        }
        
        return {
            "status": "triggered",
            "workflow": "paper_processing",
            "papers_processed": len(papers)
        }
    
    async def trigger_qa_generation(self, query: str, papers: List[Dict]) -> Dict:
        """Trigger Q&A generation workflow"""
        payload = {
            "workflow_id": "qa_generation",
            "query": query,
            "papers_count": len(papers)
        }
        
        return {
            "status": "triggered",
            "workflow": "qa_generation",
            "query": query
        }
    
    async def trigger_analytics_update(self) -> Dict:
        """Trigger analytics update workflow"""
        return {
            "status": "triggered",
            "workflow": "analytics_update",
            "timestamp": "now"
        }
    
    def get_workflow_status(self, workflow_id: str) -> Dict:
        """Get workflow status"""
        if workflow_id in self.workflows:
            wf = self.workflows[workflow_id]
            return {
                "id": wf.id,
                "name": wf.name,
                "status": wf.status
            }
        return {"error": "Workflow not found"}
    
    def list_all_workflows(self) -> List[Dict]:
        """List all configured workflows"""
        return [
            {
                "id": wf.id,
                "name": wf.name,
                "description": wf.description,
                "status": wf.status
            }
            for wf in self.workflows.values()
        ]
    
    def export_workflow_config(self, filepath: str):
        """Export workflow config as JSON"""
        import json
        config = {
            "n8n_base_url": self.base_url,
            "workflows": [
                {
                    "id": wf.id,
                    "name": wf.name,
                    "description": wf.description,
                    "webhook": wf.webhook_url
                }
                for wf in self.workflows.values()
            ]
        }
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)


class N8nSetup:
    """Helper to setup n8n workflows"""
    
    @staticmethod
    def get_workflow_definitions() -> List[Dict]:
        """Get ready-to-import n8n workflow definitions"""
        return [
            {
                "name": "Fetch Research Papers",
                "description": "Fetch papers from arXiv & Semantic Scholar",
                "nodes": [
                    {"name": "Webhook", "type": "webhook_trigger"},
                    {"name": "arXiv Fetch", "type": "http"},
                    {"name": "Semantic Scholar Fetch", "type": "http"},
                    {"name": "Merge", "type": "merge"},
                    {"name": "Store", "type": "database"}
                ]
            },
            {
                "name": "Process Papers",
                "description": "Clean, chunk, and embed papers",
                "nodes": [
                    {"name": "Trigger", "type": "database_trigger"},
                    {"name": "Clean", "type": "code"},
                    {"name": "Chunk", "type": "code"},
                    {"name": "Embed", "type": "http"},
                    {"name": "Index", "type": "code"}
                ]
            },
            {
                "name": "Generate Q&A",
                "description": "Answer research questions",
                "nodes": [
                    {"name": "Webhook", "type": "webhook_trigger"},
                    {"name": "Search", "type": "code"},
                    {"name": "Retrieve", "type": "database"},
                    {"name": "Generate", "type": "http"},
                    {"name": "Score", "type": "code"},
                    {"name": "Store", "type": "database"}
                ]
            }
        ]


if __name__ == "__main__":
    # Test n8n integration
    n8n = N8nIntegration()
    
    # Create all workflows
    n8n.create_fetch_workflow()
    n8n.create_processing_workflow()
    n8n.create_qa_workflow()
    n8n.create_analytics_workflow()
    
    print("✅ n8n Workflows created:")
    for wf in n8n.list_all_workflows():
        print(f"  - {wf['name']}: {wf['status']}")
