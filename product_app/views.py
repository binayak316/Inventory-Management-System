from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.db.models import Q 
from rest_framework.filters import SearchFilter
from rest_framework import status
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, AllowAny
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin, AccessMixin

from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTStatelessUserAuthentication
from django.views.generic import TemplateView

from django.db.models import Sum

from product_app import views
# Create your views here.


class CategoryAPI(GenericAPIView):
    """It defines a generic API view that defines the category for products."""
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissions,IsAuthenticated]
    queryset = Category.objects.all()

    def get(self,request,pk=None,format=None):
        p = Permission.objects.filter(codename='view_category')[0]
        user = request.user
        if p in user.user_permissions.filter(pk=p.pk):
            id= pk
            if id is not None:
                cat = Category.objects.get(id=id)
                serializer = CategorySerializer(cat)
                return Response(serializer.data)
            cat = Category.objects.all()
            serializer = CategorySerializer(cat, many=True)
            return Response(serializer.data)
        else:
            return Response({'message':"You don't have permissions"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self,request,*args,**kwargs):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Category is created'}, status = status.HTTP_200_OK)
        return Response({'error':serializer.errors}, status= status.HTTP_400_BAD_REQUEST)


class ProductAPI(GenericAPIView):
    """It defines a generic API view that defines the products."""
    serializer_class = ProductSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [DjangoModelPermissions,IsAuthenticated ]
    

    queryset = Product.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name']
    def get(self,request,pk=None,format=None):
        p = Permission.objects.filter(codename='view_product')[0]
        user = request.user
        
        if p in user.user_permissions.filter(pk=p.pk):
            id = pk
            if id is not None:
                prod = Product.objects.get(id=id)
                serializer = ProductSerializer(prod)
                return Response(serializer.data)
            prod = Product.objects.all()
            prod_search = request.GET.get('name')
            prod_sku_search = request.GET.get('sku')
            if prod_search or prod_sku_search:
                product_search = prod
                if prod_search:
                    product_search = product_search.filter(name__icontains=prod_search)
                if prod_sku_search:
                    product_search = product_search.filter(sku__exact=prod_sku_search)
                if not product_search:
                    return Response({'message':'No Products Found'}, status=status.HTTP_404_NOT_FOUND)
                serializer = ProductSerializer(product_search, many=True)
                return Response({
                'msg':'product you are looking for',
                'status': status.HTTP_200_OK, 
                'data' : serializer.data,
            }, status = status.HTTP_200_OK )
            serializer = ProductSerializer(prod, many=True)
            return Response(serializer.data)
                
        


            # if request.GET.get('search'):
            #     search = str(request.GET.get('search'))
            #     products = Product.objects.all().filter(Q(sku__exact=search))
            #     if not products:
            #         return Response({'message':'No products found'}, status=status.HTTP_404_NOT_FOUND)
            #     serializer = ProductSerializer(products, many=True)
            #     return Response({
            #         'msg':'product you are looking for',
            #         'status': status.HTTP_200_OK, 
            #         'data' : serializer.data,
            #      }, status = status.HTTP_200_OK )
            # serializer = ProductSerializer(prod, many=True)
            # return Response(serializer.data)
        else:
            return Response({
                'error' : "You don't have permissions "
            }, status=status.HTTP_400_BAD_REQUEST)
    
 

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
    
            return Response({'message':'Product is created'}, status = status.HTTP_200_OK)
        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self,request,pk,format=None) -> Response:
        full_updt = Product.objects.get(id=pk)
        serializer = ProductSerializer(full_updt, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Fully updated'}, status = status.HTTP_200_OK)
        return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    
    def patch(self,request,pk,format=None):
        id = pk
        partial_updt = Product.objects.get(pk=id)
        serializer = ProductSerializer(partial_updt, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partially product is updated'}, status = status.HTTP_200_OK)
        return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None)->Response:
        id=pk
        dlt = Product.objects.get(pk=id)
        dlt.delete()
        return Response({'msg':'Product is deleted'},status = status.HTTP_200_OK)
        



