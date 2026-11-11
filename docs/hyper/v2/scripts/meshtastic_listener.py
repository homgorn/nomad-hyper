#!/usr/bin/env python3
"""
NOMAD — Meshtastic LoRa Listener
Слушает входящие сообщения и пишет в очередь для оркестратора.
Запуск: python3 meshtastic_listener.py [--port /dev/ttyUSB0]
"""

import argparse
import json
import logging
import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

import meshtastic
import meshtastic.serial_interface
import meshtastic.tcp_interface
import requests
from pubsub import pub

# ── CONFIG ────────────────────────────────────────────────────
QUEUE_DIR  = Path("/tmp/meshtastic_queue")
QUEUE_FILE = QUEUE_DIR / "incoming.jsonl"
NTFY_URL   = os.getenv("NTFY_HOST", "http://localhost:8088")
MATRIX_URL = os.getenv("MATRIX_HOST", "http://localhost:8448")
LOG_FILE   = Path("/opt/project-nomad/logs/meshtastic.log")

# ── LOGGING ───────────────────────────────────────────────────
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("SIGNAL")


# ── SENDERS ───────────────────────────────────────────────────

def ntfy_send(channel: str, message: str, priority: str = "default"):
    try:
        requests.post(
            f"{NTFY_URL}/{channel}",
            data=message.encode("utf-8"),
            headers={"Priority": priority, "Content-Type": "text/plain"},
            timeout=5,
        )
    except Exception as e:
        log.warning(f"ntfy ошибка: {e}")


def matrix_send(room: str, message: str, token: str = ""):
    """Отправить в Matrix (упрощённый вариант без SDK)."""
    if not token:
        return
    try:
        requests.post(
            f"{MATRIX_URL}/_matrix/client/v3/rooms/{room}/send/m.room.message",
            headers={"Authorization": f"Bearer {token}"},
            json={"msgtype": "m.text", "body": message},
            timeout=5,
        )
    except Exception as e:
        log.warning(f"Matrix ошибка: {e}")


def write_queue(message: dict):
    """Записать сообщение в очередь для оркестратора."""
    with open(QUEUE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")


# ── CALLBACKS ─────────────────────────────────────────────────

def on_receive(packet: dict, interface):
    """Обработчик входящего пакета."""
    try:
        decoded = packet.get("decoded", {})
        msg_type = decoded.get("portnum", "")

        # Текстовые сообщения
        if "text" in decoded:
            text    = decoded["text"]
            from_id = packet.get("fromId", "unknown")
            to_id   = packet.get("toId", "all")
            rssi    = packet.get("rxRssi", 0)
            snr     = packet.get("rxSnr", 0)

            log.info(f"📨 [{from_id}→{to_id}] RSSI:{rssi}dBm SNR:{snr}dB | {text}")

            # Записать в очередь
            msg = {
                "from":      from_id,
                "to":        to_id,
                "text":      text,
                "rssi":      rssi,
                "snr":       snr,
                "timestamp": datetime.now().isoformat(),
            }
            write_queue(msg)

            # Push уведомление
            ntfy_send("comms", f"📡 LoRa [{from_id}]: {text}")

            # Если сообщение @nomad — пометить как команду
            if "@nomad" in text.lower():
                log.info(f"🤖 Команда агенту: {text}")
                ntfy_send("ai", f"🤖 Команда NOMAD: {text}", priority="high")

        # Позиционные данные
        elif "position" in decoded:
            pos     = decoded["position"]
            from_id = packet.get("fromId", "unknown")
            lat     = pos.get("latitude", 0)
            lon     = pos.get("longitude", 0)
            alt     = pos.get("altitude", 0)
            bat     = decoded.get("deviceMetrics", {}).get("batteryLevel", "?")

            log.info(f"📍 [{from_id}] lat:{lat:.5f} lon:{lon:.5f} alt:{alt}м 🔋{bat}%")

            msg = {
                "type":      "position",
                "from":      from_id,
                "lat":       lat,
                "lon":       lon,
                "alt":       alt,
                "battery":   bat,
                "timestamp": datetime.now().isoformat(),
            }
            write_queue(msg)

        # Телеметрия устройства
        elif "deviceMetrics" in decoded:
            metrics = decoded["deviceMetrics"]
            from_id = packet.get("fromId", "unknown")
            bat     = metrics.get("batteryLevel", "?")
            voltage = metrics.get("voltage", 0)

            # Алерт если батарея низкая
            if isinstance(bat, int) and bat < 20:
                log.warning(f"🔴 {from_id} батарея {bat}%!")
                ntfy_send("power", f"🔴 {from_id}: батарея {bat}%!", priority="high")

    except Exception as e:
        log.error(f"Ошибка обработки пакета: {e}", exc_info=True)


def on_connection(interface, topic=pub.AUTO_TOPIC):
    """Обработчик подключения к T-Beam."""
    log.info("✅ T-Beam подключён")
    ntfy_send("health", "📡 Meshtastic T-Beam подключён")


def on_disconnection(interface, topic=pub.AUTO_TOPIC):
    """Обработчик отключения."""
    log.warning("❌ T-Beam отключён")
    ntfy_send("alerts", "❌ Meshtastic T-Beam ОТКЛЮЧЁН!", priority="high")


# ── MAIN ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="NOMAD Meshtastic Listener")
    parser.add_argument("--port", default="/dev/ttyUSB0", help="Порт T-Beam")
    parser.add_argument("--tcp",  default="",             help="TCP хост (вместо USB)")
    args = parser.parse_args()

    # Подписаться на события
    pub.subscribe(on_receive,       "meshtastic.receive")
    pub.subscribe(on_connection,    "meshtastic.connection.established")
    pub.subscribe(on_disconnection, "meshtastic.connection.lost")

    # Подключиться к T-Beam
    iface = None
    try:
        if args.tcp:
            log.info(f"Подключаюсь по TCP: {args.tcp}")
            iface = meshtastic.tcp_interface.TCPInterface(args.tcp)
        else:
            log.info(f"Подключаюсь к {args.port}")
            iface = meshtastic.serial_interface.SerialInterface(args.port)
    except Exception as e:
        log.error(f"Не могу подключиться к Meshtastic: {e}")
        log.info("Запускаю в режиме имитации (mock)")
        # В mock-режиме просто слушаем очередь
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            pass
        return

    # Обработчик сигналов
    def shutdown(sig, frame):
        log.info("Завершение работы...")
        if iface:
            iface.close()
        ntfy_send("health", "📡 Meshtastic listener остановлен")
        sys.exit(0)

    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    log.info(f"📡 SIGNAL слушает LoRa на {args.port}")
    log.info(f"📂 Очередь: {QUEUE_FILE}")

    # Держать процесс живым
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown(None, None)


if __name__ == "__main__":
    main()
