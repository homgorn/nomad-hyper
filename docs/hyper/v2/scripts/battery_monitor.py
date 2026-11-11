#!/usr/bin/env python3
"""
NOMAD — Battery & Power Monitor
Читает INA226 через I2C, публикует в MQTT + InfluxDB.
Управляет нагрузками при низком заряде.
Запуск: python3 battery_monitor.py [--mock]
Cron:  */5 * * * * python3 /opt/project-nomad/scripts/battery_monitor.py
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
import paho.mqtt.client as mqtt

# ── CONFIG ────────────────────────────────────────────────────
INA226_ADDR  = 0x40        # I2C адрес INA226
I2C_BUS      = 1           # /dev/i2c-1 (RPi5)
SHUNT_OHMS   = 0.002       # Сопротивление шунта (2 мОм)
MAX_EXPECTED_AMPS = 50     # Максимальный ожидаемый ток
BATTERY_CAPACITY_AH = 100  # Ёмкость LiFePO4 в Ач
BATTERY_VOLTAGE_FULL   = 13.3   # В = 100%
BATTERY_VOLTAGE_EMPTY  = 12.0   # В = 0%

MQTT_HOST    = os.getenv("MQTT_HOST",   "localhost")
MQTT_PORT    = int(os.getenv("MQTT_PORT", "1883"))
INFLUX_URL   = os.getenv("INFLUX_URL",  "http://localhost:8086")
INFLUX_ORG   = "nomad"
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "")
NTFY_URL     = os.getenv("NTFY_HOST",   "http://localhost:8088")

# Пороги управления нагрузками
THRESHOLDS = {
    "critical": 10,   # % → shutdown всё кроме связи
    "emergency": 15,  # % → выключить heavy контейнеры
    "low":       25,  # % → переключить на малую модель
    "warn":      35,  # % → уведомить
}

# ── LOGGING ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [WATT] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("WATT")


# ── INA226 DRIVER ─────────────────────────────────────────────

class INA226:
    """Драйвер INA226 датчика тока/напряжения."""

    # Регистры
    REG_CONFIG    = 0x00
    REG_SHUNT_V   = 0x01
    REG_BUS_V     = 0x02
    REG_POWER     = 0x03
    REG_CURRENT   = 0x04
    REG_CALIB     = 0x05
    REG_MASK_EN   = 0x06
    REG_ALERT     = 0x07

    def __init__(self, address: int = 0x40, bus: int = 1):
        import smbus2
        self.bus     = smbus2.SMBus(bus)
        self.address = address
        self._calibrate()

    def _calibrate(self):
        """Калибровка для заданного шунта и максимального тока."""
        current_lsb = MAX_EXPECTED_AMPS / 32768
        calib = int(0.00512 / (current_lsb * SHUNT_OHMS))
        self._write_register(self.REG_CALIB, calib)
        self.current_lsb = current_lsb

    def _read_register(self, register: int) -> int:
        raw = self.bus.read_word_data(self.address, register)
        return ((raw & 0xFF) << 8) | ((raw >> 8) & 0xFF)

    def _write_register(self, register: int, value: int):
        raw = ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)
        self.bus.write_word_data(self.address, register, raw)

    @property
    def voltage(self) -> float:
        """Напряжение шины (В)."""
        raw = self._read_register(self.REG_BUS_V)
        return raw * 0.00125  # 1.25 мВ на бит

    @property
    def current(self) -> float:
        """Ток (А). Отрицательный = разрядка, положительный = зарядка."""
        raw = self._read_register(self.REG_CURRENT)
        if raw > 32767:
            raw -= 65536
        return raw * self.current_lsb

    @property
    def power(self) -> float:
        """Мощность (Вт)."""
        return abs(self.voltage * self.current)


class MockINA226:
    """Имитация для тестирования без железа."""
    import random as _r

    @property
    def voltage(self) -> float:
        import random
        return round(12.5 + random.uniform(-0.5, 0.5), 2)

    @property
    def current(self) -> float:
        import random
        return round(-2.4 + random.uniform(-0.2, 0.2), 2)  # разрядка

    @property
    def power(self) -> float:
        return abs(self.voltage * self.current)


# ── CALCULATIONS ──────────────────────────────────────────────

def voltage_to_soc(voltage: float) -> float:
    """Преобразовать напряжение в % заряда для LiFePO4."""
    soc = (voltage - BATTERY_VOLTAGE_EMPTY) / (BATTERY_VOLTAGE_FULL - BATTERY_VOLTAGE_EMPTY) * 100
    return max(0.0, min(100.0, round(soc, 1)))


def estimate_autonomy(current_ma: float, soc: float) -> float:
    """Оценить автономность в часах."""
    if current_ma >= 0:  # зарядка
        return 999.0
    remaining_ah = soc / 100 * BATTERY_CAPACITY_AH
    discharge_a  = abs(current_ma) / 1000
    if discharge_a < 0.01:
        return 999.0
    return round(remaining_ah / discharge_a, 1)


# ── LOAD MANAGEMENT ───────────────────────────────────────────

def manage_loads(soc: float):
    """Управлять нагрузками в зависимости от уровня заряда."""

    if soc <= THRESHOLDS["critical"]:
        # КРИТИЧНО: выключить всё кроме связи
        log.warning(f"🔴 КРИТИЧНО {soc}% — экстренное отключение!")
        heavy = [
            "nomad-ollama", "nomad-openwebui",
            "nomad-jellyfin", "nomad-navidrome",
            "nomad-grafana", "nomad-influxdb",
            "nomad-kolibri", "nomad-archivebox",
        ]
        for svc in heavy:
            subprocess.run(["docker", "stop", svc],
                           capture_output=True, timeout=30)

        requests.post(f"{NTFY_URL}/power",
            data=f"⚡ КРИТИЧНО {soc}%! Выключены все тяжёлые сервисы!".encode(),
            headers={"Priority": "urgent"}, timeout=5)

    elif soc <= THRESHOLDS["emergency"]:
        log.warning(f"🟠 Аварийный режим {soc}%")
        for svc in ["nomad-jellyfin", "nomad-navidrome", "nomad-kolibri"]:
            subprocess.run(["docker", "stop", svc],
                           capture_output=True, timeout=30)

        requests.post(f"{NTFY_URL}/power",
            data=f"🟠 Аварийный режим {soc}% — развлечения отключены".encode(),
            headers={"Priority": "high"}, timeout=5)

    elif soc <= THRESHOLDS["low"]:
        log.info(f"🟡 Низкий заряд {soc}% — переключаю на малую модель")
        subprocess.run(
            ["docker", "exec", "nomad-ollama", "ollama", "run", "qwen3.5:2b", "--noprompt"],
            capture_output=True, timeout=60
        )

    elif soc <= THRESHOLDS["warn"]:
        log.info(f"⚠️ Заряд {soc}% — предупреждение")
        requests.post(f"{NTFY_URL}/power",
            data=f"⚠️ Батарея {soc}% — подключи зарядку".encode(),
            timeout=5)


# ── PUBLISH ───────────────────────────────────────────────────

def publish_mqtt(client: mqtt.Client, data: dict):
    """Публикация данных в MQTT."""
    base = "nomad/power"
    for key, value in data.items():
        client.publish(f"{base}/{key}", str(value), retain=True)
    client.publish(f"{base}/json", json.dumps(data), retain=True)


def publish_influxdb(data: dict):
    """Запись в InfluxDB."""
    if not INFLUX_TOKEN:
        return
    fields = ",".join([f'{k}={v}' for k, v in data.items()
                       if isinstance(v, (int, float))])
    line = f"power,device=ina226 {fields}"
    try:
        requests.post(
            f"{INFLUX_URL}/api/v2/write",
            params={"org": INFLUX_ORG, "bucket": "sensors", "precision": "s"},
            headers={"Authorization": f"Token {INFLUX_TOKEN}",
                     "Content-Type": "text/plain"},
            data=line.encode(),
            timeout=5,
        )
    except Exception as e:
        log.warning(f"InfluxDB ошибка: {e}")


# ── MAIN ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Режим имитации без I2C")
    parser.add_argument("--once", action="store_true", help="Выполнить один раз и выйти")
    args = parser.parse_args()

    # Создать датчик
    if args.mock:
        log.info("🔧 Mock режим (без реального датчика)")
        sensor = MockINA226()
    else:
        try:
            sensor = INA226(INA226_ADDR, I2C_BUS)
            log.info("✅ INA226 подключён")
        except Exception as e:
            log.warning(f"INA226 недоступен: {e} — переключаюсь на mock")
            sensor = MockINA226()

    # MQTT клиент
    client = mqtt.Client(client_id="nomad-battery-monitor")
    try:
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        log.warning(f"MQTT недоступен: {e}")

    # Предыдущий SOC для управления нагрузками
    last_soc_action = 100

    def read_and_publish():
        nonlocal last_soc_action

        voltage  = sensor.voltage
        current  = sensor.current
        power    = sensor.power
        soc      = voltage_to_soc(voltage)
        autonomy = estimate_autonomy(current * 1000, soc)
        charging = current > 0.1
        ts       = datetime.now().isoformat()

        data = {
            "voltage_v":    round(voltage, 3),
            "current_a":    round(current, 3),
            "power_w":      round(power, 1),
            "soc_pct":      soc,
            "autonomy_h":   autonomy,
            "charging":     int(charging),
            "capacity_ah":  BATTERY_CAPACITY_AH,
            "timestamp":    ts,
        }

        log.info(
            f"🔋 {voltage:.2f}V | {soc:.0f}% | "
            f"{'▲' if charging else '▼'}{abs(current):.1f}A | "
            f"{power:.1f}W | {autonomy:.1f}ч"
        )

        publish_mqtt(client, data)
        publish_influxdb(data)

        # Управление нагрузками (только при изменении уровня)
        for threshold in sorted(THRESHOLDS.values()):
            if soc <= threshold < last_soc_action:
                manage_loads(soc)
                break

        last_soc_action = soc
        return data

    if args.once:
        data = read_and_publish()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        log.info(f"📊 Мониторинг батареи запущен (обновление каждые 30с)")
        while True:
            try:
                read_and_publish()
            except KeyboardInterrupt:
                break
            except Exception as e:
                log.error(f"Ошибка: {e}")
            time.sleep(30)


if __name__ == "__main__":
    main()
