import json
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, ListView, DetailView, View, UpdateView, CreateView, DeleteView,
)
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from apps.leads.models import Lead, LeadStatus
from apps.leads.services.telegram import send_telegram_message, format_lead_message
from apps.content.models import SiteSettings, Page, Section
from .mixins import StaffRequiredMixin
from .forms import (
    LeadStatusForm, LeadNoteForm, SiteSettingsForm,
    PageForm, SectionForm, SectionCreateForm, SectionItemFormSet,
)
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


class SitePageListView(StaffRequiredMixin, ListView):
    template_name = "panel/site/page_list.html"
    model = Page
    context_object_name = "pages"


class SitePageCreateView(StaffRequiredMixin, CreateView):
    template_name = "panel/site/page_form.html"
    form_class = PageForm

    def form_valid(self, form):
        messages.success(self.request, "Страница создана.")
        self.object = form.save()
        return redirect("panel_site_page_edit", pk=self.object.pk)


class SitePageUpdateView(StaffRequiredMixin, UpdateView):
    template_name = "panel/site/page_form.html"
    form_class = PageForm
    model = Page

    def get_context_data(self, **kwargs):
        from apps.content.models import BlockType
        ctx = super().get_context_data(**kwargs)
        ctx["sections"] = self.object.sections.all()
        ctx["block_types"] = BlockType.choices
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Страница сохранена.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("panel_site_page_edit", args=[self.object.pk])


class SectionCreateView(StaffRequiredMixin, View):
    """Создаёт секцию выбранного типа в конце страницы, ведёт к её редактированию."""
    def post(self, request, page_pk):
        page = get_object_or_404(Page, pk=page_pk)
        form = SectionCreateForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.page = page
            last = page.sections.order_by("-order").first()
            section.order = (last.order + 1) if last else 0
            section.save()
            messages.success(request, "Секция добавлена — заполните содержимое.")
            return redirect("panel_site_section_edit", pk=section.pk)
        messages.error(request, "Не выбран тип секции.")
        return redirect("panel_site_page_edit", pk=page.pk)


class SectionUpdateView(StaffRequiredMixin, UpdateView):
    template_name = "panel/site/section_form.html"
    form_class = SectionForm
    model = Section

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if "formset" not in ctx:
            ctx["formset"] = SectionItemFormSet(instance=self.object)
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = SectionItemFormSet(
            request.POST, request.FILES, instance=self.object
        )
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Секция сохранена.")
            return redirect("panel_site_section_edit", pk=self.object.pk)
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


class SectionDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        section = get_object_or_404(Section, pk=pk)
        page_pk = section.page_id
        section.delete()
        messages.success(request, "Секция удалена.")
        return redirect("panel_site_page_edit", pk=page_pk)


class SectionMoveView(StaffRequiredMixin, View):
    """Меняет местами секцию с соседней (up/down) внутри страницы."""
    def post(self, request, pk, direction):
        section = get_object_or_404(Section, pk=pk)
        qs = section.page.sections.all()
        if direction == "up":
            neighbor = qs.filter(order__lt=section.order).order_by("-order").first()
        else:
            neighbor = qs.filter(order__gt=section.order).order_by("order").first()
        if neighbor:
            section.order, neighbor.order = neighbor.order, section.order
            section.save(update_fields=["order"])
            neighbor.save(update_fields=["order"])
        return redirect("panel_site_page_edit", pk=section.page_id)


class SectionToggleView(StaffRequiredMixin, View):
    def post(self, request, pk):
        section = get_object_or_404(Section, pk=pk)
        section.is_visible = not section.is_visible
        section.save(update_fields=["is_visible"])
        return redirect("panel_site_page_edit", pk=section.page_id)


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
