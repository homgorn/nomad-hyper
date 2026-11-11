---
id: survival-roadmap
title: Survival Roadmap
summary: Additional features to fill NOMAD Hyper for survival scenarios: mesh, power, medical, navigation, comms, food, water, security.
tags: [survival, roadmap, features]
entities: [Meshtastic, FreeTAK, WeeWX, PlantNet, OctoPrint]
claims: []
sources: [docs/hyper/hyperspec.md, docs/hyper/modules-deep-research.md]
updated: 2026-11-11
---

# Survival Roadmap — What Else to Add

## Communications
- [x] Meshtastic LoRa mesh (433 MHz)
- [x] SDR (RTL-SDR, OpenWebRX, ADS-B, NOAA)
- [x] Matrix Synapse + Element
- [x] ntfy push notifications
- [ ] MeshCore (alternative to Meshtastic)
- [ ] APRS (amateur radio positioning)
- [ ] Winlink (email via HF, needs license)
- [ ] JS8Call (text via HF, -24dB)
- [ ] Jitsi Meet (LAN video calls)
- [ ] Satellite: Starlink Mini + Garmin inReach

## Power & Energy
- [x] LiFePO4 + solar + MPPT
- [x] Battery monitor (graceful shutdown)
- [ ] UPS integration (Waveshare HAT)
- [ ] Power scheduling (wake/sleep)
- [ ] Energy dashboard (Grafana)
- [ ] Generator integration (auto-start)
- [ ] Wind turbine monitoring

## Medical
- [x] FDA drug reference + interactions
- [x] Medical RAG agent
- [ ] Bahmni/OpenMRS (field clinic EMR)
- [ ] Plant identification (Qwen3.5-VL + PlantNet)
- [ ] First aid ZIM collections
- [ ] Telemedicine (Jitsi + camera)

## Navigation & Maps
- [x] ProtoMaps regional extraction
- [x] Map markers (CRUD)
- [ ] OsmAnd/Organic Maps offline sync
- [ ] GPS tracking (Meshtastic GPS)
- [ ] FreeTAK Server (SAR coordination)
- [ ] Track recording & sharing

## Knowledge & Education
- [x] Kiwix (Wikipedia, medical, survival)
- [x] Kolibri (Khan Academy)
- [x] Calibre-Web (ebooks)
- [x] Audiobookshelf (audiobooks)
- [ ] ArchiveBox (web archive)
- [ ] Docmost (team wiki)
- [ ] Wallabag (offline reader)
- [ ] Custom ZIM creation toolchain

## IoT & Sensors
- [x] ESP32 + MQTT + Home Assistant
- [x] Node-RED automations
- [x] Grafana/InfluxDB
- [ ] WeeWX (weather station)
- [ ] Air quality (MQ-135, SCD41)
- [ ] Water level / soil moisture
- [ ] Radiation detector (Geiger)
- [ ] Seismic sensor

## Tools & Fabrication
- [x] CyberChef (data tools)
- [ ] OctoPrint (3D printing)
- [ ] FreeCAD (CAD)
- [ ] iFixit repair guides
- [ ] Schematic viewer

## Security
- [x] Vaultwarden (passwords)
- [ ] Authelia (SSO/MFA)
- [ ] Nginx Proxy Manager (HTTPS)
- [ ] Fail2ban
- [ ] Network monitoring (Uptime Kuma)
- [ ] Backup (Restic/Borg)

## Food & Water
- [ ] Water purification guide (RAG)
- [ ] Foraging database (plants, mushrooms)
- [ ] Food preservation (canning, drying)
- [ ] Calorie/nutrition tracker
- [ ] Seed/planting calendar

## Education & Morale
- [ ] Navidrome (music)
- [ ] Jellyfin (video)
- [ ] Minetest (offline game)
- [ ] Language learning (Duolingo offline)
- [ ] Offline coding (Monaco editor)
