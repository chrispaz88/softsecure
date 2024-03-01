from django.db import models

# Create your models here.

from django.db import models

class Salary(models.Model):
    name = models.CharField(max_length=100)
    area = models.CharField(max_length=100)  # Asumiendo que 'Area' es una cadena
    value = models.TextField()  # Asumiendo que 'Value' es un número entero
    ci = models.BigIntegerField(default=0)


class TotalSalariesByArea(models.Model):
    area = models.CharField(max_length=100)
    total = models.TextField()