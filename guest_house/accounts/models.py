# accounts/models.py
from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_guest = models.BooleanField(default=True)   # Guests
    is_staff_member = models.BooleanField(default=False)  # Staff/admin

    def __str__(self):
        return self.username


# Note: Ensure that the AUTH_USER_MODEL setting in settings.py is set to 'accounts.User'
