#!/usr/bin/env python3
"""
NOMAD — RAG Indexer (LIBRARIAN)
Индексирует документы в Qdrant для семантического поиска.
Поддерживает: PDF, TXT, MD, DOCX
Запуск одиночный: python3 rag_indexer.py /path/to/file.pdf
Запуск watchdog:  python3 rag_indexer.py --watch /opt/project-nomad/data/incoming
"""

import argparse
import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path
from datetime import datetime

import requests

# Опциональные импорты
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False

# ── CONFIG ────────────────────────────────────────────────────
OLLAMA_URL  = os.getenv("OLLAMA_HOST",  "http://localhost:11434")
QDRANT_URL  = os.getenv("QDRANT_HOST",  "http://localhost:6333")
NTFY_URL    = os.getenv("NTFY_HOST",    "http://localhost:8088")
EMBED_MODEL = "nomic-embed-text"
CHUNK_SIZE  = 800     # символов на чанк
CHUNK_OVERLAP = 100   # перекрытие между чанками
INDEXED_DB  = Path("/opt/project-nomad/data/.rag_indexed.json")

# Коллекции по типу контента
COLLECTION_RULES = {
    "медицин":     "nomad-medical",
    "первая помощ": "nomad-medical",
    "survival":    "nomad-survival",
    "выживан":     "nomad-survival",
    "iFixit":      "nomad-technical",
    "ремонт":      "nomad-technical",
    "ификсит":     "nomad-technical",
    "карт":        "nomad-navigation",
    "маршрут":     "nomad-navigation",
}

COLLECTIONS = [
    "nomad-general",
    "nomad-medical",
    "nomad-survival",
    "nomad-technical",
    "nomad-navigation",
    "nomad-local",
]

VECTOR_SIZE = 768  # nomic-embed-text

# ── LOGGING ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [LIBRARIAN] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("LIBRARIAN")


# ── QDRANT ────────────────────────────────────────────────────

def ensure_collections():
    """Создать коллекции если не существуют."""
    for name in COLLECTIONS:
        resp = requests.get(f"{QDRANT_URL}/collections/{name}", timeout=5)
        if resp.status_code == 404:
            r = requests.put(
                f"{QDRANT_URL}/collections/{name}",
                json={"vectors": {"size": VECTOR_SIZE, "distance": "Cosine"}},
                timeout=10,
            )
            if r.status_code in (200, 201):
                log.info(f"✅ Коллекция создана: {name}")
            else:
                log.error(f"Ошибка создания коллекции {name}: {r.text}")


def detect_collection(filename: str, content: str) -> str:
    """Определить коллекцию по имени и содержимому файла."""
    combined = (filename + content[:500]).lower()
    for keyword, collection in COLLECTION_RULES.items():
        if keyword.lower() in combined:
            return collection
    return "nomad-general"


# ── EMBEDDING ─────────────────────────────────────────────────

def embed(text: str) -> list[float]:
    """Получить embedding от Ollama."""
    resp = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=60,
    )
    return resp.json()["embedding"]


# ── TEXT EXTRACTION ───────────────────────────────────────────

def extract_text(filepath: Path) -> str:
    """Извлечь текст из файла (PDF/TXT/MD/DOCX)."""
    ext = filepath.suffix.lower()

    if ext in (".txt", ".md"):
        return filepath.read_text(encoding="utf-8", errors="ignore")

    elif ext == ".pdf":
        try:
            import pdfplumber
            text_parts = []
            with pdfplumber.open(str(filepath)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            return "\n\n".join(text_parts)
        except ImportError:
            # Fallback: использовать pdftotext если установлен
            import subprocess
            result = subprocess.run(
                ["pdftotext", str(filepath), "-"],
                capture_output=True, text=True, timeout=60
            )
            return result.stdout if result.returncode == 0 else ""

    elif ext == ".docx":
        try:
            import docx
            doc = docx.Document(str(filepath))
            return "\n".join([p.text for p in doc.paragraphs])
        except ImportError:
            log.warning("python-docx не установлен")
            return ""

    elif ext == ".html":
        try:
            from html.parser import HTMLParser

            class TextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.parts = []
                def handle_data(self, data):
                    if data.strip():
                        self.parts.append(data)

            parser = TextExtractor()
            parser.feed(filepath.read_text(errors="ignore"))
            return " ".join(parser.parts)
        except Exception:
            return ""

    return ""


# ── CHUNKING ──────────────────────────────────────────────────

def chunk_text(text: str) -> list[str]:
    """Разбить текст на чанки с перекрытием."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()
        if len(chunk) > 50:  # игнорировать слишком маленькие чанки
            chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


# ── INDEXER ───────────────────────────────────────────────────

def file_hash(filepath: Path) -> str:
    """SHA256 хэш файла."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def load_indexed_db() -> dict:
    """Загрузить реестр проиндексированных файлов."""
    if INDEXED_DB.exists():
        try:
            return json.loads(INDEXED_DB.read_text())
        except Exception:
            pass
    return {}


def save_indexed_db(db: dict):
    """Сохранить реестр."""
    INDEXED_DB.parent.mkdir(parents=True, exist_ok=True)
    INDEXED_DB.write_text(json.dumps(db, ensure_ascii=False, indent=2))


def index_file(filepath: Path, force: bool = False) -> bool:
    """Проиндексировать файл. Вернуть True если успешно."""
    filepath = Path(filepath)
    if not filepath.exists():
        log.error(f"Файл не найден: {filepath}")
        return False

    ext = filepath.suffix.lower()
    if ext not in (".pdf", ".txt", ".md", ".docx", ".html"):
        log.info(f"Пропускаю (неподдерживаемый формат): {filepath.name}")
        return False

    # Проверить не проиндексирован ли уже
    db  = load_indexed_db()
    fhash = file_hash(filepath)
    if not force and db.get(str(filepath)) == fhash:
        log.info(f"Уже проиндексирован: {filepath.name}")
        return True

    log.info(f"📚 Индексирую: {filepath.name}")

    # Извлечь текст
    text = extract_text(filepath)
    if not text or len(text) < 100:
        log.warning(f"Слишком мало текста: {filepath.name}")
        return False

    # Определить коллекцию
    collection = detect_collection(filepath.name, text)
    log.info(f"  Коллекция: {collection}")

    # Разбить на чанки
    chunks = chunk_text(text)
    log.info(f"  Чанков: {len(chunks)}")

    # Индексировать каждый чанк
    points = []
    for i, chunk in enumerate(chunks):
        try:
            vector = embed(chunk)
            point_id = int(hashlib.md5(f"{filepath}{i}".encode()).hexdigest()[:8], 16)
            points.append({
                "id": point_id,
                "vector": vector,
                "payload": {
                    "text":       chunk,
                    "source":     filepath.name,
                    "path":       str(filepath),
                    "chunk":      i,
                    "total_chunks": len(chunks),
                    "collection": collection,
                    "indexed_at": datetime.now().isoformat(),
                },
            })
        except Exception as e:
            log.warning(f"Ошибка embedding чанк {i}: {e}")

    if not points:
        log.error("Нет точек для индексирования")
        return False

    # Записать в Qdrant батчами по 50
    batch_size = 50
    for batch_start in range(0, len(points), batch_size):
        batch = points[batch_start:batch_start + batch_size]
        resp = requests.put(
            f"{QDRANT_URL}/collections/{collection}/points",
            json={"points": batch},
            timeout=60,
        )
        if resp.status_code not in (200, 201):
            log.error(f"Ошибка Qdrant: {resp.text}")
            return False

    # Обновить реестр
    db[str(filepath)] = fhash
    save_indexed_db(db)

    log.info(f"✅ {filepath.name}: {len(points)} чанков → {collection}")

    # Уведомить
    try:
        requests.post(
            f"{NTFY_URL}/download",
            data=f"📚 Проиндексирован: {filepath.name} ({len(points)} чанков → {collection})".encode(),
            timeout=3,
        )
    except Exception:
        pass

    return True


# ── SEARCH ────────────────────────────────────────────────────

def search(query: str, limit: int = 5, collection: str = None) -> list[dict]:
    """Семантический поиск по базе знаний."""
    vector = embed(query)
    results = []

    target_collections = [collection] if collection else COLLECTIONS

    for coll in target_collections:
        try:
            resp = requests.post(
                f"{QDRANT_URL}/collections/{coll}/points/search",
                json={"vector": vector, "limit": limit, "with_payload": True},
                timeout=30,
            )
            if resp.status_code == 200:
                for hit in resp.json().get("result", []):
                    results.append({
                        "score":      round(hit["score"], 4),
                        "collection": coll,
                        "source":     hit["payload"].get("source", "?"),
                        "text":       hit["payload"].get("text", "")[:500],
                    })
        except Exception as e:
            log.warning(f"Ошибка поиска в {coll}: {e}")

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


# ── WATCHDOG ──────────────────────────────────────────────────

class DocumentHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            p = Path(event.src_path)
            if p.suffix.lower() in (".pdf", ".txt", ".md", ".docx"):
                time.sleep(1)  # дать файлу дописаться
                index_file(p)

    def on_modified(self, event):
        if not event.is_directory:
            p = Path(event.src_path)
            if p.suffix.lower() in (".pdf", ".txt", ".md"):
                index_file(p, force=True)


# ── MAIN ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="NOMAD RAG Indexer")
    parser.add_argument("file",     nargs="?", help="Файл для индексирования")
    parser.add_argument("--watch",  help="Директория для автомониторинга")
    parser.add_argument("--search", help="Поисковый запрос")
    parser.add_argument("--dir",    help="Проиндексировать всю директорию")
    parser.add_argument("--init",   action="store_true", help="Создать коллекции")
    parser.add_argument("--force",  action="store_true", help="Переиндексировать даже если есть")
    args = parser.parse_args()

    # Проверить доступность Qdrant
    try:
        requests.get(f"{QDRANT_URL}/collections", timeout=5)
    except Exception:
        log.error(f"Qdrant недоступен: {QDRANT_URL}")
        sys.exit(1)

    # Создать коллекции
    if args.init or True:  # всегда проверяем
        ensure_collections()

    # Один файл
    if args.file:
        success = index_file(Path(args.file), force=args.force)
        sys.exit(0 if success else 1)

    # Директория
    if args.dir:
        dir_path = Path(args.dir)
        files    = list(dir_path.rglob("*.pdf")) + \
                   list(dir_path.rglob("*.txt")) + \
                   list(dir_path.rglob("*.md"))
        log.info(f"Нашёл {len(files)} файлов в {dir_path}")
        for f in files:
            index_file(f, force=args.force)

    # Поиск
    if args.search:
        results = search(args.search)
        print(f"\n=== ПОИСК: '{args.search}' ===")
        for i, r in enumerate(results, 1):
            print(f"\n[{i}] {r['source']} (релевантность: {r['score']})")
            print(f"    {r['text'][:300]}...")
        return

    # Watchdog режим
    if args.watch:
        if not HAS_WATCHDOG:
            log.error("watchdog не установлен: pip install watchdog")
            sys.exit(1)

        watch_path = Path(args.watch)
        watch_path.mkdir(parents=True, exist_ok=True)

        # Проиндексировать существующие файлы
        existing = list(watch_path.rglob("*.pdf")) + \
                   list(watch_path.rglob("*.txt")) + \
                   list(watch_path.rglob("*.md"))
        log.info(f"Индексирую {len(existing)} существующих файлов...")
        for f in existing:
            index_file(f)

        # Запустить watchdog
        observer = Observer()
        observer.schedule(DocumentHandler(), str(watch_path), recursive=True)
        observer.start()
        log.info(f"👁️ LIBRARIAN следит за {watch_path}")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        return

    parser.print_help()


if __name__ == "__main__":
    main()
