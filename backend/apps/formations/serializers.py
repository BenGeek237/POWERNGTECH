"""
POWER NG TECHNOLOGIE — Formations Serializers
Simplified: formations are ZIP files with optional intro video.
"""
from rest_framework import serializers
from .models import Category, Formation, Enrollment


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for formation categories."""
    formation_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon", "description", "formation_count"]

    def get_formation_count(self, obj) -> int:
        return obj.formations.filter(status=Formation.Status.PUBLISHED).count()


class FormationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for formation cards.
    Used in the list view and homepage sections.
    """
    category = CategorySerializer(read_only=True)
    has_intro_video = serializers.SerializerMethodField()

    class Meta:
        model = Formation
        fields = [
            "id", "title", "slug", "category", "image", "price",
            "is_free", "level", "duration_hours", "has_intro_video", "created_at"
        ]

    def get_has_intro_video(self, obj) -> bool:
        return bool(obj.intro_video) or bool(obj.intro_video_url)


class FormationDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for the formation detail page.
    ZIP file URL is only included if the user is enrolled.
    """
    category = CategorySerializer(read_only=True)
    is_enrolled = serializers.SerializerMethodField()
    has_intro_video = serializers.SerializerMethodField()
    zip_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Formation
        fields = [
            "id", "title", "slug", "category", "description", "objectives",
            "prerequisites", "image", "price", "is_free", "level",
            "duration_hours", "status", "is_enrolled", "has_intro_video",
            "intro_video", "intro_video_url", "zip_file_url", "created_at",
        ]

    def get_is_enrolled(self, obj) -> bool:
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return Enrollment.objects.filter(
            user=request.user,
            formation=obj,
            is_active=True
        ).exists()

    def get_has_intro_video(self, obj) -> bool:
        return bool(obj.intro_video) or bool(obj.intro_video_url)

    def get_zip_file_url(self, obj):
        """Only return ZIP URL if user is enrolled or formation is free."""
        request = self.context.get("request")
        if not obj.zip_file:
            return None
        if obj.is_free:
            return request.build_absolute_uri(obj.zip_file.url) if request else obj.zip_file.url
        if request and request.user.is_authenticated:
            if Enrollment.objects.filter(user=request.user, formation=obj, is_active=True).exists():
                return request.build_absolute_uri(obj.zip_file.url) if request else obj.zip_file.url
        return None


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for user enrollments."""
    formation = FormationListSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "formation", "is_active", "enrolled_at"]
