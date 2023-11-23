from django import forms
from .models import Product
from django.db import models


class ProductForm(forms.Form):
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
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Descripción"}),
    )
    price = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Precio"}),
    )
    image_url = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "URL de la imagen"}),
    )
    available = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"placeholder": "Disponible"}),
        initial=True,
    )


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


class CarSearchForm(forms.Form):
    search = forms.CharField(max_length=255)
