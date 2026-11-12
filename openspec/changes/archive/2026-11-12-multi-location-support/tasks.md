# Tasks: multi-location-support

- [x] Add KV key `content.selectedLocations` to types/kv_store.ts
- [x] Add LOCATION_CATALOG constant
- [x] Add LocationService (get/set/validate)
- [x] Add LocationsController (GET/PUT)
- [x] Wire routes /api/locations (GET, PUT) with validation
- [x] Unit tests for LocationService (6/6 pass via node --test)
- [x] openspec validate --changes passes
- [x] Verify: typecheck passes (node_modules rebuilt; tsc --noEmit exit=0)
- [ ] Follow-ups (separate changes): frontend selector, RAG/maps/plant filtering