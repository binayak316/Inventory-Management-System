from rest_framework import serializers
from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(required=False)
    class Meta:
        model= Product
        fields = '__all__'
        # exclude = ['sku']
class ProductSpecificSerializer(serializers.ModelSerializer):
    """This is the serializer to retrive specific field from the productapi"""
    class Meta:
        model = Product
        fields = ('id','name','description','purchase_price','category')



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'