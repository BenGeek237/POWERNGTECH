"""
POWER NG TECHNOLOGIE — Monetbil Service
Handles Widget API v2.1 initialization, signature verification, and status check.
Documentation: Monetbil Widget API v2.1 & Monetbil Payment Notification API.
"""
import hashlib
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class MonetbilService:
    """
    Service class to interact with the Monetbil API.
    """

    SERVICE_KEY = getattr(settings, "MONETBIL_SERVICE_KEY", "")
    SERVICE_SECRET = getattr(settings, "MONETBIL_SERVICE_SECRET", "")
    WIDGET_BASE_URL = "https://api.monetbil.com/widget/v2.1"
    CHECK_BASE_URL = "https://api.monetbil.com/payment/v1"

    @classmethod
    def initialize_payment(
        cls,
        amount: int,
        payment_ref: str,
        return_url: str,
        notify_url: str,
        phone: str = "",
        first_name: str = "",
        last_name: str = "",
        email: str = "",
        item_ref: str = "",
        country: str = "CM",
        currency: str = "XAF",
    ) -> dict:
        """
        Initialize a payment session with Monetbil Widget API v2.1.

        Args:
            amount: Montant à payer (int)
            payment_ref: Référence unique de la commande/paiement dans notre système
            return_url: URL de retour après le paiement
            notify_url: URL du Webhook de notification de résultat
            phone: Numéro prérempli (optionnel)
            first_name: Prénom (optionnel)
            last_name: Nom (optionnel)
            email: Adresse email (optionnel)
            item_ref: Référence de l'article (optionnel)
            country: Code pays ISO (CM par défaut)
            currency: Devise (XAF par défaut)

        Returns:
            dict avec 'success', 'payment_url', 'payment_id'
        """
        url = f"{cls.WIDGET_BASE_URL}/{cls.SERVICE_KEY}"

        payload = {
            "amount": amount,
            "payment_ref": payment_ref,
            "return_url": return_url,
            "notify_url": notify_url,
            "country": country,
            "currency": currency,
        }

        if phone:
            payload["phone"] = phone
            payload["phone_lock"] = "true"
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if email:
            payload["email"] = email
        if item_ref:
            payload["item_ref"] = item_ref

        try:
            response = requests.post(url, data=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("success") is True:
                payment_url = data.get("payment_url", "")
                logger.info(f"Monetbil payment initialized: ref={payment_ref}, url={payment_url}")
                return {
                    "success": True,
                    "payment_url": payment_url,
                    "payment_ref": payment_ref,
                }
            else:
                message = data.get("message", "Erreur d'initialisation Monetbil")
                logger.error(f"Monetbil init failed: {message}")
                raise MonetbilError(f"Erreur Monetbil: {message}")

        except requests.RequestException as e:
            logger.error(f"Monetbil API error during initialization: {e}")
            raise MonetbilError(f"Erreur lors de l'initialisation du paiement Monetbil: {str(e)}")

    @classmethod
    def verify_signature(cls, params: dict, sign: str) -> bool:
        """
        Verify Monetbil notification signature using MD5.
        Algorithm:
        1. Sort parameters alphabetically by key.
        2. Exclude 'sign' from parameters.
        3. Concatenate service_secret + values of sorted parameters.
        4. Calculate MD5 hash.
        5. Compare with sign.
        """
        if not sign:
            return False

        sorted_keys = sorted([k for k in params.keys() if k != "sign"])
        concatenated_values = "".join(str(params[k]) for k in sorted_keys if params[k] is not None)
        string_to_hash = f"{cls.SERVICE_SECRET}{concatenated_values}"
        
        calculated_sign = hashlib.md5(string_to_hash.encode("utf-8")).hexdigest()
        return calculated_sign.lower() == sign.lower()

    @classmethod
    def check_payment_status(cls, payment_id: str) -> dict:
        """
        Check the status of a payment directly via POST /payment/v1/checkPayment
        """
        url = f"{cls.CHECK_BASE_URL}/checkPayment"
        payload = {"paymentId": payment_id}

        try:
            response = requests.post(url, data=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            logger.error(f"Monetbil checkPayment API error: {e}")
            raise MonetbilError(f"Erreur lors de la vérification Monetbil: {str(e)}")


class MonetbilError(Exception):
    """Raised when Monetbil API communication fails."""
    pass
