---
id: upstream-gaps
title: Upstream NOMAD — What Exists and What's Missing
summary: Gap analysis of original Project NOMAD v1.35.1: features present vs missing, based on codebase exploration.
tags: [upstream, gaps, nomad]
entities: [Project NOMAD, AdonisJS, Qdrant, Ollama]
claims: []
sources: [H:/susa ai 500/project-nomad-src]
updated: 2026-11-11
---

# Upstream NOMAD — What Exists and What's Missing

## What Exists (v1.35.1)
- Supply Depot: 9 curated apps + custom Docker apps with preflight
- AI Chat: Ollama (streaming, thinking, vision, structured output, response styles)
- RAG: PDF/DOCX/EPUB/images/ZIM ingestion, hybrid search, rerank, diversity
- Kiwix: Wikipedia selector (6 tiers), curated collections, custom libraries
- Maps: ProtoMaps regional extraction, markers CRUD
- Kolibri: education platform
- Benchmark: sysbench + AI tok/s, NOMAD Score v2, leaderboard
- Medical: FDA drug reference, interactions, conditions
- Creator Packs: gated video packs
- Easy Setup Wizard
- Auto-updates: core + apps + content (opt-in, windowed)
- OpenAPI 3.1 + Scalar docs
- In-app Markdoc documentation

## What's Missing (vs hyperspec / survival needs)
- Authentication/authorization (none by design)
- ARM64/Raspberry Pi (x86-64 only)
- Multi-language UI (English only)
- Backup/restore (manual only)
- Cluster/HA (single node)
- Plugin system (Docker apps only)
- Voice I/O (text only)
- Federated search (local KB only)
- PWA/offline-first client (responsive web only)
- Prometheus/Grafana integration
- Content authoring (read-only)
- Mesh/LoRa native (Meshtastic Web only)
- Power management (none)
- Hardware inventory (basic)
- Compliance/audit (none)
- Multi-tenancy RAG
- Graph RAG
- Telemedicine
- Food/water tracking
- Foraging database

## Confidence
- Service/controller/model inventory: 10/10 (direct scan)
- Gap analysis: 7/10 (inferred from FAQ/roadmap/common patterns)
