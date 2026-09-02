"""
POWER NG TECHNOLOGIE — PawaPay Service
Handles direct Mobile Money deposit requests with PawaPay API.
Documentation: https://pawapay.io / https://pawapay.mintlify.app/
"""
import uuid
import logging
from datetime import datetime, timezone
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class PawaPayService:
    """
    Service class to interact with PawaPay Direct Deposit API.
    """

    API_KEY = getattr(settings, "PAWAPAY_API_KEY", "")
    BASE_URL = getattr(settings, "PAWAPAY_BASE_URL", "https://api.sandbox.pawapay.cloud").rstrip("/")

    @classmethod
    def get_headers(cls) -> dict:
        """Construct authorization headers for PawaPay API requests."""
        return {
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json",
        }

    @classmethod
    def initiate_deposit(
        cls,
        amount: int,
        deposit_id: str,
        phone: str,
        provider_code: str = "MTN",
        description: str = "PowerNgTech",
        currency: str = "XAF",
        country: str = "CMR",
    ) -> dict:
        """
        Initiate a Mobile Money payment deposit via PawaPay API.

        Args:
            amount: Amount in FCFA (integer, e.g. 500)
            deposit_id: Unique deposit UUID string
            phone: Phone number (e.g. 237677676767 or 677676767)
            provider_code: 'MTN' or 'ORANGE'
            description: Statement description (max 22 alphanumeric characters, no spaces)
            currency: 'XAF'
            country: 'CMR'

        Returns:
            dict containing 'deposit_id', 'status', 'created'
        """
        url = f"{cls.BASE_URL}/deposits"

        # Format phone number to international standard without + if needed
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if len(clean_phone) == 9 and clean_phone.startswith("6"):
            clean_phone = f"237{clean_phone}"

        # Determine PawaPay correspondent code
        if "ORANGE" in provider_code.upper():
            correspondent = f"ORANGE_{country}"
        else:
            correspondent = f"MTN_MOMO_{country}"

        # Sanitize statement description (alphanumeric, max 22 chars)
        sanitized_desc = "".join(c for c in description if c.isalnum())[:22] or "PowerNgTech"

        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        payload = {
            "depositId": deposit_id,
            "amount": str(int(amount)),
            "currency": currency,
            "country": country,
            "correspondent": correspondent,
            "payer": {
                "type": "MSISDN",
                "address": {
                    "value": clean_phone
                }
            },
            "customerTimestamp": now_iso,
            "statementDescription": sanitized_desc,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=cls.get_headers(),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            logger.info(f"PawaPay deposit initiated successfully: deposit_id={deposit_id}, status={data.get('status')}")

            return {
                "deposit_id": deposit_id,
                "status": data.get("status", "ACCEPTED"),
                "created": data.get("created"),
            }

        except requests.RequestException as e:
            logger.error(f"PawaPay API error during deposit initialization: {e}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"PawaPay error response: {e.response.text}")
                error_msg = e.response.text
                try:
                    err_json = e.response.json()
                    error_msg = err_json.get("errorMessage") or err_json.get("message") or e.response.text
                except Exception:
                    pass
                raise PawaPayError(f"Erreur PawaPay: {error_msg}")
            raise PawaPayError(f"Erreur de connexion PawaPay: {str(e)}")

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
        """Generate a valid UUID v4 string for PawaPay deposit ID."""
        return str(uuid.uuid4())


class PawaPayError(Exception):
    """Raised when PawaPay API communication fails."""
    pass
