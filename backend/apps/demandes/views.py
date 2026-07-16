"""POWER NG TECHNOLOGIE — Demandes Serializer, View, URLs"""
from rest_framework import serializers, generics, permissions, status
from rest_framework.response import Response
from django.urls import path
from drf_spectacular.utils import extend_schema
from .models import DemandeFormation


class DemandeFormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeFormation
        fields = ["nom", "telephone", "email", "ville", "domaine", "niveau", "message"]


@extend_schema(tags=["Demandes"])
class DemandeFormationCreateView(generics.CreateAPIView):
    """
    POST /api/demandes/
    Submit a custom training request. No authentication required.
    """
    queryset = DemandeFormation.objects.all()
    serializer_class = DemandeFormationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Votre demande a bien été envoyée. "
                           "Notre équipe vous contactera dans les meilleurs délais."
            },
            status=status.HTTP_201_CREATED,
        )


urlpatterns = [
    path("", DemandeFormationCreateView.as_view(), name="demande-create"),
]
