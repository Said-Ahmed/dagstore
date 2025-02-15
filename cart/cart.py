import redis
from django.conf import settings
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
import logging

logger = logging.getLogger(__name__)

redis_instance = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])

def get_cart_key(session_id):
    return f"cart:{session_id}"

CART_TTL = 3600 * 24  # 24 часа

def get_cart(session_id):
    cart_key = get_cart_key(session_id)
    cart_items = redis_instance.hgetall(cart_key)

    result = []
    total_sum = Decimal(0)

    for product_uuid, quantity in cart_items.items():
        try:
            quantity = int(quantity)
            product = Product.objects.get(uuid=product_uuid.decode())  # Декодируем из bytes
            price = product.price
            total_price = price * quantity

            result.append({
                "quantity": quantity,
                "product": {
                    "uuid": str(product.uuid),
                    "name": product.name,
                    "image": product.image.url,
                    "weight": product.weight,
                    "price_per_unit": product.price_per_unit * quantity if product.price_per_unit else None,
                    "price": f"{price:.2f}",
                    "category": product.category.name
                },
                "price": f"{price:.2f}",
                "total_price": f"{total_price:.2f}",
            })

            total_sum += total_price
        except ObjectDoesNotExist:
            continue  # Если продукт не найден, просто пропускаем

    return {
        "cart": result,
        "total_sum": float(total_sum)
    }

def remove_from_cart(session_id, product_uuid):
    try:
        cart_key = get_cart_key(session_id)
        redis_instance.hincrby(cart_key, str(product_uuid), -1)  # -1 уменьшает количество на 1
        current_quantity = redis_instance.hget(cart_key, str(product_uuid))

        if current_quantity is None or int(current_quantity) <= 0:
            redis_instance.hdel(cart_key, str(product_uuid))
            current_quantity = 0

        return int(current_quantity)
    except Exception as e:
        logger.error(f"Failed to remove product {product_uuid} to cart: {e}")
        raise

def add_to_cart(session_id, product_uuid):
    try:
        cart_key = get_cart_key(session_id)
        redis_instance.hincrby(cart_key, str(product_uuid))
        redis_instance.expire(cart_key, 3600 * 24)
        current_quantity = redis_instance.hget(cart_key, str(product_uuid))

        return int(current_quantity)
    except Exception as e:
        logger.error(f"Failed to add product {product_uuid} to cart: {e}")
        raise

def clear_cart(session_id):
    cart_key = get_cart_key(session_id)
    redis_instance.delete(cart_key)

