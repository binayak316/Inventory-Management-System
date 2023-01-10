from django.contrib import admin
from .models import Sales, SalesItem
# Register your models here.

class SalesAdmin(admin.ModelAdmin):
    list_display = ['id','grand_total','sub_total','discount_amount','tax_amount', 'status']

admin.site.register(Sales,SalesAdmin)

class SalesItemAdmin(admin.ModelAdmin):
    list_display = ['id','quantity','total']

admin.site.register(SalesItem,SalesItemAdmin)