# NOMAD BMAD Skills Package

## Структура

```
nomad-bmad-skills/
├── README.md                    ← этот файл
│
├── nomad-orchestrator/          ← "SIGMA" — главный оркестратор
│   ├── SKILL.md
│   └── checklists/
│       └── field-departure.md
│
├── nomad-medic/                 ← "DOC" — медицинский агент
│   ├── SKILL.md
│   └── data/
│       └── medications.json
│
├── nomad-survival/              ← "RANGER" — выживание
│   └── SKILL.md
│
├── nomad-comms/                 ← "SIGNAL" — связь и коммуникации
│   └── SKILL.md
│
├── nomad-power/                 ← "WATT" — питание и солнечная система
│   └── SKILL.md
│
├── nomad-iot/                   ← "SENSOR" — IoT и датчики
│   └── SKILL.md
│
├── nomad-rag/                   ← "LIBRARIAN" — база знаний
│   └── SKILL.md
│
├── nomad-sdr/                   ← "SPECTRUM" — SDR радио и погода
│   └── SKILL.md
│
├── nomad-devops/                ← "OPS" — управление Docker стеком
│   └── SKILL.md
│
└── nomad-navigator/             ← "COMPASS" — навигация и карты
    └── SKILL.md
```

## Установка

### Вариант 1: Claude Agent SDK (рекомендуется)

```bash
# Скопировать в системную директорию скиллов
sudo cp -r nomad-bmad-skills/* /opt/project-nomad/skills/.claude/skills/

# Проверить структуру
ls /opt/project-nomad/skills/.claude/skills/
```

```python
# В коде агента
from claude_agent_sdk import query, ClaudeAgentOptions

async for msg in query(
    prompt="...",
    options=ClaudeAgentOptions(
        allowed_tools=["Bash", "Read", "Write", "Skill"],
        setting_sources=["user", "project"],  # загружает Skills из .claude/skills/
        cwd="/opt/project-nomad/skills"
    ),
):
    ...
```

### Вариант 2: Прямая вставка в system prompt

Для каждого агента взять содержимое SKILL.md и добавить в system prompt соответствующей Ollama конфигурации через OpenWebUI.

### Вариант 3: Директивы OpenWebUI

В OpenWebUI → Settings → System Prompt вставить содержимое нужного SKILL.md.

## Активация агентов

| Команда | Агент | Описание |
|---------|-------|---------|
| `@sigma` или `*status` | Orchestrator | Главный координатор |
| `@doc` | Medic | Медицинская помощь |
| `@ranger` | Survival | Выживание |
| `@signal` | Comms | Связь и сообщения |
| `@watt` | Power | Питание и батарея |
| `@sensor` | IoT | Датчики и автоматизация |
| `@librarian` | RAG | База знаний |
| `@spectrum` | SDR | Радио и погода |
| `@ops` | DevOps | Docker и инфраструктура |
| `@compass` | Navigator | Навигация и карты |

## Архитектура агентной системы BMAD

```
Пользователь запрос
      ↓
  SIGMA (Orchestrator)
  ├── Анализ: какой агент нужен?
  ├── Делегирование → специализированному агенту
  ├── Сбор результатов
  └── Компиляция ответа
        ↓
  Специализированный агент (DOC/RANGER/SIGNAL/...)
  ├── Загрузка SKILL.md контекста
  ├── Выполнение commands/workflows
  ├── Использование tools (Bash, RAG, Vision)
  └── Возврат результата → SIGMA
        ↓
  SIGMA → форматирует финальный ответ
      ↓
  Пользователь
```

## Связи между агентами

```
SIGMA
  ↔ DOC       (медицинские ситуации → запрос эвакуации в SIGNAL)
  ↔ RANGER    (выживание → запрос погоды в SPECTRUM)
  ↔ SIGNAL    (все коммуникации проходят через SIGNAL)
  ↔ WATT      (WATT управляет питанием → SIGMA решает что выключить)
  ↔ SENSOR    (IoT алерты → SIGMA принимает решения)
  ↔ LIBRARIAN (все агенты запрашивают знания через LIBRARIAN)
  ↔ SPECTRUM  (погода → RANGER, NAVIGATOR)
  ↔ OPS       (системные проблемы → OPS чинит)
  ↔ COMPASS   (позиции → SIGNAL, маршруты → RANGER)
```

## Добавление собственного агента BMAD

1. Создать директорию: `mkdir nomad-myagent/`
2. Создать SKILL.md со структурой:
```yaml
---
name: nomad-myagent
description: >
  Описание когда активировать. Слова-триггеры.
---

# Agent Name — "CALLSIGN"

## Persona
**role:** ...
**style:** ...
**identity:** ...
**focus:** ...
**core_principles:**
- ...

## Commands
- `*command1` — описание

## Dependencies
**tools:** Bash, Read, Write
**data:** ...

## Startup Instructions
...

## Workflows
### Workflow: Name
...
```

3. Сохранить в `/opt/project-nomad/skills/.claude/skills/nomad-myagent/`
4. Перезапустить агентный слой: `sudo systemctl restart nomad-agents`

## Лицензия

Apache 2.0 — как и базовый проект NOMAD
GitHub: https://github.com/Crosstalk-Solutions/project-nomad
