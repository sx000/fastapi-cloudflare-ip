# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы
COPY requirements.txt .
COPY app ./app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем FastAPI на 0.0.0.0:8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
