"""
Base LLM provider interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMProvider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    async def generate_summary(self, call_id: str, segments: list) -> Dict[str, Any]:
        """
        Generate a summary and action items for a call.
        
        Args:
            call_id: The call identifier
            segments: List of call segments with speaker and text
            
        Returns:
            Dictionary with 'summary' and 'action_items' keys
        """
        pass

