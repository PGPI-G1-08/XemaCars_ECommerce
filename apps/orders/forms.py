from django import forms


class FilterOrders(forms.Form):
    customer = forms.CharField(
        label="Cliente o Correo",
        required=False,
    )

    status = forms.ChoiceField(
        label="Estado",
        choices=[
            ("Todos", "Todos"),
            ("No Empezado", "No Empezado"),
            ("En Tienda", "En Tienda"),
            ("En Parking", "En Parking"),
            ("En Posesión", "En Posesión"),
            ("Finalizado", "Finalizado"),
        ],
        required=False,
    )

    no_cancelados = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"placeholder": "No cancelados"}),
        initial=False,
        required=False,
    )
