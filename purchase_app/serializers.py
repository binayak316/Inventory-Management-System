from rest_framework import serializers
from .models import Purchase, PurchaseItem
from drf_writable_nested import WritableNestedModelSerializer

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = '__all__'


class PurchaseSerializer(WritableNestedModelSerializer ,serializers.ModelSerializer):
    purchase_items = PurchaseItemSerializer(many=True)
    class Meta:
        model = Purchase
        fields = '__all__'


