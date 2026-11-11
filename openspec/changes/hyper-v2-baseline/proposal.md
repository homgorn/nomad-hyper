# Change: hyper-v2-baseline

## Summary
Import upstream Project NOMAD v1.35.1, add Hyper specification v2.0, new modules from deep research,
BMAD skills, agent layer, docker-compose v2, LLM wiki, and Unsloth LoRA training roadmap.
All work follows SDD (OpenSpec).

## Motivation
NOMAD Hyper extends Project NOMAD with AI agents, IoT, LoRa, SDR, solar power, voice, and LoRA training.
This change establishes the baseline for all future improvements.

## Scope
- Import upstream code
- Add Hyper docs (hyperspec, modules research, v2 compose, bmad skills, orchestrator)
- Add LLM wiki + indexes + DB schema
- Add OpenSpec structure
- Add .claude/skills (10 BMAD skills)
- Add agents/, docker-compose.v2.yml, install_nomad_v2.sh
- Add CI/CD (GitHub Actions)

## Capabilities
- project-baseline: overall project structure and documentation
- ai-agents: Claude Agent SDK layer + skills
- iot-power: IoT sensors + solar power monitoring
- comms: LoRa/Meshtastic + SDR + satellite
- unsloth-lora: LoRA training with Unsloth

## Non-goals
- Rewriting core AdonisJS code
- Adding authentication
