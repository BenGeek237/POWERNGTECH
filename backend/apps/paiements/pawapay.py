"""
POWER NG TECHNOLOGIE — PawaPay Service
Handles communication with the PawaPay API for hosted payment page sessions & deposit verification.
Documentation: https://pawapay.io / https://pawapay.mintlify.app/
"""
import uuid
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class PawaPayService:
    """
    Service class to interact with the PawaPay Merchant API.
    """

    API_KEY = getattr(settings, "PAWAPAY_API_KEY", "")
    BASE_URL = getattr(settings, "PAWAPAY_BASE_URL", "https://api.pawapay.cloud")

    @classmethod
    def get_headers(cls) -> dict:
        """Construct authorization headers for PawaPay API requests."""
        return {
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json",
        }

    @classmethod
    def initiate_deposit_session(
        cls,
        amount: int,
        deposit_id: str,
        return_url: str,
        description: str = "Paiement POWER NG",
        currency: str = "XAF",
        phone: str = "",
    ) -> dict:
        """
        Create a Payment Page / Hosted Deposit Session with PawaPay.

        Args:
            amount: Amount in FCFA (integer)
            deposit_id: Unique deposit UUID in our system
            return_url: URL to redirect the user after payment completion
            description: Statement description
            currency: Currency code (XAF, XOF, etc.)
            phone: User phone number (optional)

        Returns:
            dict containing 'redirect_url' and 'deposit_id'
        """
        url = f"{cls.BASE_URL}/v1/widget/sessions"

        payload = {
            "depositId": deposit_id,
            "amount": str(amount),
            "currency": currency,
            "returnUrl": return_url,
            "statementDescription": description[:22],  # Max 22 chars for PawaPay
            "reason": description,
        }

        if phone:
            payload["phoneNumber"] = phone

        try:
            response = requests.post(
                url,
                json=payload,
                headers=cls.get_headers(),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            redirect_url = data.get("redirectUrl") or data.get("checkoutUrl") or data.get("url")
            logger.info(f"PawaPay deposit session created: deposit_id={deposit_id}, redirectUrl={redirect_url}")

            return {
                "deposit_id": deposit_id,
                "redirect_url": redirect_url,
            }

        except requests.RequestException as e:
            logger.error(f"PawaPay API error during deposit initialization: {e}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"PawaPay error response: {e.response.text}")
            raise PawaPayError(f"Erreur lors de l'initialisation du paiement PawaPay: {str(e)}")

    @classmethod
    def check_deposit_status(cls, deposit_id: str) -> dict:
        """
        Check deposit status via GET /deposits/{deposit_id}
        """
        url = f"{cls.BASE_URL}/deposits/{deposit_id}"

        try:
            response = requests.get(
                url,
                headers=cls.get_headers(),
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"PawaPay check status error for {deposit_id}: {e}")
            raise PawaPayError(f"Erreur de vérification du statut PawaPay: {str(e)}")

    @staticmethod
    def generate_deposit_id() -> str:
        """Generate a valid UUID string for PawaPay deposit ID."""
        return str(uuid.uuid4())


class PawaPayError(Exception):
    """Raised when PawaPay API communication fails."""
    pass
