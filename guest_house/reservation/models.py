from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('suite', 'Suite'),
    ]

    number = models.CharField(max_length=10, unique=True)   # e.g., "101"
    type = models.CharField(max_length=20, choices=ROOM_TYPES, default='single')
    capacity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.number} - {self.type} (${self.price})"

    def clean(self):
        if self.capacity <= 0:
            raise ValidationError("Capacity must be greater than zero.")
        if self.price <= 0:
            raise ValidationError("Price must be greater than zero.")

    def save(self, *args, **kwargs):
        self.full_clean()  # validate before saving
        super().save(*args, **kwargs)




class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ("checked_in", "Checked In"),
        ("checked_out", "Checked Out"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="bookings")
    
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
       return f"Booking {self.id} - {self.user.username} ({self.room.number}) from {self.check_in} to {self.check_out} - {self.status}"

    def clean(self):
        # Check-out must be after check-in
        if self.check_out <= self.check_in:
            raise ValidationError("Check-out date must be after check-in date.")

        # Optional: prevent past bookings
        if self.check_in < timezone.now().date():
            raise ValidationError("Check-in date cannot be in the past.")

        # Ensure room is available (basic logic)
        overlapping = Booking.objects.filter(
            room=self.room,
            status__in=["pending", "confirmed"],
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
        ).exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("This room is not available for the selected dates.")

    
    def save(self, *args, **kwargs):
        self.full_clean()  # validate before saving
        super().save(*args, **kwargs)

    @property
    def duration(self):
        """Return number of nights booked."""
        return (self.check_out - self.check_in).days

    @property
    def total_price(self):
        """Calculate total price for the stay."""
        return self.duration * self.room.price
