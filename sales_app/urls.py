from django.urls import path
from sales_app import views

urlpatterns = [
    # sales
    path('api/sales/', views.SalesAPI.as_view(),name = "sales"),
    path('api/sales/<int:pk>', views.SalesAPI.as_view(),name = "sales-individually"),

    # salesitem
    path('api/salesItem/', views.SalesItemAPI.as_view(),name = "salesItem"),
    path('api/salesItem/<int:pk>', views.SalesItemAPI.as_view(),name = "salesItem-individually"),
    
    path('show_sales_report/', views.show_sales_report, name='sal'),

]