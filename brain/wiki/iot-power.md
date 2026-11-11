---
id: iot-power
title: IoT and Power
summary: IoT ecosystem with ESP32 sensors, MQTT/Mosquitto, Home Assistant, Node-RED, Grafana/InfluxDB. Solar power with LiFePO4, MPPT, INA226 monitoring.
tags: [iot, sensors, solar, power, mqtt]
entities: [ESP32, Mosquitto, Home Assistant, LiFePO4, Victron]
claims: []
sources: [docs/hyper/hyperspec.md]
updated: 2026-11-11
---

# IoT and Power

## Sensors
DHT22, BME280, SCD41, DS18B20, INA226, HC-SR501, MQ-135, ESP32 DevKit

## Power
- LiFePO4 12V 100Ah (6000+ cycles, -20C)
- MPPT controllers (Victron, Renogy, EPever)
- Solar panels 100-400W
- UPS HAT for RPi
- Battery monitor script (graceful shutdown at 10%)
