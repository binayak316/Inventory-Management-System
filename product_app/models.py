from django.db import models
from django.utils.html import mark_safe

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)

    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    purchase_price = models.FloatField()
    selling_price = models.FloatField()
    type = models.CharField(max_length=50)
    sku = models.CharField( max_length=50, default=1000, blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE )
    current_stock = models.IntegerField(default=0, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
    
    # def save(self, *args, **kwargs):
    #     last_sku = Product.objects.all().last().sku
        
    #     if last_sku is not None:
    #         new_sku = int(last_sku) + 1
    #     else:
    #         new_sku = 1000
    #     self.sku = new_sku
    #     super().save()
    def save(self, *args, **kwargs):
        if self.sku is None:
            self.sku = 1000
        else:
            last_sku = Product.objects.all().order_by('sku').last()
            print(last_sku)
            if last_sku is not None:
                self.sku = int(last_sku.sku)+ 1
            else:
                self.sku = 1000
        super().save()        

    def __str__(self):
        return self.name +" " + str(f"sku:{self.sku}") 

    def add_stock(self, quantity :int ):
        self.current_stock += quantity
    
    def sub_stock(self, quantity :int ):
        self.current_stock -= quantity


