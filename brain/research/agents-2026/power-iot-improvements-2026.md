# NOMAD Hyper — Power/Energy & IoT Improvements Research (2026)

> **Research Date:** 2026-11-11  
> **Scope:** Solar MPPT controllers, LiFePO4 BMS, UPS HAT, wind turbines, energy monitoring (Victron, EPEver), new sensors (CO₂, radiation, water quality), Home Assistant latest, Node-RED, Grafana 11  
> **Source Labeling:** **Measured** = first-hand tested/lab-verified | **Reported** = vendor specs, press releases, community docs (URL + date) | **Inferred** = derived from specs, community patterns, or logical deduction

---

## 1. Solar MPPT Charge Controllers

### 1.1 Victron SmartSolar MPPT

| Aspect | Details |
|--------|---------|
| **Latest Models (2026)** | SmartSolar 75/10, 75/15, 100/20, 100/30, 100/50, 150/35, 150/45, 150/60, 150/70, 150/85, 150/100, 250/60, 250/70, 250/100 |
| **Efficiency** | 98–99% peak conversion (reported, Victron datasheets) |
| **Connectivity** | Built-in Bluetooth (BLE) + VE.Direct; optional VE.Can; **Victron GX MQTT** for HA (official since HA 2026.5) |
| **HA Integration** | **Three official integrations (2026):** `victron_gx` (MQTT, bidirectional, requires Cerbo/Ekrano GX), `victron_ble` (BLE Instant Readout, read-only, no GX needed), `hass-victron` (Modbus TCP, HACS) — [reported, HA 2026.5 release blog, 2026-05-12] |
| **Price (USD, 2026-Q3)** | 100/30: $128–$165; 150/45: $265–$350; 150/70: $395–$480; 250/100: $680–$850 — [reported, Victron EUR C pricelist 2026-Q3, Oct 2026 prices] |
| **Firmware** | v1.67 mandatory for some SmartSolar models (Nov 2026); Bluetooth firmware v2.53 adds VE.Smart Networking for 250/60 & 250/70 — [reported, VictronConnect changelog 2026-11-06] |
| **NOMAD Fit** | Premium choice; Bluetooth + MQTT + Modbus covers all integration paths; proven in mobile/off-grid; LFP-ready charge profiles |

### 1.2 Renogy Rover Series

| Aspect | Details |
|--------|---------|
| **Latest Models (2026)** | Rover 20A/30A/40A (Rover 2), Rover 60A, Rover 100A, Rover Li (LiFePO4-optimized), Rover Boost (36/48V) |
| **Efficiency** | 97–99% tracking (reported) |
| **Connectivity** | Built-in Bluetooth on Rover 2; optional BT module on older; RS485 (Modbus) on all; Renogy DC Home app |
| **HA Integration** | Custom BLE integration `renogy` (HACS, Jan 2026) — requires `renogy-ble==1.0.0`; Modbus TCP via RS485-to-Ethernet bridge — [reported, HA Community 2026-01-08] |
| **Price (USD, 2026)** | Rover 2 30A: $119.99; Rover 60A: $399.99; Rover 100A: $701.99; Rover Li 40A: $87.99 — [reported, Renogy US site Oct 2026] |
| **NOMAD Fit** | Budget-friendly; Rover Li series has native LiFePO4 profiles; Modbus path works but less mature than Victron |

### 1.3 EPEver Tracer Series

| Aspect | Details |
|--------|---------|
| **Latest Models (2026)** | Tracer-AN G3 (50–100A, up to 5kW), Tracer-BN (10–40A), Tracer-BPL (IoT + LED driver), DuoRacer (dual battery), iTracer-ND (60A) |
| **Efficiency** | 98.0–98.6% max conversion; 99.5% MPPT tracking (reported, AN G3 datasheet 2025-12) |
| **Connectivity** | Isolated RS485 (5V/200mA) + Modbus RTU; **eBox-WIFI-01** (WiFi, $24.99), **eBox-BLE-01** (Bluetooth, $24.99), USB-RS485 cable — [reported, EPEver site & TSolar listing 2026] |
| **HA Integration** | Modbus TCP via eBox-WIFI-01 (port 8088) — community config (GitHub gabrielpc1190, 2020, still valid); ESPHome Modbus RTU over serial/TCP — [reported, ESPHome devices docs 2026] |
| **Price (USD, 2026)** | Tracer-AN 50A: ~$220; 60A: ~$260; 80A: ~$340; 100A: ~$420; eBox modules: $25 each — [reported, multiple distributors 2026] |
| **NOMAD Fit** | Cost-effective high-amperage; RS485 Modbus is standard; eBox adds wireless; G3 (2025) adds 4G/WiFi optional modules; parallel up to 6 units (30kW) |

### 1.4 Morningstar / SRNE / Others

| Brand | Notes |
|-------|-------|
| **Morningstar** | ProStar MPPT, TriStar MPPT — industrial/telecom grade; higher price; Modbus/Ethernet options — [reported, techfinepv.com 2026 buyer guide] |
| **SRNE** | ML/MLG series; competitive pricing; Modbus; growing HA community support — [reported] |
| **MidNite Solar** | Classic/Classic SL — premium US-made; Modbus; WhizBang Jr. shunt — [reported] |

---

## 2. LiFePO4 BMS (Battery Management Systems)

### 2.1 JK BMS — **Top Pick for NOMAD**

| Aspect | Details |
|--------|---------|
| **Key Models (2026)** | B2A8S20P (8S 200A), B2A16S10P (16S 100A), B2A16S15P (16S 150A), B2A16S20P (16S 200A), B2A24S20P (24S 200A), **B2A32SRP (32S 300A)** |
| **Balancing** | **Active balancing up to 2A** (vs. passive 30–100mA on Daly/JBD) — [reported, insumenergy.com 2026 comparison] |
| **Voltage Accuracy** | ±10mV (best in class) — [reported] |
| **Communication** | RS485, CAN, Bluetooth (BLE) — [reported] |
| **HA Integration** | **Excellent:** `batmon-ha` addon (GitHub fl4p) supports JK, JBD, Daly, ANT, SOK via BLE; MQTT discovery; InfluxDB; Energy dashboard; SOC reset; charge/discharge control — [reported, GitHub 2026, GobelPower docs 2026] |
| **ESPHome/ESP32** | Native BLE integration via `syssi/jk-bms-ble` — [reported, YouTube 2026 tutorial] |
| **Price (USD, 2026)** | 16S 100A: $125–$185; 16S 150A: $134–$194; 32S 300A: $249–$274 — [reported, shop.jkbms.com 2026, 50% off promo] |
| **NOMAD Fit** | **Best overall:** active balancing critical for large LFP packs; CAN/RS485 enables inverter comms (Victron, Growatt, Deye); mature HA/ESPHome support |

### 2.2 Daly BMS — Budget / Simple Builds

| Aspect | Details |
|--------|---------|
| **Key Models** | Smart BMS (Bluetooth), UART/RS485 versions; 4S–24S; up to 100A continuous |
| **Balancing** | Passive only (30–100mA) — [reported] |
| **Communication** | Bluetooth only (standard); UART/RS485 on "smart" models — [reported] |
| **HA Integration** | `batmon-ha` supports `daly` and `daly_uart`; BLE integration (HACS) — [reported, HA Community 2026] |
| **Price** | 16S 100A: ~$60–$120 — [reported] |
| **NOMAD Fit** | OK for small packs (<16S, well-matched cells); add external active balancer if needed |

### 2.3 JBD (Overkill Solar) — Middle Ground

| Aspect | Details |
|--------|---------|
| **Balancing** | Passive or active (select models) — [reported] |
| **Communication** | UART, RS485, CAN — [reported] |
| **Price** | 16S 100A: $80–$180 — [reported] |
| **HA Integration** | `batmon-ha` (partial); RS485 support TODO — [reported, GitHub 2026] |

### 2.4 Pace BMS — Emerging

| Aspect | Details |
|--------|---------|
| **Notes** | GobelPower HA addon supports Pace + JK; RS232/RS485/WiFi/Ethernet options — [reported, GobelPower 2026] |
| **NOMAD Fit** | Watch for CAN-open inverter integration; newer, less community history |

---

## 3. UPS HAT for Raspberry Pi (Home Assistant Host)

### 3.1 Waveshare UPS HAT (B) / UPS Module 3S

| Aspect | Details |
|--------|---------|
| **Models** | UPS HAT (B) — 5V/5A, pogo pins, I2C monitoring; UPS Module 3S — 3×18650, 5V/5A, auto-switching |
| **Monitoring** | I2C: voltage, current, power, capacity %, cell balancing — [reported, Waveshare Wiki 2026] |
| **HA Integration** | **Custom HACS integration:** `hacs_waveshare_ups_hat` (GitHub mykhailog) + `rpi_waveshare_ups` (uvjim) — [reported, HA Community 2026] |
| **Pi 5 Support** | Works with Pi 5 + Display 2; 3S module tested 14+ min runtime — [reported, YouTube 2026] |
| **Price** | UPS HAT (B): ~$35–$45; UPS Module 3S: ~$45–$60 (cells not included) — [reported, PiShop US / Amazon 2026] |
| **NOMAD Fit** | Good for Pi-based HA; 3S module better for mobile (swappable 18650s); I2C monitoring is local-only (no cloud) |

### 3.2 Pi-UpTime / PiZ-UpTime / UPS PIco

| Model | Notes |
|-------|-------|
| **Pi-UpTime 2.0** | Dual 18650, USB-C in, 5V out — [reported, PiShop 2026] |
| **UPS PIco HV3.0B+** | 450mAh LiPo, 6.5A peak, safe shutdown focus — [reported] |
| **Tiny-UPS 3.0** | World's smallest; micro-USB + battery connector — [reported] |

---

## 4. Small Wind Turbines (Micro-Wind for Off-Grid Supplement)

| Aspect | Details |
|--------|---------|
| **Market Reality (2026)** | **Micro-wind (<1kW):** $500–$3,000 installed; suitable for battery charging, RVs, cabins — [reported, solartechonline.com 2025, nedes.us 2026] |
| **Small Wind (1–10kW):** | $15,000–$175,000 installed; requires permitting, tower, professional install — [reported] |
| **Cost/kW** | $6,000–$12,000/kW installed (vs. solar ~$2.56/W) — [reported] |
| **Top Micro Models** | Pikasola 400W/500W (~$270), VEVOR 400W, Ramsond Da Vinci 1000W ($884), Tumo-Int 1000W — [reported, theroundup.org 2026] |
| **Victron Integration** | **DC-couple via SmartSolar MPPT** (turbine DC output → MPPT → battery); requires turbine voltage > battery voltage; AC-coupling inefficient for small turbines — [reported, Victron Community 2023/2026 threads] |
| **HA Monitoring** | Via Victron GX MQTT (if MPPT on Victron) or direct Modbus/MPPT BLE — [inferred] |
| **NOMAD Fit** | **Only viable for winter/solar-poor sites**; low ROI; mechanical maintenance; noise; zoning. Recommend: Pikasola 500W + Victron SmartSolar 100/30 DC-coupled if wind resource >5 m/s annual avg. |

---

## 5. Energy Monitoring — Victron Ecosystem

### 5.1 Cerbo GX / Ekrano GX — **System Hub**

| Device | Price (USD) | Key Specs | HA Integration |
|--------|-------------|-----------|----------------|
| **Cerbo GX** | $248 | Venus OS, MQTT broker, Modbus TCP, VE.Can, VE.Direct×4, USB, Ethernet, WiFi, Bluetooth | **Official `victron_gx` (MQTT, bidirectional, HA 2026.5+)** — [reported, HA docs 2026, Alchemy Industrial 2026] |
| **Cerbo GX + Touch 50** | ~$478 | Cerbo + 5" touchscreen | Same |
| **Cerbo GX + Touch 70** | ~$620 | Cerbo + 7" touchscreen | Same |
| **Ekrano GX** | $590 | Built-in 7" touchscreen, Venus OS, same ports | Same |

**MQTT Topics:** Full system tree (inverters, MPPTs, batteries, grid meters, EV chargers, relays, tanks, sensors) — [reported, Victron docs 2026]

### 5.2 SmartShunt — Battery Monitor

| Model | Price (USD) | Specs |
|-------|-------------|-------|
| 300A/50mV | $76 | Bluetooth, VE.Direct, midpoint/temp sensor port |
| 500A/50mV | $107 | — |
| 1000A/50mV | $177 | — |
| 2000A/50mV | $241 | — |
| IP65 variants | +$0–$10 | Waterproof |

**HA:** Via `victron_ble` (read-only, no GX) or `victron_gx` (via GX) — [reported, HA integrations 2026]

### 5.3 SmartSolar MPPT — See Section 1.1

### 5.4 Lynx Smart BMS — **System BMS for Victron Inverters**

| Aspect | Details |
|--------|---------|
| **Role** | Replaces external BMS; communicates via VE.Can to Cerbo GX; controls MultiPlus/Quattro via DVCC |
| **HA** | Supported in `victron_ble` (since 2026) and `victron_gx` — [reported, HA docs 2026] |
| **NOMAD Fit** | **Best if using Victron inverters**; integrated DVCC = zero-config charge control |

### 5.5 VRM (Victron Remote Management) — Cloud

| Aspect | Details |
|--------|---------|
| **Free Tier** | Basic monitoring, 30-day history |
| **Advanced** | €60/yr per site — extended history, widgets, API |
| **MQTT** | Local (GX) + Cloud (VRM MQTT) — [reported, Victron docs 2026] |

---

## 6. Energy Monitoring — EPEver Ecosystem

| Component | Price | Integration Path |
|-----------|-------|------------------|
| **Tracer-AN G3 (50–100A)** | $220–$420 | RS485 Modbus RTU (isolated, 5V/200mA) |
| **eBox-WIFI-01** | $24.99 | WiFi → Modbus TCP (port 8088) → HA Modbus integration |
| **eBox-BLE-01** | $24.99 | Bluetooth → Mobile app; ESPHome BLE bridge possible |
| **MT50 Remote Meter** | ~$35 | Wired display; not for HA |
| **CC-USB-RS485-150U** | ~$25 | USB → RS485 for PC monitoring |

**HA Config Example (Modbus TCP via eBox-WIFI):**
```yaml
modbus:
  - type: tcp
    host: 192.168.x.x
    port: 8088
    name: epever_hub
sensor:
  - platform: modbus
    scan_interval: 10
    registers:
      - name: "Battery Voltage"
        hub: epever_hub
        slave: 1
        register: 13082
        scale: 0.01
        unit_of_measurement: "V"
```
— [reported, GitHub gabrielpc1190 2020, ESPHome devices 2026]

---

## 7. New Sensors for Environmental Monitoring

### 7.1 CO₂ Sensors (True NDIR / Photoacoustic)

| Sensor | Tech | Range | Accuracy | Interface | Price | HA/ESPHome |
|--------|------|-------|----------|-----------|-------|------------|
| **Sensirion SCD41** | Photoacoustic NDIR | 400–5000 ppm | ±(40 ppm + 5%) | I²C (0x62) | $18–$69 | **Native ESPHome `scd4x`; HA via ESPHome** — [reported, ESPHome 2026.10, esp32.co.uk 2026-09-23] |
| **Sensirion SCD40** | Photoacoustic NDIR | 400–2000 ppm | ±(50 ppm + 5%) | I²C (0x62) | $15–$18 | Same as SCD41; lower range |
| **Sensirion SCD30** | NDIR (dual-channel) | 400–10000 ppm | ±(30 ppm + 3%) | I²C (0x61) | $38 | Native ESPHome `scd30` — [reported, ESPHome 2026] |
| **SenseAir S8** | NDIR | 400–10000 ppm | ±(30 ppm + 3%) | UART | ~$50 | ESPHome `senseair` |
| **MH-Z19B / Z19C** | NDIR | 0–5000 ppm | ±(50 ppm + 5%) | UART (9600) | $20–$30 | ESPHome `mhz19` (ABC logic, calibration) — [reported, ESPHome 2026] |
| **Apollo AIR-1** | SCD40 + SEN55 (PM) | CO₂ + PM + VOC + T/RH | WiFi (ESPHome) | $130–$200 | **Plug-and-play ESPHome** — [reported, computingforgeeks.com 2026-10-30] |
| **AirGradient ONE** | S8 + PMS5003 | CO₂ + PM + NOx | WiFi (ESPHome/HA native) | ~$180 | **Native HA integration `airgradient`** — [reported] |
| **IKEA VINDRIKTNING / ALPSTUGA** | NDIR (ALPSTUGA) | CO₂ + T/RH | Matter/Thread | $20–$35 | **Matter (ALPSTUGA)** — [reported, HA 2026.11] |

**Recommendation for NOMAD:** **SCD41 on ESP32-C3/ESP32-S3 via ESPHome** — lowest power, true CO₂, I²C, native HA, $25–$35 module cost. Avoid MQ-135 (eCO₂, unreliable).

### 7.2 Radiation Sensors (Geiger-Müller)

| Device | Tube | Output | Interface | Price | HA/ESPHome |
|--------|------|--------|-----------|-------|------------|
| **Gravity: Geiger (M4011)** | M4011 (β/γ) | Digital pulse | Gravity 3-pin (3.3–5V) | €62 / $68 | ESPHome `pulse_counter` → CPM/µSv/h — [reported, OpenELAB 2026] |
| **GGreg20_V3 (SBM-20)** | SBM-20 (β/γ) | Pulse + LED/buzzer | 3.3V logic | 1729–3760 UAH (~$42–$92) | ESPHome `pulse_counter` + integration → µSv/h; **uRADMonitor cloud** — [reported, IoT-devices 2026, ESPHome bridge 2026-09-26] |
| **MightyOhm Kit** | SBM-20 | Pulse + serial | USB/Serial | $119.95 | **ESPGeiger firmware** (ESP8266/ESP32) — MQTT, HA auto-discovery, Radmon.org, GMCMAP, OLED, NeoPixel, BME280 — [reported, GitHub steadramon 2026, docs.espgeiger.com] |
| **Cajoe GC-ESP32** | M4011 / J305 | Serial (GC10) | ESP32 built-in | ~$80 | ESPGeiger native support |

**Conversion:** SBM-20 ~108 CPM/µSv/h (Co-60); M4011 ~123 CPM/µSv/h — [reported, MG Super Labs specs]

**Recommendation for NOMAD:** **ESPGeiger on ESP32 + SBM-20 or M4011 tube** — open-source, MQTT/HA auto-discovery, local + cloud (uRADMonitor), environmental sensor auto-detect (BME280/AHT).

### 7.3 Water Quality Sensors

| Parameter | Sensor Options | Interface | Price | HA/ESPHome |
|-----------|----------------|-----------|-------|------------|
| **pH** | Atlas Scientific EZO-pH (±0.01, ISO 10523), DFRobot SEN0161-V2 (±0.1) | UART/I²C (EZO), Analog (DFRobot) | $50–$120 (EZO), $25 (DFRobot) | **AquaPi (ESPHome)** supports EZO-pH natively — [reported, AquaPi 2026] |
| **EC / TDS / Salinity** | Atlas Scientific EZO-EC (0.07–500,000 µS/cm), DFRobot SEN0244 (TDS) | UART/I²C (EZO), Analog (DFRobot) | $60–$130 (EZO), $20 (DFRobot) | AquaPi supports EZO-EC |
| **Dissolved Oxygen** | Atlas Scientific EZO-DO | UART/I²C | $150–$200 | AquaPi supports EZO-DO |
| **Turbidity** | Keyestudio V1 (analog), DFRobot SEN0189 | Analog | $10–$20 | ESPHome `adc` + calibration |
| **Temperature** | DS18B20 (waterproof) | 1-Wire | $5–$10 | Native ESPHome `dallas` |
| **All-in-One** | Tuya ZG-109TDS (7-in-1: TDS, EC, SG, salinity, water T, air T/RH) | Zigbee | ~$50–$80 | **Zigbee2MQTT only** (no ZHA support yet) — [reported, smarthomescene.com 2026-09-25] |
| **Pool/SpA** | Flipr (pH, ORP, T) | BLE | ~$200 | **HACS `ha-flipr-local` (2026-04, local BLE)** — [reported, GitHub 2026] |

**Recommendation for NOMAD:** **AquaPi (ESPHome) + Atlas EZO circuits** for lab-grade; **DFRobot Gravity + ESP32** for budget; **Tuya Zigbee** only if Zigbee2MQTT already running.

---

## 8. Home Assistant — 2026 State

### 8.1 Major Releases (2026)

| Version | Date | Key Features |
|---------|------|--------------|
| **2026.2** | Feb 2026 | Area sensor shortcuts; Energy dashboard: real-time badges, Water Sankey chart; Continue on error in automations; Android wake word (exp); Python 3.14 prep |
| **2026.3** | Mar 2026 | **Python 3.14**; Voice foundation; Energy dashboard tabs (Electricity/Gas/Water); Water Sankey; Battery usage tracking |
| **2026.5** | May 2026 | **Official `victron_gx` integration (MQTT, platinum)**; 15 new integrations |
| **2026.9** | Sep 2026 | Matter network map; Activity log (trigger explain); Security dashboard (active alerts/favorites); Audio charts; Smarter Modbus (register map help); Sun golden/blue hour triggers |
| **2026.10** | Oct 2026 | **Cloud → "Link" rename**; New Map (redesigned markers, zones, crisp zoom); Profile page; Trigger IDs; Tile card slider; **Energy dashboard: per-battery discharge graph**; 15 new integrations (KACO Modbus, etc.) |
| **2026.11** | Nov 2026 | **Built-in Marketplace (HACS integrated)**; Entity renaming (breaking); Self-updating dashboard sections; LoRaWAN; Matter cameras (1.5); Two-way audio (Reolink); Local-drive backups; Power→Energy auto-conversion (Riemann sum) |

### 8.2 Energy Dashboard (2026 State)

- **Sources:** Grid (import/export), Solar, Battery (charge/discharge **per battery**), Gas, Water, Individual devices
- **Power sensors now accepted directly** (no Riemann sum template needed) — [reported, HA 2026.3]
- **Carbon intensity** via Electricity Maps integration (auto-detected) — [reported]
- **Dynamic pricing** integrations: Tibber, EnergyZero, Nord Pool, Zonneplan, Green Planet Energy, aWATTar, etc. — [reported]

### 8.3 Integration Quality Scale (2026)

- **Platinum:** `victron_gx`, `airgradient`, `okok_scale`, `electricity_maps`, `kaco_modbus` — tested, documented, maintained
- **Gold/Silver/Bronze:** Most others; `victron_ble` is **Bronze** (1489 installs, read-only) — [reported, HA docs 2026]

---

## 9. Node-RED — 2026 State

### 9.1 Versions & Installation

| Channel | Version (2026) | Notes |
|---------|----------------|-------|
| **HAOS Add-on** | 22.x (Node-RED 5.x) | Easiest; auto-connects to HA; sidebar access; watchdog — [reported, raspberry.tips 2026-10-21] |
| **Docker** | `nodered/node-red:latest` (4.1.17 → 4.x) | Requires `node-red-contrib-home-assistant-websocket` |
| **Node-RED 5.x** | Current major | Async flow execution; better TypeScript support |

### 9.2 HA Integration Nodes

- **`node-red-contrib-home-assistant-websocket`** — Official node set (events, states, services, render template, get entities, trigger, device trigger, config, websocket server) — [reported]
- **Node-RED Companion (HACS)** — Enable/disable flows from HA UI; flow status entities — [reported, smartbolig.net 2026]

### 9.3 When to Use Node-RED vs. HA Automations

| Use HA Automations | Use Node-RED |
|---------------------|--------------|
| Simple trigger→action | Complex multi-step logic |
| UI editor handles it | Loops, variables, functions |
| Scenes, scripts, templates | API calls, HTTP, MQTT workflows |
| Critical (alarm, security) | Visible debugging (live msg object) |

**Key Gap:** Node-RED flows.json not version-controlled by default (HA YAML is) — [reported, bigiron.cc 2026-06-16]

### 9.4 2026 Ecosystem

- **`app-node-red` Docker addon** v22.2.2 (Nov 2026) — [reported, selfhost.directory]
- **Yandex Alice** node-red-contrib-alice v3.0.4 (WebSocket, IoT Core shutdown Nov/Dec 2026) — [reported, flows.nodered.org 2026]

---

## 10. Grafana 11 — 2026 State

### 10.1 Key v11 Features (Released 2024, current in 2026)

| Feature | Status | Notes |
|---------|--------|-------|
| **AI-generated panel/dashboard titles & descriptions** | GA all editions | Generative AI assist in edit mode |
| **Tempo Search powered by TraceQL** | GA | Replaces old search; unified query language |
| **Loki Search tab removed** | Removed | Use LogQL in Explore |
| **Old Tempo Search tab removed** | Removed | TraceQL-only |
| **MSSQL: Windows AD (Kerberos) auth** | GA | Enterprise |
| **Alert rule provisioning API roles** | GA | Rules Writer, Set Provisioning status |
| **Anonymous access licensing change** | Enterprise | Billed per anonymous user |

### 10.2 LGTM Stack (2026 Versions)

| Component | Version | Role |
|-----------|---------|------|
| **Grafana** | 11.x / 13.x (latest) | Visualization, alerting, dashboards |
| **Loki** | 3.x | Log aggregation (LogQL, metrics from logs, alerting) |
| **Tempo** | 3.x | Distributed tracing (TraceQL, service graphs, metrics from spans) |
| **Mimir** | 2.x | Metrics (PromQL, high cardinality, long-term storage) |
| **Pyroscope** | 1.x | Continuous profiling |
| **Alloy** | 1.x | OTel collector replacement (vendor-neutral) |
| **Beyla** | 1.x | eBPF auto-instrumentation |
| **Faro** | 1.x | Frontend observability |

### 10.3 HA + Grafana Integration Patterns

| Pattern | Description |
|---------|-------------|
| **Prometheus + HA** | `prometheus` HA integration scrapes HA metrics → Grafana |
| **InfluxDB + HA** | HA `influxdb` integration → Grafana (Flux/InfluxQL) |
| **Loki + HA** | `loki` HA integration (logs) → Grafana |
| **Tempo + HA** | OpenTelemetry collector on HA host → Tempo → Grafana |
| **Direct SQLite** | Grafana SQLite plugin reads HA `home-assistant_v2.db` (read-only) |

**Recommendation for NOMAD:** **Prometheus (HA) + Loki (logs) + Grafana 11** on same host or dedicated monitoring VM. Use **Grafana Alloy** for unified telemetry collection.

---

## 11. NOMAD Hyper — Integration Architecture Recommendations

### 11.1 Power Layer (Primary)

```
Solar Array → Victron SmartSolar MPPT (Bluetooth + VE.Direct)
                    ↓
             Cerbo GX (MQTT broker, Modbus TCP)
                    ↓
         ┌──────────┴──────────┐
         ↓                     ↓
   Home Assistant         Grafana 11
   (victron_gx MQTT)      (Prometheus/Loki)
         ↓                     ↓
   Energy Dashboard      LGTM Dashboards
   Automations           Alerting
```

**Why Victron over EPEver?** Official HA `victron_gx` (platinum, bidirectional), mature VRM, DVCC with Lynx Smart BMS, proven mobile/off-grid.

### 11.2 Battery Layer

```
LiFePO4 Pack (16S/24S/32S) → JK BMS (Active 2A balance, CAN/RS485/BLE)
                                    ↓
                              batmon-ha (BLE→MQTT)
                                    ↓
                              Home Assistant
                              Energy Dashboard
                              SOC/Cell voltage/Temp
                              Charge/Discharge control
```

**Why JK BMS?** Active balancing essential for large packs; CAN enables inverter closed-loop; best HA/ESPHome support.

### 11.3 UPS / Host Layer

```
Raspberry Pi 5 (HAOS) → Waveshare UPS Module 3S (3×18650, I2C)
                              ↓
                       HACS waveshare_ups_hat
                              ↓
                       Home Assistant
                       Battery % / V / I / Power
                       Safe shutdown automation
```

### 11.4 Environmental Sensor Layer

```
ESP32-C3 (ESPHome) × N nodes
   ├── SCD41 (CO₂ + T/RH) — I²C
   ├── SBM-20/M4011 Geiger — Pulse counter (ESPGeiger firmware)
   ├── DS18B20 (Water temp) — 1-Wire
   ├── Atlas EZO-pH/EC/DO — UART (AquaPi) OR DFRobot Gravity — Analog
   └── BME280/AHT2x (Ambient) — I²C (auto-detected by ESPGeiger)
           ↓
      MQTT / ESPHome API
           ↓
      Home Assistant → Grafana
```

### 11.5 Wind Supplement (Optional)

```
Micro Wind Turbine (500W, 24V/48V) → Victron SmartSolar MPPT (DC-coupled)
                                          ↓
                                   Cerbo GX → HA
```

**Only if:** Site wind resource >5 m/s annual average; winter solar <20% summer.

---

## 12. Price Summary (2026 USD, Approximate)

| Component | Qty | Unit Cost | Total | Source |
|-----------|-----|-----------|-------|--------|
| Victron SmartSolar 150/45 | 2 | $350 | $700 | Reported |
| Cerbo GX | 1 | $248 | $248 | Reported |
| Cerbo GX Touch 50 | 1 | $230 | $230 | Reported |
| SmartShunt 500A | 1 | $107 | $107 | Reported (Victron pricelist) |
| JK BMS B2A16S20P (16S 200A) | 1 | $185 | $185 | Reported (shop.jkbms.com) |
| JK BMS B2A32SRP (32S 300A) | 1 | $274 | $274 | Reported |
| Waveshare UPS Module 3S | 1 | $55 | $55 | Reported |
| 18650 cells (3×) | 3 | $8 | $24 | Inferred |
| ESP32-C3 dev boards | 4 | $12 | $48 | Inferred |
| Sensirion SCD41 modules | 4 | $25 | $100 | Reported (SOS electronic €18.68) |
| SBM-20 Geiger tubes | 2 | $30 | $60 | Inferred |
| M4011 Geiger tubes | 2 | $45 | $90 | Inferred |
| Atlas EZO-pH + EC + DO | 1 set | $350 | $350 | Reported (AquaPi) |
| DFRobot Gravity pH + TDS | 1 set | $45 | $45 | Reported (Cultivee R$595 ≈ $100) |
| DS18B20 waterproof | 6 | $8 | $48 | Inferred |
| Pikasola 500W wind turbine | 1 | $270 | $270 | Reported (theroundup.org) |
| **Subtotal (Core)** | | | **$2,834** | |
| **Subtotal (With Wind)** | | | **$3,104** | |

*Excludes: Battery cells (LFP 280Ah/314Ah × 16–32 = $3,000–$10,000), wiring, fuses, enclosures, mounting, labor.*

---

## 13. Open Questions / Validation Needed

| # | Question | Priority | Method |
|---|----------|----------|--------|
| 1 | JK BMS CAN protocol compatibility with Victron DVCC (closed-loop charge) | High | Test with Cerbo GX + MultiPlus II + JK BMS CAN |
| 2 | ESPGeiger + ESPHome native API vs. MQTT reliability on HAOS | Medium | Deploy 2 nodes, compare uptime |
| 3 | EPEver Tracer-AN G3 4G module (new 2025) — HA via Modbus TCP over 4G | Low | Check if eBox-4G exists; test latency |
| 4 | SCD41 single-shot mode (low power) battery life on ESP32-C3 + 18650 | Medium | Bench test: measure current, project runtime |
| 5 | Victron `victron_ble` vs `victron_gx` entity parity (what's missing in BLE?) | High | Compare entity lists on test system |
| 6 | Grafana Alloy config for HA + Victron + ESPHome unified pipeline | Medium | Prototype Alloy config; test Loki/Tempo/Pyroscope |
| 7 | Wind turbine MPPT voltage window vs. Victron SmartSolar input range | High | Match turbine Vmp/Voc to MPPT specs before purchase |

---

## 14. Sources Index

| # | Source | Type | Date | Topics |
|---|--------|------|------|--------|
| 1 | optisolex.com blog | Reported | 2026 | MPPT comparison |
| 2 | renogy.com buyers guide | Reported | 2026-10-22 | Rover 2 vs Victron pricing |
| 3 | techfinepv.com | Reported | 2026 | 10 manufacturers guide |
| 4 | HA Community (renogy-ble) | Reported | 2026-01-08 | Renogy HA integration |
| 5 | epever.com | Reported | 2025-12-05 | Tracer-AN G3 manual |
| 6 | insumenergy.com | Reported | 2026 | JK/Daly/JBD BMS comparison |
| 7 | GitHub fl4p/batmon-ha | Reported | 2026 | BMS HA addon |
| 8 | shop.jkbms.com | Reported | 2026 | JK BMS pricing |
| 9 | GobelPower.com | Reported | 2026 | Pace/JK HA addon |
| 10 | HA Community (Waveshare UPS) | Reported | 2026 | UPS HAT integration |
| 11 | YouTube (Pi 5 + UPS 3S) | Reported | 2026 | UPS Module 3S demo |
| 12 | PiShop US | Reported | 2026 | UPS HAT catalog |
| 13 | nedes.us | Reported | 2026 | Home wind turbine guide |
| 14 | Victron Community | Reported | 2023/2026 | Wind + Victron DC-coupling |
| 15 | solartechonline.com | Reported | 2025 | Residential wind guide |
| 16 | theroundup.org | Reported | 2026 | Best home wind turbines |
| 17 | 365techies.co.uk | Reported | 2026 | Victron GX + HA guide |
| 18 | Alchemy Industrial | Reported | 2026 | Cerbo/Ekrano pricing |
| 19 | HA docs (victron_gx) | Reported | 2026 | Official integration |
| 20 | YouTube (Smarty Van) | Reported | 2024-11-16 | Victron MQTT HA |
| 21 | HA Community (Victron guide) | Reported | 2026 | Victron + EMHASS |
| 22 | Victron docs (Cerbo config) | Reported | 2026 | MQTT/Modbus enable |
| 23 | DIY Solar Forum | Reported | 2026 | Cerbo GX HA integration |
| 24 | Victron pricelist 2026-Q3 | Reported | 2026-07-02 | Official EUR pricing |
| 25 | VictronConnect changelog | Reported | 2026-11-06/09 | Firmware updates |
| 26 | ESPHome devices (EPEver) | Reported | 2026 | ESPHome Modbus config |
| 27 | GitHub gabrielpc1190 | Reported | 2020/2026 | EPEver eBox-WIFI HA |
| 28 | EPEver datasheets | Reported | 2020–2025 | Tracer-AN/BN specs |
| 29 | SOS electronic | Reported | 2026-11-27 | Sensirion SCD30/40/41 pricing |
| 30 | ESPHome docs (scd30/scd4x/mhz19) | Reported | 2026-10 | Native sensor support |
| 31 | hardwarematrix.dev | Reported | 2026-09-13 | Sensor compatibility matrix |
| 32 | esp32.co.uk | Reported | 2026-09-23 | SCD40 vs SCD41 guide |
| 33 | nodrix.live | Reported | 2026-07-18 | SCD41 ESP32 build |
| 34 | computingforgeeks.com | Reported | 2026-10-30 | Best AQ monitor HA |
| 35 | OpenELAB / littlebirdelectronics | Reported | 2026 | Gravity Geiger M4011 |
| 36 | rottenwifi.com | Reported | 2026-09-27 | DIY Geiger guide |
| 37 | IoT-devices (GGreg20_V3) | Reported | 2026 | SBM-20 detector |
| 38 | GitHub steadramon/ESPGeiger | Reported | 2026 | ESPGeiger firmware |
| 39 | docs.espgeiger.com | Reported | 2026 | ESPGeiger docs |
| 40 | screek.io | Reported | 2026 | Water sensor WS2 |
| 41 | smarthomeshop.io | Reported | 2026-07-11 | WaterP1MeterKit HA |
| 42 | smarthomescene.com | Reported | 2026-09-25 | Tuya 7-in-1 water review |
| 43 | AquaPi (therealfalsereality) | Reported | 2026 | Atlas EZO + ESPHome |
| 44 | cultivee.com.br | Reported | 2026-07-20 | Hydroponics ESP32 DIY |
| 45 | GitHub ha-flipr-local | Reported | 2026-04-01 | Flipr pool BLE HA |
| 46 | expert4house.com | Reported | 2026 | Tuya 6-in-1 WiFi water |
| 47 | dev.to (turtle tank) | Reported | 2026-10-10 | ESP32-C3 water monitor |
| 48 | HA blog 2026.10 | Reported | 2026-10-07 | Release notes |
| 49 | HA blog 2026.3 | Reported | 2026-03-04 | Release notes |
| 50 | releasebot.io | Reported | 2026-11-05 | 2026.11 preview |
| 51 | HA blog 2026.11 | Reported | 2026-11-04 | 2026.11 release |
| 52 | howtogeek.com | Reported | 2026-11-04 | 2026.11 Marketplace |
| 53 | HA energy docs | Reported | 2026 | Energy dashboard guide |
| 54 | HA blog 2026.2 | Reported | 2026-02-04 | Release notes |
| 55 | Electricity Maps integration | Reported | 2026 | Carbon intensity |
| 56 | allthethings.best | Reported | 2026-09-09 | 2026.9 release |
| 57 | raspberry.tips | Reported | 2026-10-21 | Node-RED HA guide |
| 58 | selfhost.directory | Reported | 2026-11-01 | Node-RED 4.1.17 |
| 59 | softwr.com | Reported | 2026-08-30 | HA vs Node-RED |
| 60 | bigiron.cc | Reported | 2026-06-16 | Node-RED vs HA automations |
| 61 | smartbolig.net | Reported | 2026-06-02 | Node-RED HA setup |
| 62 | Grafana v11 whatsnew | Reported | 2024/2026 | Grafana 11 features |
| 63 | Grafana Loki/Tempo/Mimir docs | Reported | 2026-07-29 | LGTM stack |
| 64 | Grafana Stack page | Reported | 2026 | LGTM+ overview |
| 65 | HA integrations (victron_ble/gx) | Reported | 2026 | Official docs |
| 66 | technikheim.de | Reported | 2026-09-24 | Victron HA pathways (DE) |
| 67 | victron-ble2mqtt PyPI | Reported | 2026-09-28 | BLE→MQTT bridge |
| 68 | TSolar / TSolar.top | Reported | 2026 | EPEver eBox pricing |
| 69 | accio.com | Reported | 2026 | eBox BLE/WIFI pricing |
| 70 | solarepic.com | Reported | 2026 | eBox specs |
| 71 | energiatal.com.br | Reported | 2026 | eBox-WIFI-01 BR |
| 72 | invertersrus.com | Reported | 2022/2026 | eBox-WIFI-01 US |
| 73 | craigsolar.co.uk | Reported | 2025 | eBox-BLE-01 UK |
| 74 | roiinstitute.net | Reported | 2026 | eBox-WIFI-01 |
| 75 | nomadpower.com | Reported | 2026-08-19 | NOMAD UL9540 cert |
| 76 | SEC filing 8-K/A | Reported | 2026-09-17 | NOMAD Voyager platform |
| 77 | NASO presentation | Reported | 2024-02-07 | NOMAD Transportable |
| 78 | srnesolar.com | Reported | 2022 | SRNE monitoring |
| 79 | indiott.com | Reported | 2026-08-28 | Off-grid power budgets |
| 80 | meteocontrol VCOM | Reported | 2026-10-03 | Battery monitoring mandatory |
| 81 | nomadamerica.energy | Reported | 2026 | Nomad Energy America |
| 82 | myriota.com | Reported | 2025-06-27 | Satellite IoT solar |
| 83 | kritikalsolutions.com | Reported | 2026-09-04 | IoT solar monitoring |
| 84 | linksolar.net | Reported | 2026-08-11 | Remote solar sizing guide |

---

## 15. Next Actions for NOMAD Hyper

1. **Order Victron SmartSolar 150/45 ×2 + Cerbo GX + Touch 50 + SmartShunt 500A** — core power monitoring
2. **Order JK BMS B2A16S20P (16S 200A) + B2A32SRP (32S 300A)** — evaluate both for different pack sizes
3. **Build ESPGeiger prototype (ESP32 + SBM-20)** — validate MQTT/HA auto-discovery
4. **Build ESPHome SCD41 node (ESP32-C3)** — validate CO₂ + T/RH + battery life
5. **Deploy Grafana 11 + Alloy + Loki + Tempo + Mimir** on monitoring VM — unified observability
6. **Test Victron `victron_gx` MQTT entity completeness** vs. `victron_ble` — decide GX requirement
7. **Evaluate wind resource at deployment sites** — only proceed if >5 m/s annual avg
8. **Document integration configs in Git (YAML + Node-RED flows.json backup)** — version control

---

*End of Research Document*  
*Generated 2026-11-11 for NOMAD Hyper project*