"""
POWER NG TECHNOLOGIE — Core Utilities
Shared helpers for image processing, file validation, and more.
"""
import os
import uuid
from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.text import slugify


# ---------------------------------------------------------------------------
# File path generators
# ---------------------------------------------------------------------------

from django.utils.deconstruct import deconstructible

@deconstructible
class UploadToPathAndRename:
    def __init__(self, folder):
        self.folder = folder

    def __call__(self, instance, filename):
        ext = os.path.splitext(filename)[1].lower()
        unique_name = f"{uuid.uuid4().hex}{ext}"
        return os.path.join(self.folder, unique_name)

def upload_to(folder: str):
    """
    Returns a callable that generates an upload path with UUID filename.
    Example: upload_to('formations/images') → 'formations/images/<uuid>.jpg'
    """
    return UploadToPathAndRename(folder)


# ---------------------------------------------------------------------------
# Image processing
# ---------------------------------------------------------------------------

def compress_image(image_field, max_width: int = 1200, quality: int = 85) -> None:
    """
    Compress and resize an image field in-place using Pillow.
    Called in model.save() to keep uploaded images optimized.

    Args:
        image_field: Django ImageField instance
        max_width:   Maximum width in pixels (maintains aspect ratio)
        quality:     JPEG quality (1–95, default 85)
    """
    if not image_field:
        return

    img = Image.open(image_field.path)

    # Convert RGBA or P mode images to RGB
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Resize if wider than max_width
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)

    # Save with compression
    img.save(image_field.path, format="JPEG", quality=quality, optimize=True)


# ---------------------------------------------------------------------------
# File validators
# ---------------------------------------------------------------------------

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/webm", "video/ogg"]
ALLOWED_PDF_TYPES = ["application/pdf"]

MAX_IMAGE_SIZE_MB = 10
MAX_VIDEO_SIZE_MB = 500
MAX_PDF_SIZE_MB = 50


def validate_image_file(file):
    """Validate that an uploaded file is a valid image under size limit."""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError(
            f"Type de fichier non accepté. Types acceptés : JPEG, PNG, WebP."
        )
    if file.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError(
            f"L'image ne peut pas dépasser {MAX_IMAGE_SIZE_MB} Mo."
        )


def validate_video_file(file):
    """Validate that an uploaded file is a valid video under size limit."""
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise ValidationError(
            "Type de fichier non accepté. Types acceptés : MP4, WebM, OGG."
        )
    if file.size > MAX_VIDEO_SIZE_MB * 1024 * 1024:
        raise ValidationError(
            f"La vidéo ne peut pas dépasser {MAX_VIDEO_SIZE_MB} Mo."
        )


def validate_pdf_file(file):
    """Validate that an uploaded file is a valid PDF under size limit."""
    if file.content_type not in ALLOWED_PDF_TYPES:
        raise ValidationError("Seuls les fichiers PDF sont acceptés.")
    if file.size > MAX_PDF_SIZE_MB * 1024 * 1024:
        raise ValidationError(
            f"Le PDF ne peut pas dépasser {MAX_PDF_SIZE_MB} Mo."
        )


# ---------------------------------------------------------------------------
# Slug helper
# ---------------------------------------------------------------------------

def unique_slug(model_class, title: str, slug_field: str = "slug") -> str:
    """
    Generate a unique slug for a model instance.
    Appends a counter if the slug already exists.
    """
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    while model_class.objects.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug
