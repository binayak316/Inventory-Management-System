from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserForm
from django.contrib import messages
from auth_app.models import MyUser
import math,random
from .models import OtpModel
# otp generate packages
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMessage


from django.contrib.auth.decorators import login_required
# Create your views here.


def otp_generate():
    digits = "0123456789"
    otp = ""

    for i in range(6):
        otp += digits[math.floor(random.random()*10)]
    return otp

def send_mail(otp, reciever_email): # send mail le kk linxa (otp ra receiver male linxa)
    # otp = otp_generate()
    email = EmailMessage(
        'Hamro khata OTP',
        f'Your OTP for hamro khata:{otp}',
        settings.EMAIL_HOST_USER,
        [reciever_email] #this is the email receiver
    )
    email.fail_silently=False
    email.send()

    # print(email)

def check_otp(request, user_id):
    if request.method == "POST":
        user = MyUser.objects.get(id=user_id)
        user_otp = request.POST["otp"]
        # print(user, user_otp)
        otp = OtpModel.objects.filter(myuser=user, otp=user_otp).order_by('created_at').first()
        print(otp.otp, user_otp)
        if otp:
            if str(user_otp) == str(otp.otp):
                return redirect('/login/')
            else:
                messages.error(request, "Invalid OTP")
        else:
            messages.error(request, 'OTP is expired')

    return render(request, 'auth_app/check_otp.html')
     

def register_page(request):
    if request.method == "POST":
        register_form  = MyUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            #this two down line save the otp to the otpmodel
            otp = OtpModel(myuser=user, otp=otp_generate(), created_at=datetime.now())
            otp.save()
            send_mail(otp.otp, user.email)# paxillo otp is the otp retrived from db
            return redirect(f'/check_otp/{user.id}')
        else:
            print(register_form.errors)
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
            users = MyUser.objects.filter(email=email) #yo agadi ko email MyUser ko models ko object ho  ra paxadi ko email chai mathi ko attribute ho
            # print(users)
            if users: 
                username = users[0].username # filter query ko suru ko 0th index ko username vaneko ho esle
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






