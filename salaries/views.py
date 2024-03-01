from django.shortcuts import render, redirect
import pyrebase
from phe import paillier
import json

from .forms import SalaryForm
from .models import Salary

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

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Carga las claves Paillier
def load_paillier_keys():
    # Cargar la clave pública
    with open('public_key.json', 'r') as public_key_file:
        public_key_data = json.load(public_key_file)
        public_key = paillier.PaillierPublicKey(n=int(public_key_data['n']))

    # Cargar la clave privada
    with open('private_key.json', 'r') as private_key_file:
        private_key_data = json.load(private_key_file)
        private_key = paillier.PaillierPrivateKey(public_key=public_key,
                                                  p=int(private_key_data['p']),
                                                  q=int(private_key_data['q']))
    return public_key, private_key

# Create your views here.
def index(request):
    salary = db.child("Salaries").get().val()
    return render(request, 'index.html',
                  {'salary': salary})

def add_salary(request):
    public_key, private_key = load_paillier_keys()  # Cargar la clave pública para cifrado
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            # Extrae la información del formulario
            name = form.cleaned_data['name']
            area = form.cleaned_data['area']
            value = float(form.cleaned_data['value'])

            # Cifra el valor del salario
            encrypted_value = public_key.encrypt(value)

            Salary.objects.create(name=name, area=area, value=encrypted_value.ciphertext())

            return redirect('index')  # Redirige a la misma página
    else:
        form = SalaryForm()
    return render(request, 'add_salary.html', {'form': form})


def edit_salary(request, salary_id):
    # Obtén el salario específico de Firebase
    salary = db.child("Salaries").child(salary_id).get().val()
    # Inicializa el formulario con los datos del salario
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            db.child("Salaries").child(salary_id).update({
                "name": form.cleaned_data['name'],
                "area": form.cleaned_data['area'],
                "value": float(form.cleaned_data['value'])
            })
            return redirect('index')
    else:
        form = SalaryForm(initial=salary)
    return render(request, 'edit_salary.html', {'form': form, 'salary_id': salary_id})


def delete_salary(request, salary_id):
    salary_data = db.child("Salaries").child(salary_id).get().val()

    if request.method == 'POST':
        db.child("Salaries").child(salary_id).remove()
        return redirect('index')

    return render(request, 'delete_confirm.html', {
        'salary_id': salary_id,
        'salary_data': salary_data
    })


def sum_homomophric_encrypted_salaries(request):
    public_key, private_key = load_paillier_keys()
    salary = db.child("Salaries").get().val()
    total = 0
    for salary_id in salary:
        encrypted_value = int(salary[salary_id]['value'])
        encrypted_value = paillier.EncryptedNumber(public_key, encrypted_value)
        total += encrypted_value
    return render(request, 'total_salaries.html', {'total_encrypted': total})


def total_decrypted_salaries(request):
    public_key, private_key = load_paillier_keys()  # Cargar ambas claves
    salary_records = db.child("Salaries").get().val()  # Obtener todos los registros de salario

    # Iniciar el total cifrado como un número cifrado que representa '0'
    total_encrypted = paillier.EncryptedNumber(public_key, 0, exponent=0)

    # Iterar a través de cada registro de salario, sumar los valores cifrados
    for salary_id, salary_data in salary_records.items():
        print('salary_data', salary_data)

        #print('dencripted', dencripted_salary)
        #total_encrypted += encrypted_salary  # Realizar la suma homomórfica

    # Descifrar el total cifrado para obtener el total de salarios en forma descifrada
    total_decrypted = private_key.decrypt(total_encrypted)

    # Pasar el total descifrado a la plantilla
    return render(request, 'total_salaries.html', {'total': total_decrypted})