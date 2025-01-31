from .models import *
from django import forms

class ContactForm(forms.ModelForm):
    class Meta:
        fields = ["name", "phone_number"]
        model = Contact
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
        }