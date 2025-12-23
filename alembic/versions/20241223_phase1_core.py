"""Phase 1 core schema

Revision ID: phase1_core
Revises: 
Create Date: 2024-12-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    # Fallback for environments without pgvector installed
    Vector = None

# revision identifiers, used by Alembic.
revision: str = 'phase1_core'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Tenants
    op.create_table(
        'tenants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), unique=True, nullable=False),
        sa.Column('timezone', sa.String(), default='UTC'),
        sa.Column('default_language', sa.String(), default='en-US'),
        sa.Column('features', postgresql.JSON, default=dict),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),
    )
    
    # Users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('name', sa.String()),
        sa.Column('password_hash', sa.String()),
        sa.Column('roles', postgresql.ARRAY(sa.String()), default=list),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),
    )
    
    # Agents
    op.create_table(
        'agents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('status', sa.String(), default='ACTIVE'),
        sa.Column('languages', postgresql.ARRAY(sa.String()), default=list),
        sa.Column('voice', postgresql.JSON, default=dict),
        sa.Column('stt', postgresql.JSON, default=dict),
        sa.Column('llm', postgresql.JSON, default=dict),
        sa.Column('routing', postgresql.JSON, default=dict),
        sa.Column('policies', postgresql.JSON, default=dict),
        sa.Column('tools_enabled', postgresql.ARRAY(sa.String()), default=list),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),
    )
    op.create_index('idx_agents_tenant_status', 'agents', ['tenant_id', 'status'])
    
    # Calls
    op.create_table(
        'calls',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id'), nullable=True),
        sa.Column('provider', sa.String()),
        sa.Column('provider_call_id', sa.String()),
        sa.Column('from_phone', sa.String()),
        sa.Column('to_phone', sa.String()),
        sa.Column('direction', sa.String()),
        sa.Column('status', sa.String(), default='INITIATED'),
        sa.Column('language', sa.String()),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('ended_at', sa.DateTime()),
        sa.Column('call_metadata', postgresql.JSON, default=dict),
        sa.Column('summary', postgresql.JSON),
        sa.Column('metrics', postgresql.JSON),
        sa.Column('handoff', postgresql.JSON),
    )
    op.create_index('idx_calls_tenant_started', 'calls', ['tenant_id', 'started_at'])
    op.create_index('idx_calls_status', 'calls', ['status'])
    
    # Turns (transcripts)
    op.create_table(
        'turns',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('call_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('calls.id'), nullable=False),
        sa.Column('turn_id', sa.String(), unique=True),
        sa.Column('speaker', sa.String(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('language', sa.String()),
        sa.Column('ts', sa.DateTime(), nullable=False),
        sa.Column('confidence', sa.Float()),
        sa.Column('seq_num', sa.Integer()),
        sa.Column('intent_label', sa.String()),
        sa.Column('sentiment_score', sa.Float()),
        sa.Column('escalation_score', sa.Float()),
        sa.Column('flags', postgresql.JSON, default=dict),
        sa.Column('raw_provider_payload', postgresql.JSON),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_turns_call_seq', 'turns', ['call_id', 'seq_num'])
    op.create_index('idx_turns_intent', 'turns', ['intent_label'])
    
    # Events
    op.create_table(
        'events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('call_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('calls.id'), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('correlation_id', sa.String()),
        sa.Column('payload', postgresql.JSON, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_events_call_created', 'events', ['call_id', 'created_at'])
    op.create_index('idx_events_type', 'events', ['type'])
    
    # KB Documents
    op.create_table(
        'kb_documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('source_type', sa.String()),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('tags', postgresql.ARRAY(sa.String()), default=list),
        sa.Column('content', sa.String()),
        sa.Column('status', sa.String(), default='PENDING'),
        sa.Column('doc_metadata', postgresql.JSON, default=dict),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),
    )
    op.create_index('idx_kb_docs_tenant', 'kb_documents', ['tenant_id'])
    
    # KB Chunks (with embeddings)
    if Vector:
        embedding_col = Vector(384)
    else:
        # Fallback: use ARRAY for non-pgvector environments
        embedding_col = postgresql.ARRAY(sa.Float)
    
    op.create_table(
        'kb_chunks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('kb_documents.id'), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('embedding', embedding_col),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_kb_chunks_doc', 'kb_chunks', ['document_id', 'chunk_index'])
    # Vector index for similarity search (only if pgvector is available)
    if Vector:
        op.execute(
            "CREATE INDEX idx_kb_chunks_embedding ON kb_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
        )
    
    # Embeddings (generic)
    op.create_table(
        'embeddings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('embedding', embedding_col),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_embeddings_entity', 'embeddings', ['entity_type', 'entity_id'])
    # Vector index (only if pgvector is available)
    if Vector:
        op.execute(
            "CREATE INDEX idx_embeddings_vector ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
        )


def downgrade() -> None:
    op.drop_table('embeddings')
    op.drop_table('kb_chunks')
    op.drop_table('kb_documents')
    op.drop_table('events')
    op.drop_table('turns')
    op.drop_table('calls')
    op.drop_table('agents')
    op.drop_table('users')
    op.drop_table('tenants')
    op.execute('DROP EXTENSION IF EXISTS vector')

