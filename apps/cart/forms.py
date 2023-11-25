from apps.products.models import DeliveryPoint

from apps.payments.models import PAYMENT_FORMS, PaymentMethod
from django import forms


class EditDeliveryPointAndPaymentMethodForm(forms.Form):
    preferred_delivery_point = forms.ChoiceField(required=False)

    payment_method = forms.ChoiceField(
        required=True,
        choices=[("", "Seleccione un método de pago")] + list(PAYMENT_FORMS),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data.get("delivery_points"):
            self.fields.get("preferred_delivery_point").choices = self.data.get(
                "delivery_points"
            )
