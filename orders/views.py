from itertools import product
from platform import processor

from rest_framework import viewsets, status
from rest_framework.response import Response

from cart.cart import get_cart, clear_cart
from .models import OrderItem
from .serializers import OrderCreateSerializer


class OrderApiView(viewsets.ViewSet):
    def create(self, request):
        serializer_data = OrderCreateSerializer(request)
        if serializer_data.is_valid():
            session_id = request.GET.get('session_id')
            order = serializer_data.save()
            for item in get_cart(session_id):
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantuty=item['quantity'])
                clear_cart(session_id)
            return Response(
                {
                    'response': serializer_data.data
                 }, status=status.HTTP_200_OK
            )


