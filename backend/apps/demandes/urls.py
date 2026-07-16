"""POWER NG TECHNOLOGIE — Demandes URLs"""
from django.urls import path
from .views import DemandeFormationCreateView

app_name = "demandes"

urlpatterns = [
    path("", DemandeFormationCreateView.as_view(), name="create"),
]
