---
id: affinne-notediscovery
title: AFFiNE and NoteDiscovery
summary: AFFiNE (docs+whiteboard, local-first) and NoteDiscovery (self-hosted KB with MCP for AI agents) as knowledge-workspace options.
tags: [notes, docs, whiteboard, mcp, affine]
entities: [AFFiNE, NoteDiscovery]
claims: []
sources: [https://www.notediscovery.com, https://getaffineapp.com/self-host]
updated: 2026-11-12
---

# AFFiNE & NoteDiscovery

## NoteDiscovery (added to NOMAD Hyper compose, profile `notes`)
- Image: ghcr.io/gamosoft/notediscovery:latest
- Port: 8091 (host) → 8000 (container)
- MIT license, air-gapped friendly (no CDN), plain markdown storage
- Built-in MCP server: AI assistants (Claude, Cursor, OpenCode) can search/create/edit notes
- `MCP_ENABLED=true` set in compose
- Data: ./data/notediscovery

## AFFiNE
- Docs + whiteboard + databases in one workspace, local-first desktop app
- Self-host free up to 10 seats per workspace; Team adds seats
- MIT (editor/client) / AFFiNE EE (backend) — self-hosting requires checking EE license terms for commercial use
- Not added to compose yet: backend image/config needs verification against the official AFFiNE compose template (unverified as of 2026-11-12)
- Good fit for visual planning boards (SQRL/SAR) and collaborative survival plans

## Also considered (research, Nov 2026)
- mdnest — team notes + AI agents over MCP, MIT
- AnythingLLM — AI knowledge workspace, self-hosted Docker
- AFFiNE whiteboard — vs Excalidraw (already in supply depot)

## Open items
- [ ] Verify AFFiNE self-host compose template and add with profile `whiteboard`
- [ ] Wire MCP_ENABLED notes endpoint into docs
