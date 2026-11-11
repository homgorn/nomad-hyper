#!/bin/bash
# NOMAD v2.0 — Health Checker
# Проверяет все сервисы и отправляет уведомления при проблемах
# Cron: 0 * * * * bash /opt/project-nomad/scripts/health_checker.sh

set -euo pipefail

NTFY_URL="${NTFY_HOST:-http://localhost:8088}"
ERRORS=0
WARNS=0
REPORT=""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ─── ФУНКЦИИ ───────────────────────────────────────────────────

check_http() {
    local name="$1"
    local url="$2"
    local critical="${3:-false}"

    if curl -sf --max-time 5 "$url" > /dev/null 2>&1; then
        printf "${GREEN}✅${NC} %-25s OK\n" "$name"
        REPORT+="✅ $name "
    else
        if [[ "$critical" == "true" ]]; then
            printf "${RED}❌${NC} %-25s FAIL (критичный!)\n" "$name"
            ERRORS=$((ERRORS + 1))
            REPORT+="❌ $name "
            curl -s -H "Priority: urgent" \
                 -H "Title: NOMAD КРИТИЧНО" \
                 -d "❌ $name не отвечает!" \
                 "$NTFY_URL/alerts" > /dev/null || true
        else
            printf "${YELLOW}⚠️${NC}  %-25s WARN\n" "$name"
            WARNS=$((WARNS + 1))
            REPORT+="⚠️ $name "
        fi
    fi
}

check_docker() {
    local name="$1"
    if docker ps --format "{{.Names}}" 2>/dev/null | grep -q "^${name}$"; then
        printf "${GREEN}✅${NC} %-25s RUNNING\n" "docker:$name"
    else
        printf "${RED}❌${NC} %-25s STOPPED\n" "docker:$name"
        ERRORS=$((ERRORS + 1))
        # Попробовать перезапустить
        docker start "$name" 2>/dev/null && \
            printf "   ↳ Перезапущен автоматически\n" || true
    fi
}

# ─── НАЧАЛО ПРОВЕРКИ ──────────────────────────────────────────

echo ""
echo "=== NOMAD HEALTH CHECK $(date '+%Y-%m-%d %H:%M:%S') ==="
echo ""

# CORE
echo "[ CORE ]"
check_http "NOMAD App"    "http://localhost:8080"      true
check_http "Ollama"       "http://localhost:11434/api/tags" true
check_http "Qdrant"       "http://localhost:6333/collections" true
check_http "OpenWebUI"    "http://localhost:3000"      false

# KNOWLEDGE
echo ""
echo "[ KNOWLEDGE ]"
check_http "Kiwix"        "http://localhost:8888"      false
check_http "OSM Maps"     "http://localhost:8081"      false
check_http "Audiobookshelf" "http://localhost:13378"   false
check_http "Calibre-Web"  "http://localhost:8083"      false
check_http "ArchiveBox"   "http://localhost:8090"      false
check_http "Kolibri"      "http://localhost:8082"      false

# COLLABORATION
echo ""
echo "[ COLLABORATION ]"
check_http "Matrix"       "http://localhost:8448/_matrix/static/" false
check_http "ntfy"         "http://localhost:8088/v1/health"       true
check_http "Vikunja"      "http://localhost:3456"      false
check_http "Docmost"      "http://localhost:3100"      false
check_http "Syncthing"    "http://localhost:8384"      false

# SECURITY
echo ""
echo "[ SECURITY ]"
check_http "Vaultwarden"  "http://localhost:8480"      false
check_http "Nginx PM"     "http://localhost:81"        false

# IoT
echo ""
echo "[ IoT ]"
check_http "Home Assistant" "http://localhost:8123"    false
check_http "Node-RED"     "http://localhost:1880"      false
check_http "Grafana"      "http://localhost:3001"      false
check_http "InfluxDB"     "http://localhost:8086/ping" false

# MONITORING
echo ""
echo "[ MONITORING ]"
check_http "Uptime Kuma"  "http://localhost:3002"      false
check_http "Portainer"    "http://localhost:9000"      false
check_http "Homepage"     "http://localhost:3009"      false

# SYSTEM RESOURCES
echo ""
echo "[ RESOURCES ]"

# Диск
DISK_USED=$(df -h / | awk 'NR==2{print $5}' | tr -d '%')
DISK_FREE=$(df -h / | awk 'NR==2{print $4}')
if [[ "$DISK_USED" -gt 90 ]]; then
    printf "${RED}❌${NC} %-25s ${DISK_USED}%% использовано (${DISK_FREE} свободно)\n" "Disk /"
    ERRORS=$((ERRORS + 1))
    curl -s -H "Priority: high" \
         -d "💾 Диск ${DISK_USED}% — критично! Свободно ${DISK_FREE}" \
         "$NTFY_URL/alerts" > /dev/null || true
elif [[ "$DISK_USED" -gt 75 ]]; then
    printf "${YELLOW}⚠️${NC}  %-25s ${DISK_USED}%% использовано (${DISK_FREE} свободно)\n" "Disk /"
    WARNS=$((WARNS + 1))
else
    printf "${GREEN}✅${NC} %-25s ${DISK_USED}%% использовано (${DISK_FREE} свободно)\n" "Disk /"
fi

# RAM
RAM_TOTAL=$(free -m | awk '/Mem:/{print $2}')
RAM_USED=$(free -m | awk '/Mem:/{print $3}')
RAM_PCT=$(awk "BEGIN{printf \"%.0f\", $RAM_USED/$RAM_TOTAL*100}")
if [[ "$RAM_PCT" -gt 90 ]]; then
    printf "${RED}❌${NC} %-25s ${RAM_PCT}%% (${RAM_USED}MB / ${RAM_TOTAL}MB)\n" "RAM"
    ERRORS=$((ERRORS + 1))
elif [[ "$RAM_PCT" -gt 80 ]]; then
    printf "${YELLOW}⚠️${NC}  %-25s ${RAM_PCT}%% (${RAM_USED}MB / ${RAM_TOTAL}MB)\n" "RAM"
    WARNS=$((WARNS + 1))
else
    printf "${GREEN}✅${NC} %-25s ${RAM_PCT}%% (${RAM_USED}MB / ${RAM_TOTAL}MB)\n" "RAM"
fi

# CPU температура (если RPi)
if [ -f /sys/class/thermal/thermal_zone0/temp ]; then
    CPU_TEMP=$(($(cat /sys/class/thermal/thermal_zone0/temp) / 1000))
    if [[ "$CPU_TEMP" -gt 75 ]]; then
        printf "${RED}❌${NC} %-25s ${CPU_TEMP}°C (перегрев!)\n" "CPU Temp"
        ERRORS=$((ERRORS + 1))
    elif [[ "$CPU_TEMP" -gt 65 ]]; then
        printf "${YELLOW}⚠️${NC}  %-25s ${CPU_TEMP}°C\n" "CPU Temp"
        WARNS=$((WARNS + 1))
    else
        printf "${GREEN}✅${NC} %-25s ${CPU_TEMP}°C\n" "CPU Temp"
    fi
fi

# Docker контейнеры
TOTAL_CONTAINERS=$(docker ps -q 2>/dev/null | wc -l)
TOTAL_ALL=$(docker ps -aq 2>/dev/null | wc -l)
printf "${GREEN}✅${NC} %-25s %d/%d запущено\n" "Docker containers" "$TOTAL_CONTAINERS" "$TOTAL_ALL"

# ─── ИТОГ ─────────────────────────────────────────────────────

echo ""
echo "============================================"
if [[ "$ERRORS" -eq 0 && "$WARNS" -eq 0 ]]; then
    printf "${GREEN}✅ Все системы в норме${NC}\n"
    curl -s -d "✅ NOMAD полностью здоров ($(date '+%H:%M'))" \
         "$NTFY_URL/health" > /dev/null || true
elif [[ "$ERRORS" -eq 0 ]]; then
    printf "${YELLOW}⚠️  Предупреждений: %d, Ошибок: 0${NC}\n" "$WARNS"
    curl -s -d "⚠️ NOMAD: $WARNS предупреждений ($(date '+%H:%M'))" \
         "$NTFY_URL/health" > /dev/null || true
else
    printf "${RED}❌ Ошибок: %d | Предупреждений: %d${NC}\n" "$ERRORS" "$WARNS"
    curl -s -H "Priority: high" \
         -d "❌ NOMAD: $ERRORS ошибок, $WARNS предупреждений ($(date '+%H:%M'))" \
         "$NTFY_URL/alerts" > /dev/null || true
fi
echo "============================================"
echo ""

exit $ERRORS
