from django.db import models
from product_app.models import Product
# Create your models here.

class Purchase(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed','Completed'),
        ('Failed','Failed'),
    )

    grand_total = models.FloatField()
    sub_total = models.FloatField( null=True, blank=True)
    tax_amount = models.FloatField( null=True, blank=True)
    discount_amount = models.FloatField(null=True, blank=True)
    disc_percent = models.FloatField(null=True, blank=True)
    tax_percent = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=10,choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return str(self.grand_total)


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    total = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return str(self.quantity)