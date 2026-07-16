"""POWER NG TECHNOLOGIE — Services Serializer, View, URLs"""
from rest_framework import generics, permissions, serializers
from django.urls import path
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "title", "description", "image", "icon", "order"]


class ServiceListView(generics.ListAPIView):
    """GET /api/services/ — List all active services (max 6 for homepage)."""
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Service.objects.filter(is_active=True)[:6]


class ServiceAllView(generics.ListAPIView):
    """GET /api/services/all/ — All services (for services page)."""
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Service.objects.filter(is_active=True)


urlpatterns = [
    path("", ServiceListView.as_view(), name="service-list"),
    path("all/", ServiceAllView.as_view(), name="service-all"),
]
