from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializers import VendorSerializer, CustomerSerializer
from .models import Vendor, Customer
from django.contrib.auth.models import Permission
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
# Create your views here.



class VendorAPI(GenericAPIView):
    serializer_class = VendorSerializer
    permission_classes = [DjangoModelPermissions,IsAuthenticated]
    queryset = Vendor.objects.all()
    def get(self, request, pk=None, format=None):
        p = Permission.objects.filter(codename='view_vendor')[0]
        user = request.user
        if p in user.user_permissions.filter(pk=p.pk):

            id = pk
            if id is not None:
                vendor = Vendor.objects.get(id=id)
                serializer = VendorSerializer(vendor)
                return Response(serializer.data)
            vendor = Vendor.objects.all()
            serializer = VendorSerializer(vendor, many=True)
            return Response(serializer.data)
        else:
            return Response({'message':"You don't have permissions"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request ,*args, **kwargs):
        serializer = VendorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Vendor is created'}, status = status.HTTP_201_CREATED)
        return Response({'error':serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
            

class CustomerAPI(GenericAPIView, LoginRequiredMixin,PermissionRequiredMixin, UserPassesTestMixin, ):
    serializer_class = CustomerSerializer
    permission_classes = [DjangoModelPermissions,IsAuthenticated]
    queryset = Customer.objects.all()
    
    def get(self, request, pk=None, format=None):
        p = Permission.objects.filter(codename='view_customer')[0]
        user = request.user
        if p in user.user_permissions.filter(pk=p.pk):
            id = pk
            if id is not None:
                customer = Customer.objects.get(id=id)
                serializer = CustomerSerializer(customer)
                return Response(serializer.data)
            customer = Customer.objects.all()
            serializer = CustomerSerializer(customer, many=True)
            return Response(serializer.data)
        else:
            return Response({'message':"You don't have permissions"},status=status.HTTP_400_BAD_REQUEST)

    
    def post(self, request ,*args, **kwargs):
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Customer is created'}, status = status.HTTP_201_CREATED)
        return Response({'error':serializer.errors}, status= status.HTTP_400_BAD_REQUEST)