from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Agendamento
from agenda.serializers import AgendamentoSerializer


@api_view(['GET'])
def agendamento_detail(request, id):
    obj = get_object_or_404(Agendamento, id=id)
    serializer = AgendamentoSerializer(obj)

    return Response(serializer.data)


@api_view(['GET'])
def agendamento_list(request):
    qs = Agendamento.objects.all()
    serializer = AgendamentoSerializer(qs, many=True)

    return Response(serializer.data)
