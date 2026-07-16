"""POWER NG TECHNOLOGIE — Services Models, Serializers, Views, URLs"""
from django.db import models
from rest_framework import generics, permissions, serializers
from django.apps import AppConfig
from apps.core.models import TimeStampedModel
from apps.core.utils import upload_to, validate_image_file, compress_image


class Service(TimeStampedModel):
    """Company service offering (e.g., Installation solaire, Maintenance)."""

    title = models.CharField(max_length=255, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(
        upload_to=upload_to("services"),
        blank=True, null=True,
        verbose_name="Image",
        validators=[validate_image_file]
    )
    icon = models.CharField(
        max_length=50, blank=True,
        verbose_name="Icône",
        help_text="Nom de l'icône Hero (ex: bolt, wrench, sun)"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["order"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            compress_image(self.image)
