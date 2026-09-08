"""
POWER NG TECHNOLOGIE — Paiements Views
Handles payment initialization via PawaPay, status checking, and webhook processing.
"""
import uuid
import logging
from django.utils import timezone
from django.conf import settings
from rest_framework import permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import Payment
from .pawapay import PawaPayService, PawaPayError

from apps.formations.models import Formation, Enrollment
from apps.boutique.models import Order

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------

class PaymentInitSerializer(serializers.Serializer):
    """Input serializer for payment initialization."""
    provider = serializers.ChoiceField(
        choices=Payment.Provider.choices,
        required=False,
        default=Payment.Provider.PAWAPAY,
    )
    formation_id = serializers.IntegerField(required=False, allow_null=True)
    order_id = serializers.IntegerField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, max_length=20, default="")

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
            "transaction_id", "paid_at", "created_at"
        ]


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

@extend_schema(tags=["Paiements"])
class InitiatePaymentView(APIView):
    """
    POST /api/paiements/initier/
    Initialize a payment session via PawaPay.
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
        item_ref = ""

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
            if Enrollment.objects.filter(
                user=user, formation=formation, is_active=True
            ).exists():
                return Response(
                    {"error": "Vous êtes déjà inscrit à cette formation."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            amount = int(formation.price)
            item_ref = f"formation-{formation.pk}"

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
            item_ref = f"order-{order.pk}"

        # Generate the PawaPay deposit ID — use this as the single reference
        deposit_id = PawaPayService.generate_deposit_id()

        # Create the Payment record using deposit_id as transaction_id
        payment = Payment.objects.create(
            user=user,
            amount=amount,
            provider=Payment.Provider.PAWAPAY,
            status=Payment.Status.INITIATED,
            transaction_id=deposit_id,  # Same ID used everywhere
            pawapay_deposit_id=deposit_id,
            formation=formation,
            order=order,
        )

        user_phone = data.get("phone") or user.phone or "237677676767"

        try:
            result = PawaPayService.initiate_deposit(
                amount=amount,
                deposit_id=deposit_id,
                phone=user_phone,
                provider_code="MTN",
                description=item_ref,
            )
            payment.status = Payment.Status.PENDING
            payment.save(update_fields=["status"])

            return Response({
                "reference": deposit_id,
                "status": "PENDING",
                "message": "Paiement initié avec succès. Veuillez entrer votre code PIN Mobile Money sur votre téléphone.",
            })
        except PawaPayError as e:
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Paiements"])
class PaymentStatusView(APIView):
    """
    GET /api/paiements/statut/{reference}/
    Check the status of a payment by its reference (deposit_id).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, reference: str):
        # Look up by transaction_id first, then by pawapay_deposit_id as fallback
        payment = Payment.objects.filter(
            user=request.user,
            transaction_id=reference,
        ).first()

        if not payment:
            payment = Payment.objects.filter(
                user=request.user,
                pawapay_deposit_id=reference,
            ).first()

        if not payment:
            return Response(
                {"error": "Paiement introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(PaymentStatusSerializer(payment).data)


def _activate_payment(payment):
    """Shared logic: activate enrollment or validate order after successful payment."""
    payment.status = Payment.Status.SUCCESS
    payment.paid_at = timezone.now()
    payment.save(update_fields=["status", "paid_at"])

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

    if payment.order:
        payment.order.status = Order.Status.PAID
        payment.order.save(update_fields=["status"])
        logger.info(f"Order #{payment.order.pk} marked as PAID.")


@extend_schema(tags=["Paiements"])
class PawaPayWebhookView(APIView):
    """
    POST /api/paiements/webhook/pawapay/
    Receives PawaPay deposit callbacks / notifications.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        logger.info(f"PawaPay webhook callback received: {data}")

        deposit_id = data.get("depositId") or data.get("deposit_id")
        status_val = data.get("status", "").upper()

        if not deposit_id:
            return Response({"error": "depositId manquant."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(pawapay_deposit_id=deposit_id)
        except Payment.DoesNotExist:
            # Fallback lookup by transaction_id
            payment = Payment.objects.filter(transaction_id=deposit_id).first()
            if not payment:
                logger.warning(f"PawaPay webhook: Payment not found for depositId={deposit_id}")
                return Response({"status": "not_found"}, status=status.HTTP_200_OK)

        if status_val in ("COMPLETED", "SUCCESS", "SUBMITTED"):
            _activate_payment(payment)
            logger.info(f"PawaPay webhook: Payment depositId={deposit_id} COMPLETED")
        elif status_val in ("FAILED", "REJECTED"):
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])
            logger.info(f"PawaPay webhook: Payment depositId={deposit_id} FAILED")
        elif status_val in ("CANCELLED", "EXPIRED"):
            payment.status = Payment.Status.CANCELLED
            payment.save(update_fields=["status"])
            logger.info(f"PawaPay webhook: Payment depositId={deposit_id} CANCELLED")

        return Response({"status": "received"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Paiements"])
class MyPaymentsView(APIView):
    """GET /api/paiements/historique/ — User's payment history."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentStatusSerializer(payments, many=True)
        return Response(serializer.data)
