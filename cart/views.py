from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from .cart import get_cart, add_to_cart, remove_from_cart, clear_cart


class CartApiViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if not session_id:
            return JsonResponse(
                {
                    "cart": [],
                    "total_sum": 0.0
                }
            )
        cart_data = get_cart(session_id)
        return JsonResponse(cart_data)

    def create(self, request, product_uuid, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if not session_id:
            return JsonResponse(
                {
                    "error": "Session ID is missing"
                }, status=400
            )
        current_quantity = add_to_cart(session_id, product_uuid)
        return JsonResponse(
            {
                "message": "Product added to cart", "current_quantity": current_quantity
            }
        )

    def destroy(self, request, product_uuid, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if not session_id:
            return JsonResponse(
                {
                    "error": "Session ID is missing"
                }, status=400
            )
        current_quantity = remove_from_cart(session_id, product_uuid)
        return JsonResponse(
            {
                "message": "Product removed from cart", "current_quantity": current_quantity
             }
        )

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear_cart(self, request):
        session_id = request.GET.get('session_id')
        if not session_id:
            return JsonResponse(
                {
                "error": "Session ID is missing"
            }, status=400
            )
        clear_cart(session_id)
        return JsonResponse(
            {
                "message": "Cart cleared"
            }
        )


