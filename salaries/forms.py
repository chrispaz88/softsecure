# En salaries/forms.py
from django import forms
from .models import Salary
from django.core.exceptions import ValidationError



class SalaryForm(forms.ModelForm):
    value = forms.CharField(label='Salario', widget=forms.TextInput(attrs={'type': 'number'}), disabled=True)
    ci = forms.CharField(label='CI', widget=forms.TextInput(attrs={'type': 'number'}))
    class Meta:
        model = Salary
        fields = ['name', 'value', 'area', 'ci']
        widgets = {
            'area': forms.Select(choices=[
                ('IT', 'IT'),
                ('Marketing', 'Marketing'),
                ('Recursos Humanos', 'Recursos Humanos'),
                ('Financiero', 'Financiero'),
                ('Administrativo', 'Administrativo')
            ])
        }

class SalaryFormCreate(forms.ModelForm):
    value = forms.CharField(label='Salario', widget=forms.TextInput(attrs={'type': 'number'}))
    ci = forms.CharField(label='CI', widget=forms.TextInput(attrs={'type': 'number', 'maxlength': '10'}))  # Añadí 'maxlength' aquí

    class Meta:
        model = Salary
        fields = ['name', 'value', 'area', 'ci']
        widgets = {
            'area': forms.Select(choices=[
                ('IT', 'IT'),
                ('Marketing', 'Marketing'),
                ('Recursos Humanos', 'Recursos Humanos'),
                ('Financiero', 'Financiero'),
                ('Administrativo', 'Administrativo'),
            ])
        }

    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value:
            value = int(value)  # Convertimos el valor a entero para compararlo
            if value < 1:
                raise ValidationError('El salario debe ser mayor o igual a 1.')
        return value

    def clean_ci(self):
        ci = self.cleaned_data.get('ci')
        if ci:
            if len(ci) != 10:
                raise ValidationError('La cédula debe tener 10 dígitos.')
        return ci