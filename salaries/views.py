from django.shortcuts import render, redirect
from phe import paillier
from lightphe import LightPHE
from django.contrib.auth import logout


keyring = paillier.PaillierPrivateKeyring()


cs = LightPHE(algorithm_name='Paillier', key_size=1024, precision=4)

LightPHE.restore_keys(cs, '../keys.txt')




from .forms import SalaryForm, SalaryFormCreate
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

    salaries = Salary.objects.all().values('id', 'name', 'area', 'value', 'ci')
    return render(request, 'index.html',
                  {'salaries': salaries})

def add_salary(request):

    if request.method == 'POST':
        form = SalaryFormCreate(request.POST)
        if form.is_valid():
            # Extrae la información del formulario
            name = form.cleaned_data['name']
            area = form.cleaned_data['area']
            value = int(form.cleaned_data['value'])
            ci = int(form.cleaned_data['ci'])

            encrypted = cs.encrypt(value)

            # Cifra el valor del salario
            #encrypted_value = public_key.encrypt(value, precision=2)

            # Convertir el ciphertext (que es un gran número entero) a una cadena
            #encrypted_value_str = encrypted_value.ciphertext()
            #print('encrypted_value_str: ', encrypted_value_str)
            Salary.objects.create(name=name, area=area, value=encrypted.value, ci=ci)

            return redirect('index')  # Redirige a la misma página
    else:
        form = SalaryFormCreate()
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
            ci = form.cleaned_data['ci']
            #value = str(form.cleaned_data['value'])

            # Cifra el valor del salario
            #encrypted_value = public_key.encrypt(value, precision=2)

            # Convertir el ciphertext (que es un gran número entero) a una cadena
            #encrypted_value_str = encrypted_value.ciphertext()

            salary.name = name
            salary.area = area
            #salary.value = value
            salary.ci = ci
            salary.save()
            return redirect('index')
    else:
        salary_int = int(salary.value)
        cs.restore_keys('../keys.txt')
        salary_new = cs.create_ciphertext_obj(salary_int)
        salary_decrypted = cs.decrypt(salary_new)

        #encrypted_number = paillier.EncryptedNumber(public_key, salary_int, exponent=0)

        initial_data = {
            'id': salary.id,
            'name': salary.name,
            'area': salary.area,
            'value': salary_decrypted,
            'ci': salary.ci
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

def sum_homomophric_encrypted_salaries_total(request):
    salaries = Salary.objects.all().values('value')
    total_salaries = cs.create_ciphertext_obj(0)
    for salary in salaries:
        salary_int = int(salary['value'])
        cs.restore_keys('../keys.txt')
        salary_new = cs.create_ciphertext_obj(salary_int)
        obj_dencrypted = cs.decrypt(salary_new)
        print('obj_dencrypted: ', obj_dencrypted)
        encrypted = cs.encrypt(obj_dencrypted)

        total_salaries += encrypted
    dencrypted_total_salaries = cs.decrypt(total_salaries)
    return dencrypted_total_salaries


def sum_homomophric_encrypted_salaries(request):
    total_salaries = sum_homomophric_encrypted_salaries_total(request)
    print('total_salaries: ', total_salaries)
    return render(request, 'total_salaries.html', {'total_salaries': total_salaries})



def logout_view(request):
    # Tu lógica de cerrar sesión aquí
    logout(request)


    return render(request, 'registration/logout.html')