from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Agendamento
from agenda.serializers import AgendamentoSerializer


class AgendamentoDetail(APIView):
    def get(self, request, id):
        """
        Get a schedule by ID
        """
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializer(obj)

        return Response(serializer.data)

    def patch(self, request, id):
        """
        Update a schedule
        """
        obj = get_object_or_404(Agendamento, id=id)

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

    def delete(self, request, id):
        obj = get_object_or_404(Agendamento, id=id)
        obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AgendamentoList(APIView):
    def get(self, request):
        agendamentos = Agendamento.objects.all()
        serializer = AgendamentoSerializer(agendamentos, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = AgendamentoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
