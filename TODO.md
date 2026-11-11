# TODO — NOMAD Hyper

## P0 (Критично)
- [x] Интегрировать источники Survival LLM (WikiMed, MedlinePlus, WikEM, Ready.gov, CDC, military manuals, wikiHow, iFixit, Appropedia, Stack Exchange) в medical/RAG модули
- [x] Добавить Hikma Health как curated app (field clinics)
- [x] Добавить Unsloth Desktop как backend обучения + OpenAI-compat endpoint
- [x] Добавить "survival mode" (автопереключение на минимальную модель + отключение несущественного при низком заряде)

## P1 (Высокий приоритет)
- [ ] Поддержать MeshCore рядом с Meshtastic (документация + конфиг)
- [ ] Добавить NoteDiscovery с MCP для AI-редактирования заметок
- [ ] Добавить Needle 2 для edge-устройств (14MB, 28MB RAM)
- [ ] Добавить AFFiNE для визуального планирования
- [x] Добавить i18n (react-i18next + LLM перевод + валидация)
- [ ] Добавить multi-location support (multi-select локаций)

## P2 (Средний приоритет)
- [ ] Добавить DeepSeek V4 Flash distilled в Qwen3.5-9B
- [ ] Добавить NVIDIA Nemotron 3.5 для edge
- [ ] Добавить Qwen3.8-Flash-Next как опцию
- [ ] Добавить offline-first EHR (Hikma) в Supply Depot
- [ ] Добавить plant identification (Pl@ntNet, Seek/iNaturalist)
- [ ] Добавить drug interaction DB (MenSung)

## P3 (Низкий приоритет)
- [ ] Добавить offline maps routing (OSRM/GraphHopper)
- [ ] Добавить offline translation (LibreTranslate/Argos)
- [ ] Добавить offline coding (Monaco/CodeMirror)
- [ ] Добавить offline analytics (Metabase/Superset)
- [ ] Добавить offline CI/CD (Gitea/Woodpecker)

## Документация
- [ ] Обновить README с новыми фичами
- [ ] Добавить docs/ для каждой новой фичи
- [ ] Обновить LLM wiki при каждом изменении