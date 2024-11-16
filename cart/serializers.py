from rest_framework import serializers

from store.serializers import ProductListSerializer


class CartAddProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(max_value=21, default=1)
    override_quantity = serializers.BooleanField(required=False, default=False)

class CartListSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    product = ProductListSerializer()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

