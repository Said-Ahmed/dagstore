from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .cart import Cart
from .serializers import CartAddProductSerializer, CartListSerializer
from store.models import Product

class CartApiViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        cart = Cart(request)
        serializer_data = CartListSerializer(cart, many=True)
        print(serializer_data.data)
        return Response({'cart': serializer_data.data, 'total_sum': cart.get_total_price()})

    def create(self, request, product_uuid, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, uuid=product_uuid)
        serializer = CartAddProductSerializer(data=request.POST)
        if serializer.is_valid():
            serializer_data = serializer.validated_data
            quantity = cart.add(
                product=product,
                quantity=serializer_data.get('quantity')
            )
            return Response({'quantity': quantity}, status=status.HTTP_201_CREATED)

    def destroy(self, request, product_uuid, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, uuid=product_uuid)
        serializer = CartAddProductSerializer(data=request.POST)

        if serializer.is_valid():
            serializer_data = serializer.validated_data
            quantity = cart.remove(product=product, override_quantity=serializer_data.get('override_quantity'))
            return Response({'quantity': quantity}, status=status.HTTP_204_NO_CONTENT)


    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        cart = Cart(request)
        cart.clear()
        return Response({'status': 'Cart clear'}, status=status.HTTP_200_OK)


