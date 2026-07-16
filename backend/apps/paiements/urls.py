"""POWER NG TECHNOLOGIE — Paiements URLs"""
from django.urls import path
from .views import InitiatePaymentView, PaymentStatusView, CamerpayWebhookView, MyPaymentsView

app_name = "paiements"

urlpatterns = [
    path("initier/", InitiatePaymentView.as_view(), name="initiate"),
    path("statut/<str:reference>/", PaymentStatusView.as_view(), name="status"),
    path("webhook/", CamerpayWebhookView.as_view(), name="webhook"),
    path("historique/", MyPaymentsView.as_view(), name="history"),
]
