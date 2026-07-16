"""
POWER NG TECHNOLOGIE — Formations Serializers
Handles serialization for categories, formations, chapters, videos, and PDFs.
"""
from rest_framework import serializers
from .models import Category, Formation, Chapitre, Video, PDF, Enrollment


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for formation categories."""
    formation_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon", "description", "formation_count"]

    def get_formation_count(self, obj) -> int:
        return obj.formations.filter(status=Formation.Status.PUBLISHED).count()


class PDFSerializer(serializers.ModelSerializer):
    """Serializer for PDF resources."""

    class Meta:
        model = PDF
        fields = ["id", "title", "file", "order"]


class VideoListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for video list display."""

    class Meta:
        model = Video
        fields = ["id", "title", "duration_minutes", "order", "is_preview"]


class VideoDetailSerializer(serializers.ModelSerializer):
    """Full serializer for video playback (includes file URL)."""
    pdfs = PDFSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = [
            "id", "title", "description", "video_file", "video_url",
            "duration_minutes", "order", "is_preview", "pdfs"
        ]


class ChapitreListSerializer(serializers.ModelSerializer):
    """Serializer for chapter list (sidebar view)."""
    videos = VideoListSerializer(many=True, read_only=True)
    video_count = serializers.SerializerMethodField()

    class Meta:
        model = Chapitre
        fields = ["id", "title", "order", "video_count", "videos"]

    def get_video_count(self, obj) -> int:
        return obj.videos.count()


class ChapitreDetailSerializer(serializers.ModelSerializer):
    """Full serializer for chapter with all videos and PDFs."""
    videos = VideoDetailSerializer(many=True, read_only=True)
    pdfs = PDFSerializer(many=True, read_only=True)

    class Meta:
        model = Chapitre
        fields = ["id", "title", "description", "order", "videos", "pdfs"]


class FormationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for formation cards.
    Used in the list view and homepage sections.
    """
    category = CategorySerializer(read_only=True)
    video_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Formation
        fields = [
            "id", "title", "slug", "category", "image", "price",
            "is_free", "level", "duration_hours", "video_count", "created_at"
        ]


class FormationDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for the formation detail page.
    Includes chapters structure (without video files for access control).
    """
    category = CategorySerializer(read_only=True)
    chapters = ChapitreListSerializer(many=True, read_only=True)
    pdfs = PDFSerializer(many=True, read_only=True)
    video_count = serializers.SerializerMethodField()
    chapter_count = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Formation
        fields = [
            "id", "title", "slug", "category", "description", "objectives",
            "prerequisites", "image", "price", "is_free", "level",
            "duration_hours", "video_count", "chapter_count", "chapters",
            "pdfs", "status", "is_enrolled", "created_at",
        ]

    def get_video_count(self, obj) -> int:
        return obj.video_count

    def get_chapter_count(self, obj) -> int:
        return obj.chapter_count

    def get_is_enrolled(self, obj) -> bool:
        """Check if the current user is enrolled in this formation."""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return Enrollment.objects.filter(
            user=request.user,
            formation=obj,
            is_active=True
        ).exists()


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for user enrollments."""
    formation = FormationListSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "formation", "is_active", "enrolled_at"]


# Fix: Use IntegerField instead of IntegerProperty
class FormationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for formation cards.
    Used in the list view and homepage sections.
    """
    category = CategorySerializer(read_only=True)
    video_count = serializers.SerializerMethodField()

    class Meta:
        model = Formation
        fields = [
            "id", "title", "slug", "category", "image", "price",
            "is_free", "level", "duration_hours", "video_count", "created_at"
        ]

    def get_video_count(self, obj) -> int:
        return obj.video_count
