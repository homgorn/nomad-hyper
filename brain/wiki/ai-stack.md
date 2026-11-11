---
id: ai-stack
title: AI Stack
summary: AI stack uses Qwen3.5/3.6/3.8 models via Ollama, Claude Agent SDK for agents/sub-agents, Qdrant for RAG, nomic-embed-text for embeddings, Whisper+Piper for voice, Unsloth Desktop for LoRA training.
tags: [ai, qwen, claude-agent-sdk, rag, unsloth]
entities: [Qwen3.5, Qwen3.6, Qwen3.8, Ollama, Claude Agent SDK, Qdrant, Unsloth]
claims: []
sources: [docs/hyper/hyperspec.md, https://ollama.com, https://unsloth.ai]
updated: 2026-11-11
---

# AI Stack

## Models (Ollama 0.40.15, Nov 2026)
- qwen3.5: 0.8b / 2b / 4b / 9b / 27b / 35b / 122b (multimodal, 256K ctx)
- qwen3.6: 27b / 35b (agentic coding, thinking preservation)
- qwen3.8: 27b (experimental, Qwen4 architecture preview)
- qwen3.8-flash-next: experimental preview
- DeepSeek V4 Flash distilled variants
- Embedding: nomic-embed-text (768 dim), mxbai-embed-large, qwen3-embedding
- Decision models: pplx-decider (27B), pplx-decider-flash (4B)

## Agent layer
- Claude Agent SDK (Python/TS) orchestrator + sub-agents
- Skills: medical, meshtastic, iot-sensors, zim-search, solar-monitor, nomad-comms
- Unsloth Desktop as local inference backend (--as-subagent)

## Voice
- Whisper (STT) + Piper (TTS) via Wyoming protocol

## LoRA training
- Unsloth Desktop (Windows/macOS/Linux) + CLI
- QLoRA 4-bit on 4GB GPU
- Export: GGUF, FP8, merged 16-bit
- OpenAI-compatible inference endpoint
- Cloud parallel: RunPod / Lambda / Vast.ai
