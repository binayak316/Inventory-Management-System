from django.contrib import admin
from .models import Sales, SalesItem
from django.utils.html import format_html
# Register your models here.

# class SalesAdmin(admin.ModelAdmin):
#     list_display = ['id','grand_total','sub_total','discount_amount','tax_amount', 'status']

# admin.site.register(Sales,SalesAdmin)

class SalesItemInline(admin.TabularInline):
    model = SalesItem

class SalesAdmin(admin.ModelAdmin):
    list_display = ['serial_number','grand_total','sub_total','discount_amount','tax_amount','customer','items','invoice_number', 'status', 'sales_by', 'created_at']
    search_fields = ['customer__name', 'invoice_number']
    list_filter = ['status',]
    readonly_fields = ['serial_number']
    models = Sales
    list_per_page=10
    # inlines = [SalesItemInline]

    # def items(self, obj):
    #     sales_item = SalesItem.objects.filter(sales=obj.id)
    #     value = " "
    #     for item in sales_item:
    #         value += f'{item.product.name}({item.quantity})'
    #     return value
    def items(self, obj):
        sales_items = SalesItem.objects.filter(sales=obj.id)
        items_html = '<a class="btn btn-link" data-toggle="collapse" href="#collapse-items-{}" role="button" aria-expanded="false" aria-controls="collapse-items-{}">Show Items</a>'.format(obj.pk, obj.pk)
        items_html += '<div class="collapse" id="collapse-items-{}">'.format(obj.pk)
        items_html += '<ul>'
        for item in sales_items:
            items_html += '<li>{}</li>'.format(item.product.name + ' (' + str(item.quantity) + ')')
        items_html += '</ul></div>'
        return format_html(items_html)
    items.short_description = 'Items'
    
    # serial number in table
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

    
    
admin.site.register(Sales,SalesAdmin)

class SalesItemAdmin(admin.ModelAdmin):
    list_display = ['id','quantity','total']

admin.site.register(SalesItem,SalesItemAdmin)