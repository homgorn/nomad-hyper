# Change: multi-location-support

## Why
NOMAD Hyper serves field teams that move between regions and multi-site deployments. Users need to select one OR MORE locations; content (ZIM collections, map regions, plant DB, LoRa frequencies) is filtered per selected location.

## What Changes
- Add KV key `content.selectedLocations` (JSON string array of location ids)
- Add built-in location catalog (constant) with KZ regions + common deployments
- Add LocationService: get/set selected locations, validation, filter helpers
- Add API endpoints: GET /api/locations (catalog + selection), PUT /api/locations (set selection)
- Document filtering strategy for RAG/maps (implementation follow-ups)
- Backend validation via validator + unit tests

## Not in this change (follow-ups)
- Frontend multi-select UI (separate OpenSpec change)
- RAG/maps/weather/plant content filtering per location (needs design)
- Location model with DB (KV approach is sufficient for selection state)

## Summary
Multi-select location support, backend-first chunk.