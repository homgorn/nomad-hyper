#!/usr/bin/env python3
"""
PROJECT N.O.M.A.D. v2.0 — Agent Orchestrator
Claude Agent SDK multi-agent system
Март 2026
"""

import asyncio
import json
import logging
import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# pip install claude-agent-sdk
try:
    from claude_agent_sdk import query, ClaudeAgentOptions
except ImportError:
    print("ОШИБКА: pip install claude-agent-sdk")
    sys.exit(1)

# ============================================================
# CONFIG
# ============================================================

NOMAD_ROOT = Path(os.environ.get("NOMAD_ROOT", "/opt/project-nomad"))
SKILLS_DIR  = NOMAD_ROOT / "skills"
LOGS_DIR    = NOMAD_ROOT / "logs"
DATA_DIR    = NOMAD_ROOT / "data"
QUEUE_DIR   = Path("/tmp/meshtastic_queue")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OLLAMA_HOST       = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
NTFY_URL          = os.environ.get("NTFY_URL", "http://localhost:8088")

# Интервалы в секундах
HEALTH_CHECK_INTERVAL = 300   # 5 минут
MESHTASTIC_POLL       = 10    # 10 секунд
BATTERY_POLL          = 60    # 1 минута
RAG_WATCH_INTERVAL    = 300   # 5 минут

LOGS_DIR.mkdir(parents=True, exist_ok=True)
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOGS_DIR / "orchestrator.log"),
    ],
)
log = logging.getLogger("SIGMA")

# ============================================================
# AGENT TOOLS FACTORY
# ============================================================

def make_options(tools: list[str] | None = None, model: str = "claude-sonnet-4-6") -> ClaudeAgentOptions:
    """Создать настройки агента с загрузкой Skills"""
    return ClaudeAgentOptions(
        allowed_tools=tools or ["Bash", "Read", "Write", "Glob"],
        setting_sources=["user", "project"],   # загружает .claude/skills/
        cwd=str(SKILLS_DIR),
        model=model,
    )

async def run_agent(prompt: str, tools: list[str] | None = None) -> str:
    """Запустить агента и вернуть результат"""
    result_parts = []
    try:
        async for message in query(prompt=prompt, options=make_options(tools)):
            if hasattr(message, "result"):
                result_parts.append(message.result)
            elif hasattr(message, "text"):
                result_parts.append(message.text)
    except Exception as e:
        log.error(f"Ошибка агента: {e}")
        return f"ERROR: {e}"
    return "\n".join(result_parts)

# ============================================================
# NTFY NOTIFICATIONS
# ============================================================

import urllib.request

def ntfy(channel: str, message: str, title: str = "NOMAD", priority: str = "default", tags: str = "") -> bool:
    """Отправить push уведомление"""
    try:
        url = f"{NTFY_URL}/{channel}"
        headers = {
            "Title": title.encode(),
            "Priority": priority.encode(),
            "Content-Type": "text/plain; charset=utf-8",
        }
        if tags:
            headers["Tags"] = tags.encode()
        req = urllib.request.Request(
            url, data=message.encode("utf-8"),
            headers=headers, method="POST"
        )
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception as e:
        log.warning(f"ntfy error: {e}")
        return False

# ============================================================
# SYSTEM HEALTH CHECK
# ============================================================

import subprocess
import shutil

def check_docker_containers() -> dict:
    """Проверить статус Docker контейнеров"""
    result = {"total": 0, "running": 0, "stopped": [], "errors": []}
    try:
        out = subprocess.check_output(
            ["docker", "ps", "-a", "--format", "{{.Names}}\t{{.Status}}"],
            timeout=10
        ).decode()
        for line in out.strip().split("\n"):
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) == 2:
                name, status = parts
                result["total"] += 1
                if "Up" in status:
                    result["running"] += 1
                else:
                    result["stopped"].append(name)
    except Exception as e:
        result["errors"].append(str(e))
    return result

def check_disk() -> dict:
    """Проверить использование диска"""
    usage = shutil.disk_usage("/")
    pct = usage.used / usage.total * 100
    return {
        "used_gb": round(usage.used / 1e9, 1),
        "total_gb": round(usage.total / 1e9, 1),
        "percent": round(pct, 1),
        "critical": pct > 90,
        "warning": pct > 80,
    }

def check_memory() -> dict:
    """Проверить использование RAM"""
    try:
        with open("/proc/meminfo") as f:
            info = {}
            for line in f:
                key, val = line.split(":", 1)
                info[key.strip()] = int(val.split()[0])  # KB
        total  = info.get("MemTotal", 0)
        avail  = info.get("MemAvailable", 0)
        used   = total - avail
        pct    = used / total * 100 if total > 0 else 0
        return {
            "used_gb": round(used / 1e6, 1),
            "total_gb": round(total / 1e6, 1),
            "percent": round(pct, 1),
            "critical": pct > 95,
            "warning": pct > 85,
        }
    except Exception:
        return {"used_gb": 0, "total_gb": 0, "percent": 0, "critical": False, "warning": False}

def system_health_report() -> dict:
    """Полный отчёт о здоровье системы"""
    docker = check_docker_containers()
    disk   = check_disk()
    mem    = check_memory()

    issues = []
    if docker["stopped"]:
        issues.append(f"Остановлены: {', '.join(docker['stopped'][:5])}")
    if disk["critical"]:
        issues.append(f"Диск критично: {disk['percent']}%")
    if disk["warning"] and not disk["critical"]:
        issues.append(f"Диск: {disk['percent']}%")
    if mem["critical"]:
        issues.append(f"RAM критично: {mem['percent']}%")

    return {
        "timestamp": datetime.now().isoformat(),
        "docker": docker,
        "disk": disk,
        "memory": mem,
        "issues": issues,
        "healthy": len(issues) == 0,
    }

# ============================================================
# MESHTASTIC MESSAGE HANDLER
# ============================================================

import hashlib

PROCESSED_HASHES_FILE = QUEUE_DIR / ".processed"

def get_processed() -> set:
    try:
        return set(PROCESSED_HASHES_FILE.read_text().splitlines())
    except FileNotFoundError:
        return set()

def mark_processed(msg_hash: str):
    with open(PROCESSED_HASHES_FILE, "a") as f:
        f.write(msg_hash + "\n")

def read_meshtastic_queue() -> list[dict]:
    """Читает новые сообщения из очереди Meshtastic"""
    queue_file = QUEUE_DIR / "incoming.jsonl"
    if not queue_file.exists():
        return []

    processed = get_processed()
    new_messages = []

    try:
        lines = queue_file.read_text().splitlines()
        for line in lines:
            if not line.strip():
                continue
            msg_hash = hashlib.md5(line.encode()).hexdigest()
            if msg_hash not in processed:
                try:
                    msg = json.loads(line)
                    msg["_hash"] = msg_hash
                    new_messages.append(msg)
                except json.JSONDecodeError:
                    pass
    except Exception as e:
        log.warning(f"Ошибка чтения очереди: {e}")

    return new_messages

def send_to_matrix(room: str, text: str):
    """Отправить сообщение в Matrix"""
    try:
        matrix_url = "http://localhost:8448"
        token_file = NOMAD_ROOT / "config" / "matrix_token.txt"
        if not token_file.exists():
            return
        token = token_file.read_text().strip()

        import json as _json
        url = f"{matrix_url}/_matrix/client/v3/rooms/{room}/send/m.room.message"
        data = _json.dumps({"msgtype": "m.text", "body": text}).encode()
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/json")
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        log.warning(f"Matrix send error: {e}")

async def handle_meshtastic_message(msg: dict):
    """Обработать входящее LoRa сообщение агентом"""
    sender  = msg.get("from", "unknown")
    text    = msg.get("text", "")
    channel = msg.get("channel", 0)

    log.info(f"LoRa [{sender}] ch{channel}: {text}")

    # Переслать в Matrix
    send_to_matrix(
        "!general:nomad.local",
        f"📡 LoRa [{sender}]: {text}"
    )

    # Push уведомление
    ntfy("comms", f"[LoRa {sender}]: {text}", title="Meshtastic", tags="satellite")

    # Если медицинский запрос — делегировать DOC агенту
    medical_keywords = ["помощь", "травм", "рана", "болит", "кровь", "без сознания",
                        "help", "injury", "medical", "sos", "срочно", "эвакуация"]
    if any(kw in text.lower() for kw in medical_keywords):
        log.info("Детектирован медицинский запрос, делегирую DOC...")
        prompt = f"""
Использую навык nomad-medic (агент DOC).
Входящее сообщение через LoRa от {sender}: "{text}"
Дай краткую первичную оценку и первые действия.
Ответ должен быть кратким для отправки через LoRa (не более 200 символов).
"""
        response = await run_agent(prompt, ["Bash", "Read", "Skill"])
        if response:
            ntfy("medic", f"🏥 Ответ DOC для {sender}: {response[:500]}", priority="high")
            log.info(f"DOC ответ: {response[:200]}")

    # Если запрос статуса системы
    if any(kw in text.lower() for kw in ["статус", "status", "здоровье", "система"]):
        health = system_health_report()
        reply = (
            f"NOMAD: {health['docker']['running']}/{health['docker']['total']} "
            f"контейнеров | Диск:{health['disk']['percent']}% | "
            f"RAM:{health['memory']['percent']}%"
        )
        ntfy("status", reply, title="NOMAD Status")

    mark_processed(msg["_hash"])

# ============================================================
# BACKGROUND TASKS
# ============================================================

async def task_health_monitor():
    """Периодический мониторинг здоровья системы"""
    log.info("Запуск health monitor")
    while True:
        try:
            health = system_health_report()

            # Записать в файл
            health_file = LOGS_DIR / "health.json"
            health_file.write_text(json.dumps(health, ensure_ascii=False, indent=2))

            # Алерты
            for issue in health["issues"]:
                log.warning(f"Health issue: {issue}")
                ntfy("alerts", f"⚠️ {issue}", title="NOMAD Alert", priority="high", tags="warning")

            if health["healthy"]:
                log.debug(f"Система здорова: {health['docker']['running']} контейнеров")
            else:
                log.warning(f"Проблемы: {health['issues']}")

        except Exception as e:
            log.error(f"Health monitor error: {e}")

        await asyncio.sleep(HEALTH_CHECK_INTERVAL)


async def task_meshtastic_poller():
    """Опрос очереди Meshtastic сообщений"""
    log.info("Запуск Meshtastic poller")
    while True:
        try:
            messages = read_meshtastic_queue()
            for msg in messages:
                await handle_meshtastic_message(msg)
        except Exception as e:
            log.error(f"Meshtastic poller error: {e}")
        await asyncio.sleep(MESHTASTIC_POLL)


async def task_battery_monitor():
    """Мониторинг батареи через INA226"""
    log.info("Запуск battery monitor")
    try:
        import smbus2
        bus = smbus2.SMBus(1)
        INA226_ADDR = 0x40
        has_sensor = True
    except ImportError:
        log.warning("smbus2 не установлен — мониторинг батареи недоступен")
        return
    except Exception:
        log.warning("INA226 недоступен — пропуск battery monitor")
        return

    last_alerted = 0

    while True:
        try:
            raw = bus.read_word_data(INA226_ADDR, 0x02)
            voltage = ((raw >> 8) | (raw << 8 & 0xFF00)) * 1.25 / 1000
            soc = max(0, min(100, (voltage - 12.0) / (13.3 - 12.0) * 100))

            # Логировать в файл
            batt_file = DATA_DIR / "battery.json"
            batt_data = {
                "timestamp": datetime.now().isoformat(),
                "voltage": round(voltage, 2),
                "soc": round(soc, 1),
            }
            batt_file.write_text(json.dumps(batt_data))

            now = time.time()

            if soc < 10 and now - last_alerted > 600:
                log.critical(f"Батарея критически низкая: {soc:.0f}%!")
                ntfy("power", f"⚡ КРИТИЧНО: Батарея {soc:.0f}%! Выключение через 5 мин",
                     title="Power Alert", priority="urgent", tags="battery,warning")

                # Graceful shutdown несущественного
                for container in ["nomad-jellyfin", "nomad-navidrome", "nomad-grafana"]:
                    subprocess.run(["docker", "stop", container], capture_output=True, timeout=30)
                    log.info(f"Остановлен (low power): {container}")

                last_alerted = now

            elif soc < 25 and now - last_alerted > 1800:
                ntfy("power", f"🟠 Батарея {soc:.0f}% ({voltage:.1f}V) — подключи питание",
                     title="Power Warning", priority="high", tags="battery")
                last_alerted = now

        except Exception as e:
            log.warning(f"Battery read error: {e}")

        await asyncio.sleep(BATTERY_POLL)


async def task_morning_briefing():
    """Утренний брифинг в 7:00"""
    log.info("Запуск morning briefing scheduler")
    while True:
        now = datetime.now()
        if now.hour == 7 and now.minute == 0:
            log.info("Генерирую утренний брифинг...")
            try:
                health = system_health_report()
                briefing = (
                    f"☀️ NOMAD {now.strftime('%d.%m.%Y %H:%M')}\n"
                    f"Контейнеры: {health['docker']['running']}/{health['docker']['total']}\n"
                    f"Диск: {health['disk']['percent']}% | RAM: {health['memory']['percent']}%\n"
                )
                if health["issues"]:
                    briefing += f"⚠️ Проблемы: {', '.join(health['issues'])}\n"
                else:
                    briefing += "✅ Всё в порядке\n"

                ntfy("health", briefing, title="Утренний брифинг NOMAD")
                log.info("Утренний брифинг отправлен")
                await asyncio.sleep(61)  # пропустить следующую минуту
            except Exception as e:
                log.error(f"Briefing error: {e}")

        await asyncio.sleep(30)


async def task_rag_watcher():
    """Мониторинг новых документов для индексирования"""
    import hashlib as hl
    watch_dir = DATA_DIR / "incoming"
    watch_dir.mkdir(exist_ok=True)
    indexed_file = DATA_DIR / ".rag_indexed.json"

    try:
        indexed = json.loads(indexed_file.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        indexed = {}

    log.info(f"RAG watcher смотрит за {watch_dir}")

    while True:
        try:
            for file_path in watch_dir.rglob("*"):
                if not file_path.is_file():
                    continue
                if file_path.suffix.lower() not in {".pdf", ".txt", ".md", ".docx"}:
                    continue

                file_hash = hl.md5(file_path.read_bytes()).hexdigest()
                if file_hash in indexed:
                    continue

                log.info(f"Новый документ для индексирования: {file_path.name}")

                prompt = f"""
Используй навык nomad-rag (агент LIBRARIAN).
Проиндексируй файл: {file_path}
Определи подходящую коллекцию Qdrant автоматически по содержимому.
Сообщи сколько чанков создано и в какую коллекцию.
"""
                result = await run_agent(prompt, ["Bash", "Read", "Skill"])
                log.info(f"Индексирование: {result[:200]}")

                indexed[file_hash] = {
                    "file": str(file_path),
                    "indexed_at": datetime.now().isoformat(),
                }
                indexed_file.write_text(json.dumps(indexed, indent=2))

                ntfy("download", f"📚 Проиндексирован: {file_path.name}", title="RAG Update")

        except Exception as e:
            log.error(f"RAG watcher error: {e}")

        await asyncio.sleep(RAG_WATCH_INTERVAL)

# ============================================================
# INTERACTIVE MODE
# ============================================================

async def interactive_loop():
    """Интерактивный режим — ввод команд с терминала"""
    log.info("Интерактивный режим (Ctrl+C для выхода)")
    print("\n" + "="*50)
    print("  NOMAD SIGMA — Command Interface")
    print("  Введи команду или вопрос:")
    print("="*50 + "\n")

    while True:
        try:
            user_input = await asyncio.get_event_loop().run_in_executor(
                None, lambda: input("SIGMA> ")
            )
            user_input = user_input.strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                break

            # Специальные команды
            if user_input == "*status":
                health = system_health_report()
                print(json.dumps(health, ensure_ascii=False, indent=2))
                continue

            # Запрос к агенту
            print("⏳ Обрабатываю...")
            result = await run_agent(
                f"Ты — SIGMA, главный оркестратор NOMAD. {user_input}",
                ["Bash", "Read", "Write", "Skill"]
            )
            print(f"\n🤖 SIGMA: {result}\n")

        except (EOFError, KeyboardInterrupt):
            break
        except Exception as e:
            log.error(f"Interactive error: {e}")

# ============================================================
# MAIN
# ============================================================

shutdown_event = asyncio.Event()

def handle_shutdown(sig, frame):
    log.info(f"Получен сигнал {sig}, начинаю graceful shutdown...")
    ntfy("alerts", "🔴 NOMAD оркестратор останавливается", title="NOMAD Shutdown")
    shutdown_event.set()

async def main():
    log.info("="*50)
    log.info("  PROJECT N.O.M.A.D. v2.0 — Agent Orchestrator")
    log.info(f"  Запуск: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    log.info("="*50)

    # Проверка ключа API
    if not ANTHROPIC_API_KEY and os.environ.get("NOMAD_USE_OLLAMA", "0") == "0":
        log.warning("ANTHROPIC_API_KEY не установлен — агент будет использовать Ollama")

    # Уведомление о старте
    ntfy("health", "🟢 NOMAD оркестратор запущен", title="NOMAD Online", tags="white_check_mark")

    # Запуск фоновых задач
    tasks = [
        asyncio.create_task(task_health_monitor(),       name="health_monitor"),
        asyncio.create_task(task_meshtastic_poller(),    name="meshtastic_poller"),
        asyncio.create_task(task_battery_monitor(),      name="battery_monitor"),
        asyncio.create_task(task_morning_briefing(),     name="morning_briefing"),
        asyncio.create_task(task_rag_watcher(),          name="rag_watcher"),
    ]

    # Интерактивный режим если запущен из терминала
    if sys.stdin.isatty():
        tasks.append(asyncio.create_task(interactive_loop(), name="interactive"))

    # Ждать shutdown сигнала
    try:
        await shutdown_event.wait()
    except KeyboardInterrupt:
        pass

    log.info("Останавливаю фоновые задачи...")
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    log.info("NOMAD оркестратор остановлен.")


if __name__ == "__main__":
    # Обработчики сигналов
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT,  handle_shutdown)

    asyncio.run(main())
