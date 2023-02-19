from django.contrib import admin
from .models import Customer, Vendor
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    model= Customer
    list_per_page = 10
    list_display = ['id', 'name', 'phone', 'email']

    search_fields=['name']

admin.site.register(Customer,CustomerAdmin)

class VendorAdmin(admin.ModelAdmin):
    model = Vendor
    list_per_page = 10
    list_display = ['id', 'name', 'type']
    search_fields = ['name']

admin.site.register(Vendor, VendorAdmin)