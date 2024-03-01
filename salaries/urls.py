from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('add_salary/', views.add_salary, name='add_salary'),
    path('total_salaries/', views.total_decrypted_salaries, name='total_salaries'),
    path('edit_salary/<str:salary_id>/', views.edit_salary, name='edit_salary'),
    path('delete_salary/<str:salary_id>/', views.delete_salary, name='delete_salary'),

]