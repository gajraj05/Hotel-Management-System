from django.db import models
from django.conf import settings
from room.models import Room  # adjust import based on your structure
from django.utils import timezone

# Create your models here.

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[("Booked", "Booked"), ("CheckedOut", "CheckedOut"), ("Cancelled", "Cancelled")],
        default="Booked"
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    


    
    def __str__(self):
        return f"{self.user.username} booked {self.room.number}"
