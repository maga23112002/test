# Используем официальный Python-образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем netcat
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean
# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт запуска
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Копируем весь проект
COPY . .

# Открываем порт
EXPOSE 8000

# Запуск через entrypoint
ENTRYPOINT ["sh", "./entrypoint.sh"]


# Копируем весь проект
COPY . .

# Открываем порт (если нужно)
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
