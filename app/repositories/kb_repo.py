"""KB repository with pgvector similarity search."""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, text
from uuid import UUID
from app.db.models.kb_document import KBDocument
from app.db.models.kb_chunk import KBChunk

class KBRepository:
    """Repository for KB operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_document(self, document: KBDocument) -> KBDocument:
        """Create KB document."""
        self.db.add(document)
        self.db.flush()
        return document
    
    def get_document_by_tenant(self, tenant_id: UUID, document_id: UUID) -> Optional[KBDocument]:
        """Get document by tenant and document ID (tenant-scoped)."""
        return self.db.query(KBDocument).filter(
            and_(
                KBDocument.id == document_id,
                KBDocument.tenant_id == tenant_id
            )
        ).first()
    
    def list_documents_by_tenant(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[KBDocument], int]:
        """List documents by tenant."""
        query = self.db.query(KBDocument).filter(
            KBDocument.tenant_id == tenant_id
        )
        
        total = query.count()
        documents = query.order_by(KBDocument.created_at.desc()).offset(skip).limit(limit).all()
        
        return documents, total
    
    def create_chunks(self, chunks: List[KBChunk]) -> List[KBChunk]:
        """Create multiple chunks."""
        self.db.add_all(chunks)
        self.db.flush()
        return chunks
    
    def search_similar(
        self,
        tenant_id: UUID,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Optional[dict] = None
    ) -> List[Tuple[KBChunk, float]]:
        """
        Search for similar chunks using pgvector.
        
        Args:
            tenant_id: Tenant ID for scoping
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filters: Optional filters (e.g., {"tags": ["returns"]})
        
        Returns:
            List of (chunk, similarity_score) tuples, ordered by similarity (desc)
        """
        # Build base query with tenant scoping via document
        # Use pgvector's <=> operator for cosine distance via raw SQL
        # Convert embedding list to PostgreSQL array format
        embedding_str = '[' + ','.join(str(x) for x in query_embedding) + ']'
        
        # Build SQL query
        sql_base = """
            SELECT kb_chunks.id, 
                   (kb_chunks.embedding <=> :embedding::vector) as distance
            FROM kb_chunks
            JOIN kb_documents ON kb_chunks.document_id = kb_documents.id
            WHERE kb_documents.tenant_id = :tenant_id
        """
        
        params = {
            "embedding": embedding_str,
            "tenant_id": str(tenant_id)
        }
        
        # Add tag filter if provided
        if filters and "tags" in filters and filters["tags"]:
            tags = filters["tags"]
            sql_base += " AND kb_documents.tags && :tags::text[]"
            params["tags"] = tags
        
        sql_base += " ORDER BY distance LIMIT :top_k"
        params["top_k"] = top_k
        
        # Execute raw SQL
        result = self.db.execute(text(sql_base), params)
        rows = result.fetchall()
        
        # Fetch chunks and build results
        chunks_with_scores = []
        for row in rows:
            chunk_id = row.id
            distance = float(row.distance)
            
            # Get chunk object
            chunk = self.db.query(KBChunk).filter(KBChunk.id == chunk_id).first()
            if chunk:
                # Convert distance to similarity score (higher is better)
                # cosine_distance returns [0, 2], similarity = 1 - distance/2
                similarity = 1.0 - (distance / 2.0)
                chunks_with_scores.append((chunk, similarity))
        
        return chunks_with_scores

