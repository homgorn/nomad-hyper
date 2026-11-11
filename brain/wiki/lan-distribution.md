---
id: lan-distribution
title: LAN Distribution (Ethernet/WiFi)
summary: Options for running NOMAD Hyper across a local network: distributed model inference, shared storage, mesh, and edge nodes over cable/WiFi.
tags: [lan, distributed, networking, model]
entities: [Ollama, Qdrant, Syncthing, Meshtastic, Starlink]
claims: []
sources: [docs/hyper/hyperspec.md]
updated: 2026-11-11
---

# LAN Distribution (Ethernet/WiFi)

## Goal
Run NOMAD Hyper as a distributed system over local cable/WiFi: split model inference,
share knowledge base, and use edge nodes.

## 1. Distributed Model Inference
- **Ollama multi-host**: set `OLLAMA_HOST=0.0.0.0` on GPU node; other nodes point `OLLAMA_HOST` to it.
- **LiteLLM proxy**: route requests to multiple backends (local GPU + cloud + CPU node) with fallback.
- **Unsloth Desktop**: OpenAI-compatible endpoint on a separate machine; NOMAD uses it as backend.
- **Model sharding**: large models (70B+) split across nodes via llama.cpp RPC (experimental).
- **Edge inference**: small models (0.8b/2b) on RPi/phone; heavy models on GPU server.

## 2. Shared Knowledge Base (Qdrant)
- Qdrant supports distributed mode (sharding + replication) over LAN.
- Alternative: single Qdrant node with Syncthing for ZIM/model sync across nodes.
- RAG service can query remote Qdrant via `QDRANT_HOST`.

## 3. Storage & Sync
- **Syncthing**: P2P sync of ZIM, models, configs across NOMAD nodes (LAN, no internet).
- **NFS/SMB share**: central NAS for ZIM libraries, all nodes mount read-only.
- **Nextcloud**: file sharing + office in LAN.

## 4. Networking Options
- **Ethernet (Gigabit)**: best for model transfer and Qdrant queries.
- **WiFi 6/6E**: good for 2-5 nodes; avoid for large model pulls.
- **Mesh (Meshtastic LoRa)**: for field nodes without LAN; low bandwidth, text only.
- **Starlink/Iridium**: for remote sync between NOMAD clusters.

## 5. Edge/Field Nodes
- RPi5 (8GB) running qwen3.5:4b (CPU) + Kiwix + OsmAnd.
- Sync with main node via Syncthing when in range.
- Meshtastic for comms when out of range.

## 6. Load Balancing
- Nginx Proxy Manager in front of multiple NOMAD instances.
- Round-robin or least-connections.
- Health checks via /v1/health.

## Roadmap
- [ ] Add Ollama multi-host config to docker-compose.v2.yml
- [ ] Add LiteLLM service to stack
- [ ] Add Qdrant distributed mode docs
- [ ] Add Syncthing auto-config for NOMAD nodes
- [ ] Add edge node profile (minimal, RPi)
- [ ] Add LAN discovery (mDNS/Avahi)
