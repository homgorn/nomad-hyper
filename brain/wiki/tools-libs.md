---
id: tools-libs
title: Tools, Libraries, Frameworks
summary: Required tools/libraries/frameworks for NOMAD Hyper: existing stack + new additions for i18n, multi-location, RAG, voice, mesh, etc.
tags: [tools, libraries, frameworks, dependencies]
entities: [AdonisJS, React, Qdrant, Ollama, Unsloth]
claims: []
sources: []
updated: 2026-11-11
---

# Tools, Libraries, Frameworks

## Existing Stack
- **Backend**: AdonisJS 6 (Node.js/TS), Lucid ORM, BullMQ, Redis, MySQL 8
- **Frontend**: React 19, Inertia.js, Vite, Tailwind CSS
- **AI**: Ollama, Qdrant, nomic-embed-text
- **Infra**: Docker, Dockerode, Nginx Proxy Manager

## New Additions Needed

### i18n
- react-i18next, i18next, i18next-http-backend
- i18next-scanner (key extraction)
- LibreTranslate (self-hosted offline fallback)

### Multi-location
- No new libs; use existing KVStore + Location model

### RAG improvements
- T²RAG (triplet-based, graph-free) — research only
- EmbeddingGemma 2 (multimodal embeddings) — when available in Ollama
- MedGemma 4B (medical VLM) — via Ollama

### Voice
- Whisper (STT) — wyoming-whisper Docker
- Piper (TTS) — wyoming-piper Docker
- Wyoming protocol client

### Mesh/Comms
- meshtastic (Python SDK) — already in orchestrator
- MeshCore CLI tools (new)
- RTL-SDR drivers (rtl-sdr-blog)

### Power/IoT
- ESPHome (ESP32 firmware)
- Victron VE.Direct (Python lib)
- JK BMS (batmon-ha)

### Medical
- Hikma Health (Docker)
- MenSung (drug interactions, <10MB)
- Pl@ntNet (plant ID, offline model)

### Security
- Authelia (SSO/MFA)
- Vaultwarden (passwords)
- Restic (backup)

### Build/Dev
- OpenSpec CLI (npm) — installed
- sqlite3 (for LLM wiki DB) — installed
- Python 3.12 (agents, training) — installed

## To Search/Download
- [x] react-i18next (npm) — added to admin/package.json (install pending completion of npm cache)
- [x] Hikma Health (Docker) — added (profile `health`)
- [x] Needle 2 — verified Cactus-Compute/needle2 (Apache-2.0, 45M params, 28MB RAM); use as on-device tool-calling model via `pip install cactus`, not via Ollama
- [x] NoteDiscovery (Docker) — added (profile `notes`), MCP enabled
- [ ] i18next-scanner (npm)
- [ ] LibreTranslate (Docker)
- [ ] wyoming-whisper (Docker)
- [ ] wyoming-piper (Docker)
- [ ] MeshCore tools (GitHub)
- [ ] MenSung (GitHub)
- [ ] Pl@ntNet offline (GitHub)