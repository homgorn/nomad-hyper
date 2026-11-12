# Design: multi-location-support

## Approach
Selection state lives in KVStore (`content.selectedLocations`, JSON string array of location ids) — same pattern as `ai.tokenRatios`. No migration needed.

Catalog: static, curated locations (no user-created rows yet). Each location carries: id, name (EN/RU), country, lat/lon, region_code, lora_frequency.

API: public (no auth, same as NOMAD default) — GET returns catalog + current selection; PUT validates ids against catalog and stores JSON array.

Filtering: RAG/maps filtering is explicitly out of scope here; designed as follow-up to keep this change verifiable and small.

## Alternatives
- DB Location model: rejected for the selection slice (overkill); may be added later for user-created locations.
- Separate sessions per location: rejected; selection is a workspace-wide pref.

## Risks
- KVStore JSON parsing must be defensive (invalid JSON → empty selection, treated as "no restriction" = all content) to avoid bricking installs on manual KV edits.