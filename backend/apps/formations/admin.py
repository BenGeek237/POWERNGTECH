"""
POWER NG TECHNOLOGIE — Formations Admin
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Formation, Enrollment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "icon", "order"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order", "name"]


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = [
        "title", "category", "price", "is_free", "level",
        "status", "is_featured", "has_zip_file", "created_at"
    ]
    list_filter = ["status", "level", "is_free", "is_featured", "category"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at", "cover_preview"]
    actions = ["publish_formations", "unpublish_formations"]
    list_per_page = 20

    fieldsets = (
        ("Informations principales", {
            "fields": ("title", "slug", "category", "description", "status", "is_featured")
        }),
        ("Contenu pédagogique", {
            "fields": ("objectives", "prerequisites", "level", "duration_hours")
        }),
        ("Fichiers de la formation", {
            "fields": ("zip_file", "intro_video", "intro_video_url")
        }),
        ("Tarification", {
            "fields": ("price", "is_free")
        }),
        ("Médias", {
            "fields": ("image", "cover_preview")
        }),
        ("Métadonnées", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def cover_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" style="border-radius:8px"/>', obj.image.url)
        return "Aucune image"
    cover_preview.short_description = "Aperçu"

    def has_zip_file(self, obj):
        return bool(obj.zip_file)
    has_zip_file.short_description = "Fichier ZIP"
    has_zip_file.boolean = True

    @admin.action(description="Publier les formations sélectionnées")
    def publish_formations(self, request, queryset):
        updated = queryset.update(status=Formation.Status.PUBLISHED)
        self.message_user(request, f"{updated} formation(s) publiée(s).")

    @admin.action(description="Mettre en brouillon les formations sélectionnées")
    def unpublish_formations(self, request, queryset):
        updated = queryset.update(status=Formation.Status.DRAFT)
        self.message_user(request, f"{updated} formation(s) mise(s) en brouillon.")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["user", "formation", "is_active", "enrolled_at"]
    list_filter = ["is_active", "enrolled_at"]
    search_fields = ["user__email", "formation__title"]
    readonly_fields = ["enrolled_at"]
