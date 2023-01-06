from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class MyUser(AbstractUser):
    
    POSITION_CHOICES = (
        ('administrator', 'Administrator'),
        ('staff', 'Staff'),
    )

    phone = models.CharField(max_length=20, unique=True)
    position = models.CharField(max_length=15,choices=POSITION_CHOICES)

    