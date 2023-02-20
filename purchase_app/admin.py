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

    model = Purchase
    list_per_page = 10

    # model = Purchase
    # list_per_page = 10
    # inlines = [PurchaseItemInline]

    # def items(self, obj):
    #     purchase_items = PurchaseItem.objects.filter(purchase=obj.id)
    #     value = ""
    #     for item in purchase_items:
    #         line = '<br>'
    #         # value += f"""{item.product.name} ({item.quantity})""" + '<br>'
    #         value += f"""{item.product.name} ({item.quantity}) <br>"""
    #     return format_html(value)

        # accrodion
    def items(self, obj):
        purchase_items = PurchaseItem.objects.filter(purchase=obj.id)
        items_html = '<a class="btn btn-link" data-toggle="collapse" href="#collapse-items-{}" role="button" aria-expanded="false" aria-controls="collapse-items-{}">Show Items</a>'.format(obj.pk, obj.pk)
        items_html += '<div class="collapse" id="collapse-items-{}">'.format(obj.pk)
        items_html += '<ul>'
        for item in purchase_items:
            items_html += '<li>{}</li>'.format(item.product.name + ' (' + str(item.quantity) + ')')
        items_html += '</ul></div>'
        return format_html(items_html)
    items.short_description = 'Items'

admin.site.register(Purchase,PurchaseAdmin)