# Design: hyper-v2-baseline

## Architecture
- Base: upstream AdonisJS + React/Inertia + MySQL + Qdrant + Ollama
- Extensions: Claude Agent SDK (Python), Qwen3.5 models, IoT (HA/MQTT), LoRa, SDR, voice, Unsloth
- Docs: LLM wiki (brain/) + OpenSpec (openspec/) + Hyper docs (docs/hyper/)
- CI: GitHub Actions (lint + typecheck + tests)

## Decisions
1. Keep upstream code intact; add modules as overlays
2. Use Apache-2.0 license
3. No authentication (network-level)
4. Multi-language docs (10 locales)
5. OpenSpec for all future changes

## Risks
- Large dependency footprint; mitigated by profiles (minimal/standard/gpu)
- Unsloth requires GPU; fallback to CPU
