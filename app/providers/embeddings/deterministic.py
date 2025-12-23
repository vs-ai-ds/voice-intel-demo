"""Deterministic embeddings provider for Phase 1 (no external calls)."""
import hashlib
import numpy as np
from typing import List
from app.providers.embeddings.base import EmbeddingsProvider

class DeterministicEmbeddingsProvider(EmbeddingsProvider):
    """
    Deterministic embeddings provider for Phase 1.
    
    Generates stable embeddings from text hash.
    Normalizes to unit vectors for cosine similarity.
    """
    
    def __init__(self, dimension: int = 384):
        """
        Initialize provider.
        
        Args:
            dimension: Embedding dimension (default 384 to match KBChunk model)
        """
        self._dimension = dimension
    
    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        return self._dimension
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts."""
        return [self.embed_query(text) for text in texts]
    
    def embed_query(self, text: str) -> List[float]:
        """
        Generate deterministic embedding from text.
        
        Uses SHA256 hash to create stable vector.
        Normalizes to unit vector for cosine similarity.
        """
        # Generate hash
        hash_obj = hashlib.sha256(text.encode('utf-8'))
        hash_bytes = hash_obj.digest()
        
        # Create vector from hash (repeat if needed)
        vector = []
        for i in range(self._dimension):
            # Use hash bytes cyclically
            byte_val = hash_bytes[i % len(hash_bytes)]
            # Normalize to [-1, 1] range
            vector.append((byte_val / 127.5) - 1.0)
        
        # Normalize to unit vector
        vec_array = np.array(vector)
        norm = np.linalg.norm(vec_array)
        if norm > 0:
            vec_array = vec_array / norm
        
        return vec_array.tolist()

