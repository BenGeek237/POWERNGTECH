"""
POWER NG TECHNOLOGIE — Formations Models
Core models for the training platform: categories, courses, chapters, videos, PDFs, and enrollments.
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from apps.core.utils import upload_to, validate_image_file, validate_video_file, validate_pdf_file, validate_zip_file, compress_image

User = get_user_model()


class Category(TimeStampedModel):
    """Training category (e.g., Énergie Solaire, Électronique)."""

    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="Slug")
    icon = models.CharField(
        max_length=50, blank=True,
        verbose_name="Icône",
        help_text="Nom de l'icône (ex: solar-panel, zap, tool)"
    )
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Formation(TimeStampedModel):
    """
    Main training model.
    A formation is a downloadable ZIP file with an optional intro video.
    """

    class Level(models.TextChoices):
        BEGINNER = "DEBUTANT", "Débutant"
        INTERMEDIATE = "INTERMEDIAIRE", "Intermédiaire"
        ADVANCED = "AVANCE", "Avancé"

    class Status(models.TextChoices):
        PUBLISHED = "PUBLIE", "Publié"
        DRAFT = "BROUILLON", "Brouillon"
        ARCHIVED = "ARCHIVE", "Archivé"

    title = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField(max_length=280, unique=True, verbose_name="Slug")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="formations",
        verbose_name="Catégorie"
    )
    description = models.TextField(verbose_name="Description")
    objectives = models.TextField(
        blank=True, verbose_name="Objectifs",
        help_text="Un objectif par ligne."
    )
    prerequisites = models.TextField(
        blank=True, verbose_name="Prérequis",
        help_text="Un prérequis par ligne."
    )
    image = models.ImageField(
        upload_to=upload_to("formations/images"),
        verbose_name="Image de couverture",
        validators=[validate_image_file]
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=0,
        default=0, verbose_name="Prix (FCFA)"
    )
    is_free = models.BooleanField(default=False, verbose_name="Formation gratuite")
    level = models.CharField(
        max_length=20, choices=Level.choices,
        default=Level.BEGINNER, verbose_name="Niveau"
    )
    duration_hours = models.DecimalField(
        max_digits=5, decimal_places=1,
        default=0, verbose_name="Durée (heures)"
    )
    status = models.CharField(
        max_length=20, choices=Status.choices,
        default=Status.DRAFT, verbose_name="Statut"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Mise en avant")

    # ── ZIP content (main downloadable file) ──
    zip_file = models.FileField(
        upload_to=upload_to("formations/zips"),
        blank=True, null=True,
        verbose_name="Fichier ZIP de la formation",
        validators=[validate_zip_file],
        help_text="Contenu principal de la formation au format ZIP (max 500 Mo)."
    )

    # ── Optional intro video ──
    intro_video = models.FileField(
        upload_to=upload_to("formations/intros"),
        blank=True, null=True,
        verbose_name="Vidéo d'introduction",
        validators=[validate_video_file],
        help_text="Vidéo de présentation visible par tous (optionnelle)."
    )
    intro_video_url = models.URLField(
        blank=True, verbose_name="URL vidéo d'introduction",
        help_text="Alternative YouTube/Vimeo (si pas de fichier vidéo)."
    )

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-set is_free when price is 0
        if self.price == 0:
            self.is_free = True
        super().save(*args, **kwargs)
        # Compress image after saving
        if self.image:
            compress_image(self.image)

    @property
    def video_count(self) -> int:
        """Total number of videos across all chapters."""
        return Video.objects.filter(chapter__formation=self).count()

    @property
    def chapter_count(self) -> int:
        """Total number of chapters."""
        return self.chapters.count()


class Chapitre(TimeStampedModel):
    """A chapter within a formation."""

    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name="chapters",
        verbose_name="Formation"
    )
    title = models.CharField(max_length=255, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Chapitre"
        verbose_name_plural = "Chapitres"
        ordering = ["order"]
        unique_together = [["formation", "order"]]

    def __str__(self):
        return f"{self.formation.title} — Chapitre {self.order}: {self.title}"


class Video(TimeStampedModel):
    """A video lesson within a chapter."""

    chapter = models.ForeignKey(
        Chapitre,
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name="Chapitre"
    )
    title = models.CharField(max_length=255, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    video_file = models.FileField(
        upload_to=upload_to("formations/videos"),
        blank=True, null=True,
        verbose_name="Fichier vidéo",
        validators=[validate_video_file]
    )
    video_url = models.URLField(
        blank=True, verbose_name="URL vidéo externe",
        help_text="URL YouTube ou autre (alternative au fichier)"
    )
    duration_minutes = models.PositiveIntegerField(
        default=0, verbose_name="Durée (minutes)"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_preview = models.BooleanField(
        default=False, verbose_name="Accessible en aperçu",
        help_text="Si coché, cette vidéo est visible sans paiement."
    )

    class Meta:
        verbose_name = "Vidéo"
        verbose_name_plural = "Vidéos"
        ordering = ["order"]

    def __str__(self):
        return f"{self.chapter.title} — {self.title}"


class PDF(TimeStampedModel):
    """A PDF resource attached to a formation or chapter."""

    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name="pdfs",
        verbose_name="Formation",
        null=True, blank=True
    )
    chapter = models.ForeignKey(
        Chapitre,
        on_delete=models.CASCADE,
        related_name="pdfs",
        verbose_name="Chapitre",
        null=True, blank=True
    )
    title = models.CharField(max_length=255, verbose_name="Titre")
    file = models.FileField(
        upload_to=upload_to("formations/pdfs"),
        verbose_name="Fichier PDF",
        validators=[validate_pdf_file]
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "PDF"
        verbose_name_plural = "PDFs"
        ordering = ["order"]

    def __str__(self):
        return self.title


class Enrollment(TimeStampedModel):
    """
    Links a user to a formation they have purchased or enrolled in.
    This is the access control record for paid content.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Utilisateur"
    )
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Formation"
    )
    is_active = models.BooleanField(default=True, verbose_name="Accès actif")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Inscrit le")

    class Meta:
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"
        unique_together = [["user", "formation"]]

    def __str__(self):
        return f"{self.user.get_full_name()} → {self.formation.title}"
