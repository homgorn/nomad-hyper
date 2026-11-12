# Tasks: multi-location-support

- [x] Add KV key `content.selectedLocations` to types/kv_store.ts
- [x] Add LOCATION_CATALOG constant
- [x] Add LocationService (get/set/validate)
- [x] Add LocationsController (GET/PUT)
- [x] Wire routes /api/locations (GET, PUT) with validation
- [x] Unit tests for LocationService (6/6 pass via node --test)
- [x] openspec validate --changes passes
- [ ] Verify: typecheck passes (background tsc run in progress)
- [ ] Follow-ups (separate changes): frontend selector, RAG/maps/plant filtering