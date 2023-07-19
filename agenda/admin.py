from django.contrib import admin

from agenda.models import Agendamento


class AgendamentoAdmin(admin.ModelAdmin):
    list_display = [
        'data_horario',
        'nome_cliente',
        'email_cliente',
        'telefone_cliente'
    ]


admin.site.register(Agendamento, AgendamentoAdmin)
