from django.db import models
from django.conf import settings

# Create your models here.

class Room(models.Model):
    ROOM_TYPES = (
        ("single", "Single"),
        ("double", "Double"),
        ("suite", "Suite"),
    )

    # number = models.CharField(max_length=10, unique=True)  # e.g. "101"
    number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default="single")
    price = models.DecimalField(max_digits=8, decimal_places=2)  # e.g. 2500.00
    is_available = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Room {self.number} ({self.room_type})"
