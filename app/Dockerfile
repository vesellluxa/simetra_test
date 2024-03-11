FROM python:3.12-slim

# Устанавливка рабочей директории внутри контейнера
WORKDIR /app

# Установка зависимостей, необходимых для сборки пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в текущую директорию
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем poetry для управления зависимостями
RUN pip install poetry

# Устанавливаем зависимости проекта с помощью poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Копируем остальные файлы проекта в контейнер
COPY . /app

# Запуск FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
