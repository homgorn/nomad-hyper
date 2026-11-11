# PROJECT N.O.M.A.D. — DEEP RESEARCH: НОВЫЕ МОДУЛИ
**Дата:** Март 2026 | **Запросов:** 50+ | **Источники:** awesome-selfhosted, GitHub, первоисточники

---

## СОДЕРЖАНИЕ

1. [AI / LLM — Голос и Мультимодальность](#1-ai--llm--голос-и-мультимодальность)
2. [Управление Docker / Мониторинг](#2-управление-docker--мониторинг)
3. [Медицина / ЭМК](#3-медицина--эмк)
4. [Библиотека / Медиатека](#4-библиотека--медиатека)
5. [База знаний / Вики](#5-база-знаний--вики)
6. [Файлы и Совместная работа](#6-файлы-и-совместная-работа)
7. [Безопасность / Пароли](#7-безопасность--пароли)
8. [Бэкап и Восстановление](#8-бэкап-и-восстановление)
9. [Архивирование веба](#9-архивирование-веба)
10. [Погода / Природа / Агрономия](#10-погода--природа--агрономия)
11. [Связь и Коммуникации](#11-связь-и-коммуникации)
12. [Задачи / Продуктивность](#12-задачи--продуктивность)
13. [Аналитика и Дашборды](#13-аналитика-и-дашборды)
14. [Финансы и Учёт](#14-финансы-и-учёт)
15. [3D / CAD / Печать](#15-3d--cad--печать)
16. [Игры и Образование](#16-игры-и-образование)
17. [Специфика NOMAD: Выживание](#17-специфика-nomad-выживание)
18. [Матрица приоритетов — все модули](#18-матрица-приоритетов--все-модули)

---

## 1. AI / LLM — ГОЛОС И МУЛЬТИМОДАЛЬНОСТЬ

### 1.1 Wyoming Voice Stack (Whisper + Piper) — КРИТИЧНО

**Что делает:** Полноценный офлайн голосовой конвейер. Говоришь → Whisper транскрибирует → LLM отвечает → Piper озвучивает. Работает полностью без интернета.

**Реальный кейс (март 2026):** Связка wyoming-whisper + wyoming-piper + Ollama Qwen3:4B даёт ответ за ~3-6 секунд на RPi5. Используется как замена Alexa/Google в Home Assistant.

```yaml
services:
  wyoming-whisper:
    image: rhasspy/wyoming-whisper
    container_name: nomad-whisper
    ports: ["10300:10300"]
    volumes: [./data/whisper:/data]
    command: ["--model", "small-int8", "--language", "ru"]
    restart: unless-stopped

  wyoming-piper:
    image: rhasspy/wyoming-piper
    container_name: nomad-piper
    ports: ["10200:10200"]
    volumes: [./data/piper:/data]
    command: ["--voice", "ru_RU-irina-medium"]
    restart: unless-stopped
```

**Ссылки:**
- Whisper Docker: https://hub.docker.com/r/rhasspy/wyoming-whisper
- Piper Docker: https://hub.docker.com/r/rhasspy/wyoming-piper
- Полный гайд 2025: https://brainsteam.co.uk/2025/4/6/adding-voice-to-selfhosted-ai/

**Требования:** RPi5 (small модель), 16GB RAM (large модель)
**Приоритет:** 🔥 ВЫСОКИЙ — бесплатно, critical feature

---

### 1.2 Speaches — OpenAI-совместимый STT/TTS сервер

**Что делает:** Единый контейнер, совместимый с OpenAI API audio endpoints. Поддерживает Whisper (STT) + Kokoro-82M или Piper (TTS). Интегрируется с LiteLLM и OpenWebUI.

```bash
docker run -p 8014:8000 \
  -e WHISPER__TTL=-1 \
  -v /opt/nomad/data/huggingface:/root/.cache/huggingface \
  --name nomad-speaches \
  ghcr.io/speaches-ai/speaches:latest-cpu
```

**Ссылки:** https://speaches.ai

---

### 1.3 LocalAI — универсальный замена OpenAI API

**Что делает:** Drop-in замена OpenAI API. Запускает GGUF модели, Stable Diffusion, Whisper, TTS — всё через один REST API. OpenWebUI подключается как к обычному OpenAI.

```bash
docker run -p 8080:8080 \
  -v /opt/nomad/data/localai:/models \
  --name nomad-localai \
  localai/localai:latest-aio-cpu
```

**GitHub:** https://github.com/mudler/LocalAI
**Приоритет:** Средний — если нужен единый API endpoint

---

### 1.4 LiteLLM — прокси для множества LLM провайдеров

**Что делает:** Роутер запросов между моделями. Автоматический fallback если модель перегружена. Rate limiting. Подходит для multi-model NOMAD setup.

**GitHub:** https://github.com/BerriAI/litellm
**Приоритет:** Средний — для продвинутых конфигураций

---

## 2. УПРАВЛЕНИЕ DOCKER / МОНИТОРИНГ

### 2.1 Dockhand — НОВИНКА 2026, убивает 7 инструментов сразу

**Что делает:** Единый контейнер-мега-инструмент (конец 2025, взрывной рост в 2026):
- Управление контейнерами (замена Portainer CE)
- Realtime логи с историей (замена Dozzle)
- Мониторинг ресурсов (замена Beszel)
- Автообновление контейнеров (замена Watchtower)
- Уведомления через Apprise (замена Diun)
- Визуальный редактор Compose + Git sync (замена Dockge)
- Сканирование уязвимостей (Grype + Trivy)

**⚠️ Ранний проект** — использовать с осторожностью в продакшне.

```yaml
services:
  dockhand:
    image: ghcr.io/dockhand/dockhand:latest
    container_name: nomad-dockhand
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./data/dockhand:/data
    ports: ["9876:8080"]
    restart: unless-stopped
```

**GitHub:** https://github.com/dockhand/dockhand
**Источник:** https://mariushosting.com/farewell-to-7-docker-tools-dockhand-just-killed-them-all-in-one-go/
**Приоритет:** 🔥 ВЫСОКИЙ — сильно упрощает управление

---

### 2.2 Dozzle — realtime логи контейнеров

**Что делает:** Веб-интерфейс для просмотра логов Docker в реальном времени. Без БД, без хранения. 8MB контейнер. Оповещения в ntfy/Discord через SQL-выражения.

```yaml
services:
  dozzle:
    image: amir20/dozzle:latest
    container_name: nomad-dozzle
    volumes: [/var/run/docker.sock:/var/run/docker.sock]
    ports: ["8892:8080"]
    restart: unless-stopped
```

**Сайт:** https://dozzle.dev/
**Приоритет:** Средний (если не используешь Dockhand)

---

### 2.3 Portainer CE — полный Docker менеджмент

**Что делает:** Полнофункциональный UI для Docker. Деплой стеков, управление образами, volumes, networks. Подходит для командного использования.

```bash
docker run -d -p 9000:9000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  --name nomad-portainer \
  portainer/portainer-ce:latest
```

**Сайт:** https://www.portainer.io/
**Приоритет:** Средний (или Dockhand)

---

### 2.4 Homepage — стартовая страница для всех сервисов

**Что делает:** Красивый дашборд со всеми сервисами NOMAD. YAML-конфиг. Виджеты: Ollama статус, CPU/RAM, погода, контейнеры.

```yaml
services:
  homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: nomad-homepage
    ports: ["3002:3000"]
    volumes:
      - ./config/homepage:/app/config
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped
```

**GitHub:** https://github.com/gethomepage/homepage
**Приоритет:** 🔥 ВЫСОКИЙ — единая точка входа для всех сервисов NOMAD

---

### 2.5 Dashy — альтернативная стартовая страница

**Что делает:** Кастомизируемый дашборд с иконками, статусами, виджетами. Поддержка тем.

**GitHub:** https://github.com/Lissy93/dashy
**Приоритет:** Альтернатива Homepage

---

### 2.6 Beszel — лёгкий системный мониторинг

**Что делает:** Мониторинг CPU/RAM/диск/сеть с историей. Агентная архитектура для мониторинга нескольких хостов. Легче Netdata, красивее Cockpit.

**GitHub:** https://github.com/henrygd/beszel
**Приоритет:** Средний

---

### 2.7 Watchtower — автообновление контейнеров

**Что делает:** Мониторит Docker Hub, автоматически обновляет контейнеры при выходе новых версий. Уведомление в ntfy при обновлении.

```yaml
services:
  watchtower:
    image: containrrr/watchtower
    volumes: [/var/run/docker.sock:/var/run/docker.sock]
    environment:
      - WATCHTOWER_NOTIFICATIONS=generic
      - WATCHTOWER_NOTIFICATION_URL=http://nomad-ntfy:80/updates
    restart: unless-stopped
```

**GitHub:** https://github.com/containrrr/watchtower
**Приоритет:** Средний

---

## 3. МЕДИЦИНА / ЭМК

### 3.1 Bahmni (OpenMRS + OpenELIS + Odoo) — полная медицинская система

**Что делает:** Система EMR для малообеспеченных регионов. OpenMRS для ЭМК + OpenELIS для лабораторий + Odoo для аптеки/инвентаря. Используется в 600+ учреждениях в 40+ странах. Признана Digital Public Good.

**Bahmni Standard v1.0.0** включает:
- ЭМК (Bahmni UI + OpenMRS)
- Лаборатория (OpenELIS)
- Аптека + инвентарь (Odoo)
- PACS (рентген-снимки)
- Офлайн режим
- FHIR API

**⚠️ Тяжёлый стек** — минимум 16GB RAM, не для RPi.

```bash
git clone https://github.com/Bahmni/bahmni-docker.git
cd bahmni-docker
docker compose up -d
```

**GitHub:** https://github.com/Bahmni/bahmni-docker
**Сайт:** https://www.bahmni.org/
**Подходит для:** Полевые медицинские пункты, клиники, экспедиции с медицинским персоналом.
**Приоритет:** Средний (только с мощным железом)

---

### 3.2 OpenEMR — лёгкий вариант ЭМК

**Что делает:** Открытый EMR, более лёгкий чем Bahmni. HIPAA-совместимый. Запись пациентов, рецепты, расписание. Работает на 8GB RAM.

```bash
docker pull openemr/openemr:latest
```

**GitHub:** https://github.com/openemr/openemr
**Сайт:** https://www.open-emr.org/
**Приоритет:** Средний

---

### 3.3 Healthchecks — мониторинг здоровья cron-задач (не медицина!)

**Что делает:** Мониторинг периодических задач. Если скрипт бэкапа не отправил пинг — уведомление в ntfy. Критично для надёжности NOMAD.

**GitHub:** https://github.com/healthchecks/healthchecks
**Приоритет:** Высокий — для всех cron задач NOMAD

---

## 4. БИБЛИОТЕКА / МЕДИАТЕКА

### 4.1 Audiobookshelf — аудиокниги и подкасты

**Что делает:** Self-hosted сервер аудиокниг и подкастов. iOS/Android приложения с офлайн прослушиванием. Синхронизация прогресса между устройствами.

```yaml
services:
  audiobookshelf:
    image: ghcr.io/advplyr/audiobookshelf:latest
    container_name: nomad-audiobookshelf
    ports: ["13378:80"]
    volumes:
      - ./data/audiobooks:/audiobooks
      - ./data/podcasts:/podcasts
      - ./data/audiobookshelf/config:/config
      - ./data/audiobookshelf/metadata:/metadata
    restart: unless-stopped
```

**Сайт:** https://www.audiobookshelf.org/
**Для NOMAD:** Офлайн курсы выживания, медицинские аудиогиды, языковые курсы.
**Приоритет:** 🔥 ВЫСОКИЙ — логичное дополнение к Kiwix

---

### 4.2 Calibre-Web — библиотека электронных книг

**Что делает:** Веб-интерфейс для коллекции электронных книг. 50+ форматов. Конвертация форматов. OPDS feed для Kobo/Kindle. Чтение в браузере.

```yaml
services:
  calibre-web:
    image: lscr.io/linuxserver/calibre-web:latest
    container_name: nomad-calibre-web
    environment:
      - PUID=1000
      - PGID=1000
    volumes:
      - ./data/calibre/config:/config
      - ./data/calibre/books:/books
    ports: ["8083:8083"]
    restart: unless-stopped
```

**GitHub:** https://github.com/janeczku/calibre-web
**Для NOMAD:** Медицинские справочники, учебники, технические руководства, романы.
**Приоритет:** 🔥 ВЫСОКИЙ

---

### 4.3 Kavita — манга, комиксы, книги

**Что делает:** Сервер для EPUB, PDF, CBZ/CBR (манга/комиксы). Быстрый. Jellyfin-подобный интерфейс.

**GitHub:** https://github.com/Kareadita/Kavita
**Приоритет:** Средний

---

### 4.4 Jellyfin — медиасервер (видео/аудио)

**Что делает:** Streaming видео, музыки, фотографий. Транскодирование. iOS/Android/TV приложения. Работает офлайн в LAN.

```yaml
services:
  jellyfin:
    image: jellyfin/jellyfin:latest
    container_name: nomad-jellyfin
    volumes:
      - ./data/jellyfin/config:/config
      - ./data/jellyfin/cache:/cache
      - ./data/media:/media
    ports:
      - "8096:8096"
    restart: unless-stopped
```

**Для NOMAD:** Обучающие видео, инструкции, документальные фильмы, образовательный контент.
**GitHub:** https://github.com/jellyfin/jellyfin
**Приоритет:** Средний (Kolibri уже есть — перекрытие)

---

### 4.5 BookLore — новый красивый ридер (2025)

**Что делает:** Современный интерфейс библиотеки (Jellyfin-стиль). EPUB/PDF/CBZ. Прогресс чтения. Kobo sync. OPDS.

**GitHub:** https://github.com/adityachandupatla/booklore (проверь актуальный репозиторий)
**Приоритет:** Альтернатива Calibre-Web

---

## 5. БАЗА ЗНАНИЙ / ВИКИ

### 5.1 Docmost — коллаборативная вики (офлайн-ready!)

**Что делает:** Открытый аналог Confluence/Notion. Realtime совместное редактирование. Пространства по темам. Встроенные диаграммы (Draw.io, Excalidraw, Mermaid).

**Ключевая особенность:** Air-gapped ready — работает полностью без интернета.

```yaml
services:
  docmost:
    image: docmost/docmost:latest
    container_name: nomad-docmost
    ports: ["3100:3000"]
    environment:
      - APP_URL=http://nomad.local:3100
      - DATABASE_URL=postgresql://docmost:pass@nomad-postgres:5432/docmost
      - REDIS_URL=redis://nomad-redis:6379
    depends_on:
      - nomad-postgres
      - nomad-redis
    restart: unless-stopped
```

**GitHub:** https://github.com/docmost/docmost
**Для NOMAD:** Командная документация, процедуры, медицинские протоколы, руководства.
**Приоритет:** 🔥 ВЫСОКИЙ

---

### 5.2 BookStack — структурированная база знаний

**Что делает:** Книги → Главы → Страницы. WYSIWYG редактор. Проще Docmost, не требует Redis. PHP + MySQL.

```yaml
services:
  bookstack:
    image: lscr.io/linuxserver/bookstack:latest
    container_name: nomad-bookstack
    environment:
      - APP_URL=http://nomad.local:6875
      - DB_HOST=nomad-mysql
      - DB_USER=bookstack
      - DB_PASS=bookstackpass
      - DB_DATABASE=bookstack
    ports: ["6875:80"]
    restart: unless-stopped
```

**GitHub:** https://github.com/BookStackApp/BookStack
**Приоритет:** Средний (альтернатива Docmost)

---

### 5.3 Wiki.js — мощная вики

**Что делает:** Node.js вики. Git интеграция (версионирование страниц). Множество форматов (Markdown, WYSIWYG). Поиск. Docker Compose с PostgreSQL.

**GitHub:** https://github.com/requarks/wiki
**Приоритет:** Средний

---

### 5.4 DokuWiki — без БД, только файлы

**Что делает:** Вики на плоских файлах. Нет базы данных. Молниеносно устанавливается. Надёжна. Экономит ресурсы.

**GitHub:** https://github.com/dokuwiki/dokuwiki
**Для NOMAD:** Лучший выбор для RPi/слабого железа.
**Приоритет:** Высокий для слабого железа

---

## 6. ФАЙЛЫ И СОВМЕСТНАЯ РАБОТА

### 6.1 Nextcloud — файловое хранилище + офис

**Что делает:** Google Drive замена. Файлы, фото, контакты, календарь, видеоконференции (Talk). Sync клиенты iOS/Android/Desktop. Работает офлайн в LAN.

**+ONLYOFFICE** или **+Collabora** = редактирование Word/Excel/PowerPoint документов прямо в браузере.

```yaml
services:
  nextcloud:
    image: nextcloud:latest
    container_name: nomad-nextcloud
    ports: ["8445:80"]
    volumes:
      - ./data/nextcloud:/var/www/html
    environment:
      - MYSQL_HOST=nomad-mysql
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - MYSQL_PASSWORD=nextcloudpass
    restart: unless-stopped

  onlyoffice:
    image: onlyoffice/documentserver:latest
    container_name: nomad-onlyoffice
    ports: ["8000:80"]
    volumes:
      - ./data/onlyoffice/logs:/var/log/onlyoffice
      - ./data/onlyoffice/data:/var/www/onlyoffice/Data
    restart: unless-stopped
```

**⚠️ Тяжёлый стек:** ONLYOFFICE требует 4GB RAM отдельно. Только для мощного железа.

**Сайт:** https://nextcloud.com/
**ONLYOFFICE:** https://github.com/ONLYOFFICE/onlyoffice-nextcloud
**Приоритет:** Средний (для команды) / Низкий (для одного пользователя)

---

### 6.2 Syncthing — P2P синхронизация файлов

**Что делает:** Синхронизация файлов между устройствами без сервера-посредника. Работает в LAN без интернета. Идеален для синхронизации ZIM коллекций между NOMAD узлами.

```yaml
services:
  syncthing:
    image: lscr.io/linuxserver/syncthing:latest
    container_name: nomad-syncthing
    ports:
      - "8384:8384"  # Web UI
      - "22000:22000/tcp"  # File sync
      - "22000:22000/udp"
    volumes:
      - ./data/syncthing/config:/config
      - ./data/nomad_sync:/data1
    restart: unless-stopped
```

**Сайт:** https://syncthing.net/
**Для NOMAD:** Синхронизация ZIM, моделей, конфигов между несколькими NOMAD узлами.
**Приоритет:** 🔥 ВЫСОКИЙ

---

### 6.3 Memos — быстрые заметки

**Что делает:** Twitter-подобный интерфейс для личных заметок. Markdown. Легковесный. Полностью офлайн.

**GitHub:** https://github.com/usememos/memos
**Приоритет:** Средний

---

## 7. БЕЗОПАСНОСТЬ / ПАРОЛИ

### 7.1 Vaultwarden — менеджер паролей (Bitwarden совместимый)

**Что делает:** Лёгкий (Rust) аналог Bitwarden сервера. 50MB RAM. Работает на RPi. Использует официальные Bitwarden приложения (iOS/Android/браузер). E2E шифрование AES-256.

```yaml
services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: nomad-vaultwarden
    ports: ["8480:80"]
    volumes: [./data/vaultwarden:/data]
    environment:
      - ADMIN_TOKEN=${VAULTWARDEN_TOKEN}
      - SIGNUPS_ALLOWED=false
      - WEBSOCKET_ENABLED=true
    restart: unless-stopped
```

**GitHub:** https://github.com/dani-garcia/vaultwarden
**Для NOMAD:** Хранение паролей команды, SSH ключей, API ключей — всё офлайн.
**Приоритет:** 🔥 ВЫСОКИЙ

---

### 7.2 Authelia — двухфакторная аутентификация

**Что делает:** SSO + MFA для всех сервисов NOMAD. TOTP, WebAuthn. Интеграция с Nginx Proxy Manager/Traefik.

**GitHub:** https://github.com/authelia/authelia
**Приоритет:** Средний (если нужна auth перед NOMAD)

---

### 7.3 Nginx Proxy Manager — обратный прокси с SSL

**Что делает:** Красивый UI для настройки Nginx reverse proxy. Let's Encrypt / mkcert для HTTPS. Нужен для PWA и безопасного доступа к NOMAD сервисам.

```yaml
services:
  nginx-proxy-manager:
    image: jc21/nginx-proxy-manager:latest
    container_name: nomad-nginx-pm
    ports:
      - "80:80"
      - "443:443"
      - "81:81"  # Admin UI
    volumes:
      - ./data/nginx-pm/data:/data
      - ./data/nginx-pm/letsencrypt:/etc/letsencrypt
    restart: unless-stopped
```

**GitHub:** https://github.com/NginxProxyManager/nginx-proxy-manager
**Приоритет:** Высокий — нужен для HTTPS/PWA

---

## 8. БЭКАП И ВОССТАНОВЛЕНИЕ

### 8.1 Restic — рекомендуемый бэкап для NOMAD

**Почему Restic:** Лучший баланс надёжности и простоты. Не ломал репозитории. Работает везде. Сообщество огромное.

```bash
# Установка
apt install restic

# Инициализация репозитория на внешнем диске
restic -r /mnt/backup/nomad init

# Бэкап всего NOMAD
restic -r /mnt/backup/nomad backup \
  /opt/project-nomad/data \
  /opt/project-nomad/config \
  --exclude /opt/project-nomad/data/kiwix  # ZIM файлы большие — бэкапить отдельно

# Расписание (cron) — каждую ночь
echo "0 3 * * * root restic -r /mnt/backup/nomad backup /opt/project-nomad/data && \
  restic -r /mnt/backup/nomad forget --prune --keep-daily 7 --keep-weekly 4" \
  > /etc/cron.d/nomad-backup

# Уведомление при успехе/ошибке
curl -d "✅ Бэкап NOMAD завершён" http://localhost:8088/backup
```

**Сайт:** https://restic.net/
**GitHub:** https://github.com/restic/restic

---

### 8.2 BorgBackup + Borgmatic — эффективный бэкап

**Почему Borg:** Лучшая дедупликация. Быстрее Restic на инкрементальных бэкапах. FUSE mount для просмотра архивов как файловой системы.

```yaml
# borgmatic.yml
location:
  source_directories:
    - /opt/project-nomad/data
    - /opt/project-nomad/config
  repositories:
    - /mnt/backup/borg-nomad

storage:
  encryption_passphrase: "ТВОЙ_ПАРОЛЬ"
  compression: lz4

retention:
  keep_daily: 7
  keep_weekly: 4
  keep_monthly: 3

hooks:
  on_error:
    - curl -d "❌ Ошибка бэкапа NOMAD!" http://localhost:8088/backup
  after_backup:
    - curl -d "✅ Бэкап NOMAD OK" http://localhost:8088/backup
```

**GitHub Borg:** https://github.com/borgbackup/borg
**GitHub Borgmatic:** https://github.com/borgmatic-collective/borgmatic
**Сравнение 2026:** https://selfhosting.sh/compare/kopia-vs-restic/
**Приоритет:** 🔥 ВЫСОКИЙ — один из самых важных модулей

---

### 8.3 Volsync / Stash — бэкап Docker volumes

**Что делает:** Специализированный бэкап Docker volumes. Можно использовать в связке с Restic.

```bash
# Простой скрипт бэкапа volumes
for vol in $(docker volume ls -q); do
  docker run --rm \
    -v $vol:/source:ro \
    -v /mnt/backup/volumes:/backup \
    alpine tar czf /backup/${vol}_$(date +%Y%m%d).tar.gz -C /source .
done
```

---

## 9. АРХИВИРОВАНИЕ ВЕБА

### 9.1 ArchiveBox — веб-архив офлайн (27k+ звёзд!)

**Что делает:** Сохраняет веб-страницы в нескольких форматах: HTML, PDF, PNG скриншот, WARC, article text, видео/аудио. Идеальная архивная копия критичных ресурсов.

**Для NOMAD:** Скачать важные статьи, руководства, медицинские ресурсы ПЕРЕД отключением от интернета.

```yaml
services:
  archivebox:
    image: archivebox/archivebox:latest
    container_name: nomad-archivebox
    ports: ["8090:8000"]
    volumes:
      - ./data/archivebox:/data
    command: server --quick-init 0.0.0.0:8000
    restart: unless-stopped
```

```bash
# Добавить URL для архивирования
docker exec nomad-archivebox archivebox add 'https://survival.ru/guide'

# Добавить из RSS ленты
docker exec nomad-archivebox archivebox add 'https://healthguide.org/feed.xml'

# Массовое добавление из файла
cat urls.txt | docker exec -i nomad-archivebox archivebox add

# Расписание: каждый день проверять RSS
echo "0 6 * * * docker exec nomad-archivebox archivebox schedule --every=day 'https://...' " \
  >> /etc/cron.d/archivebox
```

**GitHub:** https://github.com/ArchiveBox/ArchiveBox
**Сайт:** https://archivebox.io/
**Приоритет:** 🔥 ВЫСОКИЙ — сохрани веб пока есть интернет

---

### 9.2 Wallabag — офлайн-reader статей

**Что делает:** Pocket-замена. Сохраняет статьи для офлайн чтения. iOS/Android приложения. Полнотекстовый поиск.

```yaml
services:
  wallabag:
    image: wallabag/wallabag:latest
    container_name: nomad-wallabag
    ports: ["8091:80"]
    volumes:
      - ./data/wallabag/images:/var/www/wallabag/web/assets/images
    restart: unless-stopped
```

**GitHub:** https://github.com/wallabag/wallabag
**Приоритет:** Средний

---

## 10. ПОГОДА / ПРИРОДА / АГРОНОМИЯ

### 10.1 WeeWX — метеостанция офлайн

**Что делает:** Собирает данные с физической метеостанции (Davis, Oregon, Fine Offset, ...) или SDR-датчиков. Генерирует HTML-дашборды, графики, отчёты. Работает на RPi.

```yaml
services:
  weewx:
    image: felddy/weewx:5
    container_name: nomad-weewx
    volumes:
      - ./data/weewx:/data
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0  # USB метеостанция
    restart: unless-stopped
```

**Поддерживаемые устройства:** Davis VantagePro, Oregon Scientific, Fine Offset (множество брендов), RTL-SDR (через плагин).

**GitHub:** https://github.com/weewx/weewx
**Docker:** https://github.com/felddy/weewx-docker
**Для NOMAD:** Гиперлокальные данные о погоде, история, прогнозы на основе трендов.
**Приоритет:** Высокий (если есть метеостанция или RTL-SDR)

---

### 10.2 iNaturalist Local / Plantnet API — идентификация растений

**Что делает:** Идентификация растений и животных по фото. Нативно онлайн, но:
- **Qwen3.5-VL** + локальный датасет растений → офлайн идентификация
- **PlantNet** скачать базу данных локально (проект поддерживает офлайн БД)

**Для NOMAD:** "Сфотографировал растение в горах Кыргызстана → определил, съедобно ли оно".

**Реализация для NOMAD:**
1. Скачать датасет PlantNet (ограниченная региональная версия)
2. Файн-тюнить или использовать Qwen3.5-VL с системным промптом и примерами
3. RAG из ZIM Wikipedia по местным растениям

**PlantNet API:** https://my.plantnet.org/ (для онлайн версии)
**Приоритет:** Средний (через Qwen3.5-VL vision)

---

### 10.3 NOAA APT Decoder — спутниковые снимки погоды

**Что делает:** Автоматическое получение снимков с NOAA метеоспутников через RTL-SDR. Без интернета — реальные снимки из космоса каждые 2-3 часа.

```bash
# noaa-apt для декодирования
pip install noaa-apt
# или Docker
docker run --device /dev/bus/usb noaa-apt-docker

# Расписание: спутники проходят над KG:
# NOAA-15: несколько раз в сутки
# NOAA-18: несколько раз в сутки
# NOAA-19: несколько раз в сутки
```

**GitHub:** https://github.com/martinber/noaa-apt
**Приоритет:** Высокий (если есть RTL-SDR)

---

## 11. СВЯЗЬ И КОММУНИКАЦИИ

### 11.1 Gotify — альтернатива ntfy

**Что делает:** Push уведомления. Android приложение. REST API. Если уже используешь, не меняй — но ntfy лучше для новых установок.

**GitHub:** https://github.com/gotify/server
**Приоритет:** Низкий (ntfy лучше)

---

### 11.2 Jitsi Meet — видеоконференции офлайн

**Что делает:** Полностью self-hosted видеозвонки. Работает в LAN. Не нужен STUN/TURN сервер если все в одной сети.

```yaml
services:
  jitsi-web:
    image: jitsi/web:stable-9584
    container_name: nomad-jitsi-web
    ports: ["8443:443"]
    volumes:
      - ./data/jitsi/web:/config
    restart: unless-stopped
```

**GitHub:** https://github.com/jitsi/docker-jitsi-meet
**Для NOMAD:** Видеозвонки между устройствами в LAN без интернета.
**Приоритет:** Средний

---

### 11.3 Rallly — голосование за время встречи

**Что делает:** Doodle-замена. Планирование встреч голосованием. Работает офлайн в LAN.

**GitHub:** https://github.com/lukevella/rallly
**Приоритет:** Низкий

---

## 12. ЗАДАЧИ / ПРОДУКТИВНОСТЬ

### 12.1 Plane — проект-менеджмент (GitHub Issues аналог)

**Что делает:** Таски, спринты, epics, roadmap. Открытая альтернатива Jira/Linear. Docker.

```yaml
services:
  plane-web:
    image: makeplane/plane-frontend:stable
    container_name: nomad-plane-web
    restart: unless-stopped
```

**GitHub:** https://github.com/makeplane/plane
**Приоритет:** Средний (Vikunja проще для NOMAD)

---

### 12.2 Actual Budget — личные финансы офлайн

**Что делает:** Мощный личный бюджетный трекер. Работает полностью офлайн. iOS/Android/Desktop. Zero-based budgeting метод.

```yaml
services:
  actual:
    image: actualbudget/actual-server:latest
    container_name: nomad-actual
    ports: ["5006:5006"]
    volumes: [./data/actual:/data]
    restart: unless-stopped
```

**GitHub:** https://github.com/actualbudget/actual
**Приоритет:** Средний — для off-grid финансового планирования

---

### 12.3 Leantime — проект-менеджмент для некоммерческих

**Что делает:** Доступный PM инструмент. Kanban, Gantt, идеи, ретроспективы.

**GitHub:** https://github.com/Leantime/leantime
**Приоритет:** Низкий

---

## 13. АНАЛИТИКА И ДАШБОРДЫ

### 13.1 Prometheus — метрики всего

**Что делает:** Pull-based метрики. Собирает данные с Docker, Node (железо), Kiwix, Ollama, PostgreSQL. Time-series БД.

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: nomad-prometheus
    ports: ["9090:9090"]
    volumes:
      - ./config/prometheus:/etc/prometheus
      - ./data/prometheus:/prometheus
    restart: unless-stopped
```

**Экспортеры для NOMAD:**
- `prom/node-exporter` — CPU, RAM, диск, сеть
- `prom/mysqld-exporter` — MySQL метрики
- `oliver006/redis_exporter` — Redis метрики
- Ollama имеет встроенный `/metrics` endpoint

**GitHub:** https://github.com/prometheus/prometheus
**Приоритет:** Средний (Grafana уже есть в стеке)

---

### 13.2 cAdvisor — метрики Docker контейнеров

**Что делает:** Анализ ресурсов каждого контейнера. Интеграция с Prometheus.

```yaml
services:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: nomad-cadvisor
    ports: ["8404:8080"]
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    restart: unless-stopped
```

**GitHub:** https://github.com/google/cadvisor
**Приоритет:** Средний

---

## 14. ФИНАНСЫ И УЧЁТ

### 14.1 Firefly III — полнофункциональная финансовая система

**Что делает:** Учёт доходов/расходов. Бюджеты. Отчёты. REST API. Поддержка множества счетов и валют.

```yaml
services:
  firefly-iii:
    image: fireflyiii/core:latest
    container_name: nomad-firefly
    ports: ["8200:8080"]
    volumes: [./data/firefly:/var/www/html/storage/upload]
    restart: unless-stopped
```

**GitHub:** https://github.com/firefly-iii/firefly-iii
**Приоритет:** Низкий (для специфических задач)

---

## 15. 3D / CAD / ПЕЧАТЬ

### 15.1 OctoPrint — управление 3D-принтером

**Что делает:** Веб-интерфейс для 3D-принтера. Печать файлов, мониторинг температуры, камера.

```yaml
services:
  octoprint:
    image: octoprint/octoprint:latest
    container_name: nomad-octoprint
    ports: ["5000:5000"]
    devices: [/dev/ttyUSB0:/dev/ttyUSB0]
    volumes: [./data/octoprint:/octoprint]
    restart: unless-stopped
```

**GitHub:** https://github.com/OctoPrint/OctoPrint
**Для NOMAD:** Печать запчастей, медицинских приспособлений, инструментов в поле.
**Приоритет:** Средний (только при наличии 3D-принтера)

---

### 15.2 FreeCAD + FreeCAD Web Server

**Что делает:** Параметрическое 3D-моделирование. Не Docker, но важен для off-grid инженерии.

**Сайт:** https://www.freecad.org/
**Приоритет:** Низкий (standalone)

---

## 16. ИГРЫ И ОБРАЗОВАНИЕ

### 16.1 Minetest — офлайн игра (образовательная)

**Что делает:** Open-source Minecraft. Работает без интернета. Полностью офлайн. Образовательный потенциал.

```yaml
services:
  minetest:
    image: linuxserver/minetest:latest
    container_name: nomad-minetest
    ports: ["30000:30000/udp"]
    volumes: [./data/minetest:/config/.minetest]
    restart: unless-stopped
```

**GitHub:** https://github.com/minetest/minetest
**Для NOMAD:** Детское образование и развлечение в изоляции.
**Приоритет:** Низкий (опциональный)

---

### 16.2 Open Surge — игровой движок

Легковесная 2D игра. Для детского образования.
**Приоритет:** Низкий

---

## 17. СПЕЦИФИКА NOMAD: ВЫЖИВАНИЕ

### 17.1 Растительный RAG-агент (кастомный)

**Что делает:** Qwen3.5-VL + база данных растений КГ + iNaturalist данные → идентификация и описание съедобности/токсичности.

**Реализация:**
1. Собрать датасет: растения Кыргызстана (Tian Shan, Pamiro-Alai) из GBIF
2. Создать PDF справочник с фото + RAG индексирование
3. System prompt с инструкцией агенту-ботанику
4. Vision модель для анализа фото

**Источники данных:**
- GBIF Kyrgyzstan: https://www.gbif.org/country/KG
- Flora of Middle Asia (доступна в PDF)
- ZIM: Wikipedia по флоре Средней Азии

---

### 17.2 Офлайн карты с треками (OrganicMaps сервер)

**Что делает:** Хост для *.obf файлов OsmAnd и org-форматов для OsmAnd/Organic Maps.

**Реализация:**
```bash
# Скачать Кыргызстан
wget https://download.geofabrik.de/asia/kyrgyzstan-latest.osm.pbf

# Конвертировать в .obf для OsmAnd через OsmAndMapCreator
java -jar OsmAndMapCreator.jar -q kyrgyzstan-latest.osm.pbf
```

---

### 17.3 ATAK (Android Team Awareness Kit)

**Что делает:** Военная/спасательная система позиционирования команды. Бесплатная версия — WinTAK (Windows). Серверная часть — FreeTAK Server.

```yaml
services:
  freetakserver:
    image: freetakteam/freetakserver:latest
    container_name: nomad-fts
    ports:
      - "8087:8087"    # TCP CoT
      - "8080:8080"    # Rest API
      - "19023:19023"  # SSL CoT
    restart: unless-stopped
```

**GitHub:** https://github.com/FreeTAKTeam/FreeTAKServer
**Для NOMAD:** SAR операции, трекинг команды на карте, обмен позициями.
**Приоритет:** Высокий для серьёзных полевых операций

---

### 17.4 Navidrome — офлайн музыкальный сервер

**Что делает:** Subsonic API-совместимый сервер. Streaming музыки. iOS/Android клиенты (DSub, Symfonium).

```yaml
services:
  navidrome:
    image: deluan/navidrome:latest
    container_name: nomad-navidrome
    ports: ["4533:4533"]
    volumes:
      - ./data/navidrome:/data
      - ./data/music:/music:ro
    restart: unless-stopped
```

**GitHub:** https://github.com/navidrome/navidrome
**Приоритет:** Низкий (офлайн музыка для моральной поддержки)

---

## 18. МАТРИЦА ПРИОРИТЕТОВ — ВСЕ МОДУЛИ

| Модуль | Категория | Приоритет | RAM | Docker |
|--------|----------|-----------|-----|--------|
| Wyoming Whisper + Piper | AI/Голос | 🔥 ВЫСОКИЙ | 1GB | ✅ |
| Homepage | UI/Dashboard | 🔥 ВЫСОКИЙ | 100MB | ✅ |
| Dockhand | Docker управление | 🔥 ВЫСОКИЙ | 200MB | ✅ (новинка 2026) |
| Vaultwarden | Пароли | 🔥 ВЫСОКИЙ | 50MB | ✅ |
| Audiobookshelf | Медиа | 🔥 ВЫСОКИЙ | 500MB | ✅ |
| Calibre-Web | Книги | 🔥 ВЫСОКИЙ | 300MB | ✅ |
| Docmost | База знаний | 🔥 ВЫСОКИЙ | 500MB | ✅ |
| Syncthing | Файлы/Sync | 🔥 ВЫСОКИЙ | 200MB | ✅ |
| Restic/BorgBackup | Бэкап | 🔥 ВЫСОКИЙ | 100MB | CLI |
| ArchiveBox | Веб-архив | 🔥 ВЫСОКИЙ | 500MB | ✅ |
| Nginx Proxy Manager | SSL/Auth | Высокий | 200MB | ✅ |
| Healthchecks | Мониторинг | Высокий | 200MB | ✅ |
| WeeWX | Погода | Высокий | 200MB | ✅ (нужна метеостанция) |
| FreeTAK Server | TAK/SAR | Высокий | 500MB | ✅ |
| Nextcloud + ONLYOFFICE | Файлы+Офис | Средний | 4GB+ | ✅ |
| Jellyfin | Видео | Средний | 1GB | ✅ |
| BookStack | Вики | Средний | 400MB | ✅ |
| Memos | Заметки | Средний | 100MB | ✅ |
| Jitsi Meet | Видеозвонки | Средний | 2GB | ✅ |
| Bahmni/OpenMRS | Медицина | Средний | 16GB | ✅ (тяжёлый!) |
| Actual Budget | Финансы | Средний | 200MB | ✅ |
| Navidrome | Музыка | Низкий | 200MB | ✅ |
| OctoPrint | 3D-печать | Низкий | 300MB | ✅ |
| LocalAI | AI API | Средний | 8GB | ✅ |
| Speaches | STT/TTS | Средний | 2GB | ✅ |
| Dozzle | Логи | Средний | 8MB | ✅ |
| Portainer | Docker UI | Средний | 300MB | ✅ |
| Wiki.js | Вики | Средний | 500MB | ✅ |

---

## ДОБАВИТЬ В docker-compose.yml — БЫСТРЫЙ СТАРТ

```yaml
# Самые важные новые модули — добавить к существующему NOMAD стеку

  # ===== ОБЯЗАТЕЛЬНЫЕ =====

  nomad-vaultwarden:
    image: vaultwarden/server:latest
    container_name: nomad-vaultwarden
    ports: ["8480:80"]
    volumes: [./data/vaultwarden:/data]
    environment:
      - ADMIN_TOKEN=${VAULTWARDEN_TOKEN}
      - SIGNUPS_ALLOWED=false
    networks: [nomad]
    restart: unless-stopped

  nomad-audiobookshelf:
    image: ghcr.io/advplyr/audiobookshelf:latest
    container_name: nomad-audiobookshelf
    ports: ["13378:80"]
    volumes:
      - ./data/audiobooks:/audiobooks
      - ./data/podcasts:/podcasts
      - ./data/audiobookshelf:/config
    networks: [nomad]
    restart: unless-stopped

  nomad-calibre-web:
    image: lscr.io/linuxserver/calibre-web:latest
    container_name: nomad-calibre-web
    ports: ["8083:8083"]
    volumes:
      - ./data/calibre/config:/config
      - ./data/calibre/books:/books
    networks: [nomad]
    restart: unless-stopped

  nomad-archivebox:
    image: archivebox/archivebox:latest
    container_name: nomad-archivebox
    ports: ["8090:8000"]
    volumes: [./data/archivebox:/data]
    command: server --quick-init 0.0.0.0:8000
    networks: [nomad]
    restart: unless-stopped

  nomad-homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: nomad-homepage
    ports: ["3002:3000"]
    volumes:
      - ./config/homepage:/app/config
      - /var/run/docker.sock:/var/run/docker.sock
    networks: [nomad]
    restart: unless-stopped

  nomad-whisper:
    image: rhasspy/wyoming-whisper
    container_name: nomad-whisper
    ports: ["10300:10300"]
    volumes: [./data/whisper:/data]
    command: ["--model", "small-int8", "--language", "ru"]
    networks: [nomad]
    restart: unless-stopped

  nomad-piper:
    image: rhasspy/wyoming-piper
    container_name: nomad-piper
    ports: ["10200:10200"]
    volumes: [./data/piper:/data]
    command: ["--voice", "ru_RU-irina-medium"]
    networks: [nomad]
    restart: unless-stopped

  nomad-docmost:
    image: docmost/docmost:latest
    container_name: nomad-docmost
    ports: ["3100:3000"]
    environment:
      - APP_URL=http://localhost:3100
      - DATABASE_URL=postgresql://docmost:docmostpass@nomad-postgres:5432/docmost
      - REDIS_URL=redis://nomad-redis:6379
    networks: [nomad]
    restart: unless-stopped

  nomad-syncthing:
    image: lscr.io/linuxserver/syncthing:latest
    container_name: nomad-syncthing
    ports:
      - "8384:8384"
      - "22000:22000/tcp"
      - "22000:22000/udp"
    volumes:
      - ./data/syncthing:/config
      - ./data/sync:/sync
    networks: [nomad]
    restart: unless-stopped

  # ===== ОПЦИОНАЛЬНЫЕ =====

  nomad-weewx:
    image: felddy/weewx:5
    container_name: nomad-weewx
    volumes: [./data/weewx:/data]
    devices: [/dev/ttyUSB0:/dev/ttyUSB0]
    networks: [nomad]
    restart: unless-stopped
    profiles: [weather]  # запускается только если есть метеостанция

  nomad-freetakserver:
    image: freetakteam/freetakserver:latest
    container_name: nomad-fts
    ports:
      - "8087:8087"
      - "19023:19023"
    networks: [nomad]
    restart: unless-stopped
    profiles: [tactical]  # запускается только для тактических операций
```

---

## ИТОГ: ЧТО ДОБАВИТЬ В ПЕРВУЮ ОЧЕРЕДЬ

**Неделя 1 (бесплатно, только pull):**
1. `Homepage` — единая стартовая страница, 10 минут
2. `Vaultwarden` — пароли команды, 10 минут
3. `Audiobookshelf` — аудиокниги и подкасты офлайн, 5 минут
4. `Calibre-Web` — электронные книги офлайн, 10 минут
5. `Whisper + Piper` — голосовой интерфейс, 15 минут

**Неделя 2:**
6. `ArchiveBox` — архивировать важные веб-ресурсы ПОКА ЕСТЬ ИНТЕРНЕТ
7. `Docmost` — вики и документация команды
8. `Syncthing` — синхронизация с другими NOMAD узлами
9. `Nginx Proxy Manager` — HTTPS для PWA
10. `Restic cron` — автоматические бэкапы

**Месяц 2:**
11. `Dockhand` — упростить управление Docker
12. `Healthchecks` — мониторинг cron задач
13. `FreeTAK Server` — если нужна тактическая координация
14. `WeeWX` — если есть RTL-SDR или метеостанция

---

*Документ создан: Март 2026 | Источники: 50+ запросов*
*GitHub: https://github.com/Crosstalk-Solutions/project-nomad*
*awesome-selfhosted: https://github.com/awesome-selfhosted/awesome-selfhosted*
