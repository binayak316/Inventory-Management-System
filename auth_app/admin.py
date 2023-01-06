from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
from .forms import MyUserForm
# Register your models here.




class MyUserAdmin(UserAdmin):
    add_form = MyUserForm
    model = MyUser
    list_display = ['username', 'phone', 'email', 'first_name', 'last_name','position', 'is_staff']

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('phone', 'position')}),
    )#this will allow to change these fields in admin module


admin.site.register(MyUser, MyUserAdmin) 