"""POWER NG TECHNOLOGIE — Boutique Admin"""
from django.contrib import admin
from django.utils.html import format_html
from .models import ProductCategory, Product, ProductImage, ProductSpec, Order, OrderItem


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order"]
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductSpecInline(admin.TabularInline):
    model = ProductSpec
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "is_available", "is_featured", "created_at"]
    list_filter = ["is_available", "is_featured", "category"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductSpecInline]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_available", "price", "stock"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "quantity", "unit_price", "subtotal"]

    def subtotal(self, obj):
        return f"{obj.subtotal:,} FCFA"
    subtotal.short_description = "Sous-total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "total_amount_display", "item_count", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__email", "user__first_name"]
    inlines = [OrderItemInline]
    readonly_fields = ["created_at", "updated_at", "total_amount"]

    def total_amount_display(self, obj):
        return f"{obj.total_amount:,} FCFA"
    total_amount_display.short_description = "Total"
