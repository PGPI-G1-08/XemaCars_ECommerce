from django import forms
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["title", "description"]
        labels = {
            "title": "Título",
            "description": "Descripción",
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["answer"]
        labels = {
            "answer": "Respuesta",
        }