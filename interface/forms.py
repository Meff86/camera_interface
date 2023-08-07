from django import forms
from .models import CarPart

class CarPartForm(forms.ModelForm):
    class Meta:
        model = CarPart
        fields = ['name', 'article_number', 'place']
