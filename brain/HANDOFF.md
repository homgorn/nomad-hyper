# HANDOFF — nomad-hyper

## State
- Repo: https://github.com/homgorn/nomad-hyper (public)
- Base: upstream Crosstalk-Solutions/project-nomad v1.35.1 imported
- OpenSpec: initialized (opencode, schema spec-driven, language ru)
- Hyper specs imported: docs/hyper/ (hyperspec, modules deep research, v2 compose, bmad skills, orchestrator)
- LLM Wiki: populated (brain/)
- OpenSpec change hyper-v2-baseline: archived

## What is the project
NOMAD Hyper is an offline-first knowledge and education server (fork of Project NOMAD)
extended with AI agents (Claude Agent SDK), Qwen3.5 models, IoT sensors, LoRa/Meshtastic,
SDR, solar power, voice stack, and Unsloth LoRA training. Apache-2.0.

## Done
- GitHub repo created and pushed
- Upstream imported
- OpenSpec initialized + change archived
- Hyper docs imported
- brain/ skeleton populated
- .claude/skills (10 BMAD skills)
- agents/, docker-compose.v2.yml, install_nomad_v2.sh
- CI/CD (GitHub Actions)
- Unsloth docs + roadmap + training script
- Multi-lang docs (en, ru, locales.json)
- README updated

## Next 3 actions
1. Run deep research on new models (Qwen3.5 variants, Unsloth latest) and update LLM wiki
2. Implement agent layer (orchestrator + sub-agents) in agents/
3. Add more OpenSpec changes for specific features (voice stack, IoT, comms)

## Blockers
- None
