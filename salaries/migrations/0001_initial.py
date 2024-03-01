# Generated by Django 5.0.2 on 2024-02-28 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('area', models.CharField(max_length=100)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
