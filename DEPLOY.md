# Деплой ССУ-138

Проект адаптирован под стандарт MyServer (см. `C:\Claude\Claude Code\server-architecture.md`).
Инстансы: **`ssu138site-ssu138-prod`** (ветка `main` → `ssu-138.ru`) и
**`ssu138site-ssu138-staging`** (ветка `test` → `ssu138.test.kotpilota.ru`).

## Как работает

```
push в test  → build образ:<SHA> → registry.kotpilota.ru → deploy staging → ssu138.test.kotpilota.ru
merge в main → build образ:<SHA> → registry.kotpilota.ru → deploy prod    → ssu-138.ru (авто; гейт = сам merge)
```

- Образ тегается **commit SHA** (`registry.kotpilota.ru/kotpilota/ssu-138:<sha>`). Откат = деплой прошлого SHA.
- Статика (`collectstatic` + WhiteNoise) запекается в образ на этапе build — контейнер stateless, nginx не нужен.
- Деплой выполняет CI на хосте через примонтированный docker-сокет (`docker compose --env-file deploy/<env>.env`).
- Каждый деплой шлёт в Telegram (тред 5) старт и итог с окружением, SHA и описанием коммита.

## Структура

```
compose.yaml            # сервисы web (gunicorn) + memcached + db (postgres), всё через ${VAR}
deploy/prod.env         # COMPOSE_PROJECT_NAME, DOMAIN, ROUTER_RULE, ALLOWED_HOSTS, БД... (БЕЗ секретов)
deploy/staging.env
.gitlab-ci.yml          # build → deploy (staging/prod)
Dockerfile              # python:3.12-slim + gunicorn, collectstatic на build
```

## Состояние (rebuild с нуля)

| Тип | Где |
|-----|-----|
| Контейнер | образ из registry — пересоздаваем |
| БД | docker volume `ssu138site-ssu138-<env>_pg_data` (NVMe) |
| Медиа | bind `/mnt/hdd/media/ssu138site-ssu138-<env>` (HDD) |
| Бэкап | платформенный systemd-таймер `myserver-backup` (ежедневно, офсайт Amsterdam) |

## Секреты (GitLab → Settings → CI/CD → Variables, masked+protected, scoped по environment)

`SECRET_KEY`, `DB_PASSWORD`, `EMAIL_HOST_PASSWORD`, `TELEGRAM_BOT_TOKEN`.
`TG_CHAT_ID` / `TG_BOT_TOKEN` / `TG_NOTIFY_URL` наследуются с группы `kotpilota`.

## Запуск нового окружения

1. Завести секреты в CI/CD variables (scoped по environment).
2. DNS: `ssu-138.ru` (+ `www`) для prod, `ssu138.test.kotpilota.ru` для staging → IP сервера. Traefik сам выпустит TLS.
3. `git push origin test` → авто-деплой на staging → проверить.
4. По команде Данила: merge в `main` → авто-деплой в прод.
5. Прод-URL `https://ssu-138.ru` добавить в **Uptime Kuma** (на VPS).

## Откат

Передеплоить прошлый образ: в GitLab перезапустить старую `deploy`-джобу, либо вручную на хосте
`IMAGE_TAG=<prev-sha> docker compose --env-file deploy/prod.env -f compose.yaml up -d`.

## Локальная разработка

`docker-compose.dev.yml` (sqlite + `config.settings.local`) — без изменений.
