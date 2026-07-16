"""
POWER NG TECHNOLOGIE — Accounts Admin
Custom admin configuration for user management.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface for the CustomUser model."""

    list_display = [
        "email", "first_name", "last_name", "phone",
        "city", "is_active", "is_staff", "created_at"
    ]
    list_filter = ["is_active", "is_staff", "is_superuser", "city", "created_at"]
    search_fields = ["email", "first_name", "last_name", "phone"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Identifiants", {"fields": ("email", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name", "phone", "city", "avatar")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "created_at", "updated_at"), "classes": ("collapse",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2"),
        }),
    )
    readonly_fields = ["created_at", "updated_at", "last_login"]

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%"/>', obj.avatar.url)
        return "—"
    avatar_preview.short_description = "Avatar"
