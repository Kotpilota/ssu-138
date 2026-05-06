from django.urls import path
from . import views

urlpatterns = [
    path("submit/", views.submit_lead, name="leads_submit"),
]
