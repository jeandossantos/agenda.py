import csv
from io import StringIO

from agenda.serializers import PrestadorSerializer
from django.contrib.auth.models import User
from _core.celery import app


@app.task
def gera_relatorio_prestador():
    output = StringIO()
    writer = csv.writer(output)
    users = User.objects.all()
    serializer = PrestadorSerializer(users, many=True)

    writer.writerow(["prestador", "horário", "Nome", "Email", "Telefone"])

    for user in serializer.data:
        for agendamento in user['agendamentos']:
            writer.writerow([
                agendamento["prestador"],
                agendamento["data_horario"],
                agendamento["nome_cliente"],
                agendamento["email_cliente"],
                agendamento["telefone_cliente"]
            ])

    print(output.getvalue())
