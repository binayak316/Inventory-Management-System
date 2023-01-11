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

    grand_total = models.FloatField(null=True, blank=True)
    sub_total = models.FloatField( null=True, blank=True)
    tax_amount = models.FloatField( null=True, blank=True)
    discount_amount = models.FloatField(null=True, blank=True)
    disc_percent = models.FloatField(blank=True, default=0.0)
    tax_percent = models.FloatField( blank=True, default=0.0)
    
    status = models.CharField(max_length=10,choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return str(self.customer) + str(self.customer.id)

    def get_subtotal(self):
        items = SalesItem.objects.filter(sales=self.id)
        total = 0
        if items:
            for item in items:
                total += item.total
            return float(total)
        return total
        

    def get_salesitem(self):
        sales_items = SalesItem.objects.filter(sales=self.id)
        return sales_items
        

    # def save(self, *args, **kwargs):

    #     self.discount_amount = (self.disc_percent /100) * self.get_subtotal()

    #     self.tax_amount = float(float(self.tax_percent)/100) * float(self.get_subtotal()-self.discount_amount)

    #     self.grand_total = float(self.sub_total) - float(self.discount_amount) + float(self.tax_amount)
    #     super().save()



    def get_grandtotal(self, *args, **kwargs):

        discount_amount = (self.disc_percent /100) * self.get_subtotal()

        tax_amount = float(float(self.tax_percent)/100) * float(self.get_subtotal()-discount_amount)

        grand_total = float(self.get_subtotal()) - float(discount_amount) + float(tax_amount)
        
        return grand_total



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