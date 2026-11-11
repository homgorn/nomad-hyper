---
id: comms
title: Communications
summary: Multi-layer comms: WiFi LAN, LoRa/Meshtastic mesh, SDR (RTL-SDR), satellite (Starlink Mini, Garmin inReach), Matrix Synapse chat, ntfy push notifications.
tags: [comms, lora, meshtastic, sdr, satellite, matrix]
entities: [Meshtastic, RTL-SDR, Starlink, Garmin inReach, Matrix]
claims: []
sources: [docs/hyper/hyperspec.md]
updated: 2026-11-11
---

# Communications

## LoRa / Meshtastic
- 433 MHz (KZ ISM), T-Beam Supreme, external antennas up to 25km
- meshtastic Python SDK, listener/sender scripts

## SDR
- RTL-SDR V4, OpenWebRX, dump1090 (ADS-B), NOAA APT weather

## Satellite
- Starlink Mini (data), Garmin inReach Mini 3+ (SOS)

## Chat/Push
- Matrix Synapse + Element, ntfy self-hosted
