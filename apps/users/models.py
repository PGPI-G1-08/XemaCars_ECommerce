from django.contrib.auth.models import User
from django.db import models

from apps.cart.models import Cart

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="customer"
    )
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    payment_methods = models.ManyToOneRel(
        "payments.PaymentMethod",
        on_delete=models.CASCADE,
        field_name="customer",
        to="payments.PaymentMethod",
    )
    preferred_delivery_point = models.ForeignKey(
        "products.DeliveryPoint", on_delete=models.SET_NULL, null=True, blank=True
    )
    cart = models.OneToOneField(
        "cart.Cart", on_delete=models.SET_NULL, null=True, blank=True
    )

    # Create cart on user creation
    def save(self, *args, **kwargs):
        cart = Cart()
        cart.save()
        self.cart = cart
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
