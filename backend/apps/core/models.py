"""
POWER NG TECHNOLOGIE — Core Abstract Models
Provides reusable base classes for all apps.
"""
from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract model that adds created_at and updated_at timestamps
    to any model that inherits from it.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SoftDeleteModel(models.Model):
    """
    Abstract model that adds soft-delete functionality.
    Objects are marked as deleted instead of being permanently removed.
    """
    is_deleted = models.BooleanField(default=False, verbose_name="Supprimé")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    class Meta:
        abstract = True

    def soft_delete(self):
        """Mark the object as deleted without removing it from the database."""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        """Restore a soft-deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])


class BaseModel(TimeStampedModel, SoftDeleteModel):
    """
    Combination of TimeStamped and SoftDelete models.
    Use this as the base for most models.
    """
    class Meta:
        abstract = True
