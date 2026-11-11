# NOMAD v2.0 Makefile
.PHONY: up down restart status logs update clean install

COMPOSE=docker compose
NOMAD_ROOT=/opt/project-nomad

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

status:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f --tail=50

update:
	$(COMPOSE) pull && $(COMPOSE) up -d

clean:
	docker system prune -f

# Профили
up-media:
	$(COMPOSE) --profile media up -d

up-sdr:
	$(COMPOSE) --profile sdr up -d

up-office:
	$(COMPOSE) --profile office up -d

up-all:
	$(COMPOSE) --profile media --profile sdr --profile office up -d

# AI модели
pull-models-minimal:
	docker exec nomad-ollama ollama pull qwen3.5:2b
	docker exec nomad-ollama ollama pull nomic-embed-text

pull-models-standard:
	docker exec nomad-ollama ollama pull qwen3.5:9b
	docker exec nomad-ollama ollama pull nomic-embed-text

pull-models-gpu:
	docker exec nomad-ollama ollama pull qwen3.5:9b
	docker exec nomad-ollama ollama pull qwen3.5:35b-a3b
	docker exec nomad-ollama ollama pull nomic-embed-text

# Agents
agents-start:
	systemctl start nomad-orchestrator nomad-meshtastic nomad-rag-watcher

agents-stop:
	systemctl stop nomad-orchestrator nomad-meshtastic nomad-rag-watcher

agents-status:
	systemctl status nomad-orchestrator nomad-meshtastic nomad-rag-watcher

# Health
health:
	bash $(NOMAD_ROOT)/scripts/health_checker.sh

backup:
	restic -r /mnt/backup/nomad backup $(NOMAD_ROOT)/data $(NOMAD_ROOT)/config
