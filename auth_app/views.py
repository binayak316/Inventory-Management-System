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
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from .serializers import UserRegistrationSerializer, UserLoginSerializer, CheckOtpSerializer
from rest_framework.generics import GenericAPIView

from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# from renderers import UserRenderers

# Create your views here.





def otp_generate():
    """
    Generates the OTP.
    """
    digits = "123456789"
    otp = ""

    for i in range(5):
        otp += digits[math.floor(random.random()*9)]
    return otp

def send_mail(otp, reciever_email): # send mail le kk linxa (otp ra receiver male linxa)
    """Sends the mail to the user mail id."""
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
def check_otp(request,user_id): #user_id urls ko parameter hunxa ra target pani tei hunxa
    """Checks the OTP number of database with the mail """
    if not  request.user.is_authenticated:
        if request.method == "POST":
            user = MyUser.objects.get(id=user_id)
            # print{user} eha email aaxa
            user_otp = request.POST["otp"]
            # print(user, user_otp)
            otp = OtpModel.objects.filter(myuser=user, otp=user_otp).order_by('created_at').first() # agadi ko myuser is a model and otp is also a model
            # print(otp.otp, user_otp)
            if otp:
                if str(user_otp) == str(otp.otp): #after otp check
                    target = request.session['target']
                    if target:
                        if target.lower().strip() == 'forgot':
                            return redirect('/password-reset-confirm/')
                            
                        elif target.lower().strip() == 'register':
                            return redirect('/login/')
                
                else:
                    messages.error(request, "Invalid OTP")
            else:
                messages.error(request, "OTP didn't match ")

        return render(request, 'auth_app/check_otp.html')
    else:
        return HttpResponseRedirect('/')
     

def register_page(request):
    """Registeration of the users"""
    if not request.user.is_authenticated:
        if request.method == "POST":
            register_form  = MyUserForm(request.POST)
            # print(request.POST)
            if register_form.is_valid():
                # print(register_form)
                user = register_form.save()
                #this two down line save the otp to the otpmodel
                otp = OtpModel(myuser=user, otp=otp_generate(), created_at=datetime.now())
                otp.save()
                send_mail(otp.otp, user.email)# paxillo otp is the otp retrived from db
                messages.success(request, "OTP has been sent please check your email")
                request.session['target'] = 'register'
                return redirect(f'/check_otp/{user.id}')
            else:
                messages.error(request, register_form.errors)
                # print(register_form.errors)
        else:
            
            register_form = MyUserForm()
    else:
        return HttpResponseRedirect('/')

            
    context = {
        'register_form':register_form,
    }
    return render(request, 'auth_app/registration.html', context)
    

def login_page(request):
    """User login """
    if not request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST['email']
            # print(request.POST)
            # username = request.POST['username']
            password = request.POST['password2']

            if email and password:
                # username = MyUser.objects.get(email=email).username
                users = MyUser.objects.filter(email=email) #yo agadi ko email MyUse r ko models ko object ho  ra paxadi ko email chai mathi ko attribute ho
                # print(users)
                if users: 
                    username = users[0].username # filter query ko suru ko 0th index ko username vaneko ho esle
                    user = authenticate(username = username, password=password)
                    if user is not None:
                        if not user.is_staff:
                            messages.error(request, "You are not authorized to  staff!!!")
                            return redirect('/login')
                        login(request,user)
                        return redirect('/')
                    else:
                        messages.error(request, 'Email and Password are incorrect')
                else:
                    messages.error(request, "Email is not registered")

            else:
                messages.error(request, "Fill the fields")

        return render(request, 'auth_app/login.html')
    else:
        return HttpResponseRedirect('/')

def index(request):
    """Frontend index page"""
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return redirect("/login/")

@login_required
def logout_page(request):
    logout(request)
    return redirect('login-page')



def password_reset_page(request , target): #target parameter is to handle the sessions for 2 mechanishm (forget pw and login process)
    """function that takes an email for forget pw"""
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = MyUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    user = associated_users.first()
                    otp = otp_generate()
                    otp_instance = OtpModel(myuser=user, otp=otp, created_at=datetime.now())
                    otp_instance.save()
                    send_mail(otp, user.email)
                    messages.success(request, "OTP has been sent to your email")


                    if target.lower().strip() == 'forgot': #target is parameter and forgot is parameter for forget mechanaishm and register for registeration process mechanishm
                        request.session['target'] = 'forgot'
                        request.session['hamrokhata_user_id'] = user.id
                        return redirect(f'/check_otp/{user.id}')
                    else:
                        request.session['target'] = 'register'
                        return redirect(f'/check_otp/{user.id}')
                    
                    # request.session['target'] = 'forgot' if target.lower().strip() == 'forgot' else 'register'
                        
                    
            else:
                messages.error(request, "No user found with the provided email")
        else:
            messages.error(request, "Invalid form data")
        
    return render(request, 'auth_app/password/password_reset.html', {'form':PasswordResetForm()})

# @user_not_authenticated
# @login_required
def password_reset_confirm_page(request):
    "function that calls the password and confirm password page to make a new password when the users forgot"
    # user = MyUser.objects.get(email=request.POST.get('email'))

    if request.method == "POST":
        # print(request.data) #password1 ra password 2 auxa

        if 'hamrokhata_user_id' in  request.session:
            user = MyUser.objects.get(id=request.session['hamrokhata_user_id'])
            print(user)
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 == new_password2:
                user.set_password(new_password1)    
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password reset successful.')
                # after resetting the password kill the session 
                if request.session['target']:
                    del request.session['target']

                return redirect('/login/')
            else:
                messages.error(request,'Passwords do not match')
                
        else:
            messages.error(request, "something went wrong")
            return redirect('/password-reset/forgot')
        # request.session['id'] = user_id
        
   
    return render(request, 'auth_app/password/password_reset_confirm.html',)
# auth_app api'sF

#generate token manually
def get_tokens_for_user(user):
    """Token generation for the API's."""
    refresh = RefreshToken.for_user(user)
    if refresh is None:
        return {'error': 'Refresh token not found'}
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationApi(GenericAPIView):
    """Api for the user registration."""
    serializer_class = UserRegistrationSerializer
    def post(self, request, format=None)-> Response:
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            otp = OtpModel(myuser=user, otp=otp_generate(), created_at=datetime.now())
            otp.save()
            send_mail(otp.otp,user.email)
            return Response ({'msg':'Registration is success please verify your OTP to login'}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class CheckOtpApi(GenericAPIView):
    serializer_class = CheckOtpSerializer
    def post(self, request, format=None):
        serializer = CheckOtpSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id') 
            print(user_id)
            user = MyUser.objects.get(id=user_id)
            user_otp = serializer.data.get('otp')
            stored_otp = OtpModel.objects.filter(myuser=user, otp=user_otp).order_by('created_at').first()
            if stored_otp:
                if str(user_otp) == str(stored_otp.otp):
                    return Response({
                        'status': 'success',
                        'message': 'OTP is valid'})
                else:
                    return Response({
                        'status': 'error', 
                        'message': 'OTP is invalid'
                        })
            else:
                return Response({
                    'status': 'error',
                    'message': 'OTP is Expired'
                    })
        else:
            return Response({
                'status': 'error',
                'message': 'Invalid data'
                })        

class UserLoginApi(GenericAPIView):
    """Api for the user login."""
    serializer_class = UserLoginSerializer
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            email = serializer.data.get('email')
            user = MyUser.objects.filter(email=email)
            if user:
                username = user[0].username
            else:
                return Response({
                    'msg' : 'Email is not registered'
                }) 
            password = serializer.data.get('password')
            # print(email, password)
            user = authenticate(username=username, password=password)
            # print(user)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'user_id':user.id, 'msg':'Login successful'}, status= status.HTTP_200_OK)
            else:
                # return Response({'errors':'Email or Password is not valid'},status=status.HTTP_404_NOT_FOUND)
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response({'error' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            

