from django.db import models
from product_app.models import Product
from third_party.models import Customer
# Create your models here.


class Sales(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed','Completed'),
        ('Failed','Failed'),
    )
# customer lai sell garinxa so foreign key
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL , null=True)

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
        return str(self.customer) + str(self.id)

    

class SalesItem(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    total = models.FloatField(blank=True, null=True) #this is the total amount which is calculated by product price * quantity

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return str(self.quantity)

    def save(self, *args, **kwargs):
        self.total = float(self.product.price) * int(self.quantity)
        super().save()