"""Contract tests for KB documents endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.db.models import Tenant, KBDocument
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

def test_create_document_contract(test_tenant):
    """Test POST /api/v1/tenants/{tenant_id}/kb/documents contract."""
    response = client.post(
        f"/api/v1/tenants/{test_tenant.id}/kb/documents",
        json={
            "source_type": "TEXT",
            "title": "Returns Policy",
            "tags": ["policy", "returns"],
            "content": "Returns accepted within 7 days with invoice. Items must be unused and in original packaging."
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify envelope
    assert data["ok"] is True
    assert "data" in data
    assert "meta" in data
    
    # Verify response structure
    doc_data = data["data"]
    assert "document_id" in doc_data
    assert "status" in doc_data
    assert doc_data["status"] == "INGESTED"
    assert "chunks_created" in doc_data
    assert isinstance(doc_data["chunks_created"], int)
    assert doc_data["chunks_created"] > 0

def test_list_documents_contract(test_tenant, db):
    """Test GET /api/v1/tenants/{tenant_id}/kb/documents contract."""
    # Create a document first
    from app.db.models import KBDocument
    doc = KBDocument(
        id=uuid.uuid4(),
        tenant_id=test_tenant.id,
        source_type="TEXT",
        title="Test Document",
        content="Test content",
        status="INGESTED"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    response = client.get(f"/api/v1/tenants/{test_tenant.id}/kb/documents?page=1&page_size=25")
    assert response.status_code == 200
    data = response.json()
    
    assert data["ok"] is True
    assert isinstance(data["data"], list)
    
    # Verify pagination meta
    meta = data["meta"]
    assert "page" in meta
    assert "page_size" in meta
    assert "total" in meta
    assert "has_more" in meta
    
    # Verify document structure
    if data["data"]:
        doc_item = data["data"][0]
        assert "document_id" in doc_item
        assert "title" in doc_item
        assert "source_type" in doc_item
        assert "tags" in doc_item
        assert "status" in doc_item
        assert "created_at" in doc_item

