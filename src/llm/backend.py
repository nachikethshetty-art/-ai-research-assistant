#!/usr/bin/env python3
"""
LLM Backend Abstraction Layer
Supports: Ollama (local) + Google Gemini (fallback)
"""

import os
import json
import requests
from typing import Generator, Optional

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class LLMBackend:
    """Unified LLM interface with Ollama/Gemini fallback"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "mistral"
        self.ollama_available = self._check_ollama()
        self.gemini_available = GEMINI_AVAILABLE and self._check_gemini()
        
    def _check_ollama(self) -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(
                f"{self.ollama_url}/api/tags",
                timeout=3
            )
            return response.status_code == 200
        except:
            return False
    
    def _check_gemini(self) -> bool:
        """Check if Gemini API key is configured"""
        api_key = os.getenv("GOOGLE_API_KEY")
        return bool(api_key)
    
    def generate_stream(self, prompt: str, max_tokens: int = 1000) -> Generator[str, None, None]:
        """Generate text with streaming - tries Ollama first, then Gemini"""
        
        # Try Ollama first (local, fast, private)
        if self.ollama_available:
            yield from self._ollama_generate(prompt, max_tokens)
            return
        
        # Fallback to Gemini API
        if self.gemini_available:
            yield from self._gemini_generate(prompt, max_tokens)
            return
        
        # If both fail, return cached/fallback response
        yield f"⚠️ LLM unavailable. Configure GOOGLE_API_KEY for Gemini or run Ollama locally.\n\nPrompt: {prompt[:100]}..."
    
    def _ollama_generate(self, prompt: str, max_tokens: int) -> Generator[str, None, None]:
        """Generate using Ollama"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "temperature": 0.7,
                "num_predict": max_tokens
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60,
                stream=True
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "response" in data:
                            yield data["response"]
        except Exception as e:
            yield f"❌ Ollama error: {str(e)}"
    
    def _gemini_generate(self, prompt: str, max_tokens: int) -> Generator[str, None, None]:
        """Generate using Google Gemini API via REST"""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            
            # Use REST API directly for better compatibility
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    text = data["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    # Stream in chunks
                    for chunk in text.split(' '):
                        if chunk:
                            yield chunk + ' '
            else:
                yield f"❌ Gemini API error: {response.status_code} - {response.text}"
                    
        except Exception as e:
            yield f"❌ Gemini error: {str(e)}"
    
    def get_status(self) -> dict:
        """Get current backend status"""
        return {
            "ollama": self.ollama_available,
            "gemini": self.gemini_available,
            "active_backend": "ollama" if self.ollama_available else ("gemini" if self.gemini_available else "unavailable")
        }
