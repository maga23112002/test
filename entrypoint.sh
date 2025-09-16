#!/bin/bash

# Ждём, пока база данных будет доступна
echo "⏳ Ожидание PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ PostgreSQL доступен!"

# Запускаем Django
exec python manage.py runserver 0.0.0.0:8000
