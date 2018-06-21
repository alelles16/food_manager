from django import forms
from .models import Registro


class ConsumirForm(forms.ModelForm):

    class Meta: 
        model = Registro
        fields = ('cantidad_comprada',)
