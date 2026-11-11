---
id: unsloth-backend
title: Unsloth Desktop Backend
summary: Unsloth Desktop as local training backend + OpenAI-compatible inference endpoint for NOMAD Hyper.
tags: [unsloth, training, backend, openai-api]
entities: [Unsloth Desktop, OpenAI-compatible API]
claims: []
sources: [https://unsloth.ai/docs/new/studio, https://unsloth.ai/docs/desktop]
updated: 2026-11-11
---

# Unsloth Desktop Backend

## Overview
Unsloth Desktop provides:
- Local training (LoRA, QLoRA, full fine-tune) on 4GB+ GPU
- OpenAI-compatible inference endpoint
- `unsloth start --as-subagent` for delegating tasks to local models
- No telemetry, sandbox, hash verification
- FP8 LoRA, MLX support, AMD GPU support

## Integration Points

### 1. Training Backend
- FastAPI wrapper in `agents/training_api.py`
- Submit jobs: POST /api/train { domain, model, epochs, lr }
- Check status: GET /api/train/{job_id}
- Download adapter: GET /api/train/{job_id}/adapter

### 2. Inference Backend (OpenAI-compatible)
- Unsloth Desktop runs on http://localhost:8000 (default)
- NOMAD agents point to it as OPENAI_BASE_URL
- No API key needed for local

### 3. Agent Integration
- Unsloth Desktop can run `--as-subagent` for Claude Code / Codex / OpenCode
- NOMAD orchestrator spawns sub-agents that use local Unsloth inference

## Configuration
```yaml
# docker-compose.v2.yml (profile: training)
services:
  nomad-unsloth:
    image: unsloth/unsloth-studio:latest
    container_name: nomad-unsloth
    ports:
      - "8000:8000"
    volumes:
      - ./data/unsloth:/data
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped
    profiles: [training]
```

## OpenAI-Compatible Endpoint
- Base URL: http://localhost:8000/v1
- Model: unsloth/qwen3.5-4b
- No auth for local

## Roadmap
- [x] Add Unsloth Desktop docs
- [x] Add training script skeleton (`scripts/train_lora.py`)
- [ ] Add FastAPI training API (`agents/training_api.py`)
- [ ] Add docker-compose profile for Unsloth
- [ ] Integrate with NOMAD agents
- [ ] Test on 4GB GPU