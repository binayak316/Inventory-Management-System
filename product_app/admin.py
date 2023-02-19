from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category
from django.contrib.auth.models import Permission
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['serial_number','name','purchase_price','selling_price','sku', 'category','current_stock', 'img_preview']
    search_fields = ['name']
    readonly_fields = ['serial_number']
    
    model=Product
    list_per_page=10

    def serial_number(self, obj):
        """calculates the serialnumber by finding the positions of the object in the sorted queryset"""
        queryset = self.get_queryset(obj) # This method returns a queryset of all objects for the current model, sorted by their id field.
        index = list(queryset).index(obj) + 1 #This is done by converting the queryset to a list, and then using the index method to find the index of the current object. We add 1 to the index to get the serial number.
        return index

    def get_queryset(self, obj=None):
        """this functions returns a sorted queryset of all objects for the model"""
        queryset = super().get_queryset(obj)
        queryset = queryset.order_by('id')
        return queryset

    def img_preview(self, obj):
        return format_html('<img src="{}" width=70px height="50px" style="object-fit:cover;" />'.format(obj.image.url if obj.image else '/static/images/images.png'))
    # img_preview.shor_description = "image preview"

admin.site.register(Product,ProductAdmin)
admin.site.register(Permission)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','description']
    model = Category
    list_per_page = 15
    class Media:
        css = {
            'all': ('css/admin.css',),
        }
   

admin.site.register(Category,CategoryAdmin)