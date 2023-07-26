from django.urls import path

from .views import AgendamentoDetail, AgendamentoList, PrestadorList, get_horarios

urlpatterns = [
    path('agendamentos/<int:id>', AgendamentoDetail.as_view()),
    path('agendamentos/', AgendamentoList.as_view()),
    path('prestadores/', PrestadorList.as_view()),
    path('horarios/', get_horarios),
]
