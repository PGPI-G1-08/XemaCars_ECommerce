from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=255, blank=True)
    payment_methods = models.ManyToOneRel(
        "payments.PaymentMethod",
        on_delete=models.CASCADE,
        field_name="customer",
        to="payments.PaymentMethod",
    )
    preferred_delivery_point = models.ForeignKey(
        "products.DeliveryPoint", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.user.username
