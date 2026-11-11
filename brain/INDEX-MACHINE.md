# LLM Wiki Index — nomad-hyper (machine-readable)

## Domains
| domain | description | path |
|--------|-------------|------|
| overview | Project overview | wiki/overview.md |
| ai-stack | AI stack (Qwen3.5/3.6/3.8, Claude Agent SDK) | wiki/ai-stack.md |
| iot-power | IoT sensors and solar power | wiki/iot-power.md |
| comms | Communications (Meshtastic, SDR, satellite) | wiki/comms.md |
| modules | New modules from deep research | wiki/modules.md |
| unsloth-lora | LoRA training with Unsloth | wiki/unsloth-lora.md |
| openspec | OpenSpec SDD workflow | wiki/openspec.md |
| lan-distribution | LAN distribution (cable/WiFi) | wiki/lan-distribution.md |
| survival-roadmap | Survival roadmap | wiki/survival-roadmap.md |
| upstream-gaps | Upstream NOMAD gaps | wiki/upstream-gaps.md |
| model-updates | Model updates Nov 2026 | wiki/model-updates.md |
| improvements-2026 | Improvements research Nov 2026 | wiki/improvements-2026.md |
| locations | Multi-location support | wiki/locations.md |
| i18n | Internationalization | wiki/i18n.md |
| tools-libs | Tools and libraries | wiki/tools-libs.md |

## Update ritual
- daily: ingest new sources into data/, re-run link check
- weekly: research freshness re-fetch
- monthly: index + graph rebuild, orphan sweep
- per gate: wiki-index.mjs after any content change

## Commands
- `python brain/data/rebuild.py` — rebuild index JSONs and SQLite DB
- `openspec list` — list in-flight changes
- `openspec archive <change> --yes` — archive completed change