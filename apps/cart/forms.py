from apps.products.models import DeliveryPoint

from apps.payments.models import PAYMENT_FORMS, PaymentMethod
from django import forms

class EditDeliveryPointAndPaymentMethodForm(forms.Form):
    delivery_points = [
        (delivery_point.get("name"), delivery_point.get("name"))
        for delivery_point in DeliveryPoint.objects.values()
    ]
    preferred_delivery_point = forms.ChoiceField(
        required=True,
        choices=[("", "Seleccione un punto de recogida")] + delivery_points,
    )
    payment_method = forms.ChoiceField(
        required=True,
        choices=[("", "Seleccione un método de pago")] + list(PAYMENT_FORMS),
    )