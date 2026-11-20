from django import forms
from .models import Equipo
class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['codigo', 'nombre', 'categoria', 'cantidad']
    def clean_codigo(self):
        return self.cleaned_data['codigo'].strip().upper()
