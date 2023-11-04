from django.db import models

# Create your models here.

PAYMENT_FORMS = (
    ("A contrareembolso", "A contrareembolso"),
    ("Tarjeta de crédito", "Tarjeta de crédito"),
)


class PaymentMethod(models.Model):
    # TODO: Add secure payment storage
    pass
