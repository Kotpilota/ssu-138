from django.db import migrations


def create_singleton(apps, schema_editor):
    SiteSettings = apps.get_model("content", "SiteSettings")
    # Дефолты полей уже совпадают с текущими прод-значениями — просто гарантируем
    # наличие записи pk=1, чтобы форма в панели работала сразу после деплоя.
    SiteSettings.objects.get_or_create(pk=1)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_singleton, noop),
    ]
