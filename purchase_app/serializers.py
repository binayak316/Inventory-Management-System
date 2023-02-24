from rest_framework import serializers
from .models import Purchase, PurchaseItem
from drf_writable_nested import WritableNestedModelSerializer
from product_app.serializers import ProductSpecificSerializer
from third_party.serializers import VendorSpecificSerializer


class PurchaseItemSerializer(serializers.ModelSerializer):
    # product = ProductSpecificSerializer()
    product_name = serializers.StringRelatedField(source='product.name', read_only=True)
    purchase_price = serializers.StringRelatedField(source='product.purchase_price', read_only=True)

    class Meta:
        model = PurchaseItem
        fields = '__all__'


class PurchaseSerializer(WritableNestedModelSerializer ,serializers.ModelSerializer):
    purchase_by_name = serializers.StringRelatedField(source='purchased_by.first_name', read_only=True)
    purchase_items = PurchaseItemSerializer(many=True)

    vendor = serializers.CharField(source='vendor.name')
    # this is used for only get vendor name get method we have to write post method to post vendor name
    # vendor = serializers.StringRelatedField(source='vendor.name')

    class Meta:
        model = Purchase
        fields = '__all__'

