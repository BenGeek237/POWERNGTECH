"""POWER NG TECHNOLOGIE — Paiements URLs"""
from django.urls import path
from .views import (
    InitiatePaymentView, PaymentStatusView,
    MyPaymentsView, PawaPayWebhookView,
)

app_name = "paiements"

urlpatterns = [
    path("initier/", InitiatePaymentView.as_view(), name="initiate"),
    path("statut/<str:reference>/", PaymentStatusView.as_view(), name="status"),
    path("historique/", MyPaymentsView.as_view(), name="history"),
    # PawaPay webhook — receives POST notifications from PawaPay
    path("webhook/pawapay/", PawaPayWebhookView.as_view(), name="pawapay-webhook"),
]
