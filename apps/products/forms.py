from django import forms

from apps.opinions.models import Opinion
from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from apps.orders.models import Order
from apps.products.models import Product


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


class FilterForm(forms.Form):
    nombre = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "¿Qué coche deseas?"}),
    )

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


class OpinionForm(forms.Form):
    customer = forms.CharField(
        widget=forms.HiddenInput(),
    )

    product = forms.CharField(
        widget=forms.HiddenInput(),
    )

    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={"placeholder": "Valoración (1-5)"}),
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Título"}),
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Describe tu experiencia"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get("customer")
        product = cleaned_data.get("product")
        if Opinion.objects.filter(product=product, customer=customer).exists():
            raise ValidationError("No puedes opinar 2 veces sobre el mismo producto")

        if not Order.objects.filter(products=product, customer=customer).exists():
            raise ValidationError(
                "No puedes opinar sobre un producto que no has comprado"
            )
