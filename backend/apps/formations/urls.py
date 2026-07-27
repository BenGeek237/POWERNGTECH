"""
POWER NG TECHNOLOGIE — Formations URL Configuration
"""
from django.urls import path
from .views import (
    CategoryListView,
    FormationListView,
    FormationDetailView,
    LatestFormationsView,
    DownloadFormationZipView,
    MyFormationsView,
)

app_name = "formations"

urlpatterns = [
    # Public catalog
    path("", FormationListView.as_view(), name="list"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("latest/", LatestFormationsView.as_view(), name="latest"),
    path("<slug:slug>/", FormationDetailView.as_view(), name="detail"),

    # ZIP download (requires enrollment)
    path("<slug:slug>/download/", DownloadFormationZipView.as_view(), name="download-zip"),
]

# User enrollments (separate from the formations namespace)
mes_formations_urlpatterns = [
    path("", MyFormationsView.as_view(), name="mes-formations"),
]
