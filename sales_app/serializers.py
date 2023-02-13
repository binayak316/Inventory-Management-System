from rest_framework import serializers
from .models import Sales, SalesItem
from product_app.serializers import ProductSpecificSerializer
from third_party.serializers import CustomerSpecificSerializer
from drf_writable_nested import WritableNestedModelSerializer




class SalesItemSerializer(serializers.ModelSerializer):
    # product = ProductSpecificSerializer()
    product_name = serializers.StringRelatedField(source='product.name', read_only=True)
    selling_price = serializers.StringRelatedField(source='product.selling_price', read_only=True)
    class Meta:
        model = SalesItem
        fields = '__all__'

class SalesSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    sales_items = SalesItemSerializer(many=True)
    # customer = CustomerSpecificSerializer()
    selling_by_name = serializers.StringRelatedField(source='sales_by.first_name', read_only=True)
    customer = serializers.StringRelatedField(source='customer.name', read_only=True)
    
    class Meta:
        model = Sales
        fields = '__all__'

