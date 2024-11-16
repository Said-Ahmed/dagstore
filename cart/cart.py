from decimal import Decimal

from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_uuid = str(product.uuid)

        if product_uuid in self.cart:

            if override_quantity:
                self.cart[product_uuid]['quantity'] = quantity
            else:
                self.cart[product_uuid]['quantity'] += quantity

        else:
            self.cart[product_uuid] = {'quantity': 1, 'price': str(product.price)}

        self.save()

        return self.cart[product_uuid]['quantity']

    def remove(self, product, override_quantity=False):
        product_uuid = str(product.uuid)

        if product_uuid in self.cart:

            if override_quantity:
                self.cart.pop(product_uuid)

            elif self.cart[product_uuid]['quantity'] > 1:
                self.cart[product_uuid]['quantity'] -= 1
            else:
                self.cart.pop(product_uuid)

        self.save()

        return self.cart[product_uuid]['quantity'] if product_uuid in self.cart else None

    def __iter__(self):
        product_uuids = self.cart.keys()
        products = Product.objects.filter(
            uuid__in=product_uuids
        )
        cart = self.cart.copy()

        for product in products:
            cart[str(product.uuid)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    def save(self):
        self.session.modified = True



