from rest_framework import serializers
from .models import Customer, Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model =Vendor
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'