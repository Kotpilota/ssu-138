from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lead",
            name="email",
            field=models.EmailField(blank=True, verbose_name="Email"),
        ),
        migrations.AddField(
            model_name="lead",
            name="contact_method",
            field=models.CharField(
                choices=[("phone", "Позвонить"), ("email", "Написать на email")],
                default="phone",
                max_length=10,
                verbose_name="Способ связи",
            ),
        ),
    ]
