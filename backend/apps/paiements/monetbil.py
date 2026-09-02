"""
POWER NG TECHNOLOGIE — MonetBil Payment Gateway Client
Handles communication with the MonetBil API v2.1 for Mobile Money payments
(MTN MoMo, Orange Money, Express Union).

API Documentation:
- Widget v2.1: POST https://api.monetbil.com/widget/v2.1/{service_key}
- Check Payment: POST https://api.monetbil.com/payment/v1/checkPayment
"""
import logging
import uuid
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MonetBil API URLs
# ---------------------------------------------------------------------------
MONETBIL_WIDGET_URL = "https://api.monetbil.com/widget/v2.1/{service_key}"
MONETBIL_CHECK_PAYMENT_URL = "https://api.monetbil.com/payment/v1/checkPayment"

# ---------------------------------------------------------------------------
# Payment status codes returned by MonetBil
# ---------------------------------------------------------------------------
MONETBIL_STATUS_SUCCESS = 1
MONETBIL_STATUS_FAILED = 0
MONETBIL_STATUS_CANCELLED = -1


def get_service_key():
    """Retrieve the MonetBil service key from settings."""
    key = getattr(settings, "MONETBIL_SERVICE_KEY", None) or ""
    if not key:
        raise ValueError(
            "MONETBIL_SERVICE_KEY is not configured. "
            "Set it in your .env file."
        )
    return key


def generate_payment_ref():
    """Generate a unique payment reference."""
    return f"PAY-{uuid.uuid4().hex[:12].upper()}"


def initiate_payment(
    amount: int,
    payment_ref: str,
    item_ref: str = "",
    phone: str = "",
    email: str = "",
    first_name: str = "",
    last_name: str = "",
    notify_url: str = "",
    return_url: str = "",
) -> dict:
    """
    Initiate a payment via MonetBil Widget API v2.1.

    Args:
        amount: Amount in FCFA (integer).
        payment_ref: Unique reference for this payment.
        item_ref: Reference for the item being purchased.
        phone: Customer phone number (optional, pre-fills widget).
        email: Customer email (optional).
        first_name: Customer first name (optional).
        last_name: Customer last name (optional).
        notify_url: Override for the webhook URL.
        return_url: Override for the redirect URL after payment.

    Returns:
        dict with 'success' (bool) and either 'payment_url' or 'error'.
    """
    service_key = get_service_key()
    url = MONETBIL_WIDGET_URL.format(service_key=service_key)

    payload = {
        "amount": str(amount),
        "payment_ref": payment_ref,
        "notify_url": notify_url or getattr(
            settings, "MONETBIL_NOTIFY_URL", ""
        ),
        "return_url": return_url or getattr(
            settings, "MONETBIL_RETURN_URL", ""
        ),
    }

    # Optional fields — only include if provided
    if item_ref:
        payload["item_ref"] = item_ref
    if phone:
        payload["phone"] = phone
    if email:
        payload["email"] = email
    if first_name:
        payload["first_name"] = first_name
    if last_name:
        payload["last_name"] = last_name

    try:
        logger.info(
            f"MonetBil: Initiating payment ref={payment_ref}, "
            f"amount={amount} FCFA"
        )
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()

        logger.debug(f"MonetBil response: {data}")

        # MonetBil returns a payment_url on success
        if "payment_url" in data and data["payment_url"]:
            return {
                "success": True,
                "payment_url": data["payment_url"],
            }
        else:
            error_msg = data.get("message", "Erreur inconnue de MonetBil.")
            logger.error(f"MonetBil initiation failed: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
            }

    except requests.exceptions.Timeout:
        logger.error("MonetBil: Request timeout")
        return {
            "success": False,
            "error": "Le serveur de paiement ne répond pas. Réessayez.",
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"MonetBil: Request error — {e}")
        return {
            "success": False,
            "error": "Erreur de connexion au serveur de paiement.",
        }
    except (ValueError, KeyError) as e:
        logger.error(f"MonetBil: Invalid response — {e}")
        return {
            "success": False,
            "error": "Réponse invalide du serveur de paiement.",
        }


def check_payment(payment_id: str) -> dict:
    """
    Verify a payment status via MonetBil API v1 checkPayment.

    Args:
        payment_id: The MonetBil paymentId received in the webhook.

    Returns:
        dict with 'status' (int), 'transaction' (dict), and raw response data.
    """
    try:
        logger.info(f"MonetBil: Checking payment {payment_id}")
        response = requests.post(
            MONETBIL_CHECK_PAYMENT_URL,
            data={"paymentId": payment_id},
            timeout=30,
        )
        data = response.json()
        logger.debug(f"MonetBil check response: {data}")

        transaction = data.get("transaction", {})
        status_code = int(transaction.get("status", 0))

        return {
            "success": status_code == MONETBIL_STATUS_SUCCESS,
            "status": status_code,
            "transaction": transaction,
            "raw": data,
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"MonetBil: Check payment error — {e}")
        return {
            "success": False,
            "status": 0,
            "transaction": {},
            "error": str(e),
        }
    except (ValueError, KeyError) as e:
        logger.error(f"MonetBil: Invalid check response — {e}")
        return {
            "success": False,
            "status": 0,
            "transaction": {},
            "error": str(e),
        }
