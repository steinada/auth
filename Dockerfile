# Используем официальный образ Python
FROM python:3.11.1-slim

# Устанавливаем зависимости для работы с PostgreSQL (если используется)
RUN apt-get update && apt-get install -y \
build-essential \
libpq-dev \
&& rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для приложения
EXPOSE 8080

# Команда для запуска приложения
CMD ["uvicorn", "lib.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
