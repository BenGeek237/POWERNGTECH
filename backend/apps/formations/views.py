"""
POWER NG TECHNOLOGIE — Formations Views
REST API views for the training catalog and ZIP downloads.
"""
import django_filters
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import Category, Formation, Enrollment
from .serializers import (
    CategorySerializer,
    FormationListSerializer,
    FormationDetailSerializer,
    EnrollmentSerializer,
)


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
    pagination_class = None


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
        ).select_related("category")


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
        ).select_related("category")

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
# ZIP Download (requires enrollment)
# ---------------------------------------------------------------------------

@extend_schema(tags=["Formations"])
class DownloadFormationZipView(APIView):
    """
    GET /api/formations/{slug}/download/
    Download the ZIP file for a formation.
    Requires authentication + enrollment (or free formation).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        formation = get_object_or_404(
            Formation, slug=slug, status=Formation.Status.PUBLISHED
        )

        if not formation.zip_file:
            return Response(
                {"error": "Cette formation n'a pas de fichier téléchargeable."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check access: free or enrolled
        if not formation.is_free:
            is_enrolled = Enrollment.objects.filter(
                user=request.user, formation=formation, is_active=True
            ).exists()
            if not is_enrolled:
                return Response(
                    {"error": "Vous devez être inscrit pour télécharger cette formation."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return FileResponse(
            formation.zip_file.open("rb"),
            as_attachment=True,
            filename=f"{formation.slug}.zip",
        )


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
