"""Unit tests for deterministic embeddings provider."""
import pytest
from app.providers.embeddings.deterministic import DeterministicEmbeddingsProvider

def test_dimension():
    """Test dimension property."""
    provider = DeterministicEmbeddingsProvider(dimension=384)
    assert provider.dimension == 384

def test_embed_query():
    """Test embedding a single query."""
    provider = DeterministicEmbeddingsProvider(dimension=384)
    embedding = provider.embed_query("test text")
    
    assert len(embedding) == 384
    assert all(isinstance(x, float) for x in embedding)

def test_embed_query_deterministic():
    """Test that embeddings are deterministic."""
    provider = DeterministicEmbeddingsProvider(dimension=384)
    embedding1 = provider.embed_query("test text")
    embedding2 = provider.embed_query("test text")
    
    assert embedding1 == embedding2

def test_embed_query_different_texts():
    """Test that different texts produce different embeddings."""
    provider = DeterministicEmbeddingsProvider(dimension=384)
    embedding1 = provider.embed_query("text one")
    embedding2 = provider.embed_query("text two")
    
    assert embedding1 != embedding2

def test_embed_query_normalized():
    """Test that embeddings are normalized (unit vectors)."""
    provider = DeterministicEmbeddingsProvider(dimension=384)
    embedding = provider.embed_query("test text")
    
    # Check unit vector (norm should be ~1.0)
    import math
    norm = math.sqrt(sum(x * x for x in embedding))
    assert abs(norm - 1.0) < 0.01  # Allow small floating point error

def test_embed_texts():
    """Test embedding multiple texts."""
    provider = DeterministicEmbeddingsProvider(dimension=384)
    texts = ["text one", "text two", "text three"]
    embeddings = provider.embed_texts(texts)
    
    assert len(embeddings) == len(texts)
    assert all(len(emb) == 384 for emb in embeddings)
    assert all(isinstance(emb, list) for emb in embeddings)

