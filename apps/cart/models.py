from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.


class Cart(models.Model):
    products = models.ManyToManyField("products.Product", through="CartProduct")

    @property
    def total(self):
        total = 0
        for product in self.products.all():
            total += product.price
        return total


class CartProduct(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ("cart", "product")

    # Check start is before end_date when creating a cart product
    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date")
