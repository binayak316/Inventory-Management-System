from django.db import models
from django.core.validators import validate_email
from django.core.validators import RegexValidator

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name

    

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^98\d{8}$', message="Phone number must be entered in the format: '98XXXXXXXXXX'. 10 digits allowed.")
    phone = models.CharField(validators=[phone_regex], blank=True, null=True, max_length=10)
    email = models.CharField(validators=[validate_email],max_length=254)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name 

    