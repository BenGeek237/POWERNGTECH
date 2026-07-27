"""
POWER NG TECHNOLOGIE — CinetPay Service
Handles all communication with the CinetPay payment API.
Documentation: https://docs.cinetpay.com/
"""
import uuid
import hashlib
import hmac
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class CinetPayService:
    """
    Service class to interact with the CinetPay API.

    Endpoints used:
    - POST /payment — Initialize a payment session
    - POST /payment/check — Check payment status
    """

    BASE_URL = "https://api-checkout.cinetpay.com/v2"
    API_KEY = getattr(settings, "CINETPAY_API_KEY", "")
    SITE_ID = getattr(settings, "CINETPAY_SITE_ID", "")
    SECRET_KEY = getattr(settings, "CINETPAY_SECRET_KEY", "")

    @classmethod
    def initialize_payment(
        cls,
        amount: int,
        currency: str,
        description: str,
        transaction_id: str,
        return_url: str,
        notify_url: str,
        customer_name: str = "",
        customer_email: str = "",
        customer_phone: str = "",
        channels: str = "ALL",
    ) -> dict:
        """
        Initialize a payment session with CinetPay.

        Args:
            amount: Payment amount (integer, e.g. 5000 for 5000 FCFA)
            currency: Currency code (XAF, XOF, USD, EUR, etc.)
            description: Description of the payment
            transaction_id: Unique transaction identifier
            return_url: URL to redirect user after payment
            notify_url: Webhook URL for payment notifications
            customer_name: Customer full name
            customer_email: Customer email
            customer_phone: Customer phone number
            channels: Payment channels (ALL, MOBILE_MONEY, CREDIT_CARD, WALLET)

        Returns:
            dict with 'payment_url' and 'payment_token' on success.
        Raises:
            CinetPayError on failure.
        """
        payload = {
            "apikey": cls.API_KEY,
            "site_id": cls.SITE_ID,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "description": description,
            "return_url": return_url,
            "notify_url": notify_url,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone_number": customer_phone,
            "channels": channels,
        }

        try:
            response = requests.post(
                f"{cls.BASE_URL}/payment",
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            if data.get("code") == "201":
                payment_url = data.get("data", {}).get("payment_url", "")
                payment_token = data.get("data", {}).get("payment_token", "")
                logger.info(
                    f"CinetPay payment initialized: txn={transaction_id}, amount={amount} {currency}"
                )
                return {
                    "payment_url": payment_url,
                    "payment_token": payment_token,
                    "transaction_id": transaction_id,
                }
            else:
                error_msg = data.get("message", "Erreur inconnue")
                logger.error(f"CinetPay initialization failed: {error_msg}")
                raise CinetPayError(f"Erreur CinetPay: {error_msg}")

        except requests.RequestException as e:
            logger.error(f"CinetPay API error during initialization: {e}")
            raise CinetPayError(f"Erreur lors de l'initialisation du paiement: {str(e)}")

    @classmethod
    def check_payment_status(cls, transaction_id: str) -> dict:
        """
        Check the status of a payment by its transaction ID.

        Returns:
            dict with payment status information.
        """
        payload = {
            "apikey": cls.API_KEY,
            "site_id": cls.SITE_ID,
            "transaction_id": transaction_id,
        }

        try:
            response = requests.post(
                f"{cls.BASE_URL}/payment/check",
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            if data.get("code") == "00":
                return data.get("data", {})
            else:
                error_msg = data.get("message", "Erreur inconnue")
                raise CinetPayError(f"Erreur de vérification: {error_msg}")

        except requests.RequestException as e:
            logger.error(f"CinetPay status check error: {e}")
            raise CinetPayError(f"Erreur lors de la vérification du statut: {str(e)}")

    @classmethod
    def verify_webhook(cls, data: dict) -> bool:
        """
        Verify a CinetPay webhook notification by checking the transaction status.
        CinetPay doesn't use HMAC signatures — instead, we verify by calling
        check_payment_status with the transaction_id from the webhook.
        """
        transaction_id = data.get("cpm_trans_id", "")
        if not transaction_id:
            return False
        try:
            status_data = cls.check_payment_status(transaction_id)
            return status_data.get("status") == "ACCEPTED"
        except CinetPayError:
            return False

    @staticmethod
    def generate_transaction_id() -> str:
        """Generate a unique transaction ID for CinetPay."""
        return f"PNT-{uuid.uuid4().hex[:16].upper()}"


class CinetPayError(Exception):
    """Raised when CinetPay API communication fails."""
    pass
