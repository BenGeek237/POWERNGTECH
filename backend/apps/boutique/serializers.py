"""
POWER NG TECHNOLOGIE — Boutique Serializers
"""
from rest_framework import serializers
from .models import ProductCategory, Product, ProductImage, ProductSpec, Order, OrderItem


class ProductCategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ["id", "name", "slug", "description", "product_count"]

    def get_product_count(self, obj) -> int:
        return obj.products.filter(is_available=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_primary", "alt_text", "order"]


class ProductSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpec
        fields = ["key", "value", "order"]


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product cards."""
    primary_image = serializers.SerializerMethodField()
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "category", "price",
            "is_available", "is_featured", "primary_image", "created_at"
        ]

    def get_primary_image(self, obj):
        img = obj.primary_image
        if img:
            request = self.context.get("request")
            return request.build_absolute_uri(img.image.url) if request else img.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for product detail page."""
    category = ProductCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    specs = ProductSpecSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "category", "description", "price",
            "stock", "is_available", "is_featured", "images", "specs", "created_at"
        ]


class OrderItemCreateSerializer(serializers.Serializer):
    """Serializer for a single item when creating an order."""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, max_value=100)


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating a new order."""
    items = OrderItemCreateSerializer(many=True)
    delivery_address = serializers.CharField(required=True)
    delivery_city = serializers.CharField(required=True)
    delivery_phone = serializers.CharField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("La commande doit contenir au moins un article.")
        return items


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=0, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    """Full order serializer for user's order history."""
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "status", "total_amount", "delivery_address",
            "delivery_city", "delivery_phone", "notes", "items",
            "item_count", "created_at"
        ]
        read_only_fields = ["id", "status", "total_amount", "created_at"]
