from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import permission_classes

from datetime import datetime, date

from .models import Agendamento
from django.contrib.auth.models import User
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from agenda.utils import get_horarios_disponiveis
from agenda.tasks import gera_relatorio_prestador


class IsOwnerOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        username = request.query_params.get('username', None)

        if request.user.username == username:
            return True

        return False


class IsPrestador(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True

        return False


class AgendamentoList(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrCreateOnly]
    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = Agendamento.objects.filter(prestador__username=username)

        return queryset


class AgendamentoDetail(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
):
    permission_classes = [IsPrestador]
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


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def relatorio_prestador(request):
    formato = request.query_params.get('formato')
    current_date = date.today()

    if formato == 'csv':
        # response = HttpResponse(
        #     content_type="text/csv",
        #     headers={
        #         "Content-Disposition": f'attachment; filename="relatorio_{current_date}.csv"'},
        # )

        result = gera_relatorio_prestador.delay()

        return Response({
            "task_id": result.task_id
        })

    else:
        users = User.objects.all()
        serializer = PrestadorSerializer(users, many=True)

        return Response(serializer.data)


@api_view(['GET'])
def get_horarios(request):
    data = request.query_params.get('data')

    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()

    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))

    return Response(horarios_disponiveis)
