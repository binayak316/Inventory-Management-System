from django.urls import path
from auth_app import views

urlpatterns = [
    path('register/', views.register_page, name="register-page"),
]