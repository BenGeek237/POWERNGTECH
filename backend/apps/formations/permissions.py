"""
POWER NG TECHNOLOGIE — Formations Permissions
Custom DRF permissions for content access control.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Enrollment


class IsEnrolledOrFree(BasePermission):
    """
    Custom permission to grant access to formation content.

    Rules:
    - Free formations: accessible to everyone (authenticated or not)
    - Paid formations: accessible only to users with an active Enrollment
    - Staff/admin users: always have access
    """

    message = "Vous devez acheter cette formation pour accéder à son contenu."

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) — view-level check
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        # Determine the formation from the object
        formation = self._get_formation(obj)
        if formation is None:
            return False

        # Staff always has access
        if request.user and request.user.is_staff:
            return True

        # Free formations are accessible to everyone
        if formation.is_free:
            return True

        # Paid formations require authentication and enrollment
        if not request.user or not request.user.is_authenticated:
            return False

        return Enrollment.objects.filter(
            user=request.user,
            formation=formation,
            is_active=True,
        ).exists()

    def _get_formation(self, obj):
        """Extract the Formation instance from various object types."""
        from .models import Formation, Chapitre, Video, PDF
        if isinstance(obj, Formation):
            return obj
        if isinstance(obj, (Chapitre, PDF)):
            return obj.formation if hasattr(obj, 'formation') and obj.formation else (
                obj.chapter.formation if hasattr(obj, 'chapter') else None
            )
        if isinstance(obj, Video):
            return obj.chapter.formation
        return None


class IsEnrolled(BasePermission):
    """
    Strict permission — user must be authenticated and enrolled.
    Used for video streaming and PDF downloads.
    """

    message = "Vous devez être connecté et avoir acheté cette formation."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        from .models import Video, PDF, Chapitre
        if request.user.is_staff:
            return True

        # Get the formation
        if isinstance(obj, Video):
            formation = obj.chapter.formation
            # Preview videos are always accessible
            if obj.is_preview:
                return True
        elif isinstance(obj, PDF):
            formation = obj.formation or (obj.chapter.formation if obj.chapter else None)
        elif isinstance(obj, Chapitre):
            formation = obj.formation
        else:
            return False

        if not formation:
            return False

        if formation.is_free:
            return True

        return Enrollment.objects.filter(
            user=request.user,
            formation=formation,
            is_active=True,
        ).exists()
