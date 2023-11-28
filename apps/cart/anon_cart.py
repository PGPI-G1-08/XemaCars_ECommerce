from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.orders.models import OrderProduct

from apps.products.models import Product


class AnonCart:
    def __init__(self, request):
        self.session = request.session
        if not "cart" in self.session:
            # save an empty cart in the session
            self.session["cart"] = {}
            cart = self.session["cart"]
        else:
            cart = self.session["cart"]
        self.cart = cart

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def add(self, product, start_date, end_date):
        self.cart[str(product.id)] = {
            "product_id": product.id,
            "start_date": str(start_date),
            "end_date": str(end_date),
        }
        self.save()

    def remove(self, product_id):
        if str(product_id) in self.cart:
            del self.cart[str(product_id)]
            self.save()

    def get_products(self):
        product_ids = self.cart.keys()
        products = []
        for product_id in product_ids:
            products.append(AnonCartProduct(self.cart, product_id))

        return products

    def total(self):
        total = 0
        for product_id in self.cart.keys():
            product = Product.objects.get(id=product_id)
            product_price = product.price
            start_date = datetime.strptime(
                self.cart[product_id]["start_date"], "%Y-%m-%d"
            ).date()
            end_date = datetime.strptime(
                self.cart[product_id]["end_date"], "%Y-%m-%d"
            ).date()
            total += (end_date - start_date).days * product_price
        return total

    def clean_product(self, product, start_date, end_date):
        if not product.available:
            raise ValidationError("Este producto no esta disponible en estos momentos")

        if start_date < datetime.now().date():
            raise ValidationError(
                "La fecha de inicio ha de ser igual o posterior a hoy"
            )

        if start_date >= end_date:
            raise ValidationError("La fecha de inicio debe ser anterior a la de fin")

        product_orders_in_range = OrderProduct.objects.filter(
            product=product,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exclude(cancelled=True)

        if product_orders_in_range.exists():
            raise ValidationError(
                "Este producto ya ha sido reservado en las fechas seleccionadas"
            )

    def count(self):
        """
        Count all items in the cart.
        """
        return len(self.cart.values())

    def has_product(self, product_id):
        return str(product_id) in self.cart


class AnonCartProduct:
    def __init__(self, cart, product_id):
        self.product = Product.objects.get(id=product_id)
        self.start_date = datetime.strptime(
            cart[product_id]["start_date"], "%Y-%m-%d"
        ).date()
        self.end_date = datetime.strptime(
            cart[product_id]["end_date"], "%Y-%m-%d"
        ).date()
        self.precio = self.product.price

    def __str__(self):
        return f"{self.product_id} - {self.start_date} - {self.end_date}"
