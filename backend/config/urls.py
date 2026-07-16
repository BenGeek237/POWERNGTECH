"""
POWER NG TECHNOLOGIE — Root URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # API v1
    path("api/auth/", include("apps.accounts.urls")),
    path("api/formations/", include("apps.formations.urls")),
    path("api/boutique/", include("apps.boutique.urls")),
    path("api/services/", include("apps.services.urls")),
    path("api/demandes/", include("apps.demandes.urls")),
    path("api/paiements/", include("apps.paiements.urls")),

    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    pass

# Custom Admin Site
admin.site.site_header = "POWER NG TECHNOLOGIE — Administration"
admin.site.site_title = "POWER NG Admin"
admin.site.index_title = "Tableau de bord"
