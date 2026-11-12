---
id: research-agents-2026
title: Deep Research Reports (Agents, Nov 2026)
summary: "Five parallel agent reports: emergency sources (80+), AI models, comms (MeshCore/Reticulum/SDR), medical (Hikma/MenSung), power/IoT (MPPT/BMS/HA). All under brain/research/agents-2026/."
tags: [research, agents, 2026]
entities: [Hikma Health, MeshCore, MenSung, Pl@ntNet]
claims: []
sources: [brain/research/agents-2026/]
updated: 2026-11-12
---

# Deep Research Reports — Agent Swarm (Nov 2026)

Five parallel agents researched what to add and improve to NOMAD Hyper. Raw reports in `brain/research/agents-2026/`. Key takeaways:

## Emergency sources (80+)
10 public-domain medical manuals, 11 military field manuals (FM 21-76, FM 4-25.11, ATP 3-50.21), 15 FEMA/Ready.gov docs, USDA Complete Guide to Home Canning (2015, 40 MB), 12 water/WASH docs, 12 foraging references, 16 repair/construction TMs. Tiered integration priorities with storage estimates. All US Gov works are Public Domain (17 USC §105).

## AI (2026)
- Needle 2 (45M, 14MB, 28MB RAM, Apache-2.0, on-device tool-calling) — **verified** at https://huggingface.co/Cactus-Compute/needle2
- Gemma 4 E4B (phone-class multimodal), Phi-4-mini
- SPARKLE / T²RAG — agentic RAG policies (+9-11% over naive RAG)
- EmbeddingGemma 2 (740M, multimodal, 191MB RAM)
- MedGemma 4B (medical VLM, +10.8% on agentic health tasks)
- Qwen3.5-9B + DeepSeek V4 Flash distilled

## Communications
- MeshCore v1.18 (MIT firmware, repeater/companion roles, path routing, 60 km field-proven) — added to wiki: `brain/wiki/meshcore.md`
- Meshtastic 2.8.2-alpha: signed broadcasts, pubkey node IDs
- Reticulum RNS 1.5.5 — transport-agnostic, higher integration effort
- LR2021 SDR chip — 150–960 MHz + 2.4 GHz FLRC
- Starlink Mini ($149–199, 25-40 W), Garmin inReach Mini 3 Plus

## Medical
- **Hikma Health** — offline-first MIT EHR, Local Sync Hub, <8 GB RAM — added to compose (profile `health`, port 3457)
- MenSung — drug safety lookup, <10 MB binary, MIT/Apache-2.0
- Pl@ntNet (embedded model ~600 MB) / Seek / iNaturalist Next for plant ID
- SDIF — 4-tier drug interaction matching (EPha, substance, ATC-class, CYP)

## Power / IoT
- MPPT: Victron SmartSolar 150/45; BMS: JK BMS B2A16S20P (active 2A balancing, CAN/RS485)
- UPS: Waveshare UPS Module 3S (swappable 18650, I2C, HA integration)
- SCD41 CO2 (±40 ppm), ESPGeiger + SBM-20/M4011 (radiation)
- Home Assistant 2026.11 — Energy dashboard accepts power sensors directly
- Grafana 11 + LGTM stack

## License notes
- wikiHow and iFixit are CC BY-NC-SA — exclude for commercial builds (see `collections/survival-sources.json`)

## Open items
- AFFiNE compose (backend image verification pending)
- Pl@ntNet offline model licensing (proprietary) — verify before bundling
- Hikma Health Docker Hub tag (`hikmahealth/hikma`) — unverified at runtime; needs test pull