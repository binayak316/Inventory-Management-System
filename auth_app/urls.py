from django.urls import path
from auth_app import views
from auth_app.views import UserRegistrationApi, UserLoginApi, CheckOtpApi, PasswordResetApi,PasswordResetConfirmApi, ChangePasswordApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# app_name = 'auth_app'

urlpatterns = [
    # web
    path('', views.index, name="index"),
    path('register/', views.register_page, name="register-page"),
    path('login/',views.login_page, name="login-page"),
    path('logout-user/', views.logout_page, name='logout-page'),
    path('password-reset/<str:target>/',views.password_reset_page, name='password-reset' ),
    path('password-reset-confirm/',views.password_reset_confirm_page, name='password-reset-confirm' ),
    # otp form
    path('check_otp/<int:user_id>', views.check_otp, name='check_otp'),


    # auth_app api's
    path('api/register/', UserRegistrationApi.as_view(), name='register-api'),
    path('api/checkotp/', CheckOtpApi.as_view(), name="check-otp"),
    path('api/login/', UserLoginApi.as_view(), name='login-api'),
    path('api/passwordreset/', PasswordResetApi.as_view(), name='passwordreset'),
    path('api/passwordresetconfirm/<int:user_id>/', PasswordResetConfirmApi.as_view(), name='passwordresetconfrim'),
    path('api/changepassword/', ChangePasswordApi.as_view(), name='changepassword'),

    # token for refresh and token generation
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    

    # charts
    # path('ChartData/', ChartData.as_view(), name="ChartData"),# shows the categories and products chart
    path('pie/', views.pie_chart, name="pie"),
    path('bar/', views.bar_chart, name='bar'),
    path('bar_chart_performance_category_wise/',views.bar_chart_performance_category_wise, name='bar_chart_performance_category_wise'),

    


]