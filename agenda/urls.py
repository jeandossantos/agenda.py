from django.urls import path

from . import views

urlpatterns = [
    path('agendamentos/<int:id>', views.agendamento_detail),
    path('agendamentos/', views.agendamento_list)
]
