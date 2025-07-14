FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Запускаем uvicorn с путем к приложению
CMD ["uvicorn", "src.main:my_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
