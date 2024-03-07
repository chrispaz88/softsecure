# En salaries/forms.py
from django import forms
from .models import Salary


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
    ci = forms.CharField(label='CI', widget=forms.TextInput(attrs={'type': 'number'}))
    class Meta:
        model = Salary
        fields = ['name', 'value','area','ci']
        widgets = {
            'area': forms.Select(choices=[
                ('IT', 'IT'),
                ('Marketing', 'Marketing'),
                ('Recursos Humanos', 'Recursos Humanos'),
                ('Financiero', 'Financiero'),
                ('Administrativo', 'Administrativo')
            ])
        }