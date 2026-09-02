"""POWER NG TECHNOLOGIE — Paiements Admin"""
from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "amount_display", "provider", "status", "paid_at", "created_at"]
    list_filter = ["status", "provider", "created_at"]
    search_fields = ["user__email", "transaction_id"]
    readonly_fields = ["user", "amount", "provider", "transaction_id", "paid_at", "created_at"]

    def amount_display(self, obj):
        return f"{obj.amount:,} FCFA"
    amount_display.short_description = "Montant"
