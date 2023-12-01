from django import forms

from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from apps.orders.models import OrderProduct

class FilterOrders(forms.Form):
    estado = forms.CharField(
        required=False,
    )

    no_cancelados = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"placeholder": "No cancelados"}),
        initial=False,
        required=False,
    )
