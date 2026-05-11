from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("stroitelstvo/", views.service_page, {"slug": "stroitelstvo"}, name="service_stroitelstvo"),
    path("proektirovanie/", views.service_page, {"slug": "proektirovanie"}, name="service_proektirovanie"),
    path("spetstehnika/", views.service_page, {"slug": "spetstehnika"}, name="service_spetstehnika"),
    path("privacy/", views.privacy, name="privacy"),
    path("healthz/", views.healthz, name="healthz"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
]
