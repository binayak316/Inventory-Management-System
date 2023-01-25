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

from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.generics import GenericAPIView

from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist

# from renderers import UserRenderers

# Create your views here.




def otp_generate():
    digits = "123456789"
    otp = ""

    for i in range(5):
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
    if not  request.user.is_authenticated:
        if request.method == "POST":
            user = MyUser.objects.get(id=user_id)
            user_otp = request.POST["otp"]
            # print(user, user_otp)
            otp = OtpModel.objects.filter(myuser=user, otp=user_otp).order_by('created_at').first()
            # print(otp.otp, user_otp)
            if otp:
                if str(user_otp) == str(otp.otp):
                    return redirect('/login/')
                else:
                    messages.error(request, "Invalid OTP")
            else:
                messages.error(request, 'OTP is expired')

        return render(request, 'auth_app/check_otp.html')
    else:
        return HttpResponseRedirect('/')
     

def register_page(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            register_form  = MyUserForm(request.POST)
            print(request.POST)
            if register_form.is_valid():
                # print(register_form)
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
    else:
        return HttpResponseRedirect('/')

            
    context = {
        'register_form':register_form,
    }
    return render(request, 'auth_app/registration.html', context)
    

def login_page(request):
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
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return redirect("/login/")

@login_required
def logout_page(request):
    logout(request)
    return redirect('login-page')


# auth_app api's

#generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    if refresh is None:
        return {'error': 'Refresh token not found'}
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationApi(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request, format=None)-> Response:
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            return Response ({'msg':'User Registration is successful'}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class UserLoginApi(GenericAPIView):
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
            

