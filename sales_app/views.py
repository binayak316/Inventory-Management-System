from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import SalesItemSerializer, SalesSerializer
from .models import SalesItem, Sales
from product_app.models import Product

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
# Create your views here.

class SalesAPI(GenericAPIView, LoginRequiredMixin,PermissionRequiredMixin, UserPassesTestMixin):
    serializer_class = SalesSerializer
    permission_classes = [IsAuthenticated]
    queryset = Sales.objects.all
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            sell = Sales.objects.get(id=id)
            serializer = SalesSerializer(sell)
            return Response(serializer.data)
        sell = Sales.objects.all()
        serializer = SalesSerializer(sell, many=True)
        return Response(serializer.data)

    def post(self, request ,*args, **kwargs):
        serializer = SalesSerializer(data = request.data)

        out_of_stock_products = []
        # print(request.data['sales_items'], type(request.data)) sales items list ma xa so we can do loop in sales_items
        for item in request.data['sales_items']: 
            product = Product.objects.get(id=int(item['product'])) #sales items is list but the data inside list are quantity and product which are dictionaries so we can access the value of dictionary by ['name']
            if product.current_stock < int(item['quantity']):
                out_of_stock_products.append(product.name)

                # return Response({
                #      "msg" : f"{product.name} is out of stock"
                # })
        if len(out_of_stock_products) > 0:
            return Response(
                {
                    "msg" : f"[{','.join(out_of_stock_products)} ]Products are out of stocks."
                }
            )


        if serializer.is_valid():
            serializer.save()
            sales = Sales.objects.get(id=serializer.data['id'])
            
            sales.sub_total = 0
            
            sales.discount_amount = (sales.disc_percent /100) * sales.get_subtotal()
            sales.tax_amount = float(float(sales.tax_percent)/100) * float(sales.get_subtotal()- sales.discount_amount)

            sales.sub_total = sales.get_subtotal()

            sales.grand_total = sales.get_grandtotal()

            sales.save()

            serializer = SalesSerializer(Sales)
            
            return Response({'msg':'Sales is created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        

    



class SalesItemAPI(GenericAPIView,LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin):
    serializer_class = SalesItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = SalesItem.objects.all()
    
    def get(self,request,pk=None,format=None):
        id = pk
        if id is not None:
            sales_item = SalesItem.objects.get(id=id)
            serializer = SalesItemSerializer(sales_item)
            return Response(serializer.data)
        sales_item = SalesItem.objects.all()
        serializer = SalesItemSerializer(sales_item, many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        serializer = SalesItemSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'SalesItem is created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    