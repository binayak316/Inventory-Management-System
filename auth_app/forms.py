from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


# register form
class MyUserForm(UserCreationForm):
    class Meta:
        model =MyUser
        fields = ['username','first_name', 'last_name', 'email','phone', 'password1', 'password2', 'position']