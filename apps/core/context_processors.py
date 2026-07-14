from django.conf import settings
from django.db.utils import Error as DBError


def _fallback():
    """Значения из settings — используются, пока БД/таблица недоступна."""
    return {
        "SITE_URL": getattr(settings, "SITE_URL", "https://ssu-138.ru"),
        "SITE_PHONE": settings.SITE_PHONE,
        "SITE_EMAIL": settings.SITE_EMAIL,
        "SITE_ADDRESS": settings.SITE_ADDRESS,
        "SITE_INN": getattr(settings, "SITE_INN", ""),
        "SITE_OGRN": getattr(settings, "SITE_OGRN", ""),
        "SITE_LEGAL_NAME": getattr(settings, "SITE_LEGAL_NAME", "ССУ-138"),
        "SITE_ADDRESS_LEGAL": getattr(settings, "SITE_ADDRESS_LEGAL", ""),
        "SITE_OG_IMAGE": getattr(settings, "SITE_OG_IMAGE", ""),
        "SITE_MAP_EMBED": "",
    }


def site_settings(request):
    """Реквизиты сайта для шаблонов. Читаем из БД (редактируется в панели),
    с фолбэком на settings, чтобы ничего не падало до миграции/сида."""
    from apps.content.models import SiteSettings

    try:
        s = SiteSettings.load()
    except DBError:
        return _fallback()

    og_image = ""
    if s.og_image:
        try:
            og_image = request.build_absolute_uri(s.og_image.url)
        except ValueError:
            og_image = ""

    return {
        "SITE_URL": s.site_url or getattr(settings, "SITE_URL", "https://ssu-138.ru"),
        "SITE_PHONE": s.phone,
        "SITE_EMAIL": s.email,
        "SITE_ADDRESS": s.address,
        "SITE_INN": s.inn,
        "SITE_OGRN": s.ogrn,
        "SITE_LEGAL_NAME": s.legal_name or "ССУ-138",
        "SITE_ADDRESS_LEGAL": s.address_legal,
        "SITE_OG_IMAGE": og_image or getattr(settings, "SITE_OG_IMAGE", ""),
        "SITE_MAP_EMBED": s.map_embed_url,
    }
