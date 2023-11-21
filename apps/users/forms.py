from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from apps.products.models import DeliveryPoint

from apps.payments.models import PAYMENT_FORMS


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Usuario"}),
    )
    password = forms.CharField(
        required=True,
        min_length=6,
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"}),
    )

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())


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


class EditDeliveryPointAndPaymentMethodForm(forms.Form):
    delivery_points = [
        (delivery_point.get("name"), delivery_point.get("name"))
        for delivery_point in DeliveryPoint.objects.values()
    ]
    preferred_delivery_point = forms.ChoiceField(
        required=False,
        choices=[("", "Seleccione un punto de recogida")] + delivery_points,
    )
    payment_method = forms.ChoiceField(
        required=False,
        choices=[("", "Seleccione un método de pago")] + list(PAYMENT_FORMS),
    )
