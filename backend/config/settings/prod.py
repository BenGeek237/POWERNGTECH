"""
POWER NG TECHNOLOGIE - Production Settings
"""
from .base import *

DEBUG = False

# Security settings for production
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# Render gère le SSL en amont (reverse proxy), ne pas forcer la redirection
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# ---------------------------------------------------------------------------
# Email — use real SMTP in production (Gmail)
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# ---------------------------------------------------------------------------
# Cloudflare R2 — S3-compatible object storage for media files
# ---------------------------------------------------------------------------
# R2 uses the S3 API. django-storages handles the abstraction.
# Set these environment variables in Railway:
#   R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME,
#   R2_ENDPOINT_URL, R2_CUSTOM_DOMAIN

USE_R2_STORAGE = os.getenv("USE_R2_STORAGE", "False") == "True"

if USE_R2_STORAGE:
    # On met uniquement à jour le stockage par défaut (fichiers médias) pour R2
    # Le stockage statique reste sur Whitenoise (défini dans base.py)
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    }

    AWS_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
    AWS_STORAGE_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "powerngtech-media")
    AWS_S3_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL", "")
    AWS_S3_REGION_NAME = "auto"  # R2 uses "auto"

    # R2 custom domain (e.g., media.powerngtech.com)
    AWS_S3_CUSTOM_DOMAIN = os.getenv("R2_CUSTOM_DOMAIN", "")

    # File settings
    AWS_DEFAULT_ACL = None  # R2 does not support ACLs
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",  # 1 day cache
    }
    AWS_QUERYSTRING_AUTH = False  # Public URLs (no signed URLs)
    AWS_S3_FILE_OVERWRITE = False  # Don't overwrite files with same name

    # Update MEDIA_URL to serve from R2
    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    elif AWS_S3_ENDPOINT_URL:
        MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"

