# Hikma Health — Offline-First EHR

## Overview
Hikma Health is an open-source, offline-first EHR designed for low-resource and field settings. Lighter than Bahmni (6-8 GB RAM mobile vs 16 GB+).

## Integration Plan
1. Add to Supply Depot catalog as curated app
2. Docker image: `hikmahealth/hikma` (verify on Docker Hub)
3. Requires: PostgreSQL, Redis
4. Port: 3000 (default)
5. Sync: Local Sync Hub for intermittent connectivity

## Configuration
```yaml
services:
  hikma-health:
    image: hikmahealth/hikma:latest
    container_name: nomad-hikma
    restart: unless-stopped
    ports:
      - "3457:3000"
    environment:
      - DATABASE_URL=postgresql://hikma:pass@nomad-postgres:5432/hikma
      - REDIS_URL=redis://nomad-redis:6379
      - NODE_ENV=production
    depends_on:
      - nomad-postgres
      - nomad-redis
    networks:
      - nomad
```

## Sources
- GitHub: https://github.com/hikmahealth/hikma
- Paper: https://pubmed.ncbi.nlm.nih.gov/41686834 (2026-02-13)
- Demo: https://demo.hikmahealth.org

## License
MIT — commercial OK

## Status
- [x] Add to service_names.ts
- [x] Add to supply_depot_docs.ts
- [x] Add docker-compose entry (host port 3457; Vikunja uses 3456)
- [x] Add documentation section in admin/docs/supply-depot-apps.md