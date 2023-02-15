from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# abstracting the user
class MyUser(AbstractUser):
    
    POSITION_CHOICES = (
        ('administrator', 'Administrator'),
        ('staff', 'Staff'),
    )

    phone = models.CharField(max_length=20, unique=True)
    position = models.CharField(max_length=15,choices=POSITION_CHOICES)
    

    def __str__(self):
        return self.first_name


class OtpModel(models.Model):
    myuser = models.ForeignKey(MyUser,on_delete=models.CASCADE, null=True)
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.otp)