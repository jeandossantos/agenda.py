from django.urls import path

from .views import AgendamentoDetail, AgendamentoList, get_horarios, relatorio_prestador

urlpatterns = [
    path('agendamentos/<int:id>', AgendamentoDetail.as_view()),
    path('agendamentos/', AgendamentoList.as_view()),
    path('prestadores/', relatorio_prestador),
    path('horarios/', get_horarios),
]
