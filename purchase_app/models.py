from django.db import models
from product_app.models import Product
from third_party.models import Vendor
from auth_app.models import MyUser
# Create your models here.


class PurchaseItem(models.Model):
    # purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
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
        self.total = float(self.product.purchase_price) * int(self.quantity)
        product = Product.objects.get(id=self.product.id)
        
        product.add_stock(self.quantity)
        product.save()
        super().save()
    

class Purchase(models.Model):
    STATUS_CHOICES = (
        # ('Pending', 'Pending'),
        ('Completed','Completed'),
        # ('Failed','Failed'),
    )
    bill_number = models.CharField(default='PUR-1500', max_length=10, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    purchase_items = models.ManyToManyField(PurchaseItem) 

    grand_total = models.FloatField(null=True, blank=True)
    sub_total = models.FloatField( null=True, blank=True)
    tax_amount = models.FloatField( null=True, blank=True)
    discount_amount = models.FloatField(null=True, blank=True)
    disc_percent = models.FloatField(default= 0.0, blank=True)
    tax_percent = models.FloatField(default=0.0, blank=True)

    status = models.CharField(max_length=10,choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    purchased_by = models.ForeignKey(MyUser, on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.vendor.name 
    

    def get_subtotal(self):
        items = PurchaseItem.objects.filter(purchase=self.id)
        total = 0
        if items:
            for item in items:
                total += item.total
            return float(total)
        return total
    
    


    def get_purchaseitem(self):
        purchase_items = PurchaseItem.objects.filter(purchase= self.id)
        return purchase_items

    def get_grandtotal(self, *args, **kwargs):
        discount_amount = (self.disc_percent/100) * self.get_subtotal()

        tax_amount = float(float(self.tax_percent)/100) * float(self.get_subtotal() - discount_amount) #this is discounted amount(minus gareko chai)

        grand_total = float(self.get_subtotal()) - float(discount_amount) + float(tax_amount)

        return grand_total

    def save(self, *args, **kwargs):
        if self.bill_number is None:
            self.bill_number = str('PUR-1500')
        else:
            last_bill = Purchase.objects.all().order_by('bill_number').last()
            if not last_bill:
                self.bill_number = "PUR-1500"
            else:
                self.bill_number = "PUR-" + str(int(str(last_bill.bill_number).split('-')[1]) + 1)
        super().save()

