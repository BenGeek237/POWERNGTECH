"""
POWER NG TECHNOLOGIE — Formations URL Configuration
"""
from django.urls import path
from .views import (
    CategoryListView,
    FormationListView,
    FormationDetailView,
    LatestFormationsView,
    ChapitreDetailView,
    VideoDetailView,
    MyFormationsView,
)

app_name = "formations"

urlpatterns = [
    # Public catalog
    path("", FormationListView.as_view(), name="list"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("latest/", LatestFormationsView.as_view(), name="latest"),
    path("<slug:slug>/", FormationDetailView.as_view(), name="detail"),

    # Protected content (requires enrollment)
    path("<slug:slug>/chapitres/<int:chapitre_id>/", ChapitreDetailView.as_view(), name="chapitre-detail"),
    path("<slug:slug>/videos/<int:video_id>/", VideoDetailView.as_view(), name="video-detail"),
]

# User enrollments (separate from the formations namespace)
mes_formations_urlpatterns = [
    path("", MyFormationsView.as_view(), name="mes-formations"),
]
