from django.core.exceptions import ValidationError
from django.db import models

from apps.orders.models import Order

# Create your models here.


class Opinion(models.Model):
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.rating < 0 or self.rating > 5:
            raise ValidationError("La puntuación debe estar entre 0 y 5")

        # If the customer has never ordered the product, raise an error
        if not Order.objects.filter(
            customer=self.customer, products=self.product
        ).exists():
            raise ValidationError(
                "Solo se puede opinar sobre productos que el cliente ha reservado al menos una vez"
            )

    class Meta:
        unique_together = ("customer", "product")


class Claim(models.Model):
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
