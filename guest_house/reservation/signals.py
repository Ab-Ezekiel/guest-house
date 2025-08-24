# reservation/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Booking, Room

def _sync_room_availability(room: Room):
    """
    Mark room unavailable if there is any confirmed or checked-in
    booking whose stay extends beyond today (present/future).
    Otherwise mark available.
    """
    today = timezone.now().date()
    has_active = Booking.objects.filter(
        room=room,
        status__in=["confirmed", "checked_in"],
        check_out__gt=today,        # booking still ongoing or in the future
    ).exists()

    new_value = not has_active
    if room.is_available != new_value:
        room.is_available = new_value
        room.save(update_fields=["is_available"])

@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance: Booking, **kwargs):
    _sync_room_availability(instance.room)

@receiver(post_delete, sender=Booking)
def booking_post_delete(sender, instance: Booking, **kwargs):
    _sync_room_availability(instance.room)
