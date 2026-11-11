#!/usr/bin/env python3
"""
PROJECT N.O.M.A.D. v2.0 — Agent Orchestrator
Claude Agent SDK · BMAD Architecture · March 2026

Главный агент-оркестратор NOMAD.
Читает запросы из stdin/API, делегирует суб-агентам,
слушает очередь Meshtastic, публикует алерты в ntfy.

Запуск: python3 orchestrator.py
Или:    uvicorn orchestrator:app --port 8099
"""

import asyncio
import json
import os
import sys
import logging
from pathlib import Path
from datetime import datetime

import httpx
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

try:
    from claude_agent_sdk import query, ClaudeAgentOptions
    HAS_SDK = True
except ImportError:
    HAS_SDK = False
    logging.warning("claude-agent-sdk не установлен — используем Ollama режим")

# ─── CONFIG ───────────────────────────────────────────────────
OLLAMA_HOST    = os.getenv("OLLAMA_HOST",   "http://localhost:11434")
QDRANT_HOST    = os.getenv("QDRANT_HOST",   "http://localhost:6333")
MATRIX_HOST    = os.getenv("MATRIX_HOST",   "http://localhost:8448")
NTFY_HOST      = os.getenv("NTFY_HOST",     "http://localhost:8088")
KIWIX_HOST     = os.getenv("KIWIX_HOST",    "http://localhost:8888")
MESHTASTIC_Q   = Path("/tmp/meshtastic_queue/incoming.jsonl")
SKILLS_PATH    = Path("/app/skills/.claude/skills")
LOG_FILE       = Path("/app/logs/orchestrator.log")
ANTHROPIC_KEY  = os.getenv("ANTHROPIC_API_KEY", "")

# Модели (приоритет: 9b → 4b → 2b в зависимости от доступности)
MODELS = {
    "main":    "qwen3.5:9b",
    "fast":    "qwen3.5:2b",
    "vision":  "qwen3.5:9b",   # для анализа фото
    "embed":   "nomic-embed-text",
}

# ─── LOGGING ──────────────────────────────────────────────────
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("SIGMA")

# ─── FASTAPI APP ───────────────────────────────────────────────
app = FastAPI(
    title="NOMAD Agent Orchestrator",
    description="BMAD Multi-Agent System for Project NOMAD",
    version="2.0.0",
)

# ─── SUB-AGENT ROUTER ─────────────────────────────────────────
AGENT_ROUTES = {
    # Медицина / здоровье
    "медицин": "nomad-medic",
    "боль":    "nomad-medic",
    "рана":    "nomad-medic",
    "симптом": "nomad-medic",
    "лечение": "nomad-medic",
    "лекарств": "nomad-medic",
    "травм":   "nomad-medic",
    "triag":   "nomad-medic",
    # Выживание
    "выживан": "nomad-survival",
    "заблудил": "nomad-survival",
    "вода в поле": "nomad-survival",
    "укрытие": "nomad-survival",
    "растени": "nomad-survival",
    # Связь
    "сообщени": "nomad-comms",
    "meshtastic": "nomad-comms",
    "matrix":   "nomad-comms",
    "broadcast": "nomad-comms",
    "отправь":  "nomad-comms",
    "lora":     "nomad-comms",
    # Питание
    "батарея": "nomad-power",
    "заряд":   "nomad-power",
    "солнечн": "nomad-power",
    "mppt":    "nomad-power",
    "автоном": "nomad-power",
    # IoT
    "датчик":  "nomad-iot",
    "температур": "nomad-iot",
    "влажност": "nomad-iot",
    "co2":     "nomad-iot",
    "mqtt":    "nomad-iot",
    "автоматиз": "nomad-iot",
    # RAG / База знаний
    "найди в баз": "nomad-rag",
    "проиндекс":   "nomad-rag",
    "wikipedia":   "nomad-rag",
    "kiwix":       "nomad-rag",
    "добавь документ": "nomad-rag",
    # SDR
    "погода":  "nomad-sdr",
    "noaa":    "nomad-sdr",
    "самолёт": "nomad-sdr",
    "ads-b":   "nomad-sdr",
    "радиочастот": "nomad-sdr",
    # DevOps
    "контейнер": "nomad-devops",
    "docker":    "nomad-devops",
    "упал сервис": "nomad-devops",
    "перезапуст": "nomad-devops",
    "обнови":    "nomad-devops",
    "логи":      "nomad-devops",
    # Навигация
    "маршрут": "nomad-navigator",
    "координат": "nomad-navigator",
    "расстояни": "nomad-navigator",
    "карта":    "nomad-navigator",
    "где наход": "nomad-navigator",
}


def route_to_agent(query_text: str) -> str:
    """Определить подходящий агент по тексту запроса."""
    lower = query_text.lower()
    for keyword, agent in AGENT_ROUTES.items():
        if keyword in lower:
            return agent
    return "nomad-orchestrator"  # fallback — главный агент


def load_skill(agent_name: str) -> str:
    """Загрузить SKILL.md для агента."""
    skill_path = SKILLS_PATH / agent_name / "SKILL.md"
    if skill_path.exists():
        return skill_path.read_text(encoding="utf-8")
    log.warning(f"Скилл не найден: {skill_path}")
    return ""


# ─── NOTIFICATIONS ────────────────────────────────────────────

async def ntfy_send(channel: str, message: str, priority: str = "default"):
    """Отправить push-уведомление через ntfy."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                f"{NTFY_HOST}/{channel}",
                content=message,
                headers={"Priority": priority},
            )
    except Exception as e:
        log.error(f"ntfy ошибка: {e}")


# ─── SYSTEM HEALTH ────────────────────────────────────────────

async def check_service(name: str, url: str) -> dict:
    """Проверить доступность сервиса."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.get(url)
            return {"name": name, "status": "ok", "code": r.status_code}
    except Exception as e:
        return {"name": name, "status": "error", "error": str(e)}


async def system_health() -> dict:
    """Полная диагностика системы."""
    checks = [
        ("Ollama",       f"{OLLAMA_HOST}/api/tags"),
        ("Qdrant",       f"{QDRANT_HOST}/collections"),
        ("Matrix",       f"{MATRIX_HOST}/_matrix/static/"),
        ("ntfy",         f"{NTFY_HOST}/v1/health"),
        ("Kiwix",        f"{KIWIX_HOST}/"),
    ]
    results = await asyncio.gather(*[check_service(n, u) for n, u in checks])
    ok_count = sum(1 for r in results if r["status"] == "ok")

    health = {
        "timestamp": datetime.now().isoformat(),
        "services": results,
        "summary": f"{ok_count}/{len(checks)} сервисов работают",
        "status": "healthy" if ok_count >= len(checks) * 0.8 else "degraded",
    }
    return health


# ─── OLLAMA INFERENCE (без Claude SDK) ────────────────────────

async def ask_ollama(prompt: str, system: str = "", model: str = None) -> str:
    """Запрос к Ollama API (офлайн режим без Anthropic API)."""
    model = model or MODELS["main"]
    payload = {
        "model": model,
        "stream": False,
        "messages": [],
    }
    if system:
        payload["messages"].append({"role": "system", "content": system})
    payload["messages"].append({"role": "user", "content": prompt})

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            r = await client.post(f"{OLLAMA_HOST}/api/chat", json=payload)
            data = r.json()
            return data.get("message", {}).get("content", "Нет ответа")
    except Exception as e:
        log.error(f"Ollama ошибка: {e}")
        return f"Ошибка подключения к Ollama: {e}"


# ─── CLAUDE SDK INFERENCE ─────────────────────────────────────

async def ask_claude_sdk(prompt: str, agent_name: str) -> str:
    """Запрос через Claude Agent SDK с загрузкой скилла."""
    if not HAS_SDK or not ANTHROPIC_KEY:
        log.info("Claude SDK недоступен — переключаюсь на Ollama")
        skill_text = load_skill(agent_name)
        system = skill_text[:3000] if skill_text else "Ты полезный ассистент NOMAD."
        return await ask_ollama(prompt, system=system)

    skill_text = load_skill(agent_name)
    full_prompt = f"{skill_text}\n\n---\n\nЗапрос: {prompt}" if skill_text else prompt

    result_parts = []
    async for message in query(
        prompt=full_prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Bash", "Read", "Write", "Skill"],
            setting_sources=["user", "project"],
            cwd=str(SKILLS_PATH.parent),
        ),
    ):
        if hasattr(message, "result"):
            result_parts.append(message.result)

    return "\n".join(result_parts) or "Нет ответа"


# ─── MESHTASTIC QUEUE LISTENER ────────────────────────────────

async def meshtastic_listener():
    """Слушать очередь входящих LoRa сообщений и обрабатывать."""
    log.info("📡 Meshtastic listener запущен")
    processed = set()

    while True:
        try:
            if MESHTASTIC_Q.exists():
                lines = MESHTASTIC_Q.read_text().strip().splitlines()
                for line in lines:
                    if line in processed:
                        continue
                    processed.add(line)

                    try:
                        msg = json.loads(line)
                        sender = msg.get("from", "unknown")
                        text = msg.get("text", "")
                        log.info(f"📨 LoRa [{sender}]: {text}")

                        # Если сообщение содержит команду агенту
                        if text.startswith("@nomad "):
                            query_text = text[7:].strip()
                            agent = route_to_agent(query_text)
                            log.info(f"Делегирую [{agent}]: {query_text}")

                            response = await ask_claude_sdk(query_text, agent)

                            # Отправить ответ обратно в LoRa (краткий)
                            short_resp = response[:200]
                            log.info(f"Ответ LoRa: {short_resp}")

                            # Уведомить через ntfy
                            await ntfy_send(
                                "comms",
                                f"[LoRa {sender}]: {text}\n→ {short_resp}",
                            )
                        else:
                            # Просто уведомить о новом сообщении
                            await ntfy_send("comms", f"📡 LoRa [{sender}]: {text}")

                    except json.JSONDecodeError:
                        pass

        except Exception as e:
            log.error(f"Meshtastic listener ошибка: {e}")

        await asyncio.sleep(5)  # проверять каждые 5 секунд


# ─── HEALTH MONITOR ───────────────────────────────────────────

async def health_monitor():
    """Периодически проверять здоровье системы."""
    log.info("🏥 Health monitor запущен")

    while True:
        await asyncio.sleep(3600)  # каждый час
        health = await system_health()

        if health["status"] == "degraded":
            failed = [s["name"] for s in health["services"] if s["status"] != "ok"]
            await ntfy_send(
                "alerts",
                f"⚠️ NOMAD: деградация сервисов: {', '.join(failed)}",
                priority="high",
            )
            log.warning(f"Деградация: {failed}")
        else:
            log.info(f"✅ Система здорова: {health['summary']}")


# ─── FASTAPI ENDPOINTS ────────────────────────────────────────

class AskRequest(BaseModel):
    query: str
    agent: str | None = None


@app.on_event("startup")
async def startup():
    """Запустить фоновые задачи при старте."""
    log.info("🚀 NOMAD Orchestrator (SIGMA) запускается...")
    asyncio.create_task(meshtastic_listener())
    asyncio.create_task(health_monitor())

    # Начальная проверка
    health = await system_health()
    log.info(f"📊 {health['summary']}")
    await ntfy_send("health", f"🚀 NOMAD SIGMA запущен. {health['summary']}")


@app.get("/health")
async def api_health():
    """Статус всех сервисов."""
    return await system_health()


@app.post("/ask")
async def api_ask(req: AskRequest, bg: BackgroundTasks):
    """Задать вопрос агентной системе."""
    agent = req.agent or route_to_agent(req.query)
    log.info(f"Запрос → [{agent}]: {req.query[:80]}")

    response = await ask_claude_sdk(req.query, agent)

    return {
        "query":    req.query,
        "agent":    agent,
        "response": response,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/agents")
async def api_agents():
    """Список доступных агентов."""
    agents = []
    if SKILLS_PATH.exists():
        for skill_dir in SKILLS_PATH.iterdir():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                # Прочитать первые строки для описания
                first_lines = skill_md.read_text()[:500]
                agents.append({
                    "name": skill_dir.name,
                    "path": str(skill_md),
                    "preview": first_lines[:200],
                })
    return {"agents": agents, "total": len(agents)}


@app.get("/status")
async def api_status():
    """Краткий статус (для мобильных приложений)."""
    return {
        "version": "2.0.0",
        "sdk": "claude-agent-sdk" if HAS_SDK else "ollama-only",
        "model": MODELS["main"],
        "skills_path": str(SKILLS_PATH),
        "uptime": "OK",
    }


# ─── MORNING BRIEFING ────────────────────────────────────────

@app.get("/briefing")
async def api_briefing():
    """Утренний брифинг — агрегирует все данные."""
    briefing_prompt = """
    Ты — SIGMA, главный агент NOMAD. Подготовь утренний брифинг в формате СОР:
    
    СИТУАЦИЯ: [проверь docker ps, df, free и опиши состояние системы]
    ОЦЕНКА: [что работает, что требует внимания]
    РЕКОМЕНДАЦИИ: [что сделать сегодня в порядке приоритета]
    
    Дай конкретные цифры: % диска, % RAM, кол-во работающих контейнеров.
    """

    response = await ask_claude_sdk(briefing_prompt, "nomad-orchestrator")
    await ntfy_send("health", f"☀️ Утренний брифинг:\n{response[:500]}")

    return {"briefing": response, "timestamp": datetime.now().isoformat()}


# ─── CLI MODE ────────────────────────────────────────────────

async def cli_mode():
    """Интерактивный CLI режим для тестирования."""
    print("NOMAD SIGMA v2.0 — Интерактивный режим")
    print("Введите запрос или 'exit' для выхода")
    print("-" * 50)

    while True:
        try:
            user_input = input("\n> ").strip()
            if user_input.lower() in ("exit", "quit", "q"):
                break
            if not user_input:
                continue

            agent = route_to_agent(user_input)
            print(f"[Делегирую → {agent}]")

            response = await ask_claude_sdk(user_input, agent)
            print(f"\n{response}")

        except (KeyboardInterrupt, EOFError):
            break

    print("\nNOMAD SIGMA отключён. До свидания.")


# ─── ENTRYPOINT ──────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser(description="NOMAD Agent Orchestrator")
    parser.add_argument("--cli",  action="store_true", help="CLI интерактивный режим")
    parser.add_argument("--port", type=int, default=8099, help="HTTP порт")
    args = parser.parse_args()

    if args.cli:
        asyncio.run(cli_mode())
    else:
        uvicorn.run(
            "orchestrator:app",
            host="0.0.0.0",
            port=args.port,
            reload=False,
            log_level="info",
        )
