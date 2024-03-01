from django.shortcuts import render, redirect
import pyrebase
from phe import paillier

keyring = paillier.PaillierPrivateKeyring()
public_key, private_key = paillier.generate_paillier_keypair()


from .forms import SalaryForm
from .models import Salary
from .scripts import load_paillier_key_public, load_paillier_key_private

config = {
    "apiKey": "AIzaSyCgXKK7zuHdinSTkmQUw2fM-lCiMFl6M6g",
    "authDomain": "softseguro-d6286.firebaseapp.com",
    "projectId": "softseguro-d6286",
    "databaseURL": "https://softseguro-d6286-default-rtdb.firebaseio.com/",
    "storageBucket": "softseguro-d6286.appspot.com",
    "messagingSenderId": "817108785109",
    "appId": "1:817108785109:web:1ccf715102296412294f5c",
    "measurementId": "G-H79N8NTSZ8",
}



# Create your views here.
def index(request):

    salaries = Salary.objects.all().values('id', 'name', 'area', 'value')
    return render(request, 'index.html',
                  {'salaries': salaries})

def add_salary(request):

    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            # Extrae la información del formulario
            name = form.cleaned_data['name']
            area = form.cleaned_data['area']
            value = str(form.cleaned_data['value'])

            # Cifra el valor del salario
            encrypted_value = public_key.encrypt(value, precision=2)

            # Convertir el ciphertext (que es un gran número entero) a una cadena
            encrypted_value_str = encrypted_value.ciphertext()
            print('encrypted_value_str: ', encrypted_value_str)
            Salary.objects.create(name=name, area=area, value=encrypted_value_str )

            return redirect('index')  # Redirige a la misma página
    else:
        form = SalaryForm()
    return render(request, 'add_salary.html', {'form': form})


def edit_salary(request, salary_id):
    salary = Salary.objects.get(id=salary_id)
    # Inicializa el formulario con los datos del salario
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            # Extrae la información del formulario
            name = form.cleaned_data['name']
            area = form.cleaned_data['area']
            value = form.cleaned_data['value']
            #value = str(form.cleaned_data['value'])

            # Cifra el valor del salario
            #encrypted_value = public_key.encrypt(value, precision=2)

            # Convertir el ciphertext (que es un gran número entero) a una cadena
            #encrypted_value_str = encrypted_value.ciphertext()

            salary.name = name
            salary.area = area
            salary.value = value
            salary.save()
            return redirect('index')
    else:
        salary_int = int(salary.value)
        encrypted_number = paillier.EncryptedNumber(public_key, salary_int, exponent=0)

        initial_data = {
            'id': salary.id,
            'name': salary.name,
            'area': salary.area,
            'value': int(private_key.decrypt(encrypted_number))
        }
        form = SalaryForm(initial=initial_data)
    return render(request, 'edit_salary.html', {'form': form, 'salary_id': salary_id})


def delete_salary(request, salary_id):
    salary_data = Salary.objects.get(id=salary_id)

    if request.method == 'POST':
        # Elimina el salario de la base de datos
        salary_data.delete()

        #db.child("Salaries").child(salary_id).remove()
        return redirect('index')

    return render(request, 'delete_confirm.html', {
        'salary_id': salary_id,
        'salary_data': salary_data
    })


def sum_homomophric_encrypted_salaries(request):
    salaries = Salary.objects.all()
    print(salaries)
    total = 0
    for salary in salaries:
        encrypted_value = int(salary.value)
        print(encrypted_value)
        encrypted_number = paillier.EncryptedNumber(public_key, encrypted_value, exponent=0)
        total += encrypted_number

    # Desencripta el valor total

    #total = int(private_key.decrypt(total))

    return render(request, 'total_salaries.html', {'total_encrypted': total})


