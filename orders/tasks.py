from celery import shared_task
from django.core.mail import send_mail
from .models import Order

import logging
logger = logging.getLogger(__name__)

@shared_task
def order_created(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order nr. {order_id}'
        message = f'Dear {order.first_name},\n\n' \
                  f'You have successfully placed an order.' \
                  f'Your order ID is {order.id}.'
        mail_sent = send_mail(
            subject,
            message,
            'said-ahmedkurbanov@yandex.ru',
            [order.email]
        )
        logger.info(f"Email sent: {mail_sent}")
        return mail_sent
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise

