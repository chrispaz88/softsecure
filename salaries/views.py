from django.shortcuts import render, redirect
import pyrebase
from phe import paillier
from lightphe import LightPHE
from rsa.cli import encrypt

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

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()



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
            value = str(form.cleaned_data['value'])

            # Cifra el valor del salario
            encrypted_value = public_key.encrypt(value, precision=2)

            # Convertir el ciphertext (que es un gran número entero) a una cadena
            encrypted_value_str = encrypted_value.ciphertext()

            salary.name = name
            salary.area = area
            salary.value = encrypted_value_str
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

    #salary_data = db.child("Salaries").child(salary_id).get().val()

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
    public_key = load_paillier_key_public()  # Cargar la clave pública

    salary = db.child("Salaries").get().val()
    total = 0
    for salary_id in salary:
        encrypted_value = int(salary[salary_id]['value'])
        encrypted_value = paillier.EncryptedNumber(public_key, encrypted_value)
        total += encrypted_value
    return render(request, 'total_salaries.html', {'total_encrypted': total})


def total_decrypted_salaries(request):
    public_key = load_paillier_key_public()  # Cargar la clave pública
    private_key = load_paillier_key_private()  # Cargar la clave privada
    salary_records = db.child("Salaries").get().val()  # Obtener todos los registros de salario

    # Iniciar el total cifrado como un número cifrado que representa '0'
    total_encrypted = paillier.EncryptedNumber(public_key, 0, exponent=0)

    # Iterar a través de cada registro de salario, sumar los valores cifrados
    for salary_id, salary_data in salary_records.items():
        print( salary_data)

        #print('dencripted', dencripted_salary)
        #total_encrypted += encrypted_salary  # Realizar la suma homomórfica

    # Descifrar el total cifrado para obtener el total de salarios en forma descifrada
    total_decrypted = private_key.decrypt(total_encrypted)

    # Pasar el total descifrado a la plantilla
    return render(request, 'total_salaries.html', {'total': total_decrypted})