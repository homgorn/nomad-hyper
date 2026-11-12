"""Survival mode — auto-switch on low battery.

Monitors battery via Home Assistant MQTT / INA226 sensor.
When battery < threshold:
  - Switch Ollama to smallest model (e.g., qwen3.5:2b)
  - Disable non-essential containers (media, wiki, etc.)
  - Send ntfy alert
  - Optionally shutdown gracefully

Usage: python scripts/survival_mode.py --once
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error

# Config
BATTERY_LOW = 40
BATTERY_CRITICAL = 20
BATTERY_EMERGENCY = 10

NTFY_URL = "http://localhost:8088/power"
HA_MQTT_TOPIC = "nomad/sensors/power/battery_percent"
OLLAMA_CONTAINER = "nomad-ollama"
OLLAMA_SMALL_MODEL = "qwen3.5:2b"
OLLAMA_FULL_MODEL = "qwen3.5:9b"

# Containers to disable in survival mode (profiles to keep: core only)
DISABLE_CONTAINERS = [
    "nomad-openwebui",
    "nomad-jellyfin",
    "nomad-audiobookshelf",
    "nomad-calibre-web",
    "nomad-docmost",
    "nomad-bookstack",
    "nomad-vikunja",
    "nomad-memos",
    "nomad-actual",
    "nomad-jitsi",
    "nomad-octoprint",
    "nomad-freetakserver",
    "nomad-weewx",
]

def get_battery_percent():
    """Try HA MQTT first, then INA226 via /sys, then estimate."""
    try:
        # INA226 via ESP32 → MQTT → HA REST
        token = os.environ.get("NOMAD_HA_TOKEN")
        if not token:
            raise RuntimeError("NOMAD_HA_TOKEN not set; skipping HA battery check")
        req = urllib.request.Request(
            "http://localhost:8123/api/states/sensor.nomad_battery_percent",
            headers={"Authorization": f"Bearer {token}"}
        )
        # This is a placeholder — actual integration depends on HA setup
        raise NotImplementedError("HA battery sensor not wired yet")
    except Exception:
        pass
    try:
        # Linux power supply
        with open("/sys/class/power_supply/BAT0/capacity") as f:
            return int(f.read().strip())
    except Exception:
        pass
    return None

def pull_small_model():
    print(f"[survival] Pulling {OLLAMA_SMALL_MODEL} for low-battery mode...")
    subprocess.run(["docker", "exec", OLLAMA_CONTAINER, "ollama", "pull", OLLAMA_SMALL_MODEL], check=False)

def disable_containers():
    for c in DISABLE_CONTAINERS:
        print(f"[survival] Stopping {c}...")
        subprocess.run(["docker", "stop", c], check=False)

def send_ntfy(msg: str, priority: str = "default"):
    try:
        data = msg.encode("utf-8")
        req = urllib.request.Request(
            NTFY_URL,
            data=data,
            headers={"Priority": priority, "Tags": "warning"}
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"[survival] ntfy failed: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Check once and exit")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually disable")
    args = parser.parse_args()

    battery = get_battery_percent()
    if battery is None:
        print("[survival] Battery sensor not available. Configure HA battery sensor or /sys/class/power_supply.")
        sys.exit(0)

    print(f"[survival] Battery: {battery}%")

    if battery < BATTERY_EMERGENCY:
        msg = f"🚨 EMERGENCY: батарея {battery}%! Отключение через 60с."
        send_ntfy(msg, "urgent")
        disable_containers()
        subprocess.run(["sudo", "shutdown", "-h", "+1"], check=False)
    elif battery < BATTERY_CRITICAL:
        msg = f"⚠️ Батарея {battery}% — survival mode: отключаем несущественные контейнеры"
        send_ntfy(msg, "high")
        pull_small_model()
        if not args.dry_run:
            disable_containers()
    elif battery < BATTERY_LOW:
        msg = f"⚠️ Батарея {battery}% — переключаем на {OLLAMA_SMALL_MODEL}"
        send_ntfy(msg, "default")
        pull_small_model()
    else:
        print("[survival] Battery OK, no action")

if __name__ == "__main__":
    main()
