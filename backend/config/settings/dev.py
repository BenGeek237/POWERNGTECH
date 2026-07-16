"""
POWER NG TECHNOLOGIE - Development Settings
"""
from .base import *

DEBUG = True

INTERNAL_IPS = ["127.0.0.1"]

# Use console email backend in development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
