#!/usr/bin/env python3
"""
Enhanced Analytics Module with Visualizations
Adds charts, metrics, and export functionality for hackathon polish
"""

import json
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

class HackathonAnalytics:
    """Advanced analytics with visualizations for hackathon presentation"""
    
    def __init__(self):
        self.papers_data = []
        self.feedback_data = []
    
    def create_citations_chart(self, papers: List[Dict]) -> go.Figure:
        """Create interactive citation distribution chart"""
        if not papers:
            return go.Figure()
        
        df = pd.DataFrame([
            {
                'title': p.get('title', 'Unknown')[:50],
                'citations': p.get('citations', 0),
                'year': p.get('year', 'N/A')
            }
            for p in papers
        ])
        
        fig = px.bar(
            df.sort_values('citations', ascending=True),
            x='citations',
            y='title',
            title='📊 Citation Impact of Papers',
            labels={'citations': 'Citation Count', 'title': 'Paper'},
            color='citations',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400, showlegend=False)
        return fig
    
    def create_year_distribution(self, papers: List[Dict]) -> go.Figure:
        """Create research publication timeline"""
        if not papers:
            return go.Figure()
        
        years = [p.get('year') for p in papers if p.get('year')]
        if not years:
            return go.Figure()
        
        df = pd.DataFrame({'year': years})
        year_counts = df['year'].value_counts().sort_index()
        
        fig = px.line(
            x=year_counts.index,
            y=year_counts.values,
            title='📈 Research Publication Timeline',
            labels={'x': 'Year', 'y': 'Number of Papers'},
            markers=True
        )
        fig.update_traces(line=dict(color='#FF6B35', width=3))
        fig.update_layout(height=300, showlegend=False)
        return fig
    
    def create_sources_pie(self, papers: List[Dict]) -> go.Figure:
        """Create paper source distribution"""
        if not papers:
            return go.Figure()
        
        sources = {}
        for p in papers:
            source = p.get('source', 'unknown').upper()
            sources[source] = sources.get(source, 0) + 1
        
        fig = px.pie(
            values=list(sources.values()),
            names=list(sources.keys()),
            title='🔍 Paper Sources Distribution'
        )
        fig.update_layout(height=300)
        return fig
    
    def create_feedback_metrics(self, feedback_history: List[Dict]) -> Dict[str, Any]:
        """Calculate key feedback metrics"""
        if not feedback_history:
            return {
                'avg_quality': 0,
                'avg_relevance': 0,
                'avg_speed': 0,
                'trend': 'neutral'
            }
        
        df = pd.DataFrame(feedback_history)
        
        metrics = {
            'avg_quality': round(df['answer_quality'].mean(), 2) if 'answer_quality' in df else 0,
            'avg_relevance': round(df['papers_quality'].mean(), 2) if 'papers_quality' in df else 0,
            'avg_speed': round(df['speed'].mean(), 2) if 'speed' in df else 0,
            'total_feedback': len(feedback_history)
        }
        
        # Determine trend
        if len(feedback_history) > 2:
            recent = df.iloc[-2:]['answer_quality'].mean()
            previous = df.iloc[:-2]['answer_quality'].mean()
            if recent > previous:
                metrics['trend'] = '📈 Improving'
            elif recent < previous:
                metrics['trend'] = '📉 Declining'
            else:
                metrics['trend'] = '➡️ Stable'
        
        return metrics
    
    def create_performance_gauge(self, feedback_history: List[Dict]) -> go.Figure:
        """Create performance gauge chart"""
        if not feedback_history:
            avg_quality = 0
        else:
            df = pd.DataFrame(feedback_history)
            avg_quality = df['answer_quality'].mean() if 'answer_quality' in df else 0
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_quality * 10,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "System Quality Score"},
            delta={'reference': 8},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': "#FF6B35"},
                'steps': [
                    {'range': [0, 3], 'color': "#FEE8C3"},
                    {'range': [3, 6], 'color': "#FDBB84"},
                    {'range': [6, 10], 'color': "#E08214"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 7
                }
            }
        ))
        fig.update_layout(height=300)
        return fig
    
    def generate_text_report(self, query: str, papers: List[Dict], 
                            summary: str, gaps: str, feedback: List[Dict]) -> str:
        """Generate text report for export"""
        
        report = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    AI RESEARCH ASSISTANT - ANALYSIS REPORT                  ║
╚════════════════════════════════════════════════════════════════════════════╝

📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 RESEARCH QUERY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: {query}
Papers Found: {len(papers)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 RESEARCH SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔎 RESEARCH GAPS & OPPORTUNITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{gaps}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 PAPERS ANALYZED ({len(papers)} total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for idx, paper in enumerate(papers, 1):
            report += f"""
{idx}. {paper.get('title', 'Unknown')}
   Authors: {', '.join(paper.get('authors', ['N/A'])[:3])}
   Year: {paper.get('year', 'N/A')}
   Citations: {paper.get('citations', 0)}
   Source: {paper.get('source', 'unknown').upper()}
   URL: {paper.get('url', 'N/A')}
"""
        
        if feedback:
            report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 SYSTEM FEEDBACK METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Feedback Points: {len(feedback)}
Average Paper Quality: {sum(f.get('papers_quality', 0) for f in feedback) / len(feedback):.1f}/10
Average Answer Quality: {sum(f.get('answer_quality', 0) for f in feedback) / len(feedback):.1f}/10
Average Speed Rating: {sum(f.get('speed', 0) for f in feedback) / len(feedback):.1f}/10
"""
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by: AI Research Assistant v3.0
Learn more: https://github.com/amshumathshetty/ai-research-assistant
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return report
