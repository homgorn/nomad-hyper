# 02-CONFLICTS

1. **Meshtastic vs MeshCore**: Both have merits. Meshtastic: larger community, simpler, all nodes relay. MeshCore: better for regional repeater networks, path routing, less airtime congestion. Verdict: support both, let user choose. (reported, https://nodakmesh.org/protocols, 2026-11-11)

2. **Bahmni vs Hikma Health**: Bahmni is heavier (16GB RAM) but more complete (lab, pharmacy, PACS). Hikma is lighter and designed for field clinics. Verdict: offer both as options, default Hikma for field/edge nodes. (inferred from specs)

3. **Ollama vs Unsloth Desktop as inference backend**: Ollama has model download features; Unsloth has training + OpenAI-compat endpoint. Verdict: use both — Ollama for model mgmt, Unsloth for training + inference. (reported)