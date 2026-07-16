"""POWER NG TECHNOLOGIE — Demandes App Config"""
from django.apps import AppConfig


class DemandesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.demandes"
    verbose_name = "Demandes de Formation"
