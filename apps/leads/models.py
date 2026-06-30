from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LeadStatus(models.TextChoices):
    NEW = "new", "Новая"
    IN_PROGRESS = "in_progress", "В работе"
    CLOSED = "closed", "Закрыта"
    SPAM = "spam", "Спам"


class ObjectType(models.TextChoices):
    INDUSTRIAL = "industrial", "Промышленный"
    CIVIL = "civil", "Гражданский"
    MILITARY = "military", "Военный / государственный"
    SOCIAL = "social", "Социальный"
    OTHER = "other", "Другое"


class ContactMethod(models.TextChoices):
    PHONE = "phone", "Позвонить"
    EMAIL = "email", "Написать на email"


class Lead(models.Model):
    name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон", max_length=32)
    email = models.EmailField("Email", blank=True)
    contact_method = models.CharField(
        "Способ связи", max_length=10,
        choices=ContactMethod.choices, default=ContactMethod.PHONE,
    )
    object_type = models.CharField(
        "Тип объекта", max_length=32,
        choices=ObjectType.choices, default=ObjectType.OTHER,
    )
    message = models.TextField("Сообщение", blank=True)

    status = models.CharField(
        "Статус", max_length=20,
        choices=LeadStatus.choices, default=LeadStatus.NEW, db_index=True,
    )

    # метаданные
    ip = models.GenericIPAddressField("IP", null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)

    # флаги уведомлений
    email_sent = models.BooleanField("Email отправлен", default=False)
    telegram_sent = models.BooleanField("TG отправлен", default=False)

    created_at = models.DateTimeField("Создана", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} {self.name} ({self.phone})"


class LeadNote(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заметка к #{self.lead_id}"
