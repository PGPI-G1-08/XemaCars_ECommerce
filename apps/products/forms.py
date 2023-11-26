from django import forms
from .models import Product
from django.db import models
from django.forms import ModelForm


class FilterForm(forms.Form):
    año_mínimo = forms.IntegerField(
        required=False,
    )

    marca = forms.CharField(
        required=False,
    )

    class combustion_type(models.TextChoices):
        NO_FILTRAR = "No_Filtrar"
        GASOLINA = "Gasolina"
        DIESEL = "Diesel"
        HÍBRIDO = "Híbrido"
        ELÉCTRICO = "Eléctrico"

    tipo_de_combustión = forms.ChoiceField(
        choices=combustion_type.choices,
        widget=forms.Select(attrs={"placeholder": "Tipo de combustible"}),
    )

    precio_máximo = forms.FloatField(
        required=False,
        min_value=0,
    )

    solo_disponibles = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"placeholder": "Disponible"}),
        initial=False,
        required=False,
    )


class ProductForm(ModelForm):
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
