FROM python:3.11-alpine

# Установка зависимостей
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    jpeg-dev \
    zlib-dev

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копирование всего проекта
COPY . .

# Команда для миграций (опционально)
RUN python manage.py migrate --noinput


EXPOSE 8000