from django.db import models


PAYMENT_FORMS = (
    ("A contrareembolso", "A contrareembolso"),
    ("Tarjeta de crédito", "Tarjeta de crédito"),
)


class PaymentMethod(models.Model):
    customer = models.ForeignKey(
        "users.Customer",
        on_delete=models.CASCADE,
        related_name="payment_methods",
        null=True,
        blank=True,
    )
    payment_type = models.CharField(max_length=255, choices=PAYMENT_FORMS, blank=True)

    class Meta:
        unique_together = ("customer", "payment_type")

    def __str__(self):
        return self.payment_type
