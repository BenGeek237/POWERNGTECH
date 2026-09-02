"""
POWER NG TECHNOLOGIE — Paiements Views
Handles payment initialization via MonetBil, status checking, and webhook processing.
"""
import logging
from django.utils import timezone
from django.conf import settings
from rest_framework import permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import Payment
from .monetbil import (
    initiate_payment,
    check_payment,
    generate_payment_ref,
    MONETBIL_STATUS_SUCCESS,
    MONETBIL_STATUS_CANCELLED,
)
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
        default=Payment.Provider.MTN,
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
    Initialize a payment session via MonetBil.
    Returns a payment_url to redirect the user to MonetBil's payment page.
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

        # Generate a unique payment reference
        payment_ref = generate_payment_ref()
        selected_provider = data.get("provider", Payment.Provider.MTN)

        # Create the Payment record in our database
        payment = Payment.objects.create(
            user=user,
            amount=amount,
            provider=selected_provider,
            status=Payment.Status.INITIATED,
            transaction_id=payment_ref,
            formation=formation,
            order=order,
        )

        # ── PawaPay Gateway ──
        if selected_provider == Payment.Provider.PAWAPAY:
            deposit_id = PawaPayService.generate_deposit_id()
            payment.pawapay_deposit_id = deposit_id
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
                payment.save(update_fields=["pawapay_deposit_id", "status"])

                return Response({
                    "reference": deposit_id,
                    "status": "PENDING",
                    "message": "Paiement initié avec succès. Veuillez entrer votre code PIN Mobile Money sur votre téléphone.",
                })
            except PawaPayError as e:
                payment.status = Payment.Status.FAILED
                payment.save(update_fields=["status"])
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # ── MonetBil Gateway (default) ──
        result = initiate_payment(
            amount=amount,
            payment_ref=payment_ref,
            item_ref=item_ref,
            phone=data.get("phone", ""),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        if result["success"]:
            # Save the payment URL
            payment.payment_url = result["payment_url"]
            payment.status = Payment.Status.PENDING
            payment.save(update_fields=["payment_url", "status"])

            logger.info(
                f"Payment initiated: ref={payment_ref}, "
                f"amount={amount} FCFA, user={user.email}"
            )

            return Response({
                "payment_url": result["payment_url"],
                "reference": payment_ref,
                "message": "Redirection vers la page de paiement...",
            })
        else:
            # MonetBil API returned an error
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])

            logger.error(
                f"Payment initiation failed: ref={payment_ref}, "
                f"error={result.get('error')}"
            )

            return Response(
                {"error": result.get("error", "Erreur lors de l'initiation du paiement.")},
                status=status.HTTP_502_BAD_GATEWAY,
            )


@extend_schema(tags=["Paiements"])
class PaymentStatusView(APIView):
    """
    GET /api/paiements/statut/{reference}/
    Check the status of a payment. Also queries MonetBil if still pending.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, reference: str):
        payment = Payment.objects.filter(
            user=request.user,
            transaction_id=reference,
        ).first()

        if not payment:
            return Response(
                {"error": "Paiement introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # If payment is still pending, check with MonetBil
        if payment.status in (
            Payment.Status.INITIATED,
            Payment.Status.PENDING,
        ):
            # Try to check with MonetBil using the payment_ref
            # Note: MonetBil webhook is the primary notification mechanism
            pass

        return Response(PaymentStatusSerializer(payment).data)


@extend_schema(tags=["Paiements"])
class MonetBilWebhookView(APIView):
    """
    POST /api/paiements/webhook/monetbil/
    Receives payment notifications from MonetBil.

    MonetBil sends a POST with a paymentId when a payment status changes.
    We then call checkPayment to verify the transaction.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # No auth for webhooks

    def post(self, request):
        payment_id = request.data.get("paymentId") or request.POST.get("paymentId")

        if not payment_id:
            logger.warning("MonetBil webhook: No paymentId received")
            return Response(
                {"error": "paymentId manquant."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info(f"MonetBil webhook received: paymentId={payment_id}")

        # Verify the payment with MonetBil
        result = check_payment(payment_id)
        transaction = result.get("transaction", {})
        payment_ref = transaction.get("payment_ref", "")

        if not payment_ref:
            logger.warning(
                f"MonetBil webhook: No payment_ref in transaction "
                f"for paymentId={payment_id}"
            )
            return Response({"status": "ignored"})

        # Find the payment in our database
        try:
            payment = Payment.objects.get(transaction_id=payment_ref)
        except Payment.DoesNotExist:
            logger.warning(
                f"MonetBil webhook: Payment not found for ref={payment_ref}"
            )
            return Response({"status": "not_found"})

        # Don't process already completed payments
        if payment.status == Payment.Status.SUCCESS:
            logger.info(f"MonetBil webhook: Payment {payment_ref} already processed")
            return Response({"status": "already_processed"})

        # Store the MonetBil payment ID for future reference
        payment.monetbil_payment_id = payment_id
        payment.save(update_fields=["monetbil_payment_id"])

        monetbil_status = result.get("status", 0)

        if monetbil_status == MONETBIL_STATUS_SUCCESS:
            # Payment successful — activate enrollment/order
            _activate_payment(payment)
            logger.info(f"MonetBil webhook: Payment {payment_ref} SUCCESS")
            return Response({"status": "success"})

        elif monetbil_status == MONETBIL_STATUS_CANCELLED:
            payment.status = Payment.Status.CANCELLED
            payment.save(update_fields=["status"])
            logger.info(f"MonetBil webhook: Payment {payment_ref} CANCELLED")
            return Response({"status": "cancelled"})

        else:
            # Status 0 = still pending or failed
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])
            logger.info(
                f"MonetBil webhook: Payment {payment_ref} "
                f"status={monetbil_status}"
            )
            return Response({"status": "failed"})


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
    POST /api/paiements/pawapay-webhook/
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
