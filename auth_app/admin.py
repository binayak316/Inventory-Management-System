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
    list_display = ['id','otp' ,'myuser']


admin.site.register(OtpModel,OtpModelAdmin)