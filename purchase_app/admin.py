from django.contrib import admin
from .models import Purchase, PurchaseItem
from django.utils.html import format_html
import datetime
from rangefilter.filters import   DateRangeFilter
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
    list_display = ['id','grand_total','sub_total','discount_amount','tax_amount','items','bill_number','vendor', 'status', 'purchased_by', 'created_at']
    # search_fields = ['vendor']
    search_fields = [ 'vendor__name', 'bill_number'] 
    list_filter = ('status','created_at')
    # inlines = [PurchaseItemInline]

    def items(self, obj):
        purchase_items = PurchaseItem.objects.filter(purchase=obj.id)
        value = ""
        for item in purchase_items:
            line = '<br>'
            # value += f"""{item.product.name} ({item.quantity})""" + '<br>'
            value += f"""{item.product.name} ({item.quantity}) <br>"""
        return format_html(value)
        # return value

admin.site.register(Purchase,PurchaseAdmin)