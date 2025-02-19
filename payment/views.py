from decimal import Decimal

import stripe
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response

from dagstore import settings
from orders.models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


class PaymentApiView(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        order_id = request.session.get('order_id', None)

        try:
            order = Order.objects.get(id=order_id)
            success_url = request.build_absolute_uri(reverse('payment:completed'))
            cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

            session_data = {
                'mode': 'payment',
                'success_url': success_url,
                'cancel_url': cancel_url,
                'line_items': []
            }

            for item in order.items.all():
                session_data['line_items'].append(
                    {
                        'price_data': {
                            'unit_amount': int(item.price) * Decimal('100'),
                            'currency': 'rub',
                            'product_data': {
                                'name': item.product.name,
                            },
                        },
                        'quantity': item.quantity,
                    }
                )

            session = stripe.checkout.Session.create(**session_data)
            print(session.url)
            return redirect(session.url, code=303)

        except Order.DoesNotExist:
            return Response(
                {"error": f"Product item['product']['uuid'] not found"},
                status=status.HTTP_404_NOT_FOUND
            )

def payment_completed(request):
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')