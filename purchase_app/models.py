from django.db import models
from product_app.models import Product
from third_party.models import Vendor
# Create your models here.

class Purchase(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed','Completed'),
        ('Failed','Failed'),
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    grand_total = models.FloatField(null=True, blank=True)
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
        return self.vendor.name 
    
    def get_subtotal(self):
        items = PurchaseItem.objects.filter(purchase = self.id)
        total = 0
        for item in items:
            total += item.total
        return float(total)

    def get_purchaseitem(self):
        purchase_items = PurchaseItem.objects.filter(purchase= self.id)
        return purchase_items

    # def save(self,*args,**kwargs):
    #     self.discount_amount = float(float(self.disc_percent)/100)* float(self.get_subtotal())
    #     self.tax_amount = float(float(self.tax_percent)/100)* float(self.get_subtotal() - self.discount_amount)
    #     self.grand_total = float(self.sub_total) - float(self.discount_amount + float(self.tax_amount))
    #     super().save()

    def get_grandtotal(self, *args, **kwargs):
        discount_amount = (self.disc_percent/100) * self.get_subtotal()

        tax_amount = float(float(self.tax_percent)/100) * float(self.get_subtotal() - discount_amount) #this is discounted amount(minus gareko chai)

        grand_total = float(self.get_subtotal()) - float(discount_amount) + float(tax_amount)

        return grand_total


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    total = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return str(self.quantity)
    
    def save(self, *args, **kwargs):
        self.total = float(self.product.price) * int(self.quantity)
        super().save()
    