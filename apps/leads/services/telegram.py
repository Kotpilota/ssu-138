import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_proxies():
    """Возвращает словарь прокси если TELEGRAM_PROXY_URL задан в настройках."""
    proxy_url = getattr(settings, "TELEGRAM_PROXY_URL", "")
    if proxy_url:
        return {"http": proxy_url, "https": proxy_url}
    return None


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

    proxies = _get_proxies()
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json=payload,
            timeout=10,
            proxies=proxies,
        )
        resp.raise_for_status()
        return True
    except requests.HTTPError as e:
        # Логируем только статус, не URL — URL содержит токен бота
        logger.error("Telegram HTTP error: %s", e.response.status_code)
        return False
    except requests.RequestException as e:
        logger.error("Telegram send failed: %s", type(e).__name__)
        return False


def format_lead_message(lead) -> str:
    contact_icon = "📧" if lead.contact_method == "email" else "📞"
    contact_label = "Написать на email" if lead.contact_method == "email" else "Позвонить"

    lines = [
        f"🔔 <b>Новая заявка #{lead.pk}</b>",
        "",
        f"👤 <b>Имя:</b> {lead.name}",
        f"📞 <b>Телефон:</b> {lead.phone}",
    ]
    if lead.email:
        lines.append(f"📧 <b>Email:</b> {lead.email}")
    lines.append(f"{contact_icon} <b>Связаться:</b> {contact_label}")
    lines.append(f"🏗 <b>Тип объекта:</b> {lead.get_object_type_display()}")
    if lead.message:
        lines += ["", f"💬 {lead.message}"]
    lines += [
        "",
        f"🕐 {lead.created_at.strftime('%d.%m.%Y %H:%M')}",
        f"🔗 https://ssu-138.ru/panel/leads/{lead.pk}/",
    ]
    return "\n".join(lines)
