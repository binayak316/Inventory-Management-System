from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserForm
from django.contrib import messages
from auth_app.models import MyUser
# Create your views here.

def register_page(request):
    if request.method == "POST":
        print(request.POST)
        register_form  = MyUserForm(request.POST)
        
        # print(register_form)
        if register_form.is_valid():
            register_form.save()
            return redirect('/login/')
    else:
        register_form = MyUserForm()

        
    context = {
        'register_form':register_form,
    }
    return render(request, 'auth_app/registration.html', context)

def login_page(request):
    if request.method == "POST":
        email = request.POST['email']
        # print(request.POST)
        # username = request.POST['username']
        password = request.POST['password2']

        if email and password:
            # username = MyUser.objects.get(email=email).username
            users = MyUser.objects.filter(email=email)
            # print(users)
            if users: 
                username = users[0].username
                user = authenticate(username = username, password=password)
                if user is not None:
                    if not user.is_staff:
                        messages.error(request, "You are not authorized to  staff!!!")
                        return redirect('/login')
                    login(request,user)
                    return redirect('/dashboard')
                else:
                    messages.error(request, 'Email and Password are incorrect')
            else:
                messages.error(request, "Email is not registered")

        else:
            messages.error(request, "Fill the fields")

    return render(request, 'auth_app/login.html')


def logout_page(request):
    logout(request)
    return redirect('login-page')