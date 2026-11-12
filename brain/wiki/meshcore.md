---
id: meshcore-vs-meshtastic
title: MeshCore vs Meshtastic
summary: Comparison and integration guidance for MeshCore (v1.18, Oct 2026) alongside existing Meshtastic support in NOMAD Hyper.
tags: [comms, mesh, meshcore, meshtastic, lora]
entities: [MeshCore, Meshtastic, LR2021]
claims: []
sources: [brain/research/agents-2026/comms-improvements-2026.md, docs/hyper/hyperspec.md]
updated: 2026-11-12
---

# MeshCore vs Meshtastic

## Status (as of Nov 2026)
| Item | Meshtastic | MeshCore |
|------|-----------|----------|
| Firmware | v2.8.2-alpha (packet signing, BLE Linux line) / 2.7.26 stable | v1.18 (Podnet GW Bluetooth, Oct 2026) |
| Firmware license | GPL-3.0 | MIT |
| Mobile apps | Open source | Closed (companion + repeater roles) |
| Range (field) | ~10-25 km typical | 60 km demonstrated (Hilversum office → home) |
| Node roles | Uniform (all relay) | Companion / Repeater / Room Server |
| Path routing | Flood | Fixed path discovery + flood for first message |
| 433/868/915 MHz | Yes | Yes (915 US: 910.525 SF7 62.5kHz) |
| Airtime efficiency | Lower (flood) | Higher (path routing) |
| Community | Large | Growing (Europe) |

## Which to choose
- **Meshtastic**: instant setup, mixed ad-hoc teams, events, hiking, larger community, sensor ecosystem
- **MeshCore**: regional/town repeater networks, long-range fixed infrastructure, battery-powered companions
- **Both** can run on the same LoRa boards (flash either). **They cannot hear each other.**

## Integration in NOMAD Hyper
- upstream NOMAD already ships `nomad_meshcore_web` (supply depot) — nothing to build for basic use
- Roadmap: add MeshCore MQTT bridge config, MeshMonitor parity doc (already in research), unified comms panel
- `config/` for LoRa: see `brain/research/agents-2026/comms-improvements-2026.md`

## Sources
- MeshCore docs: https://meshcore.io
- Colorado Mesh parity tracker (Oct 2026): https://colorado-mesh.github.io/mesh-client/meshcore-meshtastic-parity
- Meshtastic vs MeshCore: https://nodakmesh.org/protocols (checked Oct 2026)