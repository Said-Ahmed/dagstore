from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response

from cart.cart import get_cart, clear_cart
from store.models import Product
from .models import OrderItem
from .serializers import OrderCreateSerializer

class OrderApiView(viewsets.ViewSet):
    def create(self, request):
        session_id = request.GET.get('session_id')
        cart = get_cart(session_id).get('cart', [])

        if not cart:
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                order = serializer.save()
                order_items = []

                for item in cart:
                    try:
                        product = Product.objects.get(uuid=item['product']['uuid'])
                        order_items.append(
                            OrderItem(
                                order=order,
                                product=product,
                                price=item['price'],
                                quantity=item['quantity']
                            )
                        )
                    except Product.DoesNotExist:
                        return Response(
                            {"error": f"Product {item['product']['uuid']} not found"},
                            status=status.HTTP_404_NOT_FOUND
                        )

                OrderItem.objects.bulk_create(order_items)

            clear_cart(session_id)

            return Response(
                {"response": serializer.data},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"Order creation failed: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )