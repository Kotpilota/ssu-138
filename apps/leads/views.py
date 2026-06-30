import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit
from .forms import LeadForm


def get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _client_ip_key(group, request):
    # За Traefik REMOTE_ADDR — это IP прокси (одинаковый для всех посетителей),
    # поэтому key="ip" лимитировал бы весь сайт одной корзиной. Берём реальный
    # IP клиента из X-Forwarded-For (приложение всегда работает за доверенным прокси).
    return get_client_ip(request) or ""


@require_POST
@ratelimit(key=_client_ip_key, rate="10/m", block=True)
def submit_lead(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = request.POST.dict()

    form = LeadForm(data)
    if form.is_valid():
        lead = form.save(commit=False)
        lead.ip = get_client_ip(request)
        lead.user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
        lead.save()
        return JsonResponse({"ok": True})

    errors = {}
    for field, errs in form.errors.items():
        errors[field] = errs.as_text()

    # Honeypot — молча принимаем
    if "website" in errors:
        return JsonResponse({"ok": True})

    return JsonResponse({"ok": False, "errors": errors}, status=422)
