from django import forms


class SearchIdentifierOrderForm(forms.Form):
    identifier = forms.CharField(
        label="Identificador",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Identificador: 'YU393 JGSFL US3PJ O8BMD'",
            }
        ),
    )
