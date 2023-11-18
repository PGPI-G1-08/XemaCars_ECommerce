from django.db import models


PAYMENT_FORMS = (
    ("A contrareembolso", "A contrareembolso"),
    ("Tarjeta de crédito", "Tarjeta de crédito"),
)


class PaymentMethod(models.Model):
    payment_type = models.CharField(max_length=255, choices=PAYMENT_FORMS)

    def __str__(self):
        return self.payment_type
