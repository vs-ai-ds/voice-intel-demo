"""Contract tests for KB search endpoint."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.db.models import Tenant, KBDocument, KBChunk
from app.providers.embeddings.deterministic import DeterministicEmbeddingsProvider
import uuid
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def db():
    """Database session fixture."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_tenant(db):
    """Create test tenant."""
    tenant = Tenant(
        id=uuid.uuid4(),
        name="Test Tenant",
        slug="test-tenant",
        timezone="UTC",
        default_language="en-US",
        features={}
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

@pytest.fixture
def test_document_with_chunks(db, test_tenant):
    """Create test document with chunks."""
    doc = KBDocument(
        id=uuid.uuid4(),
        tenant_id=test_tenant.id,
        source_type="TEXT",
        title="Returns Policy",
        content="Returns accepted within 7 days with invoice.",
        tags=["policy", "returns"],
        status="INGESTED"
    )
    db.add(doc)
    db.flush()
    
    # Create chunks with embeddings
    provider = DeterministicEmbeddingsProvider()
    chunk_texts = [
        "Returns accepted within 7 days with invoice.",
        "Items must be unused and in original packaging.",
        "Refunds processed within 5-7 business days."
    ]
    
    for idx, text in enumerate(chunk_texts):
        embedding = provider.embed_query(text)
        chunk = KBChunk(
            id=uuid.uuid4(),
            document_id=doc.id,
            chunk_index=idx,
            text=text,
            embedding=embedding
        )
        db.add(chunk)
    
    db.commit()
    db.refresh(doc)
    return doc

def test_search_contract(test_tenant, test_document_with_chunks):
    """Test POST /api/v1/tenants/{tenant_id}/kb/search contract."""
    response = client.post(
        f"/api/v1/tenants/{test_tenant.id}/kb/search",
        json={
            "query": "How many days for returns?",
            "top_k": 5,
            "filters": {"tags": ["returns"]}
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify envelope
    assert data["ok"] is True
    assert "data" in data
    assert "meta" in data
    
    # Verify response structure
    search_data = data["data"]
    assert "hits" in search_data
    assert isinstance(search_data["hits"], list)
    
    # Verify hit structure
    if search_data["hits"]:
        hit = search_data["hits"][0]
        assert "chunk_id" in hit
        assert "score" in hit
        assert isinstance(hit["score"], (int, float))
        assert hit["score"] >= 0.0 and hit["score"] <= 1.0  # Similarity score
        assert "text" in hit
        assert "document" in hit
        assert "document_id" in hit["document"]
        assert "title" in hit["document"]

def test_search_without_filters(test_tenant, test_document_with_chunks):
    """Test search without filters."""
    response = client.post(
        f"/api/v1/tenants/{test_tenant.id}/kb/search",
        json={
            "query": "returns policy",
            "top_k": 3
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "hits" in data["data"]

