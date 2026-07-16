"""
POWER NG TECHNOLOGIE — Paiements Views
Handles payment initialization, status checking, and CAMERPAY webhooks.
"""
import json
import logging
from django.utils import timezone
from django.conf import settings
from rest_framework import permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import Payment
from .camerpay import CamerpayService, CamerpayError
from apps.formations.models import Formation, Enrollment
from apps.boutique.models import Order

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------

class PaymentInitSerializer(serializers.Serializer):
    """Input serializer for payment initialization."""
    provider = serializers.ChoiceField(choices=Payment.Provider.choices)
    formation_id = serializers.IntegerField(required=False, allow_null=True)
    order_id = serializers.IntegerField(required=False, allow_null=True)
    phone = serializers.CharField(required=True, max_length=20)

    def validate(self, attrs):
        if not attrs.get("formation_id") and not attrs.get("order_id"):
            raise serializers.ValidationError(
                "Vous devez spécifier une formation ou une commande à payer."
            )
        if attrs.get("formation_id") and attrs.get("order_id"):
            raise serializers.ValidationError(
                "Vous ne pouvez pas payer une formation et une commande en même temps."
            )
        return attrs


class PaymentStatusSerializer(serializers.ModelSerializer):
    """Serializer for payment status display."""
    class Meta:
        model = Payment
        fields = [
            "id", "amount", "status", "provider",
            "camerpay_reference", "paid_at", "created_at"
        ]


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

@extend_schema(tags=["Paiements"])
class InitiatePaymentView(APIView):
    """
    POST /api/paiements/initier/
    Initialize a CAMERPAY payment session for a formation or order.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PaymentInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        formation = None
        order = None
        amount = 0

        # Determine what is being paid for
        if data.get("formation_id"):
            try:
                formation = Formation.objects.get(
                    id=data["formation_id"],
                    status=Formation.Status.PUBLISHED,
                    is_free=False,
                )
            except Formation.DoesNotExist:
                return Response(
                    {"error": "Formation introuvable ou gratuite."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            # Check if already enrolled
            if Enrollment.objects.filter(user=user, formation=formation, is_active=True).exists():
                return Response(
                    {"error": "Vous êtes déjà inscrit à cette formation."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            amount = int(formation.price)
            description = f"Formation: {formation.title}"

        elif data.get("order_id"):
            try:
                order = Order.objects.get(
                    id=data["order_id"],
                    user=user,
                    status=Order.Status.PENDING,
                )
            except Order.DoesNotExist:
                return Response(
                    {"error": "Commande introuvable ou déjà payée."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            amount = int(order.total_amount)
            description = f"Commande #{order.pk}"

        # Generate reference and create payment record
        reference = CamerpayService.generate_reference()
        payment = Payment.objects.create(
            user=user,
            amount=amount,
            provider=data["provider"],
            camerpay_reference=reference,
            formation=formation,
            order=order,
            status=Payment.Status.INITIATED,
        )

        # Call CAMERPAY API
        try:
            callback_url = f"{settings.FRONTEND_URL}/paiement/callback/{reference}/"
            return_url = f"{settings.FRONTEND_URL}/paiement/retour/{reference}/"

            camerpay_response = CamerpayService.initialize_payment(
                amount=amount,
                description=description,
                customer_email=user.email,
                customer_phone=data["phone"],
                reference=reference,
                callback_url=f"{request.scheme}://{request.get_host()}/api/paiements/webhook/",
                return_url=return_url,
            )

            # Update with payment URL
            payment_url = camerpay_response.get("payment_url", "")
            payment.camerpay_payment_url = payment_url
            payment.status = Payment.Status.PENDING
            payment.save(update_fields=["camerpay_payment_url", "status"])

            return Response(
                {
                    "reference": reference,
                    "payment_url": payment_url,
                    "amount": amount,
                    "payment_id": payment.pk,
                },
                status=status.HTTP_201_CREATED,
            )

        except CamerpayError as e:
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])
            return Response(
                {"error": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )


@extend_schema(tags=["Paiements"])
class PaymentStatusView(APIView):
    """
    GET /api/paiements/statut/{reference}/
    Poll payment status (used by frontend after redirect).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, reference: str):
        try:
            payment = Payment.objects.get(
                camerpay_reference=reference,
                user=request.user,
            )
        except Payment.DoesNotExist:
            return Response({"error": "Paiement introuvable."}, status=status.HTTP_404_NOT_FOUND)

        return Response(PaymentStatusSerializer(payment).data)


@extend_schema(tags=["Paiements"])
class CamerpayWebhookView(APIView):
    """
    POST /api/paiements/webhook/
    Receives CAMERPAY webhook notifications.
    Verifies signature, updates payment status, and activates access.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        # Verify webhook signature
        signature = request.headers.get("X-Camerpay-Signature", "")
        raw_body = request.body

        if not CamerpayService.verify_webhook_signature(raw_body, signature):
            logger.warning("Invalid CAMERPAY webhook signature received.")
            return Response({"error": "Signature invalide."}, status=status.HTTP_403_FORBIDDEN)

        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            return Response({"error": "Corps invalide."}, status=status.HTTP_400_BAD_REQUEST)

        reference = payload.get("reference")
        webhook_status = payload.get("status")

        logger.info(f"CAMERPAY webhook: ref={reference}, status={webhook_status}")

        try:
            payment = Payment.objects.get(camerpay_reference=reference)
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for reference: {reference}")
            return Response(status=status.HTTP_200_OK)  # Always 200 to avoid CAMERPAY retries

        if webhook_status == "SUCCESS":
            payment.status = Payment.Status.SUCCESS
            payment.paid_at = timezone.now()
            payment.save(update_fields=["status", "paid_at"])

            # Activate formation enrollment
            if payment.formation:
                Enrollment.objects.get_or_create(
                    user=payment.user,
                    formation=payment.formation,
                    defaults={"is_active": True},
                )
                logger.info(
                    f"Enrollment activated: user={payment.user.email}, "
                    f"formation={payment.formation.title}"
                )

            # Validate order
            if payment.order:
                payment.order.status = Order.Status.PAID
                payment.order.save(update_fields=["status"])
                logger.info(f"Order #{payment.order.pk} marked as PAID.")

        elif webhook_status in ("FAILED", "CANCELLED"):
            payment.status = (
                Payment.Status.FAILED
                if webhook_status == "FAILED"
                else Payment.Status.CANCELLED
            )
            payment.save(update_fields=["status"])

        return Response({"message": "Webhook reçu."}, status=status.HTTP_200_OK)


@extend_schema(tags=["Paiements"])
class MyPaymentsView(APIView):
    """GET /api/paiements/historique/ — User's payment history."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentStatusSerializer(payments, many=True)
        return Response(serializer.data)
