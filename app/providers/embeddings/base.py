"""Embeddings provider interface."""
from abc import ABC, abstractmethod
from typing import List

class EmbeddingsProvider(ABC):
    """Abstract embeddings provider interface."""
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return embedding dimension."""
        pass
    
    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (each is list of floats)
        """
        pass
    
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query text.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector (list of floats)
        """
        pass

