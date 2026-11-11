---
id: model-updates
title: Model Updates (Nov 2026)
summary: Latest model and tool updates as of Nov 2026: Ollama 0.40.15, Qwen3.6/3.8, Unsloth Desktop, DeepSeek V4 distilled, MLX support.
tags: [models, updates, ollama, unsloth]
entities: [Ollama, Qwen3.6, Qwen3.8, Unsloth Desktop, DeepSeek]
claims: []
sources: [https://ollama.com, https://unsloth.ai]
updated: 2026-11-11
---

# Model Updates (Nov 2026)

## Ollama 0.40.15 (3 Nov 2026)
- MLX support on Apple Silicon (qwen3.5, qwen3.6, qwen3.8, gemma4)
- Qwen3.8: 27B experimental (Qwen4 architecture preview)
- Qwen3.6: 27B/35B agentic coding
- DeepSeek V4 Flash distilled into Qwen3.5-9B
- pplx-decider: 27B decision model on Qwen3.8
- Decision models on /v1/systemone endpoint

## Unsloth (Nov 2026)
- Unsloth Desktop app (Windows/macOS/Linux)
- Qwen3.8-Flash-Next Dynamic V3.1 GGUFs
- GRPO, DPO, FP8 training
- AMD GPU support (Windows/WSL/Linux)
- ARM64 Windows CUDA
- OpenAI-compatible inference endpoint
- `unsloth start --as-subagent` for Claude Code/Codex/OpenCode
- Image LoRA training with aspect-ratio buckets
- LTX-2.5 + Wan2.2 video generation

## Implications for NOMAD Hyper
- Use Qwen3.6 for agentic coding tasks
- Use Unsloth Desktop as local training backend on 4GB GPU
- MLX enables Apple Silicon deployments
- Decision models for routing/agent decisions
