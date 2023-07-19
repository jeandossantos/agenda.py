from rest_framework import serializers

from agenda.models import Agendamento


class AgendamentoSerializer(serializers.Serializer):
    data_horario = serializers.DateTimeField()
    nome_cliente = serializers.CharField(max_length=100)
    email_cliente = serializers.EmailField()
    telefone_cliente = serializers.CharField(max_length=20)

    def create(self, validated_data):
        """
        Add an agendamento row into table agendamento
        """
        return Agendamento.objects.create(**validated_data)
