from django.core.exceptions import ValidationError
from django.db import models

from apps.payments.models import PAYMENT_FORMS

# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
    products = models.ManyToManyField("products.Product", through="OrderProduct")
    date = models.DateField(auto_now_add=True)
    payment_form = models.CharField(max_length=255, choices=PAYMENT_FORMS)
    delivery_point = models.ForeignKey(
        "products.DeliveryPoint", on_delete=models.SET_NULL, null=True
    )

    # Estado de la reserva
    STATUS = (
        ("No empezado", "No empezado"),
        ("En posesión", "En posesión"),
        ("Finalizado", "Finalizado"),
    )
    order_status = models.CharField(max_length=255, choices=STATUS)

    @property
    def total(self):
        total = 0
        for product in self.products.all():
            total += product.price
        return total


class OrderProduct(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ("order", "product")

    # Check start is before end_date when creating a cart product
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date")
