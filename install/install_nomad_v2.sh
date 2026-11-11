#!/usr/bin/env bash
# ============================================================
# PROJECT N.O.M.A.D. v2.0 — Full Installer
# github.com/Crosstalk-Solutions/project-nomad
# Март 2026
# ============================================================
# Использование:
#   sudo bash install.sh
#   sudo bash install.sh --profile gpu        # с NVIDIA GPU
#   sudo bash install.sh --profile minimal    # только базовое (RPi5)
#   sudo bash install.sh --skip-models        # без скачивания моделей
# ============================================================

set -euo pipefail
IFS=$'\n\t'

# ====== ЦВЕТА ======
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'; BOLD='\033[1m'

# ====== ФУНКЦИИ ======
header()  { echo -e "\n${BOLD}${CYAN}══════════════════════════════════════${NC}"; echo -e "${BOLD}${CYAN}  $*${NC}"; echo -e "${BOLD}${CYAN}══════════════════════════════════════${NC}"; }
step()    { echo -e "\n${BOLD}${BLUE}▶ $*${NC}"; }
ok()      { echo -e "${GREEN}  ✅ $*${NC}"; }
warn()    { echo -e "${YELLOW}  ⚠️  $*${NC}"; }
err()     { echo -e "${RED}  ❌ $*${NC}"; exit 1; }
info()    { echo -e "     $*"; }

# ====== АРГУМЕНТЫ ======
PROFILE="standard"
SKIP_MODELS=false
SKIP_DOCKER=false

for arg in "$@"; do
    case $arg in
        --profile=*) PROFILE="${arg#*=}";;
        --profile)   shift; PROFILE="${1:-standard}";;
        --skip-models) SKIP_MODELS=true;;
        --skip-docker) SKIP_DOCKER=true;;
        --help)
            echo "Использование: sudo bash install.sh [опции]"
            echo "  --profile=minimal|standard|gpu  (по умолчанию: standard)"
            echo "  --skip-models   не скачивать модели Ollama"
            echo "  --skip-docker   не устанавливать Docker (уже установлен)"
            exit 0;;
    esac
done

# ====== ПРОВЕРКИ ======
header "PROJECT N.O.M.A.D. v2.0 Installer"

[[ $EUID -eq 0 ]] || err "Запусти от root: sudo bash install.sh"

OS_ID=$(. /etc/os-release && echo "$ID")
OS_VERSION=$(. /etc/os-release && echo "$VERSION_ID")
ARCH=$(uname -m)
RAM_GB=$(( $(grep MemTotal /proc/meminfo | awk '{print $2}') / 1024 / 1024 ))
CPU_CORES=$(nproc)

info "ОС: ${OS_ID} ${OS_VERSION}"
info "Архитектура: ${ARCH}"
info "RAM: ${RAM_GB}GB | Ядра: ${CPU_CORES}"

GPU_NVIDIA=$(lspci 2>/dev/null | grep -qi nvidia && echo "yes" || echo "no")
[[ $GPU_NVIDIA == "yes" ]] && info "GPU: NVIDIA обнаружен" || info "GPU: не найден"

# Автовыбор профиля по железу
if [[ $PROFILE == "standard" ]]; then
    if [[ $ARCH == "aarch64" || $RAM_GB -lt 8 ]]; then
        PROFILE="minimal"
        warn "Переключаю на профиль minimal (мало RAM или ARM)"
    elif [[ $GPU_NVIDIA == "yes" && $RAM_GB -ge 16 ]]; then
        PROFILE="gpu"
        warn "Переключаю на профиль gpu (NVIDIA обнаружен)"
    fi
fi

info "Профиль установки: ${BOLD}${PROFILE}${NC}"

# Модель по умолчанию по профилю
case $PROFILE in
    minimal) DEFAULT_MODEL="qwen3.5:2b";   EXTRA_MODEL="" ;;
    standard) DEFAULT_MODEL="qwen3.5:4b"; EXTRA_MODEL="qwen3.5:9b" ;;
    gpu)     DEFAULT_MODEL="qwen3.5:9b";  EXTRA_MODEL="qwen3.5:35b-a3b" ;;
esac

info "Основная AI модель: ${DEFAULT_MODEL}"

# ====== ШАГ 1: ЗАВИСИМОСТИ ======
header "Шаг 1: Системные зависимости"

step "Обновление apt"
apt-get update -qq

step "Установка зависимостей"
apt-get install -y -qq \
    curl wget git python3 python3-pip python3-venv \
    htop iotop ncdu jq unzip \
    ca-certificates gnupg lsb-release \
    usbutils i2c-tools \
    2>/dev/null
ok "Системные пакеты установлены"

# ====== ШАГ 2: DOCKER ======
header "Шаг 2: Docker"

if $SKIP_DOCKER; then
    warn "Пропуск установки Docker (--skip-docker)"
elif command -v docker &>/dev/null; then
    ok "Docker уже установлен: $(docker --version | cut -d' ' -f3)"
else
    step "Установка Docker"
    curl -fsSL https://get.docker.com | sh
    systemctl enable --now docker
    ok "Docker установлен"
fi

# Добавить пользователя в группу docker
if [[ -n "${SUDO_USER:-}" ]]; then
    usermod -aG docker "$SUDO_USER" 2>/dev/null || true
    ok "Пользователь $SUDO_USER добавлен в группу docker"
fi

# ====== ШАГ 3: NVIDIA (если GPU) ======
if [[ $PROFILE == "gpu" ]]; then
    header "Шаг 3: NVIDIA Container Toolkit"
    if dpkg -l | grep -q nvidia-container-toolkit 2>/dev/null; then
        ok "NVIDIA Container Toolkit уже установлен"
    else
        step "Установка NVIDIA Container Toolkit"
        distribution=$(. /etc/os-release && echo "$ID$VERSION_ID")
        curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
            gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit.gpg
        curl -fsSL "https://nvidia.github.io/libnvidia-container/${distribution}/libnvidia-container.list" | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit.gpg] https://#g' | \
            tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
        apt-get update -qq
        apt-get install -y nvidia-container-toolkit
        nvidia-ctk runtime configure --runtime=docker
        systemctl restart docker
        ok "NVIDIA Container Toolkit установлен"
    fi
else
    header "Шаг 3: GPU — пропуск (профиль ${PROFILE})"
fi

# ====== ШАГ 4: PYTHON ЗАВИСИМОСТИ ======
header "Шаг 4: Python пакеты"

step "Установка Python пакетов для агентов"
pip3 install -q --break-system-packages \
    claude-agent-sdk \
    meshtastic \
    smbus2 \
    paho-mqtt \
    requests \
    aiohttp \
    watchdog \
    python-dotenv \
    rich \
    2>/dev/null || pip3 install -q \
    claude-agent-sdk \
    meshtastic \
    smbus2 \
    paho-mqtt \
    requests \
    aiohttp \
    watchdog \
    python-dotenv \
    rich

ok "Python пакеты установлены"

# ====== ШАГ 5: ДИРЕКТОРИИ ======
header "Шаг 5: Структура директорий"

NOMAD_ROOT="/opt/project-nomad"

directories=(
    "$NOMAD_ROOT"
    "$NOMAD_ROOT/data/incoming"
    "$NOMAD_ROOT/data/audiobooks"
    "$NOMAD_ROOT/data/podcasts"
    "$NOMAD_ROOT/data/books"
    "$NOMAD_ROOT/data/music"
    "$NOMAD_ROOT/data/media"
    "$NOMAD_ROOT/data/zim"
    "$NOMAD_ROOT/data/osm"
    "$NOMAD_ROOT/data/weewx"
    "$NOMAD_ROOT/data/sync"
    "$NOMAD_ROOT/data/weather"
    "$NOMAD_ROOT/config/mosquitto"
    "$NOMAD_ROOT/config/ntfy"
    "$NOMAD_ROOT/config/prometheus"
    "$NOMAD_ROOT/config/homepage"
    "$NOMAD_ROOT/config/synapse"
    "$NOMAD_ROOT/config/grafana/provisioning"
    "$NOMAD_ROOT/config/mysql"
    "$NOMAD_ROOT/config/postgres"
    "$NOMAD_ROOT/logs"
    "$NOMAD_ROOT/scripts"
    "$NOMAD_ROOT/agents"
    "$NOMAD_ROOT/skills/.claude/skills"
    "/tmp/meshtastic_queue"
)

for dir in "${directories[@]}"; do
    mkdir -p "$dir"
done
ok "Директории созданы"

# ====== ШАГ 6: КОНФИГУРАЦИОННЫЕ ФАЙЛЫ ======
header "Шаг 6: Конфиги"

# .env файл
if [[ -f "$NOMAD_ROOT/.env" ]]; then
    warn ".env уже существует, пропуск"
else
    step "Генерация .env"
    python3 -c "
import secrets
import socket

hostname = socket.gethostname()
try:
    local_ip = socket.gethostbyname(hostname)
except:
    local_ip = '127.0.0.1'

print(f'''# NOMAD v2.0 - Сгенерировано при установке
NOMAD_HOST={local_ip}
TZ=Asia/Bishkek

MYSQL_ROOT_PASSWORD={secrets.token_hex(16)}
MYSQL_PASSWORD={secrets.token_hex(16)}
POSTGRES_PASSWORD={secrets.token_hex(16)}
DOCMOST_DB_PASS={secrets.token_hex(16)}
DOCMOST_SECRET={secrets.token_hex(32)}
BOOKSTACK_DB_PASS={secrets.token_hex(16)}
VIKUNJA_DB_PASS={secrets.token_hex(16)}
VIKUNJA_JWT_SECRET={secrets.token_hex(32)}
NEXTCLOUD_DB_PASS={secrets.token_hex(16)}
NEXTCLOUD_ADMIN_PASS={secrets.token_hex(12)}
ONLYOFFICE_JWT_SECRET={secrets.token_hex(32)}
HEALTHCHECKS_SECRET={secrets.token_hex(32)}
GRAFANA_PASSWORD=nomad{secrets.token_hex(6)}
VAULTWARDEN_ADMIN_TOKEN={secrets.token_hex(32)}
INFLUX_PASSWORD={secrets.token_hex(16)}
INFLUX_TOKEN={secrets.token_hex(32)}
ANTHROPIC_API_KEY=
MESHTASTIC_PORT=/dev/ttyUSB0
MESHTASTIC_REGION=KZ
MATRIX_SERVER_NAME=nomad.local
MATRIX_ADMIN_PASSWORD={secrets.token_hex(16)}
''')
" > "$NOMAD_ROOT/.env"
    ok ".env создан"
    warn "ОБЯЗАТЕЛЬНО: проверь $NOMAD_ROOT/.env и установи ANTHROPIC_API_KEY если нужен"
fi

# Скопировать конфиги если они есть рядом с установщиком
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for config_src in \
    "$SCRIPT_DIR/config/mosquitto/mosquitto.conf:$NOMAD_ROOT/config/mosquitto/mosquitto.conf" \
    "$SCRIPT_DIR/config/ntfy/server.yml:$NOMAD_ROOT/config/ntfy/server.yml" \
    "$SCRIPT_DIR/config/prometheus/prometheus.yml:$NOMAD_ROOT/config/prometheus/prometheus.yml" \
    "$SCRIPT_DIR/config/homepage/services.yaml:$NOMAD_ROOT/config/homepage/services.yaml"
do
    src="${config_src%%:*}"
    dst="${config_src##*:}"
    if [[ -f "$src" ]] && [[ ! -f "$dst" ]]; then
        cp "$src" "$dst"
        ok "Конфиг: $dst"
    fi
done

# Базовый mosquitto.conf если нет
if [[ ! -f "$NOMAD_ROOT/config/mosquitto/mosquitto.conf" ]]; then
    cat > "$NOMAD_ROOT/config/mosquitto/mosquitto.conf" << 'MQCONF'
persistence true
persistence_location /mosquitto/data/
log_dest stdout
listener 1883 0.0.0.0
listener 9001 0.0.0.0
protocol websockets
allow_anonymous true
MQCONF
    ok "Mosquitto config создан"
fi

# Скопировать скрипты
if [[ -d "$SCRIPT_DIR/scripts" ]]; then
    cp -r "$SCRIPT_DIR/scripts/"* "$NOMAD_ROOT/scripts/"
    chmod +x "$NOMAD_ROOT/scripts/"*.sh 2>/dev/null || true
    ok "Скрипты скопированы"
fi

# Скопировать docker-compose.yml
if [[ -f "$SCRIPT_DIR/docker-compose.yml" ]]; then
    cp "$SCRIPT_DIR/docker-compose.yml" "$NOMAD_ROOT/docker-compose.yml"
    ok "docker-compose.yml скопирован"
fi

# ====== ШАГ 7: ЗАПУСК NOMAD ======
header "Шаг 7: Запуск Docker стека"

cd "$NOMAD_ROOT"

# CPU-only: убрать deploy секцию из compose если нет GPU
if [[ $PROFILE != "gpu" ]]; then
    step "Адаптация docker-compose.yml для CPU-only"
    python3 -c "
import re, sys
with open('docker-compose.yml', 'r') as f:
    content = f.read()
# Убрать deploy/resources секцию для Ollama
content = re.sub(
    r'    deploy:\s+resources:\s+reservations:\s+devices:.*?capabilities: \[gpu\]',
    '',
    content,
    flags=re.DOTALL
)
with open('docker-compose.yml', 'w') as f:
    f.write(content)
print('  docker-compose.yml адаптирован для CPU')
"
fi

step "Pull Docker образов (это займёт время...)"
docker compose pull --quiet 2>/dev/null || warn "Некоторые образы не найдены, продолжаю..."

step "Запуск основного стека"
docker compose up -d

# Ждать запуска
step "Ожидание запуска сервисов (30 сек)..."
sleep 30

# Проверить статус
RUNNING=$(docker ps --filter name=nomad- --filter status=running -q | wc -l)
TOTAL=$(docker ps -a --filter name=nomad- -q | wc -l)
ok "Запущено ${RUNNING}/${TOTAL} контейнеров"

# ====== ШАГ 8: AI МОДЕЛИ ======
if $SKIP_MODELS; then
    header "Шаг 8: AI модели — пропуск (--skip-models)"
else
    header "Шаг 8: Установка AI моделей"

    # Ждать Ollama
    step "Ожидание Ollama..."
    for i in {1..30}; do
        if docker exec nomad-ollama ollama list &>/dev/null 2>&1; then
            ok "Ollama готова"
            break
        fi
        sleep 2
    done

    step "Скачивание основной модели: ${DEFAULT_MODEL}"
    docker exec nomad-ollama ollama pull "$DEFAULT_MODEL"
    ok "${DEFAULT_MODEL} установлена"

    step "Скачивание embedding модели: nomic-embed-text"
    docker exec nomad-ollama ollama pull nomic-embed-text
    ok "nomic-embed-text установлена (RAG)"

    if [[ -n "$EXTRA_MODEL" ]]; then
        step "Скачивание дополнительной модели: ${EXTRA_MODEL}"
        docker exec nomad-ollama ollama pull "$EXTRA_MODEL" || warn "${EXTRA_MODEL} не удалось скачать"
    fi

    # Qdrant коллекции
    step "Создание Qdrant коллекций"
    sleep 5
    for collection in nomad-general nomad-medical nomad-survival nomad-technical nomad-navigation nomad-local; do
        curl -sf -X PUT "http://localhost:6333/collections/${collection}" \
            -H "Content-Type: application/json" \
            -d '{"vectors": {"size": 768, "distance": "Cosine"}}' > /dev/null 2>&1 || true
        info "Коллекция: ${collection}"
    done
    ok "Qdrant коллекции созданы"
fi

# ====== ШАГ 9: SYSTEMD СЕРВИСЫ ======
header "Шаг 9: Systemd сервисы"

# Скопировать сервисы
for svc_file in "$SCRIPT_DIR/systemd/"*.service; do
    [[ -f "$svc_file" ]] || continue
    svc_name=$(basename "$svc_file")
    cp "$svc_file" "/etc/systemd/system/$svc_name"
    ok "Сервис: $svc_name"
done

systemctl daemon-reload

# Включить сервисы
for svc in nomad-orchestrator nomad-meshtastic nomad-rag-watcher; do
    if [[ -f "/etc/systemd/system/${svc}.service" ]]; then
        systemctl enable "$svc" 2>/dev/null || true
        ok "Включён: $svc"
    fi
done

# Запустить только оркестратор (остальные опциональны)
if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
    systemctl start nomad-orchestrator 2>/dev/null || warn "Оркестратор не запустился (нет API ключа?)"
fi

# ====== ШАГ 10: CRON ======
header "Шаг 10: Cron задачи"

CRON_FILE="/etc/cron.d/nomad"
cat > "$CRON_FILE" << 'CRONEOF'
# NOMAD v2.0 Cron Jobs
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Health check — каждый час
0 * * * * root bash /opt/project-nomad/scripts/health_checker.sh >> /opt/project-nomad/logs/health_check.log 2>&1

# Бэкап данных — каждую ночь в 3:00
0 3 * * * root restic -r /mnt/backup/nomad backup /opt/project-nomad/data /opt/project-nomad/config 2>/dev/null && \
    curl -s -d "✅ Ночной бэкап NOMAD OK" http://localhost:8088/backup || \
    curl -s -H "Priority: high" -d "❌ Ошибка бэкапа NOMAD!" http://localhost:8088/backup

# Очистка меташтастик очереди — каждую неделю
0 4 * * 0 root truncate -s 0 /tmp/meshtastic_queue/incoming.jsonl 2>/dev/null || true

# Обновление ZIM каталога — раз в месяц (1-го числа)
0 5 1 * * root docker exec nomad-kiwix kiwix-manage /data/library.xml update >> /opt/project-nomad/logs/zim.log 2>&1 || true
CRONEOF

chmod 644 "$CRON_FILE"
ok "Cron задачи добавлены"

# ====== ФИНАЛЬНАЯ ПРОВЕРКА ======
header "✅ Финальная проверка"

echo ""
echo -e "${BOLD}Статус контейнеров:${NC}"
docker ps --filter name=nomad- --format "  {{.Names}}\t{{.Status}}" | column -t

echo ""
echo -e "${BOLD}Сервисы NOMAD:${NC}"
services=(
    "NOMAD App|http://localhost:8080"
    "OpenWebUI (AI Chat)|http://localhost:3000"
    "Kiwix (Офлайн знания)|http://localhost:8888"
    "Grafana (Мониторинг)|http://localhost:3001"
    "ntfy (Уведомления)|http://localhost:8088"
    "Home Assistant (IoT)|http://localhost:8123"
    "Vikunja (Задачи)|http://localhost:3456"
    "Vaultwarden (Пароли)|http://localhost:8480"
    "Docmost (Вики)|http://localhost:3100"
    "Homepage (Дашборд)|http://localhost:3003"
    "Audiobookshelf|http://localhost:13378"
    "Dockhand (Docker)|http://localhost:9876"
)
for svc in "${services[@]}"; do
    name="${svc%%|*}"
    url="${svc##*|}"
    if curl -sf --max-time 3 "$url" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✅${NC} ${name}: ${CYAN}${url}${NC}"
    else
        echo -e "  ${YELLOW}⏳${NC} ${name}: ${url} (запускается...)"
    fi
done

echo ""
echo -e "${BOLD}Конфигурация:${NC}"
echo -e "  Профиль: ${BOLD}${PROFILE}${NC}"
echo -e "  AI модель: ${BOLD}${DEFAULT_MODEL}${NC}"
NOMAD_IP=$(grep NOMAD_HOST "$NOMAD_ROOT/.env" | cut -d= -f2)
echo -e "  IP сервера: ${BOLD}${NOMAD_IP}${NC}"

echo ""
header "🎉 PROJECT N.O.M.A.D. v2.0 установлен!"
echo ""
echo "  📱 Установи ntfy на телефон:"
echo "     iOS: https://apps.apple.com/app/ntfy/id1625396347"
echo "     Android: https://play.google.com/store/apps/details?id=io.heckel.ntfy"
echo "     Сервер: http://${NOMAD_IP}:8088"
echo ""
echo "  🗺️ Скачай карту Кыргызстана:"
echo "     wget -P $NOMAD_ROOT/data/osm https://download.geofabrik.de/asia/kyrgyzstan-latest.osm.pbf"
echo ""
echo "  📚 Скачай Wikipedia ZIM (Русская, Медицина):"
echo "     https://download.kiwix.org/zim/wikipedia/"
echo "     Сохрани в: $NOMAD_ROOT/data/zim/"
echo ""
echo "  🔑 Установи ANTHROPIC_API_KEY для агентов:"
echo "     nano $NOMAD_ROOT/.env"
echo ""
echo "  🚀 Открой дашборд:"
echo "     http://${NOMAD_IP}:3003"
echo ""
