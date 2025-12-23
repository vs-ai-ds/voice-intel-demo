"""KB service for document ingestion and search."""
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models.kb_document import KBDocument
from app.db.models.kb_chunk import KBChunk
from app.repositories.kb_repo import KBRepository
from app.repositories.tenant import TenantRepository
from app.providers.embeddings.base import EmbeddingsProvider
from app.providers.embeddings.deterministic import DeterministicEmbeddingsProvider
from app.core.chunking import chunk_text
from app.core.errors import APIError

class KBService:
    """Service for KB operations."""
    
    def __init__(self, db: Session, embeddings_provider: EmbeddingsProvider = None):
        self.db = db
        self.kb_repo = KBRepository(db)
        self.tenant_repo = TenantRepository(db)
        self.embeddings_provider = embeddings_provider or DeterministicEmbeddingsProvider()
    
    def ingest_document(
        self,
        tenant_id: UUID,
        source_type: str,
        title: str,
        content: str,
        tags: List[str] = None
    ) -> KBDocument:
        """
        Ingest a document: chunk, embed, and store.
        
        Args:
            tenant_id: Tenant ID
            source_type: Source type (TEXT, URL, FILE)
            title: Document title
            content: Document content
            tags: Optional tags
        
        Returns:
            Created document with status INGESTED
        """
        # Verify tenant exists
        tenant = self.tenant_repo.get(tenant_id)
        if not tenant:
            raise APIError(
                code="NOT_FOUND",
                message=f"Tenant {tenant_id} not found",
                status_code=404
            )
        
        # Create document
        document = KBDocument(
            tenant_id=tenant_id,
            source_type=source_type,
            title=title,
            content=content,
            tags=tags or [],
            status="PENDING"
        )
        document = self.kb_repo.create_document(document)
        
        try:
            # Chunk the content
            chunks_text = chunk_text(content or "", chunk_size=500, chunk_overlap=50)
            
            if not chunks_text:
                # Empty content - still mark as ingested
                document.status = "INGESTED"
                self.db.commit()
                return document
            
            # Embed chunks
            embeddings = self.embeddings_provider.embed_texts(chunks_text)
            
            # Create chunk records
            chunks = []
            for idx, (chunk_text, embedding) in enumerate(zip(chunks_text, embeddings)):
                chunk = KBChunk(
                    document_id=document.id,
                    chunk_index=idx,
                    text=chunk_text,
                    embedding=embedding
                )
                chunks.append(chunk)
            
            # Save chunks
            self.kb_repo.create_chunks(chunks)
            
            # Update document status
            document.status = "INGESTED"
            self.db.commit()
            
            return document
            
        except Exception as e:
            # Mark as failed
            document.status = "FAILED"
            self.db.commit()
            raise APIError(
                code="TOOL_EXECUTION_FAILED",
                message=f"Failed to ingest document: {str(e)}",
                status_code=500
            )
    
    def search(
        self,
        tenant_id: UUID,
        query: str,
        top_k: int = 5,
        filters: dict = None
    ) -> List[tuple]:
        """
        Search KB using semantic similarity.
        
        Args:
            tenant_id: Tenant ID
            query: Search query
            top_k: Number of results
            filters: Optional filters
        
        Returns:
            List of (chunk, score) tuples
        """
        # Verify tenant exists
        tenant = self.tenant_repo.get(tenant_id)
        if not tenant:
            raise APIError(
                code="NOT_FOUND",
                message=f"Tenant {tenant_id} not found",
                status_code=404
            )
        
        # Embed query
        query_embedding = self.embeddings_provider.embed_query(query)
        
        # Search
        results = self.kb_repo.search_similar(
            tenant_id=tenant_id,
            query_embedding=query_embedding,
            top_k=top_k,
            filters=filters
        )
        
        return results

