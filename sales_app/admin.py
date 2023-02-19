from django.contrib import admin
from .models import Sales, SalesItem
# Register your models here.

# class SalesAdmin(admin.ModelAdmin):
#     list_display = ['id','grand_total','sub_total','discount_amount','tax_amount', 'status']

# admin.site.register(Sales,SalesAdmin)

class SalesItemInline(admin.TabularInline):
    model = SalesItem

class SalesAdmin(admin.ModelAdmin):
    list_display = ['id','grand_total','sub_total','discount_amount','tax_amount','customer','items','invoice_number', 'status', 'sales_by', 'created_at']
    search_fields = ['customer__name', 'invoice_number']
    list_filter = ['status',]
    models = Sales
    list_per_page=10
    # inlines = [SalesItemInline]

    def items(self, obj):
        sales_item = SalesItem.objects.filter(sales=obj.id)
        value = " "
        for item in sales_item:
            value += f'{item.product.name}({item.quantity})'
        return value
    
admin.site.register(Sales,SalesAdmin)

class SalesItemAdmin(admin.ModelAdmin):
    list_display = ['id','quantity','total']

admin.site.register(SalesItem,SalesItemAdmin)