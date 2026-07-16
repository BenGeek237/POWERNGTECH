"""POWER NG TECHNOLOGIE — Services Admin"""
from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_active", "created_at"]
    list_filter = ["is_active"]
    list_editable = ["order", "is_active"]
    search_fields = ["title"]
