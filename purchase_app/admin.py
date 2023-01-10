from django.contrib import admin
from .models import Purchase, PurchaseItem
# Register your models here.

# class PurchaseAdmin(admin.ModelAdmin):
#     list_display = ['id','grand_total','sub_total','discount_amount','tax_amount', 'status']

# admin.site.register(Purchase,PurchaseAdmin)

class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ['id','quantity','total']

admin.site.register(PurchaseItem,PurchaseItemAdmin)


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id','grand_total','sub_total','discount_amount','tax_amount','items', 'status']
    inlines = [PurchaseItemInline]

    def items(self, obj):
        purchase_items = PurchaseItem.objects.filter(purchase=obj.id)
        value = ""
        for item in purchase_items:
            data = "Products : %s \n\t Quantity : %s " % (item.product.name , item.quantity)
            value += data
            # value += f'{item.product.name} {item.quantity}'
        return value

admin.site.register(Purchase,PurchaseAdmin)