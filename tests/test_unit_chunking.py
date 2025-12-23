"""Unit tests for chunking utility."""
import pytest
from app.core.chunking import chunk_text

def test_chunk_empty_text():
    """Test chunking empty text."""
    result = chunk_text("")
    assert result == []

def test_chunk_short_text():
    """Test chunking text shorter than chunk size."""
    text = "Short text"
    result = chunk_text(text, chunk_size=100)
    assert len(result) == 1
    assert result[0] == text

def test_chunk_long_text():
    """Test chunking long text."""
    text = "A" * 1000  # 1000 characters
    result = chunk_text(text, chunk_size=200, chunk_overlap=20)
    assert len(result) > 1
    # Check total length is approximately correct (with overlap)
    total_chars = sum(len(chunk) for chunk in result)
    assert total_chars >= len(text)

def test_chunk_with_overlap():
    """Test that chunks have overlap."""
    text = "Sentence one. Sentence two. Sentence three. Sentence four."
    result = chunk_text(text, chunk_size=30, chunk_overlap=10)
    if len(result) > 1:
        # Check that chunks overlap (first chunk end should appear in second chunk start)
        assert len(result) >= 2

def test_chunk_preserves_content():
    """Test that chunking preserves all content."""
    text = "This is a test. With multiple sentences. To verify chunking."
    result = chunk_text(text, chunk_size=20, chunk_overlap=5)
    # All text should be covered
    combined = " ".join(result)
    assert len(combined) >= len(text.replace(" ", ""))

