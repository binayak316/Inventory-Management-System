from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from rest_framework import status
from .serializers import PurchaseSerializer,PurchaseItemSerializer
from .models import Purchase, PurchaseItem
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions
#import permission mixins
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
            serializer = PurchaseSerializer(purchases, many=True)
            return Response(serializer.data)
        else:
            return Response({'message':"You don't have permissions"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request ,*args, **kwargs):
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

    