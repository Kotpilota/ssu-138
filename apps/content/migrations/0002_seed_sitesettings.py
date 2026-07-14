from django.conf import settings
from django.db import migrations


def create_singleton(apps, schema_editor):
    SiteSettings = apps.get_model("content", "SiteSettings")
    # Заполняем реквизиты из settings (в проде читаются из env), чтобы первый
    # деплой перенёс актуальные значения, а не дефолты модели.
    if SiteSettings.objects.filter(pk=1).exists():
        return
    SiteSettings.objects.create(
        pk=1,
        phone=getattr(settings, "SITE_PHONE", ""),
        email=getattr(settings, "SITE_EMAIL", ""),
        address=getattr(settings, "SITE_ADDRESS", ""),
        inn=getattr(settings, "SITE_INN", ""),
        ogrn=getattr(settings, "SITE_OGRN", ""),
        legal_name=getattr(settings, "SITE_LEGAL_NAME", ""),
        address_legal=getattr(settings, "SITE_ADDRESS_LEGAL", ""),
        site_url=getattr(settings, "SITE_URL", "https://ssu-138.ru"),
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_singleton, noop),
    ]
