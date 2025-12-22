# Voice Intelligence Platform — SPEC

## Goal
Deployed, streaming-first demo for e-commerce support calls:
live transcript (simulated), saved calls, summaries, and search.

## Phase 1 scope (today)
- Simulated streaming call generator
- Store call + segments in Postgres
- End call -> summary + action items
- Call list + call detail pages
- Simple search (keyword). Vector search in next iteration.

## Providers (must be swappable)
- LLMProvider (summary)
- StorageProvider (future: audio blobs)
- VectorStore (later: embeddings)

## Entities
Call(id, started_at, ended_at, scenario, language, summary_json)
Segment(id, call_id, t_ms, speaker, text)

## Quality
- Always-on demo URL
- Deterministic demo scenarios
