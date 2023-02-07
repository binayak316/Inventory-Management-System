from django.urls import path
from product_app import views
urlpatterns = [
    # category
    path('api/categorylist/',views.CategoryAPI.as_view(), name="category-list"),
    path('api/categorylist/<int:pk>',views.CategoryAPI.as_view(), name="category-list"),

    # products 
    path('api/productlist/', views.ProductAPI.as_view(), name="product-list"),
    path('api/product/<int:pk>',views.ProductAPI.as_view(), name="product-id"),

# for frontend
    path('tables/', views.tables_products, name="tables"),

]