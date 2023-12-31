from collections.abc import Mapping
from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from apps.products.models import DeliveryPoint

from apps.payments.models import PAYMENT_FORMS


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Correo electrónico"}),
    )

    password = forms.CharField(
        required=True,
        min_length=6,
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"}),
    )

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("El usuario no existe")
        return email


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nombre"}),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Apellido"}),
    )
    phone_number = forms.IntegerField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Número de teléfono"}),
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Usuario"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Correo electrónico"}),
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"}),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmar contraseña"}),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if len(str(phone_number)) != 9:
            raise forms.ValidationError("El número de teléfono debe tener 9 dígitos")
        return phone_number

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El usuario ya existe")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya existe")
        return email


class EditForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Nombre"}),
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Apellido"}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Correo electrónico"}),
    )
    phone_number = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Número de teléfono"}),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and len(str(phone_number)) != 9:
            raise ValidationError("Phone number must be exactly 9 digits long")
        return phone_number


class DeliveryAndPaymentForm(forms.Form):
    DELIVERY_TYPES = (
        ("Recogida en Parking", "Recogida en Parking"),
        ("Recogida en Tienda", "Recogida en Tienda"),
    )

    preferred_delivery_method = forms.ChoiceField(
        required=False,
        choices=[("", "Seleccione un método de entrega")] + list(DELIVERY_TYPES),
    )
    preferred_delivery_point = forms.ChoiceField()
    payment_method = forms.ChoiceField(
        required=False,
        choices=[("", "Seleccione un método de pago")] + list(PAYMENT_FORMS),
    )
    stripe_payment_methods = forms.ChoiceField(
        required=False,
        choices=[("", "Nueva Tarjeta")],
    )

    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Correo electrónico"}),
    )

    def __init__(self, *args, **kwargs):
        super(DeliveryAndPaymentForm, self).__init__(*args, **kwargs)
        if self.data.get("delivery_points"):
            self.fields.get("preferred_delivery_point").choices = self.data.get(
                "delivery_points"
            )
        if self.data.get("stripe_payment_methods"):
            self.fields.get("stripe_payment_methods").choices = self.data.get(
                "stripe_payment_methods"
            )
