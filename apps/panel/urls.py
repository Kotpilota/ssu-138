from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.PanelLoginView.as_view(), name="panel_login"),
    path("logout/", views.PanelLogoutView.as_view(), name="panel_logout"),
    path("", views.DashboardView.as_view(), name="panel_dashboard"),
    path("site/settings/", views.SiteSettingsView.as_view(), name="panel_site_settings"),
    path("leads/", views.LeadListView.as_view(), name="panel_leads"),
    path("leads/export.csv", views.LeadExportCsvView.as_view(), name="panel_leads_export"),
    path("leads/<int:pk>/", views.LeadDetailView.as_view(), name="panel_lead_detail"),
    path("leads/<int:pk>/status/", views.LeadStatusUpdateView.as_view(), name="panel_lead_status"),
    path("leads/<int:pk>/note/", views.LeadNoteCreateView.as_view(), name="panel_lead_note"),
    path("leads/<int:pk>/resend-tg/", views.LeadResendTelegramView.as_view(), name="panel_lead_resend_tg"),
]
