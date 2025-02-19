from rest_framework import serializers

from .models import Product, Category


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = ['uuid', 'name', 'image', 'price', 'category', 'slug', 'weight', 'price_per_unit']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {'response': data}


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['uuid', 'name', 'slug', 'image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {'response': data}

