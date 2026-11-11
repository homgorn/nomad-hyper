FROM python:3.11-slim

WORKDIR /app

# Зависимости системы
RUN apt-get update && apt-get install -y \
    curl \
    git \
    gcc \
    libffi-dev \
    mosquitto-clients \
    && rm -rf /var/lib/apt/lists/*

# Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код агентов
COPY . .

# Создать директории
RUN mkdir -p /tmp/meshtastic_queue /app/logs /app/data

# Порт HTTP API
EXPOSE 8099

CMD ["python3", "orchestrator.py", "--port", "8099"]
