"""
POWER NG TECHNOLOGIE — CAMERPAY Service
Handles all communication with the CAMERPAY payment API.
"""
import uuid
import hashlib
import hmac
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class CamerpayService:
    """
    Service class to interact with the CAMERPAY API.

    Endpoints used:
    - POST /payment/initialize — Initialize a payment session
    - GET  /payment/status/{reference} — Check payment status
    """

    BASE_URL = settings.CAMERPAY_BASE_URL
    API_KEY = settings.CAMERPAY_API_KEY
    SECRET_KEY = settings.CAMERPAY_SECRET_KEY

    @classmethod
    def _get_headers(cls) -> dict:
        return {
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @classmethod
    def initialize_payment(
        cls,
        amount: int,
        description: str,
        customer_email: str,
        customer_phone: str,
        reference: str,
        callback_url: str,
        return_url: str,
    ) -> dict:
        """
        Initialize a payment session with CAMERPAY.

        Returns:
            dict with 'payment_url' and 'reference' on success.
        Raises:
            CamerpayError on failure.
        """
        payload = {
            "amount": amount,
            "currency": "XAF",
            "description": description,
            "reference": reference,
            "customer": {
                "email": customer_email,
                "phone": customer_phone,
            },
            "callback_url": callback_url,
            "return_url": return_url,
        }

        try:
            response = requests.post(
                f"{cls.BASE_URL}/payment/initialize",
                json=payload,
                headers=cls._get_headers(),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            logger.info(f"CAMERPAY payment initialized: ref={reference}, amount={amount}")
            return data
        except requests.RequestException as e:
            logger.error(f"CAMERPAY API error during initialization: {e}")
            raise CamerpayError(f"Erreur lors de l'initialisation du paiement: {str(e)}")

    @classmethod
    def get_payment_status(cls, reference: str) -> dict:
        """Check the status of a payment by its reference."""
        try:
            response = requests.get(
                f"{cls.BASE_URL}/payment/status/{reference}",
                headers=cls._get_headers(),
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"CAMERPAY status check error: {e}")
            raise CamerpayError(f"Erreur lors de la vérification du statut: {str(e)}")

    @classmethod
    def verify_webhook_signature(cls, payload: bytes, signature: str) -> bool:
        """
        Verify that a webhook notification is genuinely from CAMERPAY.
        Uses HMAC-SHA256 with the webhook secret.
        """
        expected = hmac.new(
            cls.SECRET_KEY.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    @staticmethod
    def generate_reference() -> str:
        """Generate a unique payment reference."""
        return f"PNT-{uuid.uuid4().hex[:16].upper()}"


class CamerpayError(Exception):
    """Raised when CAMERPAY API communication fails."""
    pass
