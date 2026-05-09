from django.conf import settings


def site_settings(request):
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
    }
