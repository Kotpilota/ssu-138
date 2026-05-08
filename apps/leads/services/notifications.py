import logging
import threading
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .telegram import send_telegram_message, format_lead_message

logger = logging.getLogger(__name__)


def notify_new_lead(lead):
    """Отправляет email + Telegram в отдельном потоке (не блокирует ответ)."""
    t = threading.Thread(target=_send_notifications, args=(lead.pk,))
    t.start()


def _send_notifications(lead_pk: int):
    from apps.leads.models import Lead
    try:
        lead = Lead.objects.get(pk=lead_pk)
    except Lead.DoesNotExist:
        return

    _send_email(lead)
    if settings.TELEGRAM_ENABLED:
        _send_telegram(lead)


def _send_email(lead):
    recipient = getattr(settings, "LEAD_RECIPIENT_EMAIL", "")
    if not recipient:
        logger.warning("LEAD_RECIPIENT_EMAIL not set")
        return
    try:
        subject = f"Новая заявка #{lead.pk} от {lead.name}"
        body = render_to_string("emails/new_lead.txt", {"lead": lead})
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient])
        lead.email_sent = True
        lead.save(update_fields=["email_sent"])
        logger.info("Email sent for lead #%d", lead.pk)
    except Exception as e:
        logger.error("Email error for lead #%d: %s", lead.pk, e)


def _send_telegram(lead):
    try:
        text = format_lead_message(lead)
        ok = send_telegram_message(text)
        if ok:
            lead.telegram_sent = True
            lead.save(update_fields=["telegram_sent"])
            logger.info("Telegram sent for lead #%d", lead.pk)
    except Exception as e:
        logger.error("Telegram error for lead #%d: %s", lead.pk, e)
