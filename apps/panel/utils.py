import csv
import io
from apps.leads.models import Lead


def apply_lead_filters(queryset, params):
    """Фильтрация заявок по GET-параметрам. Общая для списка и экспорта CSV,
    чтобы выгрузка всегда соответствовала тому, что отфильтровано на экране."""
    status = params.get("status")
    object_type = params.get("object_type")
    date_from = params.get("date_from")
    date_to = params.get("date_to")
    if status:
        queryset = queryset.filter(status=status)
    if object_type:
        queryset = queryset.filter(object_type=object_type)
    if date_from:
        queryset = queryset.filter(created_at__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(created_at__date__lte=date_to)
    return queryset


def _safe_csv_value(value: str) -> str:
    """Защита от CSV Injection: префикс ' для строк начинающихся с формульных символов."""
    s = str(value) if value is not None else ""
    if s and s[0] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + s
    return s


def leads_to_csv(queryset) -> str:
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerow(["ID", "Имя", "Телефон", "Тип объекта", "Сообщение", "Статус", "Email отправлен", "TG отправлен", "Создана"])
    for lead in queryset:
        writer.writerow([
            lead.pk,
            _safe_csv_value(lead.name),
            _safe_csv_value(lead.phone),
            _safe_csv_value(lead.get_object_type_display()),
            _safe_csv_value(lead.message),
            _safe_csv_value(lead.get_status_display()),
            "Да" if lead.email_sent else "Нет",
            "Да" if lead.telegram_sent else "Нет",
            lead.created_at.strftime("%d.%m.%Y %H:%M"),
        ])
    return output.getvalue()


def dashboard_stats(leads_qs):
    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Count
    from django.db.models.functions import TruncDate

    now = timezone.now()
    today = now.date()

    stats = {
        "today": leads_qs.filter(created_at__date=today).count(),
        "week": leads_qs.filter(created_at__gte=now - timedelta(days=7)).count(),
        "month": leads_qs.filter(created_at__gte=now - timedelta(days=30)).count(),
        "total": leads_qs.count(),
    }

    # График за 30 дней
    chart_data = (
        leads_qs
        .filter(created_at__gte=now - timedelta(days=30))
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )
    stats["chart"] = [
        {"date": str(row["day"]), "count": row["count"]}
        for row in chart_data
    ]

    # Статусы для donut
    status_data = (
        leads_qs
        .values("status")
        .annotate(count=Count("id"))
    )
    from apps.leads.models import LeadStatus
    status_labels = dict(LeadStatus.choices)
    stats["statuses"] = [
        {"label": status_labels.get(row["status"], row["status"]), "count": row["count"]}
        for row in status_data
    ]

    return stats
