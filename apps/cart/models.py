from django.core.exceptions import ValidationError
from django.db import models

from apps.orders.models import OrderProduct
from datetime import datetime

# Create your models here.


class Cart(models.Model):
    products = models.ManyToManyField("products.Product", through="CartProduct")

    @property
    def total(self):
        total = 0
        for product in self.products.all():
            product_price = product.price
            start_date = CartProduct.objects.get(cart=self, product=product).start_date
            end_date = CartProduct.objects.get(cart=self, product=product).end_date
            total += (end_date - start_date).days * product_price
        return total

    def add(self, product, start_date, end_date):
        cart_product = CartProduct(
            cart=self, product=product, start_date=start_date, end_date=end_date
        )
        cart_product.clean()
        cart_product.save()
        return cart_product


class CartProduct(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ("cart", "product")

    def clean(self):
        if self.start_date < datetime.now().date():
            raise ValidationError(
                "La fecha de inicio ha de ser igual o posterior a hoy"
            )

        if self.start_date >= self.end_date:
            raise ValidationError("La fecha de inicio debe ser anterior a la de fin")

        product_orders_in_range = OrderProduct.objects.filter(
            product=self.product,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        )

        if product_orders_in_range.exists():
            raise ValidationError(
                "El producto ya está reservado en ese rango de fechas"
            )
