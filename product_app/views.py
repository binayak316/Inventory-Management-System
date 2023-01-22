from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from rest_framework import status
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin

# Create your views here.


class CategoryAPI(GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all

    def get(self,request,pk=None,format=None):
        id= pk
        if id is not None:
            cat = Category.objects.get(id=id)
            serializer = CategorySerializer(cat)
            return Response(serializer.data)
        cat = Category.objects.all()
        serializer = CategorySerializer(cat, many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Category is created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)



class ProductAPI(GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all

    def get(self,request,pk=None,format=None):
        id = pk
        if id is not None:
            prod = Product.objects.get(id=id)
            serializer = ProductSerializer(prod)
            return Response(serializer.data)
        prod = Product.objects.all()
        serializer = ProductSerializer(prod, many=True)
        return Response(serializer.data)
    

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Product is created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self,request,pk,format=None) -> Response:
        full_updt = Product.objects.get(id=pk)
        serializer = ProductSerializer(full_updt, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'fully updated'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    def patch(self,request,pk,format=None):
        id = pk
        partial_updt = Product.objects.get(pk=id)
        serializer = ProductSerializer(partial_updt, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partially product is updated'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None)->Response:
        id=pk
        dlt = Product.objects.get(pk=id)
        dlt.delete()
        return Response({'msg':'Product is deleted'})
        




