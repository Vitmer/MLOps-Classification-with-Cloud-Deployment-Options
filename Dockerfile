# Используем базовый образ для FastAPI приложения
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости проекта в контейнер
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем исходный код приложения в контейнер
COPY ./src /app/src

# Открываем порт для FastAPI приложения
EXPOSE 8000

# Команда по умолчанию при старте контейнера
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
