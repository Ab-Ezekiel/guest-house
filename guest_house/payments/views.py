from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Payment
from reservation.models import Booking
from .utils import initialize_payment, verify_payment
import uuid
import requests
from django.conf import settings


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initialize_payment_view(request):
    reservation_id = request.data.get("reservation_id")
    amount = float(request.data.get("amount"))
    reservation = get_object_or_404(Booking, id=reservation_id, user=request.user)

    reference = str(uuid.uuid4())
    response = initialize_payment(request.user.email, amount, reference)

    if response.get("status"):
        Payment.objects.create(
            user=request.user,
            reservation=reservation,
            amount=amount,
            reference=reference,
            status="pending"
        )
        return Response({
            "authorization_url": response["data"]["authorization_url"],
            "reference": reference
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verify_payment_view(request, reference):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    res = requests.get(url, headers=headers)
    response = res.json()

    if response.get("status"):
        Payment.objects.filter(reference=reference).update(status="success")
        return Response(response["data"], status=status.HTTP_200_OK)
    else:
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
