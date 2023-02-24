from rest_framework import serializers
from .models import Sales, SalesItem
from third_party.models import Customer
from product_app.serializers import ProductSpecificSerializer
from third_party.serializers import CustomerSpecificSerializer,CustomerSerializer
from drf_writable_nested import WritableNestedModelSerializer




class SalesItemSerializer(serializers.ModelSerializer):
    # product = ProductSpecificSerializer()
    product_name = serializers.StringRelatedField(source='product.name', read_only=True)
    selling_price = serializers.StringRelatedField(source='product.selling_price', read_only=True)
    class Meta:
        model = SalesItem
        fields = '__all__'

class SalesSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    selling_by_name = serializers.StringRelatedField(source='sales_by.first_name', read_only=True)
    sales_items = SalesItemSerializer(many=True)
    # customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())



    customer = serializers.CharField(source='customer.name')


    # customer = CustomerSpecificSerializer()
    # customer = serializers.StringRelatedField(source='customer.name')
    # customer = serializers.StringRelatedField()

    class Meta:
        model = Sales
        fields = '__all__'

    
    