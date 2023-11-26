from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from apps.payments.models import PAYMENT_FORMS

# Create your models here.


class Order(models.Model):
    DELIVERY_TYPES = (
        ("Recogida en Parking", "Recogida en Parking"),
        ("Recogida en Tienda", "Recogida en Tienda"),
    )

    customer = models.ForeignKey(
        "users.Customer", on_delete=models.CASCADE, null=True, blank=True
    )
    email = models.EmailField(null=True, blank=True)
    products = models.ManyToManyField("products.Product", through="OrderProduct")
    date = models.DateField(auto_now_add=True)
    payment_form = models.ForeignKey(
        "payments.PaymentMethod", on_delete=models.SET_NULL, null=True
    )
    delivery_point = models.ForeignKey(
        "products.DeliveryPoint", on_delete=models.SET_NULL, null=True
    )

    @property
    def total(self):
        total = 0
        for product in self.products.all():
            product_price = product.price
            start_date = OrderProduct.objects.get(
                order=self, product=product
            ).start_date
            end_date = OrderProduct.objects.get(order=self, product=product).end_date
            total += (end_date - start_date).days * product_price
        if self.delivery_point.delivery_type == "Recogida en Parking" and total < 5000:
            total += 100
        return total

    @property
    def completely_cancelled(self):
        cancelled = self.orderproduct_set.filter(cancelled=False).count() == 0
        return cancelled

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(customer__isnull=False) | models.Q(email__isnull=False),
                name="customer_or_email",
            )
        ]


class OrderProduct(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    cancelled = models.BooleanField(default=False)

    @property
    def order_product_status(self):
        if self.start_date > date.today():
            return "No empezado"
        elif self.start_date <= date.today() and date.today() <= self.end_date:
            return "En posesión"
        else:
            return "Finalizado"

    class Meta:
        unique_together = ("order", "product")

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("La fecha de inicio debe ser anterior a la de fin")

        product_orders_in_range = OrderProduct.objects.filter(
            product=self.product,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        ).exclude(order=self.order)

        if product_orders_in_range.exists():
            raise ValidationError(
                "El producto ya está reservado en ese rango de fechas"
            )
