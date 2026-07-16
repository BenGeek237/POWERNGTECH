"""POWER NG TECHNOLOGIE — Demandes Admin"""
from django.contrib import admin
from .models import DemandeFormation


@admin.register(DemandeFormation)
class DemandeFormationAdmin(admin.ModelAdmin):
    list_display = ["nom", "email", "telephone", "domaine", "niveau", "status", "created_at"]
    list_filter = ["status", "niveau", "created_at"]
    search_fields = ["nom", "email", "domaine"]
    readonly_fields = ["nom", "email", "telephone", "ville", "domaine", "niveau", "message", "created_at"]
    list_editable = ["status"]
    fieldsets = (
        ("Demande", {"fields": ("nom", "email", "telephone", "ville", "domaine", "niveau", "message")}),
        ("Traitement", {"fields": ("status", "admin_notes")}),
        ("Dates", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
