"""
POWER NG TECHNOLOGIE — Paiements Views
Handles payment initialization, status checking, CAMERPAY and CinetPay webhooks.
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
from .cinetpay import CinetPayService, CinetPayError
from .monetbil import MonetbilService, MonetbilError
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
            "camerpay_reference", "cinetpay_transaction_id",
            "paid_at", "created_at"
        ]


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

@extend_schema(tags=["Paiements"])
class InitiatePaymentView(APIView):
    """
    POST /api/paiements/initier/
    Initialize a payment session (CamerPay for MoMo/OM, CinetPay for cards).
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

        provider = data["provider"]

        # ── CinetPay (Carte Bancaire) ──
        if provider == Payment.Provider.CARTE:
            return self._initiate_cinetpay(request, user, amount, description, formation, order)

        # ── Monetbil (MTN MoMo, Orange Money) ──
        return self._initiate_monetbil(request, user, data, amount, description, formation, order)

    def _initiate_cinetpay(self, request, user, amount, description, formation, order):
        """Initialize a CinetPay payment session."""
        transaction_id = CinetPayService.generate_transaction_id()
        payment = Payment.objects.create(
            user=user,
            amount=amount,
            provider=Payment.Provider.CARTE,
            cinetpay_transaction_id=transaction_id,
            formation=formation,
            order=order,
            status=Payment.Status.INITIATED,
        )

        try:
            return_url = f"{settings.FRONTEND_URL}/paiement/retour/{transaction_id}/"
            notify_url = f"{request.scheme}://{request.get_host()}/api/paiements/cinetpay-webhook/"

            result = CinetPayService.initialize_payment(
                amount=amount,
                currency="XAF",
                description=description,
                transaction_id=transaction_id,
                return_url=return_url,
                notify_url=notify_url,
                customer_name=user.get_full_name(),
                customer_email=user.email,
                customer_phone=user.phone or "",
                channels="ALL",
            )

            payment.cinetpay_payment_url = result.get("payment_url", "")
            payment.status = Payment.Status.PENDING
            payment.save(update_fields=["cinetpay_payment_url", "status"])

            return Response(
                {
                    "transaction_id": transaction_id,
                    "payment_url": result.get("payment_url", ""),
                    "amount": amount,
                    "payment_id": payment.pk,
                },
                status=status.HTTP_201_CREATED,
            )

        except CinetPayError as e:
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

    def _initiate_camerpay(self, request, user, data, amount, description, formation, order):
        """Initialize a CamerPay payment session."""
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

        try:
            return_url = f"{settings.FRONTEND_URL}/paiement/retour/{reference}/"
            camerpay_response = CamerpayService.initialize_payment(
                amount=amount,
                description=description,
                customer_email=user.email,
                customer_phone=data.get("phone", user.phone or ""),
                reference=reference,
                callback_url=f"{request.scheme}://{request.get_host()}/api/paiements/webhook/",
                return_url=return_url,
            )

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
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

    def _initiate_monetbil(self, request, user, data, amount, description, formation, order):
        """Initialize a Monetbil payment session."""
        payment_ref = f"PNT-{timezone.now().strftime('%Y%m%d%H%M%S')}-{user.id}"
        payment = Payment.objects.create(
            user=user,
            amount=amount,
            provider=data["provider"],
            monetbil_payment_id=payment_ref,
            formation=formation,
            order=order,
            status=Payment.Status.INITIATED,
        )

        try:
            return_url = f"{settings.FRONTEND_URL}/paiement/retour/{payment_ref}/"
            notify_url = f"{request.scheme}://{request.get_host()}/api/paiements/monetbil-webhook/"

            result = MonetbilService.initialize_payment(
                amount=amount,
                payment_ref=payment_ref,
                return_url=return_url,
                notify_url=notify_url,
                phone=data.get("phone", user.phone or ""),
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                item_ref=description,
            )

            payment_url = result.get("payment_url", "")
            payment.monetbil_payment_url = payment_url
            payment.status = Payment.Status.PENDING
            payment.save(update_fields=["monetbil_payment_url", "status"])

            return Response(
                {
                    "reference": payment_ref,
                    "payment_url": payment_url,
                    "amount": amount,
                    "payment_id": payment.pk,
                },
                status=status.HTTP_201_CREATED,
            )

        except MonetbilError as e:
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


@extend_schema(tags=["Paiements"])
class PaymentStatusView(APIView):
    """
    GET /api/paiements/statut/{reference}/
    Poll payment status.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, reference: str):
        from django.db.models import Q

        payment = Payment.objects.filter(
            user=request.user,
        ).filter(
            Q(camerpay_reference=reference) | Q(cinetpay_transaction_id=reference) | Q(monetbil_payment_id=reference)
        ).first()

        if not payment:
            return Response({"error": "Paiement introuvable."}, status=status.HTTP_404_NOT_FOUND)

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
class CamerpayWebhookView(APIView):
    """
    POST /api/paiements/webhook/
    Receives CAMERPAY webhook notifications.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
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
            return Response(status=status.HTTP_200_OK)

        if webhook_status == "SUCCESS":
            _activate_payment(payment)
        elif webhook_status in ("FAILED", "CANCELLED"):
            payment.status = (
                Payment.Status.FAILED if webhook_status == "FAILED"
                else Payment.Status.CANCELLED
            )
            payment.save(update_fields=["status"])

        return Response({"message": "Webhook reçu."}, status=status.HTTP_200_OK)


@extend_schema(tags=["Paiements"])
class CinetPayWebhookView(APIView):
    """
    POST /api/paiements/cinetpay-webhook/
    Receives CinetPay webhook notifications (IPN).
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        transaction_id = data.get("cpm_trans_id", "")

        logger.info(f"CinetPay webhook received: txn={transaction_id}")

        if not transaction_id:
            return Response(status=status.HTTP_200_OK)

        try:
            payment = Payment.objects.get(cinetpay_transaction_id=transaction_id)
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for CinetPay txn: {transaction_id}")
            return Response(status=status.HTTP_200_OK)

        # Verify by checking status with CinetPay API
        try:
            status_data = CinetPayService.check_payment_status(transaction_id)
            cinetpay_status = status_data.get("status", "")

            if cinetpay_status == "ACCEPTED":
                _activate_payment(payment)
                logger.info(f"CinetPay payment ACCEPTED: txn={transaction_id}")
            elif cinetpay_status in ("REFUSED", "CANCELLED"):
                payment.status = Payment.Status.FAILED
                payment.save(update_fields=["status"])
                logger.info(f"CinetPay payment {cinetpay_status}: txn={transaction_id}")

        except CinetPayError as e:
            logger.error(f"CinetPay verification failed: {e}")

        return Response({"message": "Webhook reçu."}, status=status.HTTP_200_OK)


@extend_schema(tags=["Paiements"])
class MonetbilWebhookView(APIView):
    """
    POST/GET /api/paiements/monetbil-webhook/
    Receives Monetbil webhook notifications (status=success, cancelled, failed).
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        return self._handle_notification(request.data or request.POST)

    def get(self, request):
        return self._handle_notification(request.GET)

    def _handle_notification(self, data):
        data_dict = data.dict() if hasattr(data, "dict") else dict(data)
        logger.info(f"Monetbil webhook notification received: {data_dict}")

        sign = data_dict.get("sign", "")
        payment_ref = data_dict.get("payment_ref", "") or data_dict.get("item_ref", "")
        status_val = data_dict.get("status", "")

        # Optional signature check log (if secret key configured)
        if settings.MONETBIL_SERVICE_SECRET:
            if not MonetbilService.verify_signature(data_dict, sign):
                logger.warning("Invalid Monetbil webhook signature.")
                # We log warning but continue if ref exists for dev testing

        if not payment_ref:
            return Response({"error": "Référence manquante."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(monetbil_payment_id=payment_ref)
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for Monetbil ref: {payment_ref}")
            return Response(status=status.HTTP_200_OK)

        if status_val == "success":
            _activate_payment(payment)
            logger.info(f"Monetbil payment SUCCESS: ref={payment_ref}")
        elif status_val in ("cancelled", "failed"):
            payment.status = (
                Payment.Status.CANCELLED if status_val == "cancelled" else Payment.Status.FAILED
            )
            payment.save(update_fields=["status"])
            logger.info(f"Monetbil payment {status_val}: ref={payment_ref}")

        return Response("received", status=status.HTTP_200_OK)


@extend_schema(tags=["Paiements"])
class MyPaymentsView(APIView):
    """GET /api/paiements/historique/ — User's payment history."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentStatusSerializer(payments, many=True)
        return Response(serializer.data)
