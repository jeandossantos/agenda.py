from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

from .models import Agendamento
from agenda.serializers import AgendamentoSerializer


class AgendamentoDetail(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    lookup_field = "id"

    def get(self, request, id, *args, **kwargs):
        """
        Get a schedule by ID
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Update a schedule
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete a schedule"""
        return self.destroy(request, *args, **kwargs)


class AgendamentoList(
        generics.ListCreateAPIView
):

    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = Agendamento.objects.filter(prestador__username=username)

        return queryset
