import csv
import io
from apps.leads.models import Lead


def leads_to_csv(queryset) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Имя", "Телефон", "Тип объекта", "Сообщение", "Статус", "Email отправлен", "TG отправлен", "Создана"])
    for lead in queryset:
        writer.writerow([
            lead.pk,
            lead.name,
            lead.phone,
            lead.get_object_type_display(),
            lead.message,
            lead.get_status_display(),
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
