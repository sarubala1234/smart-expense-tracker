from django import forms
from .models import smart

class smartform(forms.ModelForm):
    class Meta:
        model = smart
        fields = ["title", "category", "amount", "date", "notes"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control"}),
        }
