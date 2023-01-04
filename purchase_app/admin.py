from django.contrib import admin
from .models import Purchase, PurchaseItem
# Register your models here.

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id','grand_total','sub_total','discount_amount','tax_amount', 'status']

admin.site.register(Purchase,PurchaseAdmin)

class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ['id','quantity','total']

admin.site.register(PurchaseItem,PurchaseItemAdmin)