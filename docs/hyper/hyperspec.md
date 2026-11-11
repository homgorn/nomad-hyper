# PROJECT N.O.M.A.D. — HYPER SPECIFICATION v2.0
### Node for Offline Media, Archives, and Data
**Дата:** Март 2026 | **Статус:** Living Document | **Лицензия:** Apache 2.0

---

## СОДЕРЖАНИЕ

1. [Обзор и концепция](#1-обзор-и-концепция)
2. [AI-стек — Qwen3.5 (март 2026)](#2-ai-стек--qwen35-март-2026)
3. [Claude Agent SDK — Агенты и Суб-агенты](#3-claude-agent-sdk--агенты-и-суб-агенты)
4. [Skills — Навыки агентов](#4-skills--навыки-агентов)
5. [IoT-экосистема — датчики и автоматизация](#5-iot-экосистема--датчики-и-автоматизация)
6. [LoRa / Meshtastic — офлайн mesh-связь](#6-lora--meshtastic--офлайн-mesh-связь)
7. [Спутниковая связь](#7-спутниковая-связь)
8. [Радио-интернет и SDR](#8-радио-интернет-и-sdr)
9. [Автономное питание — Солнце + LiFePO4](#9-автономное-питание--солнце--lifepo4)
10. [Уведомления — push на телефон](#10-уведомления--push-на-телефон)
11. [Мобайл — чаты, карты, задачи](#11-мобайл--чаты-карты-задачи)
12. [Полный Docker стек — все контейнеры](#12-полный-docker-стек--все-контейнеры)
13. [Архитектура агентной системы NOMAD](#13-архитектура-агентной-системы-nomad)
14. [Скрипты автоматизации](#14-скрипты-автоматизации)
15. [Каталог железа — ссылки и цены](#15-каталог-железа--ссылки-и-цены)
16. [HYPER ИНСТРУКЦИИ — Сборка с нуля](#16-hyper-инструкции--сборка-с-нуля)

---

## 1. ОБЗОР И КОНЦЕПЦИЯ

Project N.O.M.A.D. — самодостаточный офлайн-узел знаний, AI и коммуникаций.
Репозиторий: https://github.com/Crosstalk-Solutions/project-nomad

### Целевые сценарии
- **Emergency Prep** — инфраструктура упала, интернет недоступен, нужны знания и связь
- **Off-Grid** — кабин, RV, яхта, горная экспедиция (актуально для Кыргызстана)
- **Field Operations** — поисково-спасательные операции, военизированные сценарии
- **Education** — офлайн-обучение в районах без связи

### Принципы архитектуры v2.0
1. **Всё офлайн** — нет зависимости от внешних сервисов в рантайме
2. **Docker-first** — каждый компонент в контейнере, изолирован, обновляем
3. **Agent-first** — AI не просто чат, а агент с инструментами и суб-агентами
4. **IoT-native** — датчики и автоматизация встроены с первого дня
5. **Multi-layer comm** — WiFi LAN + LoRa mesh + спутник + HF радио

---

## 2. AI-СТЕК — QWEN3.5 (МАРТ 2026)

### 2.1 Семейство Qwen3.5 — что это

Alibaba выпустила Qwen3.5 в три волны:
- **Флагман (16 февраля 2026):** Qwen3.5-397B-A17B
- **Средние модели (24 февраля 2026):** 27B, 35B-A3B, 122B-A10B
- **Малые модели (2 марта 2026):** 0.8B, 2B, 4B, 9B

Ключевые особенности всего семейства:
- Нативный мультимодал: текст + изображения + видео (ранняя fusion-архитектура)
- Thinking + No-thinking режимы на всех размерах
- 201 язык и диалект (vs 119 у Qwen3)
- 256K контекст, расширяемый до 1M токенов
- Нативный tool calling и agentic coding
- Apache 2.0 лицензия — полностью свободный коммерческий use

Qwen3.5 — первая открытая модель с unified vision-language training от первого токена.
Источник: https://techie007.substack.com/p/qwen-35-the-complete-guide-benchmarks

### 2.2 Таблица моделей для NOMAD

| Модель | Параметры | RAM/VRAM | Железо | Особенность |
|--------|-----------|----------|--------|-------------|
| `qwen3.5:0.8b` | 0.8B | 2GB VRAM / 3GB RAM | RPi4, телефон | Под 2GB, edge-устройства |
| `qwen3.5:2b` | 2B | 3GB VRAM / 5GB RAM | RPi5, планшет | Быстрый инференс |
| `qwen3.5:4b` | 4B | 4GB VRAM / 8GB RAM | RPi5 8GB | Мультимодал база, 262K ctx |
| `qwen3.5:9b` | 9B | 8GB VRAM / 16GB RAM | RTX3060 8GB | Звезда: бьёт 120B модели |
| `qwen3.5:27b` | 27B | 22GB VRAM | RTX3090 / 32GB RAM | Dense, без MoE overhead |
| `qwen3.5:35b-a3b` | 35B / 3B active | 8GB VRAM | RTX3060! | MoE: умный как 35B, быстрый как 3B |
| `qwen3.5:122b-a10b` | 122B / 10B active | 80GB | A100 / A6000 | Sweet spot для серверов |
| `qwen3.5:397b-a17b` | 397B / 17B active | 8× A100 | Кластер | Frontier-уровень офлайн |

**Для типичного NOMAD (RTX3060 12GB + 32GB RAM):**
- Основная модель: `qwen3.5:9b` — лучший баланс скорость/качество
- Альтернатива: `qwen3.5:35b-a3b` — нужно 8GB VRAM, умнее при той же скорости
- Лёгкая задача / быстрый ответ: `qwen3.5:2b`

**Для NOMAD RPi5 (8GB RAM, без GPU):**
- Основная: `qwen3.5:4b` (CPU-only, ~4-6 tok/s)
- Запасная: `qwen3.5:2b` (быстрее, для простых запросов)

**Важно:** Qwen3.5 Small series (0.8B–9B) thinking отключён по умолчанию.
Для включения через llama.cpp: `--chat-template-kwargs '{"enable_thinking":true}'`
Источник: https://unsloth.ai/docs/models/qwen3.5

### 2.3 Команды установки

```bash
# Основная мультимодальная модель
ollama pull qwen3.5:9b

# Малая для edge-устройств
ollama pull qwen3.5:0.8b
ollama pull qwen3.5:2b
ollama pull qwen3.5:4b

# MoE модель (требует 8GB VRAM)
ollama pull qwen3.5:35b-a3b

# Проверка
ollama list
ollama run qwen3.5:9b "Опиши симптомы аппендицита"

# Тест с изображением (через API)
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3.5:9b",
  "messages": [{
    "role": "user",
    "content": "Что на этом фото?",
    "images": ["<base64_image>"]
  }]
}'
```

### 2.4 Важное замечание по Vision

Внимание: на март 2026, Qwen3.5 GGUF-версии (для llama.cpp и Ollama) имеют
отдельные mmproj-файлы для vision. Нативный Ollama pull может не включать
vision автоматически. Используй llama-server или Unsloth Studio для гарантии.

Источник: https://unsloth.ai/docs/models/qwen3.5

Рекомендуем также: `llama-server --model qwen3.5-9b.gguf --mmproj qwen3.5-mmproj.gguf`

### 2.5 Дополнительные модели для специализаций

```bash
# Голосовой STT (Speech-to-Text) — офлайн
# whisper.cpp через Docker
docker pull ghcr.io/ggerganov/whisper.cpp

# TTS (Text-to-Speech) — офлайн
# Piper — 60+ языков, модели <5MB
pip install piper-tts
piper --model ru_RU-irina-medium --output_file speech.wav <<< "Привет NOMAD"

# Embedding модель для RAG (офлайн)
ollama pull nomic-embed-text    # 274MB, лучший офлайн embedding
ollama pull mxbai-embed-large   # 670MB, точнее для длинных текстов
```

---

## 3. CLAUDE AGENT SDK — АГЕНТЫ И СУБ-АГЕНТЫ

### 3.1 Что такое Claude Agent SDK

Claude Agent SDK (бывший Claude Code SDK, переименован осень 2025) — runtime для
создания автономных агентов. Это то же ядро, что работает внутри Claude Code.

Версии на март 2026: Python v0.1.48 на PyPI, TypeScript v0.2.71 на npm.
Источник: https://letsdatascience.com/blog/claude-agent-sdk-tutorial

**Почему это нужно NOMAD:**
- Агент может сам решать задачи: скачать ZIM, проиндексировать в RAG,
  отправить уведомление, проверить здоровье системы, ответить на LoRa-сообщение
- Суб-агенты работают параллельно и изолированно
- Полная поддержка MCP серверов (подключение внешних инструментов)

### 3.2 Установка

```bash
# Python
pip install claude-agent-sdk

# TypeScript / Node
npm install @anthropic-ai/claude-agent-sdk
```

Документация: https://platform.claude.com/docs/en/agent-sdk/overview
GitHub Python: https://github.com/anthropics/claude-agent-sdk-python
npm package: https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk

### 3.3 Базовый агент — Python

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def nomad_agent(task: str):
    async for message in query(
        prompt=task,
        options=ClaudeAgentOptions(
            allowed_tools=["Bash", "Read", "Write", "Glob"],
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(nomad_agent("Проверь статус всех Docker контейнеров NOMAD"))
```

### 3.4 Суб-агенты — параллелизация и изоляция контекста

Суб-агенты решают две задачи:
1. **Параллелизация** — несколько задач одновременно
2. **Изоляция контекста** — каждый суб-агент имеет свой контекст,
   возвращает только релевантное

Источник: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk

Sweet spot по документации Anthropic: **2–5 суб-агентов, 5–6 задач каждый**.
Команды с >5 агентов теряют координационное преимущество.

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

# Главный оркестратор NOMAD
async def nomad_orchestrator():
    """
    Главный агент запускает суб-агентов параллельно:
    - health_checker: мониторинг контейнеров
    - rag_indexer: индексирование новых документов
    - meshtastic_handler: обработка LoRa сообщений
    - weather_fetcher: получение погоды через SDR/NOAA
    """

    task = """
    Ты — оркестратор NOMAD. Запусти параллельно следующие задачи:
    1. Проверь статус Docker контейнеров (bash: docker ps)
    2. Найди новые PDF в /nomad/incoming/ и добавь их в RAG
    3. Проверь очередь Meshtastic сообщений в /tmp/meshtastic_queue/
    4. Отправь health-отчёт через ntfy: curl -d 'All OK' http://localhost:8088/health
    Используй суб-агентов для параллельного выполнения.
    """

    async for message in query(
        prompt=task,
        options=ClaudeAgentOptions(
            allowed_tools=["Bash", "Read", "Write", "Glob", "mcp__nomad-tools"],
            setting_sources=["user", "project"],  # загрузка Skills
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(nomad_orchestrator())
```

### 3.5 Специализированные агенты для NOMAD

```python
# agents/medical_agent.py
MEDICAL_AGENT_PROMPT = """
Ты — медицинский ассистент NOMAD.
Ты имеешь доступ к:
- Оффлайн базе знаний Merck Manual (через RAG)
- WHO Essential Medicines list
- First Aid ZIM коллекции Kiwix
- Возможности анализировать фотографии через qwen3.5

Всегда отвечай: "Это не замена врачу. При возможности обратитесь к специалисту."
При описании симптомов:
1. Определи вероятный диагноз
2. Укажи срочность (немедленно / в течение часа / можно подождать)
3. Дай первичные действия
4. Процитируй источник из RAG базы
"""

# agents/survival_agent.py
SURVIVAL_AGENT_PROMPT = """
Ты — эксперт по выживанию NOMAD.
Доступ к: SAS Survival Guide (ZIM), Wilderness Medicine, iFixit, Bushcraft guides.
Учитывай регион (горы Кыргызстана), сезон, имеющееся оборудование.
"""

# agents/navigation_agent.py
NAVIGATION_AGENT_PROMPT = """
Ты — навигационный агент NOMAD.
Доступ к: OpenStreetMap тайлам, треки местности, ADS-B данным (самолёты),
  APRS позициям (если SDR включён), Meshtastic GPS-координатам.
"""

# agents/tech_repair_agent.py
TECH_REPAIR_AGENT_PROMPT = """
Ты — технический агент NOMAD.
Доступ к: iFixit ZIM, Arduino документации, ESP32 даташитам,
  Схемам контроллеров заряда, datasheet базе.
Можешь анализировать фото плат и схем через qwen3.5 vision.
"""

# agents/comms_agent.py
COMMS_AGENT_PROMPT = """
Ты — агент коммуникаций NOMAD.
Контролируешь: Meshtastic mesh сеть, статус LoRa узлов, Matrix Synapse чат,
  очередь ntfy уведомлений, статус Starlink/Iridium.
При входящем Meshtastic сообщении — парсишь и отправляешь в Matrix канал.
"""
```

### 3.6 Multi-agent система — архитектура

```
NOMAD Orchestrator Agent (Claude Agent SDK)
├── health_agent         — мониторинг системы каждые 5 минут
├── rag_agent            — индексирование новых документов
├── meshtastic_agent     — получение/отправка LoRa сообщений
├── iot_agent            — обработка MQTT данных с датчиков
├── notification_agent   — отправка алертов через ntfy
├── medical_agent        — ответы на медицинские запросы
├── survival_agent       — инструкции по выживанию
├── navigation_agent     — карты и маршруты
├── tech_repair_agent    — ремонт оборудования
└── comms_agent          — управление коммуникациями
```

---

## 4. SKILLS — НАВЫКИ АГЕНТОВ

### 4.1 Что такое Skills

Skills — filesystem-based пакеты экспертизы для Claude Agent SDK.
Создаются как директории с файлом `SKILL.md`.
Агент автоматически обнаруживает и применяет Skills.

Источник: https://platform.claude.com/docs/en/agent-sdk/skills

### 4.2 Включение Skills

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for msg in query(
    prompt="...",
    options=ClaudeAgentOptions(
        allowed_tools=["Bash", "Read", "Skill"],  # Skill в allowed_tools!
        setting_sources=["user", "project"],       # загрузка из filesystem
    ),
):
    ...
```

### 4.3 Структура директорий Skills для NOMAD

```
/opt/project-nomad/
└── .claude/
    └── skills/
        ├── medical/
        │   ├── SKILL.md          # инструкции агенту
        │   ├── medications.json  # база лекарств
        │   └── symptoms.json     # база симптомов
        ├── meshtastic/
        │   ├── SKILL.md
        │   └── send_message.sh   # скрипт отправки
        ├── iot-sensors/
        │   ├── SKILL.md
        │   └── read_sensors.py   # чтение через MQTT
        ├── zim-search/
        │   ├── SKILL.md
        │   └── search_kiwix.py   # поиск по ZIM
        ├── solar-monitor/
        │   ├── SKILL.md
        │   └── battery_status.py # статус батарей
        └── nomad-comms/
            ├── SKILL.md
            └── send_ntfy.sh      # отправка уведомлений
```

### 4.4 Пример SKILL.md — Meshtastic

```markdown
# Meshtastic Communication Skill

## Purpose
Send and receive messages via LoRa mesh network through connected Meshtastic device.

## When to use
- User asks to send a message to someone in the field
- User asks about status of mesh network nodes
- Incoming LoRa message needs processing

## Tools available
- send_message.sh <channel> <message> — отправить сообщение
- list_nodes.sh — список активных узлов сети
- get_messages.sh — получить последние сообщения

## Example usage
User: "Отправь Саше что мы выходим через 2 часа"
→ Run: ./send_message.sh group "Выходим через 2 часа"

## Node information
Channel 0: primary (все участники)
Channel 1: admin (только координаторы)
Frequency: 433MHz (настроено для КГ)
```

### 4.5 Пример SKILL.md — Solar Monitor

```markdown
# Solar Power Monitor Skill

## Purpose
Monitor battery status, solar input, and power consumption of NOMAD system.

## Metrics available
- battery_voltage: текущее напряжение батареи (12V LiFePO4)
- battery_percent: уровень заряда в %
- solar_watts: мощность от солнечной панели
- load_watts: текущее потребление
- time_remaining: прогноз автономности

## Thresholds
- CRITICAL: battery < 20% → отключить Ollama, оставить только core
- WARNING: battery < 40% → уведомить через ntfy
- OPTIMAL: solar > load → записать излишек, зарядить

## Data source
MQTT topic: nomad/sensors/power
INA226 sensor on ESP32, обновление каждые 30 секунд
```

---

## 5. IoT-ЭКОСИСТЕМА — ДАТЧИКИ И АВТОМАТИЗАЦИЯ

### 5.1 Стек IoT

```
ESP32/Arduino → MQTT/Mosquitto → Home Assistant → Grafana/InfluxDB
                                 ↓
                          Claude Agent SDK (iot_agent)
                                 ↓
                          ntfy уведомления
```

### 5.2 Home Assistant + MQTT

```bash
# docker-compose фрагмент
services:
  homeassistant:
    image: homeassistant/home-assistant:stable
    container_name: nomad-hass
    restart: unless-stopped
    volumes:
      - ./config/hass:/config
    network_mode: host
    privileged: true

  mosquitto:
    image: eclipse-mosquitto:2
    container_name: nomad-mqtt
    restart: unless-stopped
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./config/mosquitto:/mosquitto/config
      - ./data/mosquitto:/mosquitto/data
```

### 5.3 ESP32 прошивка для датчиков (Arduino/MicroPython)

```python
# micropython для ESP32 — отправка данных через MQTT
import network
import time
from umqtt.simple import MQTTClient
import dht  # DHT22 датчик

# Конфиг
WIFI_SSID = "NOMAD"           # имя WiFi точки NOMAD
WIFI_PASS = "nomad2026"
MQTT_BROKER = "192.168.100.1"  # IP NOMAD сервера
DEVICE_ID = "esp32-01"

# Датчики
sensor_temp = dht.DHT22(machine.Pin(4))  # Пин D4
sensor_voltage = machine.ADC(machine.Pin(34))  # аналоговый вход

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        time.sleep(0.5)

def main():
    connect_wifi()
    client = MQTTClient(DEVICE_ID, MQTT_BROKER)
    client.connect()

    while True:
        sensor_temp.measure()
        temp = sensor_temp.temperature()
        humidity = sensor_temp.humidity()
        voltage = sensor_voltage.read() * 3.3 / 4095 * 4  # делитель напряжения

        # Публикация в MQTT
        client.publish(f"nomad/sensors/{DEVICE_ID}/temperature", str(temp))
        client.publish(f"nomad/sensors/{DEVICE_ID}/humidity", str(humidity))
        client.publish(f"nomad/sensors/{DEVICE_ID}/battery_voltage", str(voltage))

        time.sleep(30)  # каждые 30 секунд

main()
```

### 5.4 Node-RED — автоматизации без кода

```bash
docker run -p 1880:1880 \
  -v /opt/project-nomad/data/nodered:/data \
  --name nomad-nodered \
  --restart unless-stopped \
  nodered/node-red
```

Примеры автоматизаций в Node-RED:
- MQTT сенсор батареи < 20% → отправить ntfy + отключить Ollama
- Новый Meshtastic пакет → парсить → отправить в Matrix канал
- Температура CPU > 75°C → снизить ollama concurrency
- Новый файл в /incoming/ → запустить RAG индексирование

### 5.5 Список датчиков с ценами

| Датчик | Что измеряет | Цена | Ссылка |
|--------|-------------|------|--------|
| DHT22 | Температура + влажность воздуха | $3–5 | https://www.aliexpress.com/w/wholesale-DHT22.html |
| BME280 | Температура + влажность + давление + высота | $3–6 | https://www.aliexpress.com/w/wholesale-BME280.html |
| SCD41 | CO2 (точный) | $25–35 | https://www.amazon.com/s?k=SCD41+CO2+sensor |
| DS18B20 | Температура воды/почвы/трубы | $2–4 | https://www.aliexpress.com/w/wholesale-DS18B20.html |
| INA226 | Ток + напряжение (батарея/солнце) | $4–7 | https://www.amazon.com/s?k=INA226+module |
| HC-SR501 | Движение (PIR) | $1–3 | https://www.aliexpress.com/w/wholesale-HC-SR501.html |
| MQ-135 | Качество воздуха / газы | $3–5 | https://www.aliexpress.com/w/wholesale-MQ-135.html |
| JS-DC008 | Датчик воды / дождя | $2–4 | AliExpress |
| ESP32 DevKit | WiFi + BLE контроллер | $5–8 | https://www.aliexpress.com/w/wholesale-esp32-devkit.html |
| Arduino Mega 2560 | GPIO контроллер | $10–15 | https://www.amazon.com/s?k=arduino+mega+2560 |

---

## 6. LORA / MESHTASTIC — ОФЛАЙН MESH-СВЯЗЬ

### 6.1 Почему Meshtastic — killer feature NOMAD

LoRa (Long Range) + mesh = связь без инфраструктуры.
- Дальность: 5–25 км на узел, прямая видимость
- Каждый узел = ретранслятор сети
- Зашифрованные каналы
- GPS-трекинг всех участников
- Работает на ISM диапазонах: 433 MHz или 868 MHz (без лицензии в большинстве стран)

Для Кыргызстана: 433 MHz (ISM диапазон, малая мощность — без лицензии)
Официальный сайт: https://meshtastic.org

### 6.2 Железо Meshtastic — таблица выбора

| Устройство | Чип | GPS | Дисплей | Батарея | Цена | Ссылка |
|-----------|-----|-----|---------|---------|------|--------|
| LILYGO T-Beam Supreme | ESP32-S3 + SX1262 | u-blox M10S | OLED 1.3" | 18650 | $45–65 | https://lilygo.cc/en-us/products/t-beam-supreme-meshtastic |
| LILYGO T-Beam V1.2 | ESP32 + SX1276 | NEO-6M | OLED 0.96" | 18650 | $30–45 | https://lilygo.cc/products/t-beam-meshtastic |
| LILYGO T-Echo | NRF52840 + SX1262 | L76K | e-Paper | встроен | $45–65 | Rokland Store |
| Heltec WiFi LoRa 32 V3 | ESP32-S3 + SX1262 | нет | OLED 0.96" | внешний | $20–30 | https://www.amazon.com/s?k=Heltec+LoRa+V3+meshtastic |
| RAKwireless WisBlock | nRF52840 | модуль | модуль | модуль | $40–80 | https://store.rokland.com/pages/meshtastic-hardware-rak-lilygo |

**Рекомендация для NOMAD:**
- Стационарный узел (на NOMAD сервере): T-Beam Supreme + внешняя антенна
- Полевой носимый: T-Echo (2 недели батарея) или T-Beam V1.2

### 6.3 Антенны для LoRa

Стоковые антенны T-Beam дают 2–5 км. С внешней антенной — до 25 км.

| Антенна | dBi | Дальность | Цена | Ссылка |
|---------|-----|-----------|------|--------|
| Стоковая T-Beam | 2 dBi | 2–5 км | в комплекте | — |
| Rokland Backcountry 5dBi (433MHz) | 5 dBi | 10–15 км | $15–20 | https://store.rokland.com/collections/antennas-for-helium-hotspots |
| Rokland 10 dBi (433MHz) | 10 dBi | 20–30 км | $25–35 | Rokland Store |
| AliExpress 433MHz 5dBi | 5 dBi | 8–15 км | $5–10 | https://www.aliexpress.com/w/wholesale-lora-antenna-433mhz.html |

### 6.4 Интеграция Meshtastic → NOMAD

```bash
# Установка Python SDK
pip install meshtastic

# Подключение устройства (USB)
meshtastic --port /dev/ttyUSB0 --info

# Скрипт: слушать входящие сообщения
python3 /opt/project-nomad/scripts/meshtastic_listener.py
```

```python
# scripts/meshtastic_listener.py
import meshtastic
import meshtastic.serial_interface
import requests
import json

def on_receive(packet, interface):
    """Получение сообщения из Meshtastic сети"""
    if 'decoded' in packet and 'text' in packet['decoded']:
        msg = packet['decoded']['text']
        sender = packet.get('fromId', 'unknown')
        print(f"LoRa [{sender}]: {msg}")

        # Пересылка в Matrix Synapse
        matrix_send(f"[LoRa от {sender}]: {msg}")

        # Пересылка в ntfy
        requests.post("http://localhost:8088/meshtastic",
                      data=f"[{sender}]: {msg}")

        # Сохранение в очередь для агента
        with open('/tmp/meshtastic_queue/incoming.jsonl', 'a') as f:
            f.write(json.dumps({"from": sender, "text": msg}) + "\n")

def matrix_send(text):
    """Отправка в Matrix комнату"""
    requests.post(
        "http://localhost:8448/_matrix/client/v3/rooms/!ROOM_ID:localhost/send/m.room.message",
        headers={"Authorization": "Bearer TOKEN"},
        json={"msgtype": "m.text", "body": text}
    )

interface = meshtastic.serial_interface.SerialInterface("/dev/ttyUSB0")
pub = meshtastic.mesh_pb2.MeshPacket()
# подписка на события
from pubsub import pub
pub.subscribe(on_receive, "meshtastic.receive")

import time
while True:
    time.sleep(1)
```

```python
# scripts/meshtastic_sender.py — отправка сообщений
import meshtastic
import meshtastic.serial_interface
import sys

def send_message(text, channel=0):
    interface = meshtastic.serial_interface.SerialInterface("/dev/ttyUSB0")
    interface.sendText(text, channelIndex=channel)
    print(f"Отправлено в канал {channel}: {text}")
    interface.close()

if __name__ == "__main__":
    send_message(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 0)
```

---

## 7. СПУТНИКОВАЯ СВЯЗЬ

### 7.1 Starlink Mini — реальный интернет в поле

Starlink Mini — портативная тарелка весом 1.16 кг со встроенным WiFi роутером.
Скорость 50–200 Mbps, пинг 25–60ms. Работает в движении до 160 км/ч.

Для NOMAD: скачать ZIM-коллекции, обновить модели, синхронизировать между узлами.

| Параметр | Значение |
|---------|---------|
| Цена устройства | $199 (новые клиенты) |
| Roam 100GB/мес | $50/мес |
| Roam Unlimited | $165/мес |
| Потребление | 20–40W активно |
| Вес | 1.16 kg |
| Скорость | 50–200 Mbps |

Сайт: https://www.starlink.com/roam
Amazon: https://www.amazon.com/STARLINK-Satellite-High-Speed-Connectivity-Phased-Array/dp/B0FMX5S83D

**Покрытие Кыргызстана:** проверь на https://www.starlink.com/map

### 7.2 Garmin inReach Mini 3 Plus — SOS и мессенджер

Запущен 2 декабря 2025. Сеть Iridium = 100% покрытие Земли.
Ключевая кнопка SOS с 24/7 координационным центром Garmin.
Голосовые сообщения до 30 сек, фото, текст до 1600 символов.

| Параметр | Mini 3 ($449) | Mini 3 Plus ($499) |
|---------|--------------|-------------------|
| Текстовые сообщения | ✅ | ✅ |
| GPS трекинг | ✅ | ✅ |
| SOS 24/7 | ✅ | ✅ |
| Голосовые сообщения | ❌ | ✅ |
| Фото в сообщениях | ❌ | ✅ |
| Дисплей | ч/б 1.55" | цветной 1.88" touchscreen |
| Батарея трекинг | 400 часов | 350 часов |

Сайт Garmin: https://www.garmin.com/en-US/p/1756582/
Amazon: https://www.amazon.com/dp/B0G4SDZP8S

Подписки: $15/мес (Safety Plan 10 сообщений) → $50/мес (Freedom Plan безлимит)

**Рекомендация:** купи оба — Starlink для данных, Garmin для ЧС/SOS.

---

## 8. РАДИО-ИНТЕРНЕТ И SDR

### 8.1 RTL-SDR — приём без лицензии

RTL-SDR dongle принимает 100 kHz — 1.7 GHz. Передача не нужна = лицензия не нужна.

**Что можно принимать:**
- NOAA спутниковые снимки погоды (APT) — бесплатная метеосводка из космоса
- ADS-B (1090 MHz) — самолёты на карте в реальном времени
- AIS (162 MHz) — суда на воде
- APRS (144.800 MHz) — позиционирование объектов
- FM/AM/SSB/CW — все радиостанции
- ATC (118–137 MHz) — авиационные переговоры
- ACARS — цифровые сообщения между самолётами и диспетчерами

Купить RTL-SDR Blog V4: $30–40
https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/
Amazon: https://www.amazon.com/s?k=RTL-SDR+V4+blog

### 8.2 Программный стек SDR для NOMAD

```bash
# OpenWebRX — веб-интерфейс SDR в браузере (Docker)
docker run -p 8073:8073 \
  --device /dev/bus/usb \
  --name nomad-sdr \
  -v ./config/openwebrx:/var/lib/openwebrx \
  --restart unless-stopped \
  jketterl/openwebrx:stable

# dump1090 — ADS-B самолёты
docker run -p 30005:30005 -p 30003:30003 \
  --device /dev/bus/usb \
  --name nomad-adsb \
  antirez/dump1090

# NOAA погодные снимки
pip install noaa-apt
noaa-apt --resample-output 11025 output.wav -o weather.png
```

GitHub OpenWebRX: https://github.com/jketterl/openwebrx

### 8.3 Winlink — email через HF радио (требует лицензии!)

Winlink — глобальная сеть email-шлюзов через радио. Использовался при ураганах.
Клиент **Pat** работает на Linux / RPi.

```bash
# Установка Pat (Winlink клиент для Linux)
go install github.com/la5nta/pat@latest

# Конфигурация
pat configure

# Отправить письмо через Winlink
pat compose --to winlink@winlink.org
```

Winlink: https://winlink.org
Pat: https://github.com/la5nta/pat

**Важно:** Требует лицензии радиолюбителя. Сообщения НЕ зашифрованы (требование FCC).
В Кыргызстане: обратись в Государственную инспекцию электросвязи.

### 8.4 JS8Call — текстовые сообщения через HF

Работает при сигнале -24 dB (там где всё остальное не работает).
Store-and-forward: узлы ретранслируют сообщения дальше.
Устанавливается как обычная программа, работает на RPi.

https://js8call.com

### 8.5 Минимальный ham-стек для выживания

| Оборудование | Назначение | Цена | Ссылка |
|-------------|-----------|------|--------|
| Baofeng UV-5R | VHF/UHF портативная (144/430 MHz) | $30 | https://www.amazon.com/s?k=Baofeng+UV-5R |
| Yaesu FT-991A | HF/VHF/UHF трансивер | ~$900 | yaesu.com |
| Icom IC-705 | HF/VHF/UHF SDR трансивер + RPi интеграция | ~$1400 | icomamerica.com |
| RTL-SDR V4 | Только приём, без лицензии | $35 | rtl-sdr.com |

---

## 9. АВТОНОМНОЕ ПИТАНИЕ — СОЛНЦЕ + LiFePO4

### 9.1 Почему LiFePO4, а не Li-Ion

| Параметр | LiFePO4 | Li-Ion |
|---------|---------|--------|
| Циклов | 6000+ | 500 |
| Температура работы | -20°C / +60°C | 0°C / +45°C |
| Безопасность | не горит | горит при повреждении |
| Для Кыргызстана (зима -20°C) | ✅ работает | ❌ деградирует |
| Цена 100Ah 12V | $180–250 | $120–180 |

### 9.2 Расчёт системы для NOMAD

**Потребление RPi5 NOMAD стека:**
- RPi5 (16W) + NVMe SSD (3W) + LoRa T-Beam (1W)
- + WiFi роутер (5W) + switch (3W) + ESP32 датчики (1W)
- = ~29W непрерывно

**24 часа:** 29W × 24h = 696 Wh/сутки

**Батарея 12V 100Ah LiFePO4:**
- Ёмкость: 1200 Wh (100% usable у LiFePO4)
- Автономность без солнца: 1200 / 29 = **41 час**

**Солнечная панель 200W, 5 часов пика в день:**
- Генерация: 200W × 5h × 0.85 (КПД MPPT) = **850 Wh/день**
- Дефицит: 696 - 850 = -154 Wh (излишек! 100Ah батареи хватает)

**Для NOMAD с GPU (RTX3060, 150W при инференсе):**
- Потребление системы: ~200W при инференсе, ~50W idle
- Средняя нагрузка (50% времени): ~125W
- 24ч: ~3000 Wh
- Нужно: 400W+ панелей + 200Ah батарея

### 9.3 MPPT контроллеры

| Контроллер | Ток | Особенность | Цена | Ссылка |
|-----------|-----|-------------|------|--------|
| Victron SmartSolar MPPT 75/15 | 15A | Bluetooth, лучшее качество | $80 | https://www.amazon.com/s?k=victron+smartsolar+mppt+75+15 |
| Victron SmartSolar MPPT 100/20 | 20A | LiFePO4 профиль | $110 | https://www.amazon.com/s?k=victron+smartsolar+mppt+100+20 |
| Renogy Rover 40A | 40A | Надёжный бюджет | $75 | https://www.amazon.com/s?k=renogy+rover+40a+mppt |
| EPever Tracer 4210AN | 40A | Modbus / RS485 интеграция | $85 | https://www.amazon.com/s?k=EPever+Tracer+4210AN |

Мониторинг Victron в NOMAD: VE.Direct USB адаптер ($30) → collectd → InfluxDB → Grafana

### 9.4 Солнечные панели

| Мощность | Применение | Цена | Ссылка |
|---------|-----------|------|--------|
| 100W монокристалл | RPi NOMAD базовый | $50–80 | https://www.amazon.com/s?k=renogy+100w+solar+panel |
| 200W монокристалл | RPi5 полный стек | $80–130 | https://www.amazon.com/s?k=renogy+200w+solar+panel |
| 400W монокристалл | NOMAD с GPU | $150–250 | renogy.com |
| 100W гибкая | Рюкзак, авто, палатка | $70–120 | https://www.aliexpress.com/w/wholesale-flexible-solar-panel-100w.html |

### 9.5 UPS для RPi — критично!

При обрыве питания RPi теряет данные (SD-карта, InfluxDB).

```bash
# Waveshare UPS HAT для RPi
# I2C мониторинг → при падении питания сигнал на GPIO → graceful shutdown
# https://www.amazon.com/s?k=waveshare+ups+raspberry+pi

# Автоматический shutdown при низком заряде
# /etc/cron.d/battery-check
*/1 * * * * root python3 /opt/project-nomad/scripts/battery_monitor.py
```

```python
# scripts/battery_monitor.py
import smbus2
import subprocess
import requests

INA226_ADDR = 0x40
bus = smbus2.SMBus(1)

def read_voltage():
    # INA226 регистр напряжения
    raw = bus.read_word_data(INA226_ADDR, 0x02)
    return ((raw >> 8) | (raw << 8 & 0xFF00)) * 1.25 / 1000

voltage = read_voltage()
percent = max(0, min(100, (voltage - 11.0) / (13.5 - 11.0) * 100))

if percent < 10:
    requests.post("http://localhost:8088/power", data="⚡ КРИТИЧНО: батарея 10%! Выключение через 60 сек")
    subprocess.run(["sudo", "shutdown", "-h", "+1"])
elif percent < 25:
    requests.post("http://localhost:8088/power", data=f"⚠️ Батарея {percent:.0f}% — подключи питание")
```

---

## 10. УВЕДОМЛЕНИЯ — PUSH НА ТЕЛЕФОН

### 10.1 ntfy — self-hosted push notifications

ntfy — HTTP pub/sub сервер. Одна команда curl = уведомление на все телефоны.
Документация: https://ntfy.sh
App Store: https://apps.apple.com/app/ntfy/id1625396347
Google Play: https://play.google.com/store/apps/details?id=io.heckel.ntfy

```bash
# Запуск
docker run -p 8088:80 \
  -v /opt/project-nomad/data/ntfy:/var/lib/ntfy \
  -v /opt/project-nomad/config/ntfy:/etc/ntfy \
  --name nomad-ntfy \
  --restart unless-stopped \
  binwiederhier/ntfy serve

# Отправка уведомления
curl -d "Диск 91% — нужна очистка" http://localhost:8088/alerts
curl -d "Входящий LoRa от Алексей: Выходим через час" http://localhost:8088/comms
curl -d "LLM ответ готов" http://localhost:8088/ai

# С иконкой и приоритетом
curl \
  -H "Title: КРИТИЧНО" \
  -H "Priority: urgent" \
  -H "Tags: warning" \
  -d "Батарея 10%! Подключи питание немедленно" \
  http://localhost:8088/power
```

### 10.2 Список каналов ntfy для NOMAD

| Канал | Назначение |
|-------|-----------|
| `/alerts` | Системные алерты (диск, память, CPU) |
| `/power` | Статус батареи и солнечной системы |
| `/comms` | Meshtastic и Matrix сообщения |
| `/ai` | Готовность ответов от агентов |
| `/iot` | Алерты датчиков (CO2, дым, движение) |
| `/health` | Ежечасные health-репорты |
| `/download` | Завершение загрузок ZIM/моделей |

### 10.3 Uptime Kuma — мониторинг

```bash
docker run -p 3001:3001 \
  -v /opt/project-nomad/data/uptime-kuma:/app/data \
  --name nomad-uptime-kuma \
  --restart unless-stopped \
  louislam/uptime-kuma:1
```

GitHub: https://github.com/louislam/uptime-kuma

Настрой мониторинг всех NOMAD контейнеров с уведомлением в ntfy при падении.

---

## 11. МОБАЙЛ — ЧАТЫ, КАРТЫ, ЗАДАЧИ

### 11.1 Matrix Synapse + Element — зашифрованный LAN чат

```bash
# docker-compose
services:
  synapse:
    image: matrixdotorg/synapse:latest
    container_name: nomad-matrix
    restart: unless-stopped
    volumes:
      - ./data/synapse:/data
    ports:
      - "8448:8448"
    environment:
      - SYNAPSE_CONFIG_PATH=/data/homeserver.yaml
```

Element клиенты:
- iOS: https://apps.apple.com/app/element/id1083446067
- Android: https://play.google.com/store/apps/details?id=im.vector.app
- Desktop: https://element.io/download

После установки Synapse — создай комнаты:
- `#general:nomad.local` — общий чат команды
- `#alerts:nomad.local` — системные алерты (Matrix webhook из ntfy)
- `#meshtastic:nomad.local` — LoRa сообщения (через скрипт)
- `#medic:nomad.local` — медицинские запросы к AI агенту

### 11.2 Vikunja — task manager офлайн

```bash
docker run -p 3456:3456 \
  -v /opt/project-nomad/data/vikunja:/app/vikunja \
  --name nomad-vikunja \
  --restart unless-stopped \
  vikunja/vikunja
```

Сайт: https://vikunja.io
Документация: https://vikunja.io/docs/install-with-docker

### 11.3 Офлайн карты на телефоне

- **OsmAnd** (мощный навигатор): https://osmand.net
  - Скачать: Кыргызстан + соседние страны
  - Включить: велосипед, пешеходные маршруты, рельеф
- **Organic Maps** (быстрый и чистый): https://organicmaps.app

### 11.4 Meshtastic мобайл

- Android: https://meshtastic.org/docs/software/android/
- iOS: https://meshtastic.org/docs/software/apple/
- Bluetooth подключение к T-Beam → mesh сеть

### 11.5 PWA — NOMAD на домашнем экране телефона

Добавить в Command Center TypeScript:

```typescript
// public/manifest.json
{
  "name": "NOMAD Command Center",
  "short_name": "NOMAD",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1a1a2e",
  "theme_color": "#16213e",
  "icons": [
    {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}
  ]
}

// Service Worker для офлайн кэширования
// public/sw.js
const CACHE = "nomad-v1";
const OFFLINE_URLS = ["/", "/dashboard", "/ai", "/maps", "/comms"];
```

HTTPS для PWA требует сертификат. Используй mkcert:
```bash
brew install mkcert  # macOS
# или
sudo apt install mkcert  # Linux

mkcert -install
mkcert nomad.local localhost 127.0.0.1
# Получишь nomad.local+2.pem и nomad.local+2-key.pem
```

---

## 12. ПОЛНЫЙ DOCKER СТЕК — ВСЕ КОНТЕЙНЕРЫ

### 12.1 docker-compose.yml — полный NOMAD v2.0

```yaml
version: '3.8'

networks:
  nomad:
    driver: bridge
    ipam:
      config:
        - subnet: 192.168.100.0/24

volumes:
  mysql_data:
  qdrant_data:
  ollama_data:
  kiwix_data:
  openstreetmap_data:
  kolibri_data:
  synapse_data:
  vikunja_data:
  ntfy_data:
  hass_data:
  mosquitto_data:
  influxdb_data:
  grafana_data:
  nodered_data:
  uptime_kuma_data:

services:

  # ==================== CORE NOMAD ====================
  nomad-app:
    image: ghcr.io/crosstalk-solutions/project-nomad:latest
    container_name: nomad-app
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - DB_HOST=nomad-mysql
      - QDRANT_HOST=nomad-qdrant
      - OLLAMA_HOST=nomad-ollama
    depends_on:
      - nomad-mysql
      - nomad-qdrant
    networks:
      - nomad

  nomad-mysql:
    image: mysql:8.0
    container_name: nomad-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: nomad
      MYSQL_USER: nomad
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - nomad

  nomad-qdrant:
    image: qdrant/qdrant:latest
    container_name: nomad-qdrant
    restart: unless-stopped
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - nomad

  # ==================== AI ====================
  nomad-ollama:
    image: ollama/ollama:latest
    container_name: nomad-ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    networks:
      - nomad

  nomad-openwebui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: nomad-openwebui
    restart: unless-stopped
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://nomad-ollama:11434
    volumes:
      - ./data/openwebui:/app/backend/data
    depends_on:
      - nomad-ollama
    networks:
      - nomad

  # ==================== KNOWLEDGE ====================
  nomad-kiwix:
    image: ghcr.io/kiwix/kiwix-serve:latest
    container_name: nomad-kiwix
    restart: unless-stopped
    ports:
      - "8888:8080"
    volumes:
      - kiwix_data:/data
    command: --library /data/library.xml
    networks:
      - nomad

  nomad-osm:
    image: overv/openstreetmap-tile-server:latest
    container_name: nomad-osm
    restart: unless-stopped
    ports:
      - "8081:80"
    volumes:
      - openstreetmap_data:/data/database
      - ./data/osm:/data/region
    shm_size: 1g
    networks:
      - nomad

  nomad-kolibri:
    image: learningequality/kolibri:latest
    container_name: nomad-kolibri
    restart: unless-stopped
    ports:
      - "8082:8080"
    volumes:
      - kolibri_data:/root/.kolibri
    networks:
      - nomad

  # ==================== COMMUNICATIONS ====================
  nomad-matrix:
    image: matrixdotorg/synapse:latest
    container_name: nomad-matrix
    restart: unless-stopped
    ports:
      - "8448:8448"
    volumes:
      - synapse_data:/data
    networks:
      - nomad

  # ==================== NOTIFICATIONS ====================
  nomad-ntfy:
    image: binwiederhier/ntfy:latest
    container_name: nomad-ntfy
    restart: unless-stopped
    ports:
      - "8088:80"
    volumes:
      - ntfy_data:/var/lib/ntfy
      - ./config/ntfy/server.yml:/etc/ntfy/server.yml
    command: serve
    networks:
      - nomad

  # ==================== TASKS ====================
  nomad-vikunja:
    image: vikunja/vikunja:latest
    container_name: nomad-vikunja
    restart: unless-stopped
    ports:
      - "3456:3456"
    volumes:
      - vikunja_data:/app/vikunja
    networks:
      - nomad

  # ==================== IoT ====================
  nomad-homeassistant:
    image: homeassistant/home-assistant:stable
    container_name: nomad-homeassistant
    restart: unless-stopped
    ports:
      - "8123:8123"
    volumes:
      - hass_data:/config
    network_mode: host  # нужен для mDNS/устройств в сети
    privileged: true

  nomad-mosquitto:
    image: eclipse-mosquitto:2
    container_name: nomad-mosquitto
    restart: unless-stopped
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - mosquitto_data:/mosquitto/data
      - ./config/mosquitto:/mosquitto/config
    networks:
      - nomad

  nomad-nodered:
    image: nodered/node-red:latest
    container_name: nomad-nodered
    restart: unless-stopped
    ports:
      - "1880:1880"
    volumes:
      - nodered_data:/data
    networks:
      - nomad

  # ==================== MONITORING ====================
  nomad-influxdb:
    image: influxdb:2
    container_name: nomad-influxdb
    restart: unless-stopped
    ports:
      - "8086:8086"
    volumes:
      - influxdb_data:/var/lib/influxdb2
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=nomad
      - DOCKER_INFLUXDB_INIT_PASSWORD=${INFLUX_PASSWORD}
      - DOCKER_INFLUXDB_INIT_ORG=nomad
      - DOCKER_INFLUXDB_INIT_BUCKET=sensors
    networks:
      - nomad

  nomad-grafana:
    image: grafana/grafana:latest
    container_name: nomad-grafana
    restart: unless-stopped
    ports:
      - "3001:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    depends_on:
      - nomad-influxdb
    networks:
      - nomad

  nomad-uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: nomad-uptime-kuma
    restart: unless-stopped
    ports:
      - "3001:3001"
    volumes:
      - uptime_kuma_data:/app/data
    networks:
      - nomad

  # ==================== SDR ====================
  nomad-sdr:
    image: jketterl/openwebrx:stable
    container_name: nomad-sdr
    restart: unless-stopped
    ports:
      - "8073:8073"
    devices:
      - /dev/bus/usb:/dev/bus/usb
    volumes:
      - ./config/openwebrx:/var/lib/openwebrx
    networks:
      - nomad
    # Запускать только если RTL-SDR подключён
    profiles:
      - sdr
```

### 12.2 .env файл

```bash
# /opt/project-nomad/.env
MYSQL_ROOT_PASSWORD=$(openssl rand -hex 32)
MYSQL_PASSWORD=$(openssl rand -hex 32)
INFLUX_PASSWORD=$(openssl rand -hex 32)
GRAFANA_PASSWORD=$(openssl rand -hex 32)
NOMAD_VERSION=2.0.0
```

---

## 13. АРХИТЕКТУРА АГЕНТНОЙ СИСТЕМЫ NOMAD

### 13.1 Структура директорий агентов

```
/opt/project-nomad/
├── agents/
│   ├── orchestrator.py          # главный агент-оркестратор
│   ├── medical_agent.py         # медицинский ассистент
│   ├── survival_agent.py        # выживание
│   ├── navigation_agent.py      # навигация и карты
│   ├── tech_repair_agent.py     # ремонт техники
│   ├── comms_agent.py           # управление связью
│   ├── iot_agent.py             # IoT и датчики
│   ├── rag_agent.py             # индексирование знаний
│   └── health_agent.py          # мониторинг системы
├── skills/
│   └── .claude/skills/
│       ├── medical/SKILL.md
│       ├── meshtastic/SKILL.md
│       ├── iot-sensors/SKILL.md
│       ├── zim-search/SKILL.md
│       ├── solar-monitor/SKILL.md
│       └── nomad-comms/SKILL.md
├── scripts/
│   ├── meshtastic_listener.py   # слушатель LoRa
│   ├── meshtastic_sender.py     # отправка LoRa
│   ├── battery_monitor.py       # мониторинг батареи
│   ├── rag_indexer.py           # индексирование в Qdrant
│   ├── zim_downloader.py        # загрузка ZIM коллекций
│   └── health_checker.sh        # проверка всех сервисов
└── config/
    ├── mosquitto/               # MQTT конфиг
    ├── openwebrx/               # SDR конфиг
    ├── ntfy/server.yml          # уведомления
    └── hass/                    # Home Assistant
```

### 13.2 Запуск агентного слоя (systemd)

```ini
# /etc/systemd/system/nomad-agents.service
[Unit]
Description=NOMAD Agent Orchestrator
After=docker.service nomad-ollama.service
Requires=docker.service

[Service]
Type=simple
User=nomad
WorkingDirectory=/opt/project-nomad
ExecStart=/usr/bin/python3 /opt/project-nomad/agents/orchestrator.py
Restart=always
RestartSec=10
Environment=ANTHROPIC_API_KEY=sk-ant-xxx  # если используешь Claude API
Environment=OLLAMA_HOST=http://localhost:11434

[Install]
WantedBy=multi-user.target
```

### 13.3 Взаимодействие компонентов

```
Пользователь (браузер/телефон)
    ↓ HTTP POST
Command Center (TypeScript, порт 8080)
    ↓ WebSocket / REST
Agent Orchestrator (Python, Claude Agent SDK)
    ├── Ollama (qwen3.5) — LLM инференс
    ├── Qdrant — поиск по знаниям (RAG)
    ├── Kiwix API — поиск ZIM
    ├── Meshtastic — LoRa сообщения
    ├── MQTT — IoT датчики
    └── ntfy — отправка уведомлений
```

---

## 14. СКРИПТЫ АВТОМАТИЗАЦИИ

### 14.1 install_nomad_v2.sh — расширенный установщик

```bash
#!/bin/bash
# NOMAD v2.0 installer
set -euo pipefail

echo "=== NOMAD v2.0 Installation ==="

# Цвета
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

# Проверка прав
[[ $EUID -eq 0 ]] || { echo -e "${RED}Требуются права root${NC}"; exit 1; }

# Определение железа
ARCH=$(uname -m)
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
GPU_INFO=$(lspci | grep -i nvidia || echo "no nvidia")

echo -e "${YELLOW}Железо: $ARCH, RAM: ${RAM_GB}GB${NC}"

# Выбор профиля
if [[ $ARCH == "aarch64" ]] || [[ $RAM_GB -lt 8 ]]; then
    PROFILE="minimal"
    DEFAULT_MODEL="qwen3.5:2b"
elif [[ $RAM_GB -lt 16 ]]; then
    PROFILE="standard"
    DEFAULT_MODEL="qwen3.5:4b"
elif echo "$GPU_INFO" | grep -qi "nvidia"; then
    PROFILE="gpu"
    DEFAULT_MODEL="qwen3.5:9b"
else
    PROFILE="standard"
    DEFAULT_MODEL="qwen3.5:9b"
fi

echo -e "${GREEN}Профиль: $PROFILE, модель: $DEFAULT_MODEL${NC}"

# Docker
if ! command -v docker &>/dev/null; then
    curl -fsSL https://get.docker.com | sh
    usermod -aG docker "${SUDO_USER:-$USER}"
fi

# Директории
mkdir -p /opt/project-nomad/{data,config,logs,agents,scripts,skills}
mkdir -p /opt/project-nomad/skills/.claude/skills/{medical,meshtastic,iot-sensors,zim-search,solar-monitor,nomad-comms}

# .env
cat > /opt/project-nomad/.env << EOF
MYSQL_ROOT_PASSWORD=$(openssl rand -hex 32)
MYSQL_PASSWORD=$(openssl rand -hex 32)
INFLUX_PASSWORD=$(openssl rand -hex 32)
GRAFANA_PASSWORD=$(openssl rand -hex 32)
NOMAD_PROFILE=$PROFILE
DEFAULT_MODEL=$DEFAULT_MODEL
EOF

# Pull модели Ollama
docker pull ollama/ollama:latest
docker run -d --name nomad-ollama-tmp -p 11434:11434 -v ollama_data:/root/.ollama ollama/ollama
sleep 5
docker exec nomad-ollama-tmp ollama pull $DEFAULT_MODEL
docker exec nomad-ollama-tmp ollama pull nomic-embed-text  # для RAG
docker stop nomad-ollama-tmp && docker rm nomad-ollama-tmp

# Установка Claude Agent SDK
pip3 install claude-agent-sdk meshtastic ntfy-client

# Python зависимости
pip3 install meshtastic smbus2 paho-mqtt requests aiohttp

# Запуск стека
cd /opt/project-nomad
docker compose up -d

echo -e "${GREEN}=== NOMAD v2.0 установлен! ===${NC}"
echo "Открой: http://localhost:8080"
```

### 14.2 health_checker.sh — проверка всех сервисов

```bash
#!/bin/bash
# /opt/project-nomad/scripts/health_checker.sh
NTFY="http://localhost:8088/health"
ERRORS=0

check_service() {
    local name=$1
    local url=$2
    if curl -sf "$url" > /dev/null 2>&1; then
        echo "✅ $name: OK"
    else
        echo "❌ $name: FAIL"
        curl -s -d "❌ $name не отвечает!" "$NTFY"
        ERRORS=$((ERRORS+1))
    fi
}

check_service "Ollama"          "http://localhost:11434/api/tags"
check_service "OpenWebUI"       "http://localhost:3000"
check_service "Kiwix"           "http://localhost:8888"
check_service "Matrix"          "http://localhost:8448/_matrix/static/"
check_service "ntfy"            "http://localhost:8088/v1/health"
check_service "Home Assistant"  "http://localhost:8123"
check_service "Grafana"         "http://localhost:3001"
check_service "Vikunja"         "http://localhost:3456"

# Disk check
DISK=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [[ $DISK -gt 85 ]]; then
    curl -s -H "Priority: urgent" \
         -d "💾 Диск ${DISK}% — нужна очистка!" \
         "http://localhost:8088/alerts"
fi

# RAM check
RAM=$(free | awk '/Mem:/{printf "%.0f", $3/$2*100}')
if [[ $RAM -gt 90 ]]; then
    curl -s -d "🧠 RAM ${RAM}% — критично!" "http://localhost:8088/alerts"
fi

if [[ $ERRORS -eq 0 ]]; then
    curl -s -d "✅ Все сервисы NOMAD работают" "http://localhost:8088/health"
fi
```

### 14.3 rag_indexer.py — индексирование документов

```python
#!/usr/bin/env python3
"""Автоматическое индексирование новых документов в Qdrant RAG"""
import os
import time
import hashlib
import requests
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIR = "/opt/project-nomad/data/incoming"
QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = "http://localhost:11434"
PROCESSED_FILE = "/opt/project-nomad/data/.rag_processed"

class DocumentIndexer(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.index_file(event.src_path)

    def index_file(self, filepath):
        path = Path(filepath)
        if path.suffix.lower() not in ['.pdf', '.txt', '.md', '.docx']:
            return

        # Читаем файл
        try:
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()[:50000]  # первые 50K символов
        except:
            return

        # Чанкинг
        chunks = [content[i:i+1000] for i in range(0, len(content), 800)]

        for i, chunk in enumerate(chunks):
            # Embed через Ollama
            resp = requests.post(f"{OLLAMA_URL}/api/embeddings",
                json={"model": "nomic-embed-text", "prompt": chunk})
            embedding = resp.json()["embedding"]

            # Сохранить в Qdrant
            requests.put(f"{QDRANT_URL}/collections/nomad/points",
                json={"points": [{
                    "id": int(hashlib.md5(f"{filepath}_{i}".encode()).hexdigest()[:8], 16),
                    "vector": embedding,
                    "payload": {"text": chunk, "source": path.name, "chunk": i}
                }]})

        # Уведомление
        requests.post("http://localhost:8088/download",
                      data=f"📚 Проиндексирован: {path.name} ({len(chunks)} чанков)")
        print(f"✅ Проиндексирован: {filepath}")

if __name__ == "__main__":
    # Создать коллекцию если нет
    requests.put(f"{QDRANT_URL}/collections/nomad",
        json={"vectors": {"size": 768, "distance": "Cosine"}})

    os.makedirs(WATCH_DIR, exist_ok=True)
    observer = Observer()
    observer.schedule(DocumentIndexer(), WATCH_DIR, recursive=True)
    observer.start()
    print(f"👁 Слежу за {WATCH_DIR}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
```

---

## 15. КАТАЛОГ ЖЕЛЕЗА — ССЫЛКИ И ЦЕНЫ

### 15.1 Основное железо

| Компонент | Модель | Цена | Ссылка |
|----------|--------|------|--------|
| **NOMAD сервер (мощный)** | AMD Ryzen 7 7840U мини-ПК 32GB | $300–500 | https://www.amazon.com/s?k=mini+pc+ryzen+7+7840u+32gb |
| **NOMAD сервер (GPU)** | RTX3060 12GB + i7 + 32GB | $800–1200 | NVIDIA RTX3060: https://www.amazon.com/s?k=rtx+3060+12gb |
| **NOMAD узел (полевой)** | Raspberry Pi 5 8GB | $80 | https://www.raspberrypi.com/products/raspberry-pi-5/ |
| **NVMe SSD 1TB** | Samsung 990 Pro | $80–100 | https://www.amazon.com/s?k=samsung+990+pro+1tb+nvme |
| **LoRa узел** | LILYGO T-Beam Supreme | $45–65 | https://lilygo.cc/en-us/products/t-beam-supreme-meshtastic |
| **LoRa узел бюджет** | Heltec WiFi LoRa 32 V3 | $20–30 | https://www.amazon.com/s?k=Heltec+LoRa+V3 |
| **SDR донгл** | RTL-SDR Blog V4 | $30–40 | https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/ |
| **Спутник интернет** | Starlink Mini | $199 + $50/мес | https://www.starlink.com/roam |
| **Спутник SOS** | Garmin inReach Mini 3 Plus | $499 + $15/мес | https://www.garmin.com/en-US/p/1756582/ |

### 15.2 Питание и солнечная система

| Компонент | Модель | Цена | Ссылка |
|----------|--------|------|--------|
| **Солнечная панель 200W** | Renogy 200W монокристалл | $80–130 | https://www.amazon.com/s?k=renogy+200w+solar+panel |
| **Солнечная панель гибкая** | Renogy 100W Flexible | $70–100 | https://www.amazon.com/s?k=renogy+flexible+100w |
| **MPPT контроллер** | Victron SmartSolar 100/20 | $110 | https://www.amazon.com/s?k=victron+smartsolar+mppt+100+20 |
| **MPPT контроллер бюджет** | Renogy Rover 40A | $75 | https://www.amazon.com/s?k=renogy+rover+40a+mppt |
| **Батарея 100Ah LiFePO4** | LiTime 12V 100Ah | $200–250 | https://www.litime.com |
| **Батарея 50Ah** | Renogy 12V 50Ah LiFePO4 | $130–160 | https://www.amazon.com/s?k=renogy+lifepo4+12v+50ah |
| **UPS для RPi** | Waveshare UPS HAT (B) | $25–40 | https://www.amazon.com/s?k=waveshare+ups+raspberry+pi+hat |
| **Датчик тока** | INA226 модуль | $4–7 | https://www.amazon.com/s?k=INA226+module |

### 15.3 IoT и датчики

| Компонент | Цена | Ссылка |
|----------|------|--------|
| ESP32 DevKit V1 | $5–8 | https://www.aliexpress.com/w/wholesale-esp32-devkit.html |
| ESP8266 NodeMCU | $3–5 | https://www.aliexpress.com/w/wholesale-nodemcu-esp8266.html |
| Arduino Mega 2560 | $10–15 | https://www.amazon.com/s?k=arduino+mega+2560 |
| DHT22 датчик | $3–5 | https://www.aliexpress.com/w/wholesale-DHT22.html |
| BME280 датчик | $3–6 | https://www.aliexpress.com/w/wholesale-BME280.html |
| SCD41 CO2 | $25–35 | https://www.amazon.com/s?k=SCD41+CO2+sensor |
| DS18B20 температура воды | $2–4 | https://www.aliexpress.com/w/wholesale-DS18B20.html |

---

## 16. HYPER ИНСТРУКЦИИ — СБОРКА С НУЛЯ

### ШАГ 0: Подготовка (30 минут)

```bash
# 1. Обновить Ubuntu 22.04+
sudo apt update && sudo apt upgrade -y

# 2. Установить Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# 3. Docker Compose (уже входит в Docker Desktop, проверь)
docker compose version

# 4. Python инструменты
sudo apt install -y python3 python3-pip git curl wget htop

# 5. NVIDIA GPU (опционально — только если есть GPU)
# Следуй: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update && sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### ШАГ 1: Установка NOMAD (10 минут)

```bash
# Скачать и запустить установщик
curl -fsSL https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/master/install/install_nomad.sh \
    -o install_nomad.sh
sudo bash install_nomad.sh

# Открыть в браузере
xdg-open http://localhost:8080  # Linux
open http://localhost:8080       # macOS
```

### ШАГ 2: Установка Qwen3.5 моделей (15–60 минут зависит от скорости)

```bash
# Войти в Ollama контейнер
docker exec -it nomad-ollama bash

# Установить модели по профилю
# Для RPi5 (8GB RAM):
ollama pull qwen3.5:2b
ollama pull qwen3.5:4b

# Для стандартного NOMAD (16GB RAM):
ollama pull qwen3.5:9b

# Для NOMAD с GPU (RTX3060 12GB):
ollama pull qwen3.5:9b
ollama pull qwen3.5:35b-a3b

# Embedding модель для RAG (нужна всем!)
ollama pull nomic-embed-text

# Проверить
ollama list
exit
```

### ШАГ 3: Расширенный стек (20 минут)

```bash
# Создать расширенный docker-compose.yml
cd /opt/project-nomad
sudo nano docker-compose.yml
# Добавь сервисы: ntfy, Matrix, Vikunja, HA, MQTT, Grafana из Секции 12

# Сгенерировать .env
cat > .env << 'EOF'
MYSQL_ROOT_PASSWORD=$(openssl rand -hex 32)
MYSQL_PASSWORD=$(openssl rand -hex 32)
INFLUX_PASSWORD=$(openssl rand -hex 32)
GRAFANA_PASSWORD=nomad2026
EOF

# Запустить новые контейнеры
sudo docker compose up -d

# Проверить статус
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### ШАГ 4: Установка агентного слоя (15 минут)

```bash
# Python зависимости
pip3 install claude-agent-sdk meshtastic watchdog \
    smbus2 paho-mqtt requests aiohttp

# Создать директории агентов
mkdir -p /opt/project-nomad/agents
mkdir -p /opt/project-nomad/skills/.claude/skills/{medical,meshtastic,iot-sensors,solar-monitor}

# Скопировать агенты из репозитория (или из этого спека)
# ...

# Создать systemd service
sudo tee /etc/systemd/system/nomad-agents.service << 'EOF'
[Unit]
Description=NOMAD Agent Orchestrator
After=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/project-nomad
ExecStart=/usr/bin/python3 /opt/project-nomad/agents/orchestrator.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable nomad-agents
sudo systemctl start nomad-agents
```

### ШАГ 5: Подключение Meshtastic (10 минут)

```bash
# Подключить T-Beam по USB
lsusb  # найти устройство
ls /dev/ttyUSB*  # обычно /dev/ttyUSB0

# Установить права
sudo usermod -aG dialout $USER

# Тест подключения
pip3 install meshtastic
meshtastic --port /dev/ttyUSB0 --info

# Настроить частоту для Кыргызстана
meshtastic --port /dev/ttyUSB0 --set lora.region KZ

# Запустить слушатель как сервис
sudo tee /etc/systemd/system/nomad-meshtastic.service << 'EOF'
[Unit]
Description=NOMAD Meshtastic Listener
After=docker.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/project-nomad/scripts/meshtastic_listener.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable --now nomad-meshtastic
```

### ШАГ 6: IoT и датчики (30 минут)

```bash
# 1. Открыть Home Assistant
xdg-open http://localhost:8123
# Пройти wizard установки

# 2. Настроить MQTT интеграцию в HA
# Settings → Devices → Add Integration → MQTT
# Broker: localhost:1883

# 3. Прошить ESP32
# Установить Arduino IDE или PlatformIO
# Использовать скетч из Секции 5.3
# Загрузить на устройство

# 4. Открыть Node-RED
xdg-open http://localhost:1880
# Импортировать flow для автоматизаций батареи

# 5. Открыть Grafana
xdg-open http://localhost:3001
# Добавить InfluxDB как data source
# Импортировать дашборд IoT
```

### ШАГ 7: Солнечная система (зависит от железа)

```bash
# 1. Физическое подключение
# Панель → MPPT контроллер → LiFePO4 батарея → инвертор/DC-DC → NOMAD

# 2. Настройка Victron MPPT
# Скачать VictronConnect на телефон
# Bluetooth → найти контроллер
# Тип батареи: LiFePO4
# Напряжение абсорбции: 14.2V
# Напряжение плавающего заряда: 13.5V

# 3. Мониторинг через NOMAD
# VE.Direct USB адаптер → USB → NOMAD
pip3 install vedirect
python3 /opt/project-nomad/scripts/vedirect_to_mqtt.py  # публикует в MQTT

# 4. Grafana дашборд солнечной системы
# Метрики: напряжение, ток, SOC, мощность панели, прогноз автономности
```

### ШАГ 8: Уведомления и мобайл (15 минут)

```bash
# 1. ntfy уже запущен
# Скачать приложение ntfy на телефон
# Подписаться на каналы: http://IP_NOMAD:8088/alerts
# (IP-адрес сервера NOMAD в твоей сети)

# 2. Matrix Element
# Открыть http://localhost:8448
# Создать аккаунт
# Скачать Element на телефон
# Войти: сервер nomad.local:8448

# 3. Проверка health checker
bash /opt/project-nomad/scripts/health_checker.sh

# Добавить в cron — каждый час
echo "0 * * * * root bash /opt/project-nomad/scripts/health_checker.sh" | \
    sudo tee /etc/cron.d/nomad-health
```

### ФИНАЛЬНАЯ ПРОВЕРКА — чеклист

```bash
#!/bin/bash
echo "=== NOMAD v2.0 FINAL CHECK ==="

services=(
    "http://localhost:8080|Command Center"
    "http://localhost:11434/api/tags|Ollama"
    "http://localhost:3000|OpenWebUI"
    "http://localhost:8888|Kiwix"
    "http://localhost:8123|Home Assistant"
    "http://localhost:1880|Node-RED"
    "http://localhost:3001|Grafana"
    "http://localhost:8088/v1/health|ntfy"
    "http://localhost:3456|Vikunja"
    "http://localhost:8073|OpenWebRX (SDR)"
)

ALL_OK=true
for entry in "${services[@]}"; do
    URL="${entry%%|*}"
    NAME="${entry##*|}"
    if curl -sf "$URL" > /dev/null 2>&1; then
        echo "✅ $NAME"
    else
        echo "❌ $NAME — $URL"
        ALL_OK=false
    fi
done

echo ""
echo "Ollama модели:"
docker exec nomad-ollama ollama list 2>/dev/null || echo "⚠️ Ollama недоступен"

echo ""
if $ALL_OK; then
    echo "🎉 NOMAD v2.0 полностью установлен и работает!"
else
    echo "⚠️ Есть проблемы. Проверь логи: docker logs <container_name>"
fi
```

---

## ССЫЛКИ — ПОЛНЫЙ СПИСОК

### Репозитории
- NOMAD: https://github.com/Crosstalk-Solutions/project-nomad
- Claude Agent SDK Python: https://github.com/anthropics/claude-agent-sdk-python
- Whisper.cpp: https://github.com/ggerganov/whisper.cpp
- Piper TTS: https://github.com/rhasspy/piper
- OpenWebRX: https://github.com/jketterl/openwebrx
- Meshtastic Python: https://github.com/meshtastic/python
- Uptime Kuma: https://github.com/louislam/uptime-kuma
- Winlink Pat: https://github.com/la5nta/pat
- direwolf APRS: https://github.com/wb2osz/direwolf

### Документация
- Qwen3.5 Guide: https://techie007.substack.com/p/qwen-35-the-complete-guide-benchmarks
- Claude Agent SDK Docs: https://platform.claude.com/docs/en/agent-sdk/overview
- Claude Agent Skills: https://platform.claude.com/docs/en/agent-sdk/skills
- Building Agents guide: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- Qwen3.5 Unsloth: https://unsloth.ai/docs/models/qwen3.5
- Ollama Qwen3.5: https://ollama.com/library/qwen3.5
- Meshtastic Docs: https://meshtastic.org/docs/hardware/devices/

### Где покупать
- Meshtastic железо: https://store.rokland.com/pages/meshtastic-hardware-rak-lilygo
- LILYGO прямой: https://lilygo.cc/en-us/products/t-beam-supreme-meshtastic
- RTL-SDR: https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/
- Victron MPPT: https://www.victronenergy.com/solar-charge-controllers
- LiFePO4 батареи: https://www.litime.com
- Starlink Mini: https://www.starlink.com/roam
- Garmin inReach Mini 3+: https://www.garmin.com/en-US/p/1756582/
- AliExpress ESP32: https://www.aliexpress.com/w/wholesale-esp32-devkit.html

---

*Document version: 2.0 | Last updated: March 2026 | Project NOMAD Hyperspec*
*Лицензия содержания: Apache 2.0*
