import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_message(text: str) -> bool:
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    thread_id = settings.TELEGRAM_THREAD_ID

    if not token or not chat_id:
        logger.warning("Telegram not configured")
        return False

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    if thread_id:
        payload["message_thread_id"] = int(thread_id)

    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json=payload,
            timeout=5,
        )
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.error("Telegram send error: %s", e)
        return False


def format_lead_message(lead) -> str:
    status_icons = {"new": "🔔", "in_progress": "🔄", "closed": "✅", "spam": "🚫"}
    icon = status_icons.get(lead.status, "📋")

    lines = [
        f"{icon} <b>Новая заявка #{lead.pk}</b>",
        "",
        f"👤 <b>Имя:</b> {lead.name}",
        f"📞 <b>Телефон:</b> {lead.phone}",
        f"🏗 <b>Тип объекта:</b> {lead.get_object_type_display()}",
    ]
    if lead.message:
        lines.append(f"💬 <b>Сообщение:</b> {lead.message}")
    lines += [
        "",
        f"🕐 {lead.created_at.strftime('%d.%m.%Y %H:%M')}",
    ]
    return "\n".join(lines)
