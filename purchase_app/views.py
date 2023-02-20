from django.shortcuts import render ,redirect
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from rest_framework import status
from django.db.models import Q
from .serializers import PurchaseSerializer,PurchaseItemSerializer
from .models import Purchase, PurchaseItem
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions
from django.http import JsonResponse
#import permission mixins

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa











# Create your views here.


class PurchaseAPI(GenericAPIView):
    """It defines the Generic API View for the products and calculates
    total, grandtotal, subtotal, tax amount and discount amount for the purchased
    Item and Items are purchased from the vendors """
    serializer_class = PurchaseSerializer
    permission_classes = [DjangoModelPermissions,IsAuthenticated]
    queryset = Purchase.objects.all()

    def get(self, request, pk=None, format=None):
        p = Permission.objects.filter(codename='view_purchase')[0]
        user = request.user
        if p in user.user_permissions.filter(pk=p.pk):
            id = pk
            if id is not None:
                purchase = Purchase.objects.get(id=id)
                serializer = PurchaseSerializer(purchase)
                return Response(serializer.data)
            purchases = Purchase.objects.all()

            if request.GET.get('search'):
                search = str(request.GET.get('search'))
                pur_order = Purchase.objects.all().filter(Q(vendor__name__contains=search) | Q(status__contains=search) )
                if not pur_order:
                    return Response({'message':'Not Found'})
                serializer = PurchaseSerializer(pur_order, many=True)
                return Response({
                    'msg':'Order you are looking for ',
                    'status':status.HTTP_200_OK,
                    'data':serializer.data,

                },status = status.HTTP_200_OK)
            serializer = PurchaseSerializer(purchases, many=True)
            return Response(serializer.data)
        else:
            return Response({'message':"You don't have permissions"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request ,*args, **kwargs):
        # print(request.data)
        # print(request.data.purchase_items)
        serializer = PurchaseSerializer(data = request.data)
        # print(serializer)


        if serializer.is_valid():
            serializer.save()
            purchase = Purchase.objects.get(id=serializer.data['id'])
            purchase.sub_total = 0

            purchase.discount_amount = (purchase.disc_percent/100) * purchase.get_subtotal()
            purchase.tax_amount = float(float(purchase.tax_percent)/100 * float(purchase.get_subtotal() - purchase.discount_amount))

            purchase.sub_total = purchase.get_subtotal()
            purchase.grand_total = purchase.get_grandtotal()
            purchase.save()
            serializer = PurchaseSerializer(purchase)
            return Response({
                'msg':'Purchase is created',
                 'status': status.HTTP_201_CREATED, 
                 'data' : serializer.data,
                 }, status = status.HTTP_201_CREATED)
        return Response({'error':serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

class PurchaseItemAPI(GenericAPIView):
    """It is a Generic API view for the purchaseitem where it means purchase of item once where it calculates only total like products * quantity"""
    serializer_class = PurchaseItemSerializer
    permission_classes = [DjangoModelPermissions,IsAuthenticated]
    queryset = PurchaseItem.objects.all()
    
    def get(self,request,pk=None,format=None):
        p = Permission.objects.filter(codename='view_purchaseItem')[0]
        user = request.user
        if p in user.user_permissions.filter(pk=p.pk):
            id = pk
            if id is not None:
                purchase_item = PurchaseItem.objects.get(id=id)
                serializer = PurchaseItemSerializer(purchase_item)
                return Response(serializer.data)
            purchase_item = PurchaseItem.objects.all()
            serializer = PurchaseItemSerializer(purchase_item, many=True)
            return Response(serializer.data)
        else:
            return Response({'message':"You don't have permissions"}, status=status.HTTP_400_BAD_REQUEST)
      

    def post(self,request,*args,**kwargs):
        serializer = PurchaseItemSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'PurchaseItem is created'}, status = status.HTTP_200_OK)
        return Response({'error':serializer.errors}, status = status.HTTP_400_BAD_REQUEST)


from datetime import datetime
from datetime import timedelta
from django.db.models import Sum
def show_purchase_report(request):
    if request.method == "POST":
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')
        # print(start_date, end_date)
        if start_date and end_date:
            
            start_date_d = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_d = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days = 1)

            today = datetime.today()
            if end_date_d or start_date_d > today:
                print('thulo aayo')
            
            data = Purchase.objects.filter(created_at__range=(start_date_d, end_date_d ), status = 'Completed')
            # sum = data.aggregate(Sum('grand_total'))
            # sum = round(data.aggregate(Sum('grand_total'))['grand_total__sum'],3)
            sum = data.aggregate(Sum('grand_total'))['grand_total__sum']
            if sum is not None:
                sum = round(sum, 4)
            else:
                sum = 0.0

            context = {
                'data':data,
                'sum':sum,
                'start_date_d':start_date_d,
                'end_date_d':end_date_d
            }
        else:
            return redirect('/dashboard/') 
        

        return render(request, 'purchase_app/pdf_format_purchase.html',context)
    return redirect('/dashboard/')







# ajax method
# import os
# from datetime import datetime

# def purchase_history(request):
#     """this function gives the data with in the range(date) """
#     if request.method == "POST":
#         # print(request.POST)
#         start_date = request.POST.get('start')
#         end_date = request.POST.get('end')
#         # print(start_date, end_date)
#         start_date_d = datetime.strptime(start_date, "%Y-%m-%d")
#         end_date_d = datetime.strptime(end_date, "%Y-%m-%d")

#         print(start_date_d) 
#         print(end_date_d)

#         data = Purchase.objects.filter(created_at__range=(start_date_d, end_date_d))
#         purchase_data = []
#         for purchase in data:
#             vendor_name = purchase.vendor.name if purchase.vendor is not None else None
           
#             purchase_data.append({
#                 'id':purchase.id,
#                 'bill_number':purchase.bill_number,
#                 'vendor':purchase.vendor.name,
#                 'vendor':vendor_name, 
#                 'grand_total':purchase.grand_total,
#                 'sub_total':purchase.sub_total,
#                 'disc_percent':purchase.disc_percent,
#                 'tax_percent':purchase.tax_percent,
#                 'tax_amount':purchase.tax_amount,
#                 'status':purchase.status,
#                 'created_at':purchase.created_at,
#                 'status':purchase.status,
#             })

#             #create a report pdf here and store anywhere in application server 
#         return JsonResponse(purchase_data, safe=False)
#         # return JsonResponse({
#         #     'path' : "/media/images/blak.jpg"
#         # })
#     else:
#         return JsonResponse({'msg':"Error occured!!"})



    