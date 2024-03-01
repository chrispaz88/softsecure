from django.db import models

# Create your models here.

from django.db import models

class Salary(models.Model):
    name = models.CharField(max_length=100)
    area = models.CharField(max_length=100)  # Asumiendo que 'Area' es una cadena
    value = models.TextField()



class EncryptedSalary(models.Model):
    name = models.CharField(max_length=100)
    encrypted_value = models.TextField()
    area = models.CharField(max_length=100)