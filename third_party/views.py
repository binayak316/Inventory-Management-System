from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializers import VendorSerializer, CustomerSerializer
from .models import Vendor, Customer

# Create your views here.



class VendorAPI(GenericAPIView):
    serializer_class = VendorSerializer

    queryset = Vendor.objects.all()
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            vendor = Vendor.objects.get(id=id)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        vendor = Vendor.objects.all()
        serializer = VendorSerializer(vendor, many=True)
        return Response(serializer.data)

    def post(self, request ,*args, **kwargs):
        serializer = VendorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Vendor is created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
            

class CustomerAPI(GenericAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            customer = Customer.objects.get(id=id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    
    def post(self, request ,*args, **kwargs):
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Customer is created'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)