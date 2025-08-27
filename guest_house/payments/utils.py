import requests
from django.conf import settings

PAYSTACK_BASE_URL = "https://api.paystack.co"

def initialize_payment(email: str, amount: float, reference: str) -> dict:
    """
    Initialize a Paystack payment.
    """
    url = f"{PAYSTACK_BASE_URL}/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "amount": int(amount * 100),  # Convert to kobo
        "reference": reference
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def verify_payment(reference: str) -> dict:
    """
    Verify a Paystack payment.
    """
    url = f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    response = requests.get(url, headers=headers)
    return response.json()
