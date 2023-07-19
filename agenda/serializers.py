from rest_framework import serializers

from agenda.models import Agendamento

from django.utils import timezone


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ['id', "data_horario", "nome_cliente",
                  "email_cliente", "telefone_cliente"]

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                'Agendamento não pode ser feito no passado!')

        return value
