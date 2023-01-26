from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category
from django.contrib.auth.models import Permission
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','id','purchase_price','selling_price','sku', 'category','current_stock', 'img_preview']

    def img_preview(self, obj):
        return format_html('<img src="{}" width=70px height="50px" style="object-fit:cover;" />'.format(obj.image.url if obj.image else '/static/images/images.png'))
    # img_preview.shor_description = "image preview"

admin.site.register(Product,ProductAdmin)
admin.site.register(Permission)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','description']

admin.site.register(Category,CategoryAdmin)