#!/usr/bin/env bash
# deploy.sh — деплой ССУ-138 на сервер
# Использование: ./deploy/scripts/deploy.sh

set -euo pipefail

REMOTE_USER="kotpilota"
REMOTE_HOST="91.218.84.56"
REMOTE_DIR="/srv/ssu-138"
SSH_ALIAS="MyServer"

echo "==> Деплой ССУ-138 → ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}"

# 1. Синхронизировать код на сервер (исключая .git, .env, staticfiles)
rsync -az --delete \
  --exclude='.git' \
  --exclude='.env' \
  --exclude='.env.local' \
  --exclude='staticfiles/' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='node_modules' \
  . "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/"

# 2. Выполнить команды на сервере
ssh "${REMOTE_USER}@${REMOTE_HOST}" << 'ENDSSH'
  set -e
  cd /srv/ssu-138

  echo "--> Pull образов (если нужно)"
  docker compose pull --quiet || true

  echo "--> Build"
  docker compose build --no-cache web

  echo "--> Миграции БД"
  docker compose run --rm web python manage.py migrate \
    --settings=config.settings.production

  echo "--> Collect static"
  docker compose run --rm web python manage.py collectstatic \
    --noinput --settings=config.settings.production

  echo "--> Рестарт контейнеров"
  docker compose up -d --remove-orphans

  echo "--> Очистка старых образов"
  docker image prune -f

  echo "✓ Деплой завершён"
ENDSSH

echo "==> Готово!"
