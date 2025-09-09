from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User_Profile(AbstractUser):
    # username = models.CharField(max_length=30,unique=True)
    # first_name = models.CharField(max_length=15)
    # last_name = models.CharField(max_length=15)
    # email = models.EmailField(max_length=50,unique=True)
    phone = models.CharField(max_length=10)
    # password = models.CharField(max_length=100)
    role = models.CharField(max_length=10,default='guest')

    def __str__(self):
        return self.username
    