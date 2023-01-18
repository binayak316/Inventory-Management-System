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
    sku = models.CharField(unique=True, max_length=50, default=1000, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True )
    current_stock = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
    
    def save(self, *args, **kwargs):
        last_sku = Product.objects.all().last().sku
        if last_sku:
            new_sku = int(last_sku) + 1
        else:
            new_sku = 1000
        self.sku = new_sku
        super().save()
        

    def __str__(self):
        return self.name +" " + str(f"sku:{self.sku}") 

    def add_stock(self, quantity :int ):
        self.current_stock += quantity
    
    def sub_stock(self, quantity :int ):
        self.current_stock -= quantity


