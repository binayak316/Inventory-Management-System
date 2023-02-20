from django.contrib import admin
from .models import Customer, Vendor
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    model= Customer
    list_per_page = 10
    list_display = ['serial_number', 'name', 'phone', 'email']
    readonly_fields = ['serial_number']
    search_fields=['name']

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

admin.site.register(Customer,CustomerAdmin)

class VendorAdmin(admin.ModelAdmin):
    model = Vendor
    list_per_page = 10
    list_display = ['serial_number', 'name', 'type']
    readonly_fields = ['serial_number']
    search_fields = ['name']


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




admin.site.register(Vendor, VendorAdmin)