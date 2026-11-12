# HANDOFF — nomad-hyper

## State
- Repo: https://github.com/homgorn/nomad-hyper (public), Apache-2.0
- Base: upstream Project NOMAD v1.35.1 + Hyper extensions (docs/hyper canonical snapshot)
- OpenSpec: 4 changes archived (hyper-v2-baseline, lan-survival-roadmap, improvements-research-2026, locations-i18n-tools); 1 in-flight (multi-location-support — backend implemented, unit tests pass 6/6; openspec validate pending verify)
- LLM Wiki: 18 topics, SQLite DB at brain/data/knowledge.db (rebuilt via brain/data/rebuild.py)
- CI: .github/workflows/ci.yml (lint+typecheck+openspec validate) — note: typecheck of admin/ will fail on Windows once libzim missing; intended for Linux runner

## Done (Nov 12)
- Survival LLM sources collection; i18n infra + 10 valid locale files (parity-verified); Hikma Health curated app (host port 3457); Unsloth Desktop backend (FastAPI training API stub + compose profile); survival_mode.py (battery-aware); LAN distribution design; survival roadmap; MeshCore docs; NoteDiscovery compose (profile notes); Needle 2 verification (Apache-2.0)
- Multi-location backend: /api/locations GET/PUT, catalog (constants/locations.ts), KV `content.selectedLocations`, defensive parsing, 6 unit tests pass
- i18n locale parity across 10 languages
- npm install works only with --ignore-scripts on Windows (libzim native build needs Linux/WSL); audit down from 78 → 61 vulns (rest are upstream majors)

## Next 3 actions
1. Typecheck in background — confirm zero new errors (running now)
2. Frontend multi-select selector + locale switcher (Inertia React) — needs design review
3. Add real Unsloth training loop + test on 4GB GPU

## Blockers
- admin/ typecheck on Windows blocked by @openzim/libzim native build; use WSL2/Docker or accept ignore-scripts state
- 78→61 audit vulnerabilities remain in upstream dependencies (maplibre-gl, proxy-addr, tar — major bumps)