"""
POWER NG TECHNOLOGIE — Boutique Views
"""
import django_filters
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import ProductCategory, Product, Order, OrderItem
from .serializers import (
    ProductCategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    OrderCreateSerializer,
    OrderSerializer,
)


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    is_available = django_filters.BooleanFilter()
    is_featured = django_filters.BooleanFilter()

    class Meta:
        model = Product
        fields = ["category", "is_available", "is_featured"]


@extend_schema(tags=["Boutique"])
class ProductCategoryListView(generics.ListAPIView):
    """GET /api/boutique/categories/"""
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


@extend_schema(tags=["Boutique"])
class ProductListView(generics.ListAPIView):
    """GET /api/boutique/produits/"""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["created_at", "price", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Product.objects.filter(
            is_available=True
        ).select_related("category").prefetch_related("images")


@extend_schema(tags=["Boutique"])
class ProductDetailView(generics.RetrieveAPIView):
    """GET /api/boutique/produits/{slug}/"""
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        return Product.objects.filter(
            is_available=True
        ).select_related("category").prefetch_related("images", "specs")


@extend_schema(tags=["Boutique"])
class LatestProductsView(generics.ListAPIView):
    """GET /api/boutique/latest/ — 6 latest products for homepage."""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Product.objects.filter(
            is_available=True
        ).select_related("category").prefetch_related("images")[:6]


@extend_schema(tags=["Commandes"])
class OrderCreateView(APIView):
    """POST /api/boutique/commandes/ — Create a new order."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Validate all products exist and are available
        items_data = data["items"]
        order_items = []
        total = 0

        for item_data in items_data:
            try:
                product = Product.objects.get(
                    id=item_data["product_id"], is_available=True
                )
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Produit #{item_data['product_id']} introuvable ou indisponible."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if product.stock < item_data["quantity"]:
                return Response(
                    {"error": f"Stock insuffisant pour '{product.name}'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            order_items.append((product, item_data["quantity"]))
            total += product.price * item_data["quantity"]

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            delivery_address=data.get("delivery_address", ""),
            delivery_city=data.get("delivery_city", ""),
            delivery_phone=data.get("delivery_phone", ""),
            notes=data.get("notes", ""),
        )

        # Create order items
        for product, qty in order_items:
            OrderItem.objects.create(
                order=order, product=product,
                quantity=qty, unit_price=product.price
            )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )


@extend_schema(tags=["Commandes"])
class MyOrdersView(generics.ListAPIView):
    """GET /api/boutique/mes-commandes/ — User's order history."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related("items__product__images")


@extend_schema(tags=["Commandes"])
class OrderDetailView(generics.RetrieveAPIView):
    """GET /api/boutique/mes-commandes/{id}/ — Single order detail."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
