from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, OtpModel
from .forms import MyUserForm





# Register your models here.

#  discovery of page starts

from .views import login_page, logout_page
# this discover the pages and points django login to login_page
admin.autodiscover()
admin.site.login = login_page
admin.site.logout = logout_page



# discovery of page ends


class MyUserAdmin(UserAdmin):
    add_form = MyUserForm
    model = MyUser
    list_per_page = 10
    list_display = ['username', 'phone', 'email', 'first_name', 'last_name','position', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('phone', 'position')}),
    )#this will allow to change these fields in admin module

admin.site.register(MyUser, MyUserAdmin) 

class OtpModelAdmin(admin.ModelAdmin):
    model = OtpModel
    list_per_page=10
    list_display = ['serial_number','otp' ,'myuser']
    readonly_fields = ['serial_number']
    
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



admin.site.register(OtpModel,OtpModelAdmin)