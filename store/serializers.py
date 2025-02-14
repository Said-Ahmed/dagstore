from rest_framework import serializers

from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = ['uuid', 'name', 'image', 'price', 'category', 'weight', 'price_per_unit']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

