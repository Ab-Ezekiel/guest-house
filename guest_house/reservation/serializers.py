from rest_framework import serializers
from .models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "number", "type", "capacity", "price", "is_available"]


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")            # display username
    room_detail = RoomSerializer(source="room", read_only=True)         # nested read
    room_id = serializers.PrimaryKeyRelatedField(                        # write room by id
        source="room", queryset=Room.objects.all(), write_only=True
    )

    class Meta:
        model = Booking
        fields = [
            "id", "user",
            "room_id", "room_detail", "occupants",
            "check_in", "check_out",
            "status", "created_at",
        ]
        read_only_fields = ["created_at", "status"]
