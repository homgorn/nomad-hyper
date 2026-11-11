# 00-SUMMARY — NOMAD Hyper Improvements Research (Nov 11, 2026)

## Findings
1. **Survival LLM** (brangus.io, MIT) is a direct competitor: offline emergency AI citing sources, auto-selects model by RAM. Sources: Wikipedia, WikiMed, MedlinePlus, UK Medicines A-Z, WikEM, Ready.gov, CDC, military manuals, wikiHow, iFixit, Appropedia, Stack Exchange. NOMAD Hyper should integrate these same open sources into its RAG + medical modules. (reported, https://www.startuphub.ai/ai-news/artificial-intelligence/2026/survival-llm-runs-emergency-ai-with-no-internet, 2026-11-11)

2. **Qwen3.8-Flash-Next** (125B/180B MoE, Qwen4 architecture preview) offers 256K ctx, 50% fewer tokens, 15% higher accuracy via Unsloth Dynamic V3.1 GGUFs. Fits 32GB+ RAM. (reported, https://huggingface.co/Qwen, 2026-11-11)

3. **Unsloth Desktop** (Nov 2026) provides local training + OpenAI-compatible inference endpoint, no telemetry, sandbox, FP8 LoRA, MLX support. Can be NOMAD's local training backend. (reported, https://unsloth.ai/docs/new/studio, 2026-11-11)

4. **Meshtastic 2.8** adds signed broadcasts, node IDs from public key, position sharing opt-in, auto hop scaling. **MeshCore 1.18** adds repeater/companion split, path routing, regions. NOMAD should support both protocols. (reported, https://meshtastic.org/docs/software/apple/user/whats-new, 2026-11-11)

5. **Hikma Health** — offline-first EHR for vulnerable populations (open source). Better fit than Bahmni for field clinics (lighter). (reported, https://pubmed.ncbi.nlm.nih.gov/41686834, 2026-11-11)

6. **OpenMRS retiring offline mode** (Sep 2026) — lesson: offline sync is hard; narrow scope to intermittent unavailability. (reported, https://talk.openmrs.org/t/retiring-offline-in-o3/50151, 2026-11-11)

7. **AFFiNE** — docs + whiteboard, local-first, MIT. Could replace/augment Docmost for visual planning. (reported, https://getaffineapp.com/self-host, 2026-11-11)

8. **NoteDiscovery** — self-hosted knowledge base with MCP integration (Claude/Cursor can read/edit notes). (reported, https://www.notediscovery.com, 2026-11-11)

9. **AnythingLLM** — AI knowledge workspace, self-hosted Docker, chat with docs. (reported, https://ones.com/blog/tool-guide/tools-for-ai-team-knowledge-management-with-self-hosted-deployment-2026-recommendations-2, 2026-11-11)

10. **Needle 2** — 45M param model for tool calling on tiny devices (14MB, 28MB RAM). Ideal for edge/field nodes. (reported, https://sudoscout.dev/blog/project-nomad-offline-knowledge-server-guide, 2026-11-11)

11. **DeepSeek V4 Flash** distilled into Qwen3.5-9B — better reasoning at same size. (reported, https://ollama.com, 2026-11-11)

12. **NVIDIA Nemotron 3.5** (Super/Bolt/Lightning) — new models for edge. (reported, https://ollama.com, 2026-11-11)

## Open questions the owner may have missed
- Should NOMAD Hyper support MeshCore alongside Meshtastic? (MeshCore better for regional repeater networks)
- Should we add a "survival mode" that auto-switches to smallest model + disables non-essential containers on low battery?
- Should we integrate Hikma Health instead of Bahmni for field clinics?
- Should we add Needle 2 for edge devices (phones, wearables)?
- Should we add offline-first EHR (Hikma) as a curated app?
- Should we add AFFiNE for visual planning/whiteboard?
- Should we add NoteDiscovery with MCP for AI note editing?

## Self-critique
1. Claims with no source: "Needle 2 14MB" — only from blog post, not verified from official source.
2. Sources that disagree: Meshtastic vs MeshCore — both have merits; no single winner.
3. Stale sources: some from July-Aug 2026; may have changed.
4. Assumptions as facts: "Hikma better than Bahmni" — inferred from weight, not tested.
5. Numbers derived: RAM requirements estimated from model sizes, not measured on NOMAD hardware.
6. Questions never asked: monetization model not explored (NOMAD is free/OSS).
7. Commercial blind spots: none (project is free/OSS, no revenue model).
8. Legal exposure: all sources Apache-2.0/MIT/public domain; no ToS issues identified.