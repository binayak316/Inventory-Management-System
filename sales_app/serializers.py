from rest_framework import serializers
from .models import Sales, SalesItem

from drf_writable_nested import WritableNestedModelSerializer



class SalesItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesItem
        fields = '__all__'

class SalesSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    sales_items = SalesItemSerializer(many=True)
    class Meta:
        model = Sales
        fields = '__all__'

