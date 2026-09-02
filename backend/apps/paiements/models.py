"""
POWER NG TECHNOLOGIE — Paiements Models
Handles MonetBil payment records, webhooks, and enrollment activation.
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()


class Payment(TimeStampedModel):
    """
    Records a payment transaction.
    Links to either a Formation (for enrollment) or an Order (for products).
    Payments are processed via MonetBil (MTN MoMo, Orange Money).
    """

    class Status(models.TextChoices):
        INITIATED = "INITIE", "Initié"
        PENDING = "EN_ATTENTE", "En attente"
        SUCCESS = "SUCCES", "Succès"
        FAILED = "ECHOUE", "Échoué"
        CANCELLED = "ANNULE", "Annulé"
        REFUNDED = "REMBOURSE", "Remboursé"

    class Provider(models.TextChoices):
        MTN = "MTN", "MTN MoMo"
        ORANGE = "ORANGE", "Orange Money"
        EU = "EU", "Express Union"
        PAWAPAY = "PAWAPAY", "PawaPay Multi-pays"

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name="Utilisateur"
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=0,
        verbose_name="Montant (FCFA)"
    )
    status = models.CharField(
        max_length=20, choices=Status.choices,
        default=Status.INITIATED, verbose_name="Statut"
    )
    provider = models.CharField(
        max_length=20, choices=Provider.choices,
        default=Provider.MTN,
        verbose_name="Méthode de paiement"
    )

    # MonetBil references
    transaction_id = models.CharField(
        max_length=255, unique=True, blank=True, null=True,
        verbose_name="Référence de paiement",
        help_text="Notre référence interne (payment_ref envoyé à MonetBil/PawaPay)"
    )
    monetbil_payment_id = models.CharField(
        max_length=255, blank=True, default="",
        verbose_name="MonetBil Payment ID",
        help_text="ID de transaction MonetBil (reçu via webhook)"
    )
    pawapay_deposit_id = models.CharField(
        max_length=255, blank=True, default="",
        verbose_name="PawaPay Deposit ID",
        help_text="ID de dépôt PawaPay (reçu via API/webhook)"
    )
    payment_url = models.URLField(
        blank=True, verbose_name="URL de paiement (MonetBil/PawaPay)"
    )

    # What is being paid for (one of these should be set)
    formation = models.ForeignKey(
        "formations.Formation",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="payments",
        verbose_name="Formation"
    )
    order = models.ForeignKey(
        "boutique.Order",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="payments",
        verbose_name="Commande"
    )

    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Payé le")

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ["-created_at"]

    def __str__(self):
        target = self.formation or self.order
        return f"Paiement #{self.pk} — {self.user.email} — {self.amount} FCFA ({self.status})"
