from django.contrib.auth.models import User
from django.db import models

from apps.cart.models import Cart
import stripe

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="customer"
    )
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    preferred_payment_method = models.ForeignKey(
        "payments.PaymentMethod", on_delete=models.SET_NULL, null=True, blank=True
    )
    preferred_delivery_point = models.ForeignKey(
        "products.DeliveryPoint", on_delete=models.SET_NULL, null=True, blank=True
    )
    cart = models.OneToOneField(
        "cart.Cart", on_delete=models.SET_NULL, null=True, blank=True
    )

    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)

    # Create cart on user creation
    def save(self, *args, **kwargs):
        cart = Cart()
        cart.save()
        self.cart = cart
        self.stripe_customer_id = stripe.Customer.create(email=self.user.email).id
        super().save(*args, **kwargs)

    def get_stripe_payment_methods(self):
        if self.stripe_customer_id == None:
            self.stripe_customer_id = stripe.Customer.create(email=self.user.email).id
        stripe_customer = stripe.Customer.retrieve(self.stripe_customer_id)
        payment_methods = stripe.PaymentMethod.list(
            customer=stripe_customer.id, type="card"
        )
        return payment_methods

    def __str__(self):
        return self.user.username
