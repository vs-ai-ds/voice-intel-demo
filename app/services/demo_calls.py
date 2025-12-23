"""
Demo call generation service for simulating streaming calls.
"""
import asyncio
from typing import AsyncIterator, Dict, Any
from datetime import datetime

class DemoCallGenerator:
    """Generates deterministic demo call scenarios."""
    
    SCENARIOS = {
        "order_inquiry": {
            "language": "en",
            "segments": [
                {"t_ms": 0, "speaker": "agent", "text": "Hello, thank you for calling. How can I help you today?"},
                {"t_ms": 2000, "speaker": "customer", "text": "Hi, I'd like to check the status of my order #12345."},
                {"t_ms": 5000, "speaker": "agent", "text": "Let me look that up for you. One moment please."},
                {"t_ms": 8000, "speaker": "agent", "text": "I can see your order is currently being processed and should ship tomorrow."},
                {"t_ms": 12000, "speaker": "customer", "text": "Great, thank you so much!"},
                {"t_ms": 14000, "speaker": "agent", "text": "You're welcome! Is there anything else I can help you with?"},
                {"t_ms": 16000, "speaker": "customer", "text": "No, that's all. Have a great day!"},
            ]
        },
        "return_request": {
            "language": "en",
            "segments": [
                {"t_ms": 0, "speaker": "agent", "text": "Good morning, how may I assist you?"},
                {"t_ms": 2000, "speaker": "customer", "text": "I need to return an item I received last week."},
                {"t_ms": 5000, "speaker": "agent", "text": "I'd be happy to help with that. What's the order number?"},
                {"t_ms": 7000, "speaker": "customer", "text": "It's #67890."},
                {"t_ms": 9000, "speaker": "agent", "text": "I've initiated the return process. You'll receive a return label via email."},
                {"t_ms": 12000, "speaker": "customer", "text": "Perfect, thank you!"},
            ]
        }
    }
    
    async def generate_stream(self, scenario: str = "order_inquiry") -> AsyncIterator[Dict[str, Any]]:
        """
        Generate a streaming call simulation.
        
        Args:
            scenario: The scenario name to use
            
        Yields:
            Call segments as they would appear in a real stream
        """
        if scenario not in self.SCENARIOS:
            scenario = "order_inquiry"
        
        call_data = self.SCENARIOS[scenario]
        
        for segment in call_data["segments"]:
            await asyncio.sleep(segment["t_ms"] / 1000.0)  # Convert ms to seconds
            yield {
                "t_ms": segment["t_ms"],
                "speaker": segment["speaker"],
                "text": segment["text"]
            }

