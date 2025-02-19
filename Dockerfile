# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /usr/src/app

# Копируем файл зависимостей (requirements.txt) в контейнер
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в рабочую директорию контейнера
COPY . .

# Указываем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
