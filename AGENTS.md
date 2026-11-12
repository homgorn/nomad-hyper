# AGENTS.md — Rules for AI agents working in nomad-hyper

These rules are mandatory for every agent that touches this repository.

## 1. Deletion
**NEVER delete a file, directory, branch, remote object, or git history item without an explicit, typed confirmation from the human owner — twice.** "I'm sure it's junk" is not confirmation. If you believe something is safe to remove (generated output such as `node_modules/`, a broken `node_modules.broken-*`), ask first anyway.

## 2. Secrets
Never print, log, or commit secrets. `.env`, `*.key`, `*.pem`, tokens — touch only via `.env.example`. If you spot a hardcoded secret, report it; do not copy it elsewhere.

## 3. Generated artifacts
`collections/`, `admin/`, and `docs/` source-of-truth files must not be silently overwritten. Before overwriting: state what exists vs. what will replace it and why, and ask if unsure.

## 4. Claims and sources
Label claims as measured / reported (URL + date) / inferred. Do not invent version numbers, prices, licenses, or benchmark results. Uncertainty is stated as a 0–10 confidence.

## 5. Platform reality (Windows)
`npm install` in `admin/` fails on Windows (`@openzim/libzim`). Workarounds: WSL2, Docker, or `npm install --ignore-scripts` (JS-only; ZIM features unavailable). Never commit `node_modules.broken-*`.

## 6. Verification before "done"
Run what you can: unit tests, openspec validate, YAML parse, wiki rebuild. Report what you could NOT verify and why. Do not report success for checks that didn't run.

## 7. Encoding
All files UTF-8. Never round-trip through PowerShell `Get-Content | Set-Content` — it double-encodes UTF-8 on Windows. Use the editor/append APIs or byte-exact tools.

## 8. Scope
Prefer small, reviewable chunks. One concern per commit. Update TODO.md and the LLM wiki (`brain/`) when you finish or skip a task.