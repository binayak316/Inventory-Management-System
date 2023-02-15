from django.urls import path
from purchase_app import views

urlpatterns = [
    # purchase
    path('api/purchase/', views.PurchaseAPI.as_view(), name="purchase"),
    path('api/purchase/<int:pk>', views.PurchaseAPI.as_view(), name="purchase-individual"),

    # purchaseitem
    path('api/purchaseitem/', views.PurchaseItemAPI.as_view(), name="purchaseItem"),
    path('api/purchaseitem/<int:pk>', views.PurchaseItemAPI.as_view(), name="purchaseItem-individually"),



    # jsonresponse url(date range)
    # path('purchasehistory/', views.purchase_history, name="purchase_history"),
    
    path('show_purchase_report/', views.show_purchase_report, name='pur'),


]