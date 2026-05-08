from .base import *

DEBUG = True
SECRET_KEY = "dev-secret-key-not-for-production"
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
LEAD_RECIPIENT_EMAIL = "dev@localhost"

TELEGRAM_ENABLED = False

# django-ratelimit: в dev LocMemCache нормально, заглушаем system checks
RATELIMIT_ENABLE = False
SILENCED_SYSTEM_CHECKS = ["django_ratelimit.E003", "django_ratelimit.W001"]

try:
    import debug_toolbar
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]
except ImportError:
    pass
