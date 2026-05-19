from django import forms
from .models import Formation


class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['titre', 'duree', 'prix']