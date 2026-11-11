---
id: locations
title: Multi-Location Support
summary: NOMAD Hyper supports multiple locations (regions/cities) with multi-select for content (ZIM, maps, weather, plants, comms frequencies).
tags: [locations, multi-select, content]
entities: [ProtoMaps, Kiwix, Meshtastic]
claims: []
sources: [docs/hyper/hyperspec.md]
updated: 2026-11-11
---

# Multi-Location Support

## Concept
A NOMAD instance can serve multiple geographic locations simultaneously. Users select one or more locations; content (ZIM, maps, weather, plants, LoRa freq) is filtered per location.

## Use cases
- Field team moving between regions
- Multi-site deployment (camp A + camp B)
- Travelers with regional content packs

## Implementation
- Location selector in UI (multi-select dropdown)
- Location stored in user prefs (KVStore or session)
- Content filtered by location tags (ZIM collections, map regions, plant DB)
- Meshtastic region/frequency per location (KZ 433MHz, etc.)
- Weather (WeeWX) per location
- Plant identification (regional flora DB)

## Data model
- `Location` model: id, name, country, lat, lon, region_code, timezone
- `ContentLocation` join: content_id, location_id
- User prefs: selected_locations[]

## OpenSpec change
- `multi-location-support` — add Location model, UI selector, content filtering