"""
POWER NG TECHNOLOGIE — Boutique Models
Products, categories, orders, and order items.
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from apps.core.utils import upload_to, validate_image_file, compress_image

User = get_user_model()


class ProductCategory(TimeStampedModel):
    """Product category (e.g., Panneaux solaires, Batteries, Onduleurs)."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Catégorie de produit"
        verbose_name_plural = "Catégories de produits"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    """A product available in the store."""

    name = models.CharField(max_length=255, verbose_name="Nom du produit")
    slug = models.SlugField(max_length=280, unique=True, verbose_name="Slug")
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Catégorie"
    )
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(
        max_digits=12, decimal_places=0,
        verbose_name="Prix (FCFA)"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    is_featured = models.BooleanField(default=False, verbose_name="Mis en avant")

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def primary_image(self):
        """Return the primary image or the first one."""
        primary = self.images.filter(is_primary=True).first()
        return primary or self.images.first()


class ProductImage(TimeStampedModel):
    """Product image gallery."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Produit"
    )
    image = models.ImageField(
        upload_to=upload_to("boutique/products"),
        verbose_name="Image",
        validators=[validate_image_file]
    )
    is_primary = models.BooleanField(default=False, verbose_name="Image principale")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Texte alternatif")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Image produit"
        verbose_name_plural = "Images produit"
        ordering = ["-is_primary", "order"]

    def __str__(self):
        return f"{self.product.name} — Image {self.order}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            compress_image(self.image)


class ProductSpec(TimeStampedModel):
    """Key-value specification for a product (e.g., Puissance: 100W)."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specs",
        verbose_name="Produit"
    )
    key = models.CharField(max_length=100, verbose_name="Caractéristique")
    value = models.CharField(max_length=255, verbose_name="Valeur")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        verbose_name = "Caractéristique"
        verbose_name_plural = "Caractéristiques"
        ordering = ["order"]

    def __str__(self):
        return f"{self.key}: {self.value}"


class Order(TimeStampedModel):
    """A customer order."""

    class Status(models.TextChoices):
        PENDING = "EN_ATTENTE", "En attente"
        PAID = "PAYE", "Payé"
        PROCESSING = "EN_COURS", "En cours de traitement"
        SHIPPED = "EXPEDIE", "Expédié"
        DELIVERED = "LIVRE", "Livré"
        CANCELLED = "ANNULE", "Annulé"
        REFUNDED = "REMBOURSE", "Remboursé"

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Client"
    )
    status = models.CharField(
        max_length=20, choices=Status.choices,
        default=Status.PENDING, verbose_name="Statut"
    )
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=0,
        verbose_name="Montant total (FCFA)"
    )
    # Delivery information
    delivery_address = models.TextField(blank=True, verbose_name="Adresse de livraison")
    delivery_city = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    delivery_phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone livraison")
    notes = models.TextField(blank=True, verbose_name="Notes")

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Commande #{self.pk} — {self.user.get_full_name()} ({self.status})"

    @property
    def item_count(self) -> int:
        return self.items.count()


class OrderItem(TimeStampedModel):
    """A line item within an order."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Commande"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="Produit"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    unit_price = models.DecimalField(
        max_digits=12, decimal_places=0,
        verbose_name="Prix unitaire (FCFA)"
    )

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def subtotal(self):
        if self.quantity is None or self.unit_price is None:
            return 0
        return self.quantity * self.unit_price
