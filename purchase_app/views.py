from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PurchaseSerializer,PurchaseItemSerializer
from .models import Purchase, PurchaseItem
#import permission mixins
# Create your views here.


class PurchaseAPI(APIView):
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
            return Response({'msg':'Purchase is created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class PurchaseItemAPI(APIView):
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

    