from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework import status
from .serializers import PurchaseSerializer,PurchaseItemSerializer
from .models import Purchase, PurchaseItem
from rest_framework.permissions import IsAuthenticated
#import permission mixins
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
# Create your views here.


class PurchaseAPI(GenericAPIView, PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Purchase.objects.all()

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            purchase = Purchase.objects.get(id=id)
            serializer = PurchaseSerializer(purchase)
            return Response(serializer.data)
        purchases = Purchase.objects.all()
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)

    def post(self, request ,*args, **kwargs):
        serializer = PurchaseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            purchase = Purchase.objects.get(id=serializer.data['id'])
            purchase.sub_total = 0

            purchase.discount_amount = (purchase.disc_percent/100) * purchase.get_subtotal()
            purchase.tax_amount = float(float(purchase.tax_percent)/100 * float(purchase.get_subtotal() - purchase.discount_amount))

            purchase.sub_total = purchase.get_subtotal()
            purchase.grand_total = purchase.get_grandtotal()
            purchase.save()
            serializer = PurchaseSerializer(Purchase)
            
            return Response({'msg':'Purchase is created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class PurchaseItemAPI(GenericAPIView, PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin):
    serializer_class = PurchaseItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = PurchaseItem.objects.all()
    
    def get(self,request,pk=None,format=None):
        id = pk
        if id is not None:
            purchase_item = PurchaseItem.objects.get(id=id)
            serializer = PurchaseItemSerializer(purchase_item)
            return Response(serializer.data)
        purchase_item = PurchaseItem.objects.all()
        serializer = PurchaseItemSerializer(purchase_item, many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        serializer = PurchaseItemSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'PurchaseItem is created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    