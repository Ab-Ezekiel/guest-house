from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import RoomFilter


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by("number")
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RoomFilter
    filterset_fields = ["type", "is_available"]
    search_fields = ["number", "type"]
    ordering_fields = ["price", "number"]


class BookingViewSet(viewsets.ModelViewSet):
    """
    - Auth required.
    - Users see ONLY their own bookings by default (supports ?user=me|all for staff).
    - Filtering: ?room=ID, ?status=confirmed, ?check_in_date=YYYY-MM-DD, etc.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["room", "status", "check_in", "check_out"]
    ordering_fields = ["created_at", "check_in", "check_out"]

    def get_queryset(self):
        qs = Booking.objects.select_related("room", "user")
        user = self.request.user

        # Support ?user=me or ?user=all (staff only)
        who = self.request.query_params.get("user")
        if user.is_staff and who == "all":
            return qs
        # default: only my bookings
        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
