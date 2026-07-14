from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.PanelLoginView.as_view(), name="panel_login"),
    path("logout/", views.PanelLogoutView.as_view(), name="panel_logout"),
    path("", views.DashboardView.as_view(), name="panel_dashboard"),
    path("site/settings/", views.SiteSettingsView.as_view(), name="panel_site_settings"),
    path("site/pages/", views.SitePageListView.as_view(), name="panel_site_pages"),
    path("site/pages/add/", views.SitePageCreateView.as_view(), name="panel_site_page_add"),
    path("site/pages/<int:pk>/", views.SitePageUpdateView.as_view(), name="panel_site_page_edit"),
    path("site/pages/<int:page_pk>/sections/add/", views.SectionCreateView.as_view(), name="panel_site_section_add"),
    path("site/sections/<int:pk>/", views.SectionUpdateView.as_view(), name="panel_site_section_edit"),
    path("site/sections/<int:pk>/delete/", views.SectionDeleteView.as_view(), name="panel_site_section_delete"),
    path("site/sections/<int:pk>/move/<str:direction>/", views.SectionMoveView.as_view(), name="panel_site_section_move"),
    path("site/sections/<int:pk>/toggle/", views.SectionToggleView.as_view(), name="panel_site_section_toggle"),
    path("leads/", views.LeadListView.as_view(), name="panel_leads"),
    path("leads/export.csv", views.LeadExportCsvView.as_view(), name="panel_leads_export"),
    path("leads/<int:pk>/", views.LeadDetailView.as_view(), name="panel_lead_detail"),
    path("leads/<int:pk>/status/", views.LeadStatusUpdateView.as_view(), name="panel_lead_status"),
    path("leads/<int:pk>/note/", views.LeadNoteCreateView.as_view(), name="panel_lead_note"),
    path("leads/<int:pk>/resend-tg/", views.LeadResendTelegramView.as_view(), name="panel_lead_resend_tg"),
]
