from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Agendamento
from agenda.serializers import AgendamentoSerializer


@api_view(['GET', 'PATCH', 'DELETE'])
def agendamento_detail(request, id):
    obj = get_object_or_404(Agendamento, id=id)

    if request.method == 'GET':
        serializer = AgendamentoSerializer(obj)

        return Response(serializer.data)
    elif request.method == 'PATCH':
        data = {
            "nome_cliente": request.data.get('nome_cliente')
        }

        serializer = AgendamentoSerializer(
            obj, data=data, partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)
    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def agendamento_list(request):
    if request.method == 'GET':
        qs = Agendamento.objects.all()
        serializer = AgendamentoSerializer(qs, many=True)

        return Response(serializer.data)

    if request.method == 'POST':
        serializer = AgendamentoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
