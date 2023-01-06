from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import MyUserForm
from django.contrib import messages
# Create your views here.

def register_page(request):
    if request.method == "POST":
        print(request.POST)
        register_form  = MyUserForm(request.POST)
        
        # print(register_form)
        if register_form.is_valid():
            register_form.save()
            return redirect('/')
    else:
        register_form = MyUserForm()

        
    context = {
        'register_form':register_form,
    }
    return render(request, 'auth_app/registration.html', context)