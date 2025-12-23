"""
Mock LLM provider for testing and demos.
"""
from typing import Dict, Any
from app.providers.llm.base import LLMProvider

class MockLLMProvider(LLMProvider):
    """Mock LLM provider that returns deterministic summaries."""
    
    async def generate_summary(self, call_id: str, segments: list) -> Dict[str, Any]:
        """
        Generate a mock summary and action items.
        
        Args:
            call_id: The call identifier
            segments: List of call segments
            
        Returns:
            Dictionary with 'summary' and 'action_items' keys
        """
        # Count segments by speaker
        agent_segments = sum(1 for s in segments if s.get("speaker") == "agent")
        customer_segments = sum(1 for s in segments if s.get("speaker") == "customer")
        
        return {
            "summary": f"Customer inquiry call with {len(segments)} segments. "
                      f"Agent responded {agent_segments} times, customer spoke {customer_segments} times.",
            "action_items": [
                "Follow up on customer request",
                "Update order status if applicable",
                "Send confirmation email"
            ]
        }

