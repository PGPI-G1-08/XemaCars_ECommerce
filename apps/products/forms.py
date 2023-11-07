from django import forms
from .models import Product
from django.db import models


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "brand",
            "year",
            "combustion_type",
            "description",
            "price",
            "image_url",
            "available",
        ]

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nombre del coche"}),
    )
    brand = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Marca"}),
    )
    year = forms.IntegerField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Año"}),
    )

    class combustion_type(models.TextChoices):
        GASOLINE = "Gasolina"
        DIESEL = "Diesel"
        HYBRID = "Híbrido"
        ELECTRIC = "Eléctrico"

    combustion_type = forms.ChoiceField(
        choices=combustion_type.choices,
        widget=forms.Select(attrs={"placeholder": "Tipo de combustible"}),
    )

    description = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Descripción"}),
    )
    price = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Precio"}),
    )
    image_url = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "URL de la imagen"}),
    )
    available = forms.BooleanField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Disponible"}),
    )
