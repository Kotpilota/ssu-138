FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/
RUN pip install -r requirements/production.txt

COPY . .

# Статика запекается в образ (контейнер stateless, без static-тома).
# Прод-настройки требуют SECRET_KEY/DB_PASSWORD на импорте — даём build-заглушки (в образ не попадают).
ENV DJANGO_SETTINGS_MODULE=config.settings.production
RUN SECRET_KEY=build-dummy DB_PASSWORD=build-dummy \
    python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
