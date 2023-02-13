from rest_framework import serializers
from .models import Purchase, PurchaseItem
from drf_writable_nested import WritableNestedModelSerializer
from product_app.serializers import ProductSpecificSerializer
from third_party.serializers import VendorSpecificSerializer


class PurchaseItemSerializer(serializers.ModelSerializer):
    product = ProductSpecificSerializer()

    class Meta:
        model = PurchaseItem
        fields = '__all__'


class PurchaseSerializer(WritableNestedModelSerializer ,serializers.ModelSerializer):
    purchase_by_name = serializers.StringRelatedField(source='purchased_by.username', read_only=True)
    purchase_items = PurchaseItemSerializer(many=True)
    vendor = VendorSpecificSerializer()
    class Meta:
        model = Purchase
        fields = '__all__'


