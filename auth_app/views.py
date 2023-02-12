from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserForm
from django.contrib import messages
from auth_app.models import MyUser
from purchase_app.models import Purchase, PurchaseItem
from sales_app.models import Sales, SalesItem
from product_app.models import Product, Category
import math,random
from .models import OtpModel
# otp generate packages
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q

from .serializers import UserRegistrationSerializer, UserLoginSerializer, CheckOtpSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, ChangePasswordSerializer
from rest_framework.generics import GenericAPIView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from django.contrib.auth.forms import PasswordResetForm
from django.http import JsonResponse



from django.contrib.auth import update_session_auth_hash

# from renderers import UserRenderers

# Create your views here.


# function for password validation


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
            if register_form.is_valid():
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

# def logout_view(request):
#     logout(request)
#     return JsonResponse({'result': 'success'})


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
                    
                        
                    
            else:
                messages.error(request, "No user found with the provided email")
        else:
            messages.error(request, "Invalid form data")
        
    return render(request, 'auth_app/password/password_reset.html', {'form':PasswordResetForm()})


def password_reset_confirm_page(request):
    "function that calls the password and confirm password page to make a new password when the users forgot"

    if request.method == "POST":
        # print(request.data) #password1 ra password 2 auxa

        if 'hamrokhata_user_id' in  request.session:
            user = MyUser.objects.get(id=request.session['hamrokhata_user_id']) #catching the session
            # print(user)
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
            return Response ({'msg':'Registration is success please verify your OTP to login', 'user_id':user.id,}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class CheckOtpApi(GenericAPIView):
    serializer_class = CheckOtpSerializer
    def post(self, request, format=None):
        serializer = CheckOtpSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id') 
            # print(user_id)
            user = MyUser.objects.get(id=user_id)
            user_otp = serializer.data.get('otp')
            stored_otp = OtpModel.objects.filter(myuser=user, otp=user_otp).order_by('created_at').first()
            if stored_otp:
                if str(user_otp) == str(stored_otp.otp):
                    return Response({
                        # 'user_id':user_id,
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
                    'message': "OTP didn't match "
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

class PasswordResetApi(GenericAPIView):
    """ API where user puts their email to get otp and redirect to the password and set password page"""
    serializer_class = PasswordResetSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data = request.data)
        # print(serializer.initial_data) #this prints the email
        if serializer.is_valid():
            # extracting email from serializer.is_valid()
            email = serializer.validated_data['email'] # this retrives the email from validated data returned by serializer (api bata aako email validate garne)
            try:
                user = MyUser.objects.get(email=email)
            except MyUser.DoesNotExist:
                return Response({'error':'User with the given email doesnot exists'}, status=status.HTTP_400_BAD_REQUEST)

            otp = otp_generate()
            otp_instance = OtpModel(myuser = user, otp=otp, created_at = datetime.now())
            otp_instance.save()

            send_mail(otp, email)
            return Response({'status':'OTP sent successfully to the given email',  'user_id':user.id,}, status=status.HTTP_200_OK)

        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmApi(GenericAPIView):
    """API where user confirms their password by putting password and confirm password"""
    serializer_class = PasswordResetConfirmSerializer
    def post(self, request,user_id, format=None):
        user = MyUser.objects.filter(id=user_id).first()
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            # this below line validates the incoming password from the serializer
            password = serializer.validated_data['password']
            user.set_password(password)
            user.save()
            return Response({'message':"Password reset successfully"})
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordApi(generics.UpdateAPIView):
    """
    An endpoint for chaging password
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [ IsAuthenticated]

    def get_object(self,queryset=None):
        obj = self.request.user
        # user ko sab data aaye yo function ma
        print(obj)
        return obj
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            # check old pw
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password":"wrong password"},status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response ={
                'status':'success',
                'code':status.HTTP_200_OK,
                'message':'Password Updated Successfully',
                'data':[]
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       

def pie_chart(request):
    """function that shows the pie chart"""
    categories = Category.objects.all()
    
    data = []
    labels = []
    product_count = []

    for category in categories:
        labels.append(category.name)
        product_count.append(category.product_count())

    data.append({
        'labels' : labels,
        'product_count' : product_count
    })
    return JsonResponse(data, safe=False)


def radar_chart(request):
    return JsonResponse("hy")