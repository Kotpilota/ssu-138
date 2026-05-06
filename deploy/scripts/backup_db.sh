#!/usr/bin/env bash
# backup_db.sh — резервное копирование PostgreSQL
# Запускать на сервере: /srv/ssu-138/deploy/scripts/backup_db.sh
# Рекомендуется добавить в cron: 0 3 * * * /srv/ssu-138/deploy/scripts/backup_db.sh

set -euo pipefail

BACKUP_DIR="/srv/backups/ssu138"
DB_CONTAINER="ssu138-db"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="${BACKUP_DIR}/db_${DATE}.sql.gz"
KEEP_DAYS=14

mkdir -p "${BACKUP_DIR}"

echo "==> Backup: ${FILENAME}"

docker exec "${DB_CONTAINER}" pg_dump \
  -U "${DB_USER:-ssu138}" \
  "${DB_NAME:-ssu138}" \
  | gzip > "${FILENAME}"

echo "✓ Backup создан ($(du -sh "${FILENAME}" | cut -f1))"

# Удаление старых бэкапов
find "${BACKUP_DIR}" -name "db_*.sql.gz" -mtime "+${KEEP_DAYS}" -delete
echo "✓ Старые бэкапы (>${KEEP_DAYS} дней) удалены"
