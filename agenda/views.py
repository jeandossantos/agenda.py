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
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView
):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
