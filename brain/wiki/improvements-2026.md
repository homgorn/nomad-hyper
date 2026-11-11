---
id: improvements-2026
title: Improvements Research (Nov 2026)
summary: Deep research findings: Survival LLM competitor, Qwen3.8-Flash-Next, Unsloth Desktop, Meshtastic 2.8/MeshCore 1.18, Hikma Health, AFFiNE, NoteDiscovery, Needle 2.
tags: [research, improvements, 2026]
entities: [Survival LLM, Qwen3.8-Flash-Next, Unsloth Desktop, Hikma Health, AFFiNE, NoteDiscovery, Needle 2]
claims: []
sources: [brain/research/nomad-hyper-improvements-2026/]
updated: 2026-11-11
---

# Improvements Research (Nov 2026)

## Key Findings
1. **Survival LLM** (brangus.io, MIT) — competitor. Sources: Wikipedia, WikiMed, MedlinePlus, UK Medicines A-Z, WikEM, Ready.gov, CDC, military manuals, wikiHow, iFixit, Appropedia, Stack Exchange. → Integrate these sources.
2. **Qwen3.8-Flash-Next** (125B/180B MoE, Qwen4 preview) — 256K ctx, 50% fewer tokens, 15% higher accuracy. Fits 32GB+.
3. **Unsloth Desktop** — local training + OpenAI-compat endpoint, no telemetry, sandbox, FP8 LoRA, MLX.
4. **Meshtastic 2.8** — signed broadcasts, node IDs from pubkey, position sharing opt-in. **MeshCore 1.18** — repeater/companion, path routing.
5. **Hikma Health** — offline-first EHR for field clinics (lighter than Bahmni).
6. **OpenMRS retiring offline mode** — lesson: narrow scope to intermittent unavailability.
7. **AFFiNE** — docs + whiteboard, local-first, MIT.
8. **NoteDiscovery** — self-hosted KB with MCP for AI note editing.
9. **AnythingLLM** — AI knowledge workspace, self-hosted.
10. **Needle 2** — 45M param, 14MB, 28MB RAM for edge tool calling.
11. **DeepSeek V4 Flash** distilled into Qwen3.5-9B.
12. **NVIDIA Nemotron 3.5** — edge models.

## Recommended Next Actions
- Add Survival LLM sources to medical/RAG modules
- Support MeshCore alongside Meshtastic
- Add Hikma Health as curated app (field clinics)
- Add Unsloth Desktop as training backend
- Add NoteDiscovery with MCP
- Add Needle 2 for edge devices
- Add "survival mode" (auto-switch to smallest model on low battery)