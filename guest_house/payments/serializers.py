from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "reservation",
            "amount",
            "reference",
            "status",
            "created_at",
        ]
        read_only_fields = ["status", "created_at"]
