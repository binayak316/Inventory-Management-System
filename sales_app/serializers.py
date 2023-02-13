from rest_framework import serializers
from .models import Sales, SalesItem
from product_app.serializers import ProductSpecificSerializer
from third_party.serializers import CustomerSpecificSerializer
from drf_writable_nested import WritableNestedModelSerializer




class SalesItemSerializer(serializers.ModelSerializer):
    product = ProductSpecificSerializer()
    class Meta:
        model = SalesItem
        fields = '__all__'

class SalesSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    purchase_by_name = serializers.StringRelatedField(source='sales_by.username', read_only=True)
    sales_items = SalesItemSerializer(many=True)
    customer = CustomerSpecificSerializer()
    class Meta:
        model = Sales
        fields = '__all__'

