from rest_framework import serializers
from .models import Product,Category,Cartitem, Cart
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields= '__all__'
        model= Category

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartitem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'