"""
POWER NG TECHNOLOGIE — Formations Views
REST API views for the training catalog, video player, and enrollments.
"""
import django_filters
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Category, Formation, Chapitre, Video, PDF, Enrollment
from .serializers import (
    CategorySerializer,
    FormationListSerializer,
    FormationDetailSerializer,
    ChapitreDetailSerializer,
    VideoDetailSerializer,
    EnrollmentSerializer,
)
from .permissions import IsEnrolled


# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------

class FormationFilter(django_filters.FilterSet):
    """Filter formations by category, level, price range, and type."""

    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="exact")
    level = django_filters.CharFilter(field_name="level", lookup_expr="exact")
    is_free = django_filters.BooleanFilter(field_name="is_free")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Formation
        fields = ["category", "level", "is_free"]


# ---------------------------------------------------------------------------
# Category views
# ---------------------------------------------------------------------------

@extend_schema(tags=["Formations"])
class CategoryListView(generics.ListAPIView):
    """GET /api/formations/categories/ — List all categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # Return all categories without pagination


# ---------------------------------------------------------------------------
# Formation views
# ---------------------------------------------------------------------------

@extend_schema(tags=["Formations"])
class FormationListView(generics.ListAPIView):
    """
    GET /api/formations/
    List published formations with filtering, search, and ordering.
    """
    serializer_class = FormationListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = FormationFilter
    search_fields = ["title", "description", "category__name"]
    ordering_fields = ["created_at", "price", "title", "duration_hours"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Formation.objects.filter(
            status=Formation.Status.PUBLISHED
        ).select_related("category").prefetch_related("chapters__videos")


@extend_schema(tags=["Formations"])
class FormationDetailView(generics.RetrieveAPIView):
    """
    GET /api/formations/{slug}/
    Full detail of a single formation.
    """
    serializer_class = FormationDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Formation.objects.filter(
            status=Formation.Status.PUBLISHED
        ).select_related("category").prefetch_related(
            "chapters__videos", "chapters__pdfs", "pdfs"
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context


@extend_schema(tags=["Formations"])
class LatestFormationsView(generics.ListAPIView):
    """
    GET /api/formations/latest/
    Returns the 6 most recent published formations (for homepage).
    """
    serializer_class = FormationListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Formation.objects.filter(
            status=Formation.Status.PUBLISHED
        ).select_related("category")[:6]


# ---------------------------------------------------------------------------
# Protected content views (requires enrollment)
# ---------------------------------------------------------------------------

@extend_schema(tags=["Formations — Lecteur"])
class ChapitreDetailView(generics.RetrieveAPIView):
    """
    GET /api/formations/{slug}/chapitres/{chapitre_id}/
    Returns full chapter with videos and PDFs.
    Requires authentication + enrollment (or free formation).
    """
    serializer_class = ChapitreDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnrolled]

    def get_object(self):
        formation = get_object_or_404(
            Formation, slug=self.kwargs["slug"], status=Formation.Status.PUBLISHED
        )
        chapitre = get_object_or_404(
            Chapitre, id=self.kwargs["chapitre_id"], formation=formation
        )
        self.check_object_permissions(self.request, chapitre)
        return chapitre


@extend_schema(tags=["Formations — Lecteur"])
class VideoDetailView(generics.RetrieveAPIView):
    """
    GET /api/formations/{slug}/videos/{video_id}/
    Returns video details for the player.
    Requires authentication + enrollment (unless is_preview).
    """
    serializer_class = VideoDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnrolled]

    def get_object(self):
        video = get_object_or_404(
            Video,
            id=self.kwargs["video_id"],
            chapter__formation__slug=self.kwargs["slug"],
            chapter__formation__status=Formation.Status.PUBLISHED,
        )
        self.check_object_permissions(self.request, video)
        return video


# ---------------------------------------------------------------------------
# User enrollment views
# ---------------------------------------------------------------------------

@extend_schema(tags=["Mes formations"])
class MyFormationsView(generics.ListAPIView):
    """
    GET /api/mes-formations/
    Returns all formations the current user is enrolled in.
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(
            user=self.request.user,
            is_active=True
        ).select_related("formation__category")
