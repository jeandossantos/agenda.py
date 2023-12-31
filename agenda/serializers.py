from rest_framework import serializers
from django.contrib.auth.models import User
from agenda.models import Agendamento

from django.utils import timezone

from agenda.utils import get_horarios_disponiveis


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = "__all__"

    prestador = serializers.CharField()

    def validate_prestador(self, value):
        try:
            obj = User.objects.get(username=value)

            return obj
        except User.DoesNotExist:
            raise serializers.ValidationError("Username não existe!")

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                'Agendamento não pode ser feito no passado!')

        if value not in get_horarios_disponiveis(value.date()):
            raise serializers.ValidationError("horario não disponível")
        return value


class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'agendamentos']

    agendamentos = AgendamentoSerializer(many=True, read_only=True)
