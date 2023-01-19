from django.urls import path
from auth_app import views
from auth_app.views import UserRegistrationApi, UserLoginApi

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register_page, name="register-page"),
    path('login/',views.login_page, name="login-page"),
    path('logout-user/', views.logout_page, name='logout-page'),

    # otp form
    path('check_otp/<int:user_id>', views.check_otp, name='check_otp'),

    # auth_app api's
    path('api/register/', UserRegistrationApi.as_view(), name='register-api'),
    path('api/login/', UserLoginApi.as_view(), name='login-api'),
]