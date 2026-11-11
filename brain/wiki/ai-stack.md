---
id: ai-stack
title: AI Stack
summary: AI stack uses Qwen3.5 models via Ollama, Claude Agent SDK for agents/sub-agents, Qdrant for RAG, nomic-embed-text for embeddings, Whisper+Piper for voice, Unsloth for LoRA training.
tags: [ai, qwen, claude-agent-sdk, rag, unsloth]
entities: [Qwen3.5, Ollama, Claude Agent SDK, Qdrant, Unsloth]
claims: []
sources: [docs/hyper/hyperspec.md]
updated: 2026-11-11
---

# AI Stack

## Models
- qwen3.5:0.8b / 2b / 4b / 9b / 27b / 35b-a3b / 122b-a10b / 397b-a17b
- Embedding: nomic-embed-text (768 dim), mxbai-embed-large

## Agent layer
- Claude Agent SDK (Python/TS) orchestrator + 10 sub-agents
- Skills: medical, meshtastic, iot-sensors, zim-search, solar-monitor, nomad-comms

## Voice
- Whisper (STT) + Piper (TTS) via Wyoming protocol

## LoRA training
- Unsloth (local, 4GB GPU + CPU) + cloud parallel
- Internal API for training jobs
