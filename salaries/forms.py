# En salaries/forms.py
from django import forms
from .models import Salary


class SalaryForm(forms.ModelForm):
    value = forms.CharField(label='Salario', widget=forms.TextInput(attrs={'type': 'number'}))
    class Meta:
        model = Salary
        fields = ['name', 'value', 'area']
        widgets = {
            'area': forms.Select(choices=[
                ('IT', 'IT'),
                ('Marketing', 'Marketing'),
                ('Recursos Humanos', 'Recursos Humanos'),
                ('Financiero', 'Financiero'),
                ('Administrativo', 'Administrativo')
            ])
        }