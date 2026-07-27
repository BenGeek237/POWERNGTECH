"""
POWER NG TECHNOLOGIE — Demandes Models
Handles custom training requests and contact messages.
"""
from django.db import models
from apps.core.models import TimeStampedModel


class DemandeFormation(TimeStampedModel):
    """
    A request for a customized training session.
    No payment or authentication required — submitted by anyone.
    """

    class Status(models.TextChoices):
        RECEIVED = "RECU", "Reçu"
        PROCESSING = "EN_TRAITEMENT", "En traitement"
        PROCESSED = "TRAITE", "Traité"
        REJECTED = "REJETE", "Rejeté"

    class Level(models.TextChoices):
        BEGINNER = "DEBUTANT", "Débutant"
        INTERMEDIATE = "INTERMEDIAIRE", "Intermédiaire"
        ADVANCED = "AVANCE", "Avancé"
        PROFESSIONAL = "PROFESSIONNEL", "Professionnel"

    # Contact info
    nom = models.CharField(max_length=150, verbose_name="Nom complet")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Adresse email")
    ville = models.CharField(max_length=100, verbose_name="Ville")

    # Training details
    domaine = models.CharField(max_length=200, verbose_name="Domaine souhaité")
    niveau = models.CharField(
        max_length=20, choices=Level.choices,
        default=Level.BEGINNER, verbose_name="Niveau"
    )
    message = models.TextField(verbose_name="Message / Précisions")

    # Admin management
    status = models.CharField(
        max_length=20, choices=Status.choices,
        default=Status.RECEIVED, verbose_name="Statut"
    )
    admin_notes = models.TextField(
        blank=True, verbose_name="Notes internes",
        help_text="Notes réservées à l'administration."
    )

    class Meta:
        verbose_name = "Demande de formation"
        verbose_name_plural = "Demandes de formation"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nom} — {self.domaine} ({self.status})"


class ContactMessage(TimeStampedModel):
    """
    A general contact message sent from the Contact page.
    """
    nom = models.CharField(max_length=150, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Adresse email")
    telephone = models.CharField(max_length=30, blank=True, verbose_name="Téléphone")
    sujet = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    lu = models.BooleanField(default=False, verbose_name="Lu")

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nom} - {self.sujet}"
