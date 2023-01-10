from django.urls import path
from third_party import views

urlpatterns = [
    path('api/vendor/', views.VendorAPI.as_view(), name="vendor_list"),
    path('api/vendor/<int:pk>', views.VendorAPI.as_view(), name="vendor_list"),

    
    path('api/customer/', views.CustomerAPI.as_view(), name="customer_list"),
    path('api/customer/<int:pk>', views.CustomerAPI.as_view(), name="customer_list"),

]