"""
POWER NG TECHNOLOGIE — Custom User Model
Uses email as the primary identifier instead of username.
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from apps.core.models import TimeStampedModel
from apps.core.utils import upload_to, validate_image_file


class CustomUserManager(BaseUserManager):
    """Manager for the CustomUser model with email-based authentication."""

    def create_user(self, email: str, password: str = None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    Custom User model for POWER NG TECHNOLOGIE.
    Email is used as the login identifier.
    """

    email = models.EmailField(
        unique=True,
        verbose_name="Adresse email",
        help_text="Utilisée comme identifiant de connexion."
    )
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    phone = models.CharField(
        max_length=20, blank=True, verbose_name="Téléphone",
        help_text="Format: +237 6XX XXX XXX"
    )
    city = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    country = models.CharField(
        max_length=2, default="CM", verbose_name="Pays",
        help_text="Code ISO 2 lettres (ex: CM, CI, FR, SN)"
    )
    avatar = models.ImageField(
        upload_to=upload_to("accounts/avatars"),
        blank=True,
        null=True,
        verbose_name="Photo de profil",
        validators=[validate_image_file],
    )
    is_active = models.BooleanField(default=True, verbose_name="Compte actif")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_full_name()} <{self.email}>"

    def get_full_name(self) -> str:
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self) -> str:
        """Return the user's first name."""
        return self.first_name
