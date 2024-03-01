"""
URL configuration for softsecure project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from salaries import views


urlpatterns = [
    path("", views.index, name="index"),
    path('admin/', admin.site.urls),
    path('add_salary/', views.add_salary, name='add_salary'),
    path('total_salaries/', views.total_decrypted_salaries, name='total_salaries'),
    path('edit_salary/<str:salary_id>/', views.edit_salary, name='edit_salary'),
    path('delete_salary/<str:salary_id>/', views.delete_salary, name='delete_salary'),
]
