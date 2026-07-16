"""POWER NG TECHNOLOGIE — Boutique URL Configuration"""
from django.urls import path
from .views import (
    ProductCategoryListView, ProductListView, ProductDetailView,
    LatestProductsView, OrderCreateView, MyOrdersView, OrderDetailView
)

app_name = "boutique"

urlpatterns = [
    path("produits/", ProductListView.as_view(), name="product-list"),
    path("produits/latest/", LatestProductsView.as_view(), name="product-latest"),
    path("produits/categories/", ProductCategoryListView.as_view(), name="category-list"),
    path("produits/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("commandes/", OrderCreateView.as_view(), name="order-create"),
    path("mes-commandes/", MyOrdersView.as_view(), name="my-orders"),
    path("mes-commandes/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
