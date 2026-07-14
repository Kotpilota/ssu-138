import json
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, View, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from apps.leads.models import Lead, LeadStatus
from apps.leads.services.telegram import send_telegram_message, format_lead_message
from apps.content.models import SiteSettings
from .mixins import StaffRequiredMixin
from .forms import LeadStatusForm, LeadNoteForm, SiteSettingsForm
from .utils import leads_to_csv, dashboard_stats, apply_lead_filters


class PanelLoginView(LoginView):
    template_name = "panel/login.html"
    redirect_authenticated_user = True


class PanelLogoutView(LogoutView):
    pass


class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = "panel/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        all_leads = Lead.objects.all()
        stats = dashboard_stats(all_leads)
        ctx.update({
            "stats": stats,
            "chart_json": json.dumps(stats["chart"]),
            "status_json": json.dumps(stats["statuses"]),
            "recent_leads": all_leads.select_related()[:10],
            "status_choices": LeadStatus.choices,
        })
        return ctx


class LeadListView(StaffRequiredMixin, ListView):
    template_name = "panel/leads_list.html"
    context_object_name = "leads"
    paginate_by = 25

    def get_queryset(self):
        return apply_lead_filters(Lead.objects.all(), self.request.GET)

    def get_context_data(self, **kwargs):
        from apps.leads.models import ObjectType
        ctx = super().get_context_data(**kwargs)
        ctx["status_choices"] = LeadStatus.choices
        ctx["object_type_choices"] = ObjectType.choices
        ctx["filters"] = self.request.GET.dict()
        return ctx


class LeadDetailView(StaffRequiredMixin, DetailView):
    template_name = "panel/lead_detail.html"
    model = Lead
    context_object_name = "lead"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["status_form"] = LeadStatusForm(instance=self.object)
        ctx["note_form"] = LeadNoteForm()
        ctx["notes"] = self.object.notes.select_related("author").all()
        ctx["status_choices"] = LeadStatus.choices
        return ctx


class LeadStatusUpdateView(StaffRequiredMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadStatusForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, f"Статус заявки #{pk} обновлён.")
        return redirect("panel_lead_detail", pk=pk)


class LeadNoteCreateView(StaffRequiredMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.lead = lead
            note.author = request.user
            note.save()
            messages.success(request, "Комментарий добавлен.")
        return redirect("panel_lead_detail", pk=pk)


class LeadResendTelegramView(StaffRequiredMixin, View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        text = format_lead_message(lead)
        ok = send_telegram_message(text)
        if ok:
            lead.telegram_sent = True
            lead.save(update_fields=["telegram_sent"])
            messages.success(request, "Уведомление в Telegram отправлено.")
        else:
            messages.error(request, "Ошибка отправки в Telegram.")
        return redirect("panel_lead_detail", pk=pk)


class SiteSettingsView(StaffRequiredMixin, UpdateView):
    """Редактирование реквизитов сайта (синглтон)."""
    template_name = "panel/site/settings.html"
    form_class = SiteSettingsForm
    success_url = reverse_lazy("panel_site_settings")

    def get_object(self, queryset=None):
        return SiteSettings.load()

    def form_valid(self, form):
        messages.success(self.request, "Реквизиты сохранены.")
        return super().form_valid(form)


class LeadExportCsvView(StaffRequiredMixin, View):
    def get(self, request):
        qs = apply_lead_filters(Lead.objects.all(), request.GET)
        csv_data = leads_to_csv(qs)
        response = HttpResponse(
            "﻿" + csv_data,  # BOM для Excel
            content_type="text/csv; charset=utf-8",
        )
        response["Content-Disposition"] = 'attachment; filename="leads.csv"'
        return response
