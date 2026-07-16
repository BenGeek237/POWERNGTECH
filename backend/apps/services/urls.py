"""POWER NG TECHNOLOGIE — Services URLs"""
from django.urls import path
from .views import ServiceListView, ServiceAllView

app_name = "services"

urlpatterns = [
    path("", ServiceListView.as_view(), name="list"),
    path("all/", ServiceAllView.as_view(), name="all"),
]
