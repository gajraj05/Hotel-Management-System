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
    rent = models.DecimalField(max_digits=8, decimal_places=2)  # e.g. 2500.00
    is_available = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField(default=2)  # e.g. 2
    room_img = models.ImageField(upload_to="room_images", null=True, blank=True)
    bed_type  = models.CharField(max_length=20,default="Double")
    floor_no = models.IntegerField(default=2)  # e.g. 3
    capacity = models.IntegerField(default=2)  # e.g. 2
    room_size = models.CharField(max_length=20,default="Medium")
    room_view = models.CharField(max_length=20,default="private")
    smoke = models.BooleanField(default=False)
    facility = models.CharField(max_length=100,default="Wifi, Air-Conditioner, Breakfast, Restaurant, Swimming Pool")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Room {self.number} ({self.room_type})"
